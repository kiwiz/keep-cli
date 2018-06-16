import urwid
import constants
import gkeepapi
import query
import widget.note

class List(urwid.ListBox):
    def __init__(self, q: query.Query):
        self.query = q
        super(List, self).__init__(urwid.SimpleFocusListWalker([]))

    def refresh(self, keep: gkeepapi.Keep):
        self.body[:] = [
            urwid.BoxAdapter(widget.note.Note(n), 10) for n in self.query.filter(keep)
        ]

class KanBan(urwid.Columns):
    def __init__(self, qa: query.Query, qb: query.Query, qc: query.Query):
        self.lista = List(qa)
        self.listb = List(qb)
        self.listc = List(qc)

        super(KanBan, self).__init__([
            self.lista,
            self.listb,
            self.listc,
        ], dividechars=1)

    def refresh(self, keep: gkeepapi.Keep):
        self.lista.refresh(keep)
        self.listb.refresh(keep)
        self.listc.refresh(keep)
