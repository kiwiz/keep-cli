# -*- coding: utf-8 -*-
import urwid
import constants

class Labels(urwid.Columns):
    def __init__(self, labels):
        super(Labels, self).__init__([
            ('pack', urwid.Text(label.name)) for label in labels
        ], dividechars=1)

class Note(urwid.AttrMap):
    def __init__(self, note):
        w_text = urwid.Text(note.text)
        w_title = urwid.Text(('b' + str(note.color), note.title), wrap='clip')
        w_title = urwid.Text(('underline', note.title), wrap='clip')
        w_labels = Labels(note.labels.all())

        super(Note, self).__init__(
            urwid.Frame(
                urwid.Filler(
                    w_text,
                    valign='top'
                ),
                header=w_title,
                footer=w_labels
            ),
            note.color
        )


    """
        ('📥' if self.note.archived else '  ') +
        ('📍' if self.note.pinned else '  ')
    """
