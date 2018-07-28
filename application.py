import copy
import urwid
import logging
import constants
import gkeepapi
import widget.grid
import widget.kanban
# import widget.settings
# import widget.search
import query

class Application(urwid.WidgetWrap):
    """
    Base application widget
    """
    def __init__(self, config: dict, keep: gkeepapi.Keep):
        self.config = config
        self.keep = keep
        self.stack = []

        w_main = widget.grid.Grid(self, self.hydrateQuery('default'))
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
        return key

    def hydrateQuery(self, key: str) -> query.Query:
        views = self.config.get('views', {})
        view = copy.deepcopy(views.get(key, {}))

        if 'labels' in view:
            labels = []
            for i in view.get('labels', []):
                l = self.keep.findLabel(i)
                if l is not None:
                    labels.append(l)
                else:
                    logging.warn('Label not found %s', i)
            view['labels'] = labels

        if 'colors' in view:
            colors = []
            for i in view.get('colors', []):
                try:
                    c = gkeepapi.node.ColorValue(i.upper())
                    colors.append(c)
                except:
                    logging.warn('Color not found %s', i)
            view['colors'] = colors

        return query.Query.fromConfig(view)
