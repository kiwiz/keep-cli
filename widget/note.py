# -*- coding: utf-8 -*-
import urwid
import constants
import gkeepapi

from typing import List

class Labels(urwid.Columns):
    def __init__(self, labels: List[gkeepapi.node.Label], attribute: str):
        super(Labels, self).__init__([
            ('pack', urwid.Text((attribute, label.name))) for label in labels
        ], dividechars=1)

class Note(urwid.AttrMap):
    def __init__(self, note: gkeepapi.node.TopLevelNode):
        children = []

        if note.title:
            children.append(('pack', urwid.Text(('b' + note.color.value, note.title), wrap='clip')))

        children.append(('pack', urwid.Text(note.text)))

        if len(note.labels):
            children.append(('pack', urwid.Divider()))
            children.append(('pack', Labels(note.labels.all(), 'l' + note.color.value)))

        super(Note, self).__init__(
            urwid.Frame(
                urwid.Padding(
                    urwid.Pile(children),
                    align='center',
                    left=1,
                    right=1
                ),
                header=urwid.Text('📍' if note.pinned else '', align='right'),
                footer=urwid.Text('📥' if note.archived else '', align='right'),
            ),
            note.color.value
        )
