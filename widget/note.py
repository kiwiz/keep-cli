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
                header=urwid.Text('📍' if note.pinned else '', align=urwid.RIGHT),
                footer=urwid.Text('📥' if note.archived else '', align=urwid.RIGHT),
            ),
            note.color.value,
            'GREEN'
        )

    def keypress(self, size, key):
        if key == 'f':
            self.note.pinned = not self.note.pinned
            self._invalidate()
            key = None
        super(Note, self).keypress(size, key)
        return key
