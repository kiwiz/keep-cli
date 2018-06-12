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
        w_text = urwid.Text(note.text)
        w_labels = Labels(note.labels.all(), 'l' + note.color.value)
        w_title = None
        if note.title:
            w_title = urwid.Text(('b' + note.color.value, note.title), wrap='clip')

        super(Note, self).__init__(
            urwid.LineBox(
                urwid.Frame(
                    urwid.Filler(
                        w_text,
                        valign='top'
                    ),
                    header=w_title,
                    footer=w_labels
                ),
                tlcorner='',
                tline=' ',
                lline=' ',
                trcorner='',
                blcorner='',
                rline=' ',
                bline=' ',
                brcorner=''
            ),
            note.color.value
        )


    """
        ('📥' if self.note.archived else '  ') +
        ('📍' if self.note.pinned else '  ')
    """
