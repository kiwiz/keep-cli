import urwid
import logging
import constants
import gkeepapi
import widget.grid
import widget.kanban
import widget.search
import widget.help
# import widget.settings
import query

class Application(urwid.WidgetWrap):
    """
    Base application widget
    """
    def __init__(self, config: dict, keep: gkeepapi.Keep):
        self.config = config
        self.keep = keep
        self.stack = []

        w_main = self.hydrateView('default')
        self.stack.append(w_main)

        super(Application, self).__init__(w_main)
        self.refresh()

    def push(self, w: urwid.Widget):
        """
        Push a widget onto the rendering stack
        """
        self.stack.append(w)
        self._w = w

    def pop(self):
        """
        Pop a widget off the rendering stack
        """
        if len(self.stack) <= 1:
            return

        self.stack.pop()
        self._w = self.stack[-1]
        self._w.refresh(self.keep)

    def replace(self, w: urwid.Widget):
        """
        Replace the active widget on the rendering stack
        """
        self.pop()
        self.push(w)

    def refresh(self):
        """
        Refresh keep and the active widget
        """
        self.keep.sync()
        self._w.refresh(self.keep)

    def keypress(self, size, key):
        """
        Handle global keypresses
        """
        key = super(Application, self).keypress(size, key)
        if key == 'r':
            self.refresh()
            key = None
        elif key == '/':
            self.replace(widget.search.Search(self, self.keep))
            key = None
        elif key == '?':
            self.push(widget.help.Help())
            key = None
        elif key == 'esc':
            raise urwid.ExitMainLoop()
        return key

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
