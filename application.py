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
        # self.w_main = widget.kanban.KanBan(query.Query(), query.Query(), query.Query())
        self.w_main = widget.grid.Grid(query.Query())
        self.refresh()

        super(Application, self).__init__(self.w_main)

    def refresh(self):
        self.keep.sync()
        self.w_main.refresh(self.keep)

    def keypress(self, size, key):
        if key == 'r':
            self.refresh()
            key = None

        super(Application, self).keypress(size, key)
        return key
