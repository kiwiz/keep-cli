import urwid
import logging
import constants
import json
import gkeepapi
import widget.status
import widget.grid
import widget.kanban
import widget.search
import widget.help
import query

class Application(urwid.Frame):
    """
    Base application widget
    """
    def __init__(self, config: dict, keep: gkeepapi.Keep, offline: bool=False):
        self.config = config
        self.keep = keep
        self.offline = offline
        self.stack = []

        self.w_status = widget.status.Status(self)

        self.load()

        w_main = self.hydrateView('default')
        self.stack.append(w_main)

        super(Application, self).__init__(w_main, footer=self.w_status)
        self.refresh()

    def push(self, w: urwid.Widget):
        """
        Push a widget onto the rendering stack
        """
        self.stack.append(w)
        self.body = w

    def pop(self):
        """
        Pop a widget off the rendering stack
        """
        if len(self.stack) <= 1:
            return

        self.stack.pop()
        self.body = self.stack[-1]
        self.body.refresh(self.keep)

    def replace(self, w: urwid.Widget):
        """
        Replace the active widget on the rendering stack
        """
        self.pop()
        self.push(w)

    def overlay(self, w: urwid.Widget=None):
        w_top = self.stack[-1]

        if w is None:
            self.body = w_top
        else:
            self.body = urwid.Overlay(
                w, w_top,
                urwid.CENTER, (urwid.RELATIVE, 80),
                urwid.MIDDLE, urwid.PACK
            )

    def refresh(self):
        """
        Refresh keep and the active widget
        """
        if not self.offline:
            self.keep.sync()
        self.body.refresh(self.keep)

    def keypress(self, size, key):
        """
        Handle global keypresses
        """
        key = super(Application, self).keypress(size, key)
        if key == 'r':
            self.refresh()
            key = None
        elif key == '/':
            self.replace(widget.search.Search(self))
            key = None
        elif key == '?':
            self.overlay(widget.help.Help(self))
            key = None
        elif key == 'esc':
            self.save()
            raise urwid.ExitMainLoop()
        return key

    def load(self):
        username = self.config.get('username', 'user')
        try:
            fh = open('%s.keep' % username, 'r')
            state = json.load(fh)
            fh.close()
            self.keep.restore(state)
        except FileNotFoundError:
            pass

    def save(self):
        state = self.keep.dump()
        username = self.config.get('username', 'user')
        fh = open('%s.keep' % username, 'w')
        json.dump(state, fh)
        fh.close()

    def hydrateView(self, key: str) -> query.Query:
        views = self.config.get('views') or {}
        view = views.get(key) or {}
        _type = view.get('type', 'grid')

        if _type == 'kanban':
            raw_queries = view.get('queries') or []
            return widget.kanban.KanBan(
                self,
                [query.Query.fromConfig(self.keep, raw_query) for raw_query in raw_queries]
            )

        raw_query = view.get('query') or {}
        q = query.Query.fromConfig(self.keep, raw_query)
        return widget.grid.Grid(self, q)
