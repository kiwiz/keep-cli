import urwid
import gkeepapi
from . import note
from .. import query
from .. import constants

from typing import List

class NoteList(urwid.Frame):
    def __init__(self, q: query.Query):
        self.query = q
        self.w_list = urwid.ListBox(urwid.SimpleFocusListWalker([]))

        super(NoteList, self).__init__(
            self.w_list,
            header=urwid.Text(self.query.name, align=urwid.CENTER)
        )

    def refresh(self, keep: gkeepapi.Keep):
        self.w_list.body[:] = [
            urwid.BoxAdapter(note.Note(n), 10) for n in self.query.filter(keep)
        ]

class KanBan(urwid.Columns):
    def __init__(self, app: 'application.Application', queries: List[query.Query]):
        self.lists = [NoteList(q) for q in queries]

        super(KanBan, self).__init__(self.lists, dividechars=1)

    def refresh(self, keep: gkeepapi.Keep):
        for l in self.lists:
            l.refresh(keep)
