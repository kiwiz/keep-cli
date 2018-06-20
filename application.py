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
    def __init__(self, keep: gkeepapi.Keep):
        self.keep = keep
        self.stack = []

        w_main = widget.grid.Grid(self, query.Query())
        self.stack.append(w_main)

        super(Application, self).__init__(w_main)
        self.refresh()

    def push(self, w: urwid.Widget):
        self.stack.append(w)
        self._w = w

    def pop(self):
        if len(self.stack) <= 1:
            return

        self.stack.pop()
        self._w = self.stack[-1]

    def replace(self, w: urwid.Widget):
        self.pop()
        self.push(w)

    def refresh(self):
        self.keep.sync()
        self._w.refresh(self.keep)

    def keypress(self, size, key):
        key = super(Application, self).keypress(size, key)
        if key == 'r':
            self.refresh()
            key = None
        return key
