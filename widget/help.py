# -*- coding: utf-8 -*-
import urwid
import widget.util

from typing import Union

docs = [
    'Navigation',
    (('up', 'k'), 'Navigate up'),
    (('down', 'j'), 'Navigate down'),
    (('left', 'h'), 'Navigate left'),
    (('right', 'l'), 'Navigate right'),
    ('/', 'Search notes'),

    'Action',
    ('c', 'Compose a new note'),
    ('C', 'Compose a new list'),
    ('r', 'Sync with server'),
    ('#', 'Trash note'),
    ('f', 'Pin or unpin notes'),
    ('e', 'Archive note'),

    'Misc',
    ('?', 'Open keyboard shortcut help'),
    ('Esc', 'Finish editing / Quit'),
]

class Line(urwid.Columns):
    def __init__(self, key: Union[str, tuple], doc: str):
        super(Line, self).__init__([
            (urwid.WEIGHT, 2, urwid.Text(('mTEXT', doc))),
            urwid.Text(', '.join(key) if isinstance(key, tuple) else key),
        ], dividechars=1)

class Help(widget.util.Border):
    def __init__(self, app: 'application.Application'):
        self.application = app

        content = [
            urwid.Text(('buTEXT', 'Keyboard shortcuts'), align=urwid.CENTER),
        ]

        for line in docs:
            if isinstance(line, str):
                content.append(urwid.Divider())
                content.append(urwid.Text(('bTEXT', line)))
            else:
                content.append(Line(line[0], line[1]))

        super(Help, self).__init__(urwid.Pile(content))

    def selectable(self):
        return True

    def keypress(self, size, key):
        key = super(Help, self).keypress(size, key)
        if key == 'esc':
            self.application.overlay(None)
            key = None
        return key
