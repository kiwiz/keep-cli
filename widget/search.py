# -*- coding: utf-8 -*-
import urwid
import constants
import gkeepapi
import logging
import widget.labels
import widget.edit

from typing import List

class Search(urwid.Filler):
    def __init__(self, app: 'application.Application'):
        self.application = app

        self.w_pinned = urwid.CheckBox('Pinned', state=False, has_mixed=True)
        self.w_archived = urwid.CheckBox('Archived', state='mixed', has_mixed=True)
        self.w_trashed = urwid.CheckBox('Trashed', state=False, has_mixed=True)

        self.w_note = urwid.CheckBox('Note', state=True)
        self.w_list = urwid.CheckBox('List', state=True)

        self.w_labels = widget.labels.Labels()
        self.w_colors = widget.edit.Colors()

        self.w_labels.setLabels(app.keep.labels(), gkeepapi.node.ColorValue.White)

        self.w_header = urwid.Text(u'', align=urwid.RIGHT)
        self.w_footer = urwid.Text(u'', align=urwid.RIGHT)

        super(Search, self).__init__(urwid.Pile([
            urwid.Text('State'),
            self.w_pinned,
            self.w_archived,
            self.w_trashed,

            urwid.Divider(),

            urwid.Text('Type'),
            self.w_note,
            self.w_list,

            urwid.Divider(),

            urwid.Text('Labels'),
            self.w_labels,

            urwid.Divider(),

            urwid.Text('Colors'),
            self.w_colors
        ]))

    def keypress(self, size, key):
        key = super(Search, self).keypress(size, key)
        return key
