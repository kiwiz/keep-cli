# -*- coding: utf-8 -*-
import urwid
import constants
import gkeepapi
import logging

from typing import List

class Labels(urwid.Columns):
    def __init__(self, labels: List[gkeepapi.node.Label], attribute: str):
        super(Labels, self).__init__([
            (urwid.PACK, urwid.Text((attribute, label.name))) for label in labels
        ], dividechars=1)

class Note(urwid.AttrMap):
    def __init__(self, note: gkeepapi.node.TopLevelNode):
        self.note = note
        self.w_header = urwid.Text('', align=urwid.RIGHT)
        self.w_footer = urwid.Text('', align=urwid.RIGHT)

        children = []

        if note.title:
            children.append((urwid.PACK, urwid.Text(('b' + note.color.value, note.title), wrap=urwid.CLIP)))

        children.append((urwid.PACK, urwid.Text(note.text)))

        if len(note.labels):
            children.append((urwid.PACK, urwid.Divider()))
            children.append((urwid.PACK, Labels(note.labels.all(), 'l' + note.color.value)))

        super(Note, self).__init__(
            urwid.Frame(
                urwid.Padding(
                    urwid.Pile(children),
                    align='center',
                    left=1,
                    right=1
                ),
                header=self.w_header,
                footer=self.w_footer,
            ),
            note.color.value,
            'GREEN'
        )

        self._updatePinned()
        self._updateArchived()

    def _updateArchived(self):
        self.w_footer.set_text('📥' if self.note.archived else '')

    def _updatePinned(self):
        self.w_header.set_text('📍' if self.note.pinned else '')

    def keypress(self, size, key):
        if key == 'f':
            self.note.pinned = not self.note.pinned
            self._updatePinned()
            key = None
        elif key == 'e':
            self.note.archived = not self.note.archived
            self._updateArchived()
            key = None
        elif key == 'z':
            label = gkeepapi.node.Label()
            label.name = 'a'
            self.note.labels.add(label)
            logging.error(self.note.labels.all())

        super(Note, self).keypress(size, key)
        return key
