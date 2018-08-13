# -*- coding: utf-8 -*-
import urwid
import gkeepapi
from . import labels
from .. import constants
import logging

class Note(urwid.AttrMap):
    def __init__(self, note: gkeepapi.node.TopLevelNode):
        self.note = note

        tmp = urwid.Text('')

        self.w_title = urwid.Text(u'', wrap=urwid.CLIP)
        self.w_text = urwid.Text(u'')
        self.w_labels = labels.Labels()

        self.w_state = urwid.Text(u'', align=urwid.RIGHT)
        self.w_header = urwid.AttrMap(self.w_state, None)
        self.w_footer = urwid.Text(u'', align=urwid.RIGHT)
        self.w_content = urwid.Frame(
            urwid.Filler(self.w_text, valign=urwid.TOP),
            header=tmp,
            footer=tmp
        )

        super(Note, self).__init__(
            urwid.Frame(
                urwid.Padding(
                    self.w_content,
                    align='center',
                    left=1,
                    right=1
                ),
                header=self.w_header,
                footer=self.w_footer,
            ),
            note.color.value
        )

        self._updateContent()
        self._updateLabels()
        self._updateState()

    def _updateContent(self):
        w_title = (None, self.w_content.options())
        if self.note.title:
            w_title = (self.w_title, self.w_content.options())
            self.w_title.set_text(('b' + self.note.color.value, self.note.title))

        self.w_content.contents['header'] = w_title
        self.w_text.set_text(self.note.text)

    def _updateLabels(self):
        w_labels = (None, self.w_content.options())
        if len(self.note.labels):
            w_labels = (self.w_labels, self.w_content.options())
            self.w_labels.setLabels(self.note.labels.all(), self.note.color)

        self.w_content.contents['footer'] = w_labels

    def _updateFocus(self, focus):
        self.w_header.set_attr_map({None: constants.Attribute.Selected.value if focus else None})

    def _updateState(self):
        parts = [
            '🔄' if self.note.dirty else '  ',
            '📦' if self.note.archived else '  ',
            '📍' if self.note.pinned else '  ',
        ]
        self.w_state.set_text(''.join(parts))

    def render(self, size, focus=False):
        self._updateFocus(focus)
        return super(Note, self).render(size, focus)

    def keypress(self, size, key):
        if key == 'f':
            self.note.pinned = not self.note.pinned
            self._updateState()
            key = None
        elif key == 'e':
            self.note.archived = not self.note.archived
            self._updateState()
            key = None
        elif key == '#':
            self.note.trashed = True
            key = None

        key = super(Note, self).keypress(size, key)
        return key
