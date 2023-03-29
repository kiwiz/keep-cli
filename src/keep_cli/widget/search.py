# -*- coding: utf-8 -*-
import urwid
import gkeepapi
import logging
from . import labels
from . import edit
from . import util
from . import grid
from .. import query
from .. import constants

from typing import List

class Search(util.Border):
    def __init__(self, app: 'application.Application'):
        self.application = app

        self.w_pinned = urwid.CheckBox('Pinned', state='mixed', has_mixed=True)
        self.w_archived = urwid.CheckBox('Archived', state=False, has_mixed=True)
        self.w_trashed = urwid.CheckBox('Trashed', state=False, has_mixed=True)

        self.w_note = urwid.CheckBox('Note', state=True)
        self.w_list = urwid.CheckBox('List', state=True)

        self.w_labels = labels.Labels()
        self.w_colors = edit.Colors()

        self.w_labels.setLabels(app.keep.labels(), gkeepapi.node.ColorValue.White)

        self.w_header = urwid.Text(u'', align=urwid.RIGHT)
        self.w_footer = urwid.Text(u'', align=urwid.RIGHT)

        super(Search, self).__init__(urwid.Pile([
            urwid.Text(('buTEXT', 'Search'), align=urwid.CENTER),

            urwid.Divider(),

            urwid.Text(('bTEXT', 'State')),
            self.w_pinned,
            self.w_archived,
            self.w_trashed,

            urwid.Divider(),

            urwid.Text(('bTEXT', 'Type')),
            self.w_note,
            self.w_list,

            urwid.Divider(),

            urwid.Text(('bTEXT', 'Labels')),
            self.w_labels,

            urwid.Divider(),

            urwid.Text(('bTEXT', 'Colors')),
            self.w_colors,

            urwid.Divider(),

            urwid.Columns([
                urwid.Button('Apply', lambda x: self.onSearch()),
                urwid.Button('Cancel', lambda x: self.onCancel()),
            ], dividechars=1)
        ]))

    def onSearch(self):
        q = query.Query(
            labels=self.w_labels.getSelected() or None,
            colors=self.w_colors.getSelected() or None,
            pinned=self._getCheckboxValue(self.w_pinned),
            archived=self._getCheckboxValue(self.w_archived),
            trashed=self._getCheckboxValue(self.w_trashed)
        )

        self.application.replace(grid.Grid(self.application, q))
        self.application.overlay(None)

    def onCancel(self):
        self.application.overlay(None)

    def _getCheckboxValue(self, checkbox):
        state = checkbox.get_state()
        if isinstance(state, bool):
            return state
        return None

    def keypress(self, size, key):
        key = super(Search, self).keypress(size, key)
        return key
