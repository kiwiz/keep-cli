# -*- coding: utf-8 -*-
import urwid
import constants
import gkeepapi
import logging

from typing import List

keys = [
    (('up', 'k'), 'Navigate up'),
    (('down', 'j'), 'Navigate down'),
    (('left', 'h'), 'Navigate left'),
    (('right', 'l'), 'Navigate right'),
    ('c', 'Compose a new note'),
    ('C', 'Compose a new list'),
    ('r', 'Sync with server'),
    ('/', 'Search notes'),
    ('?', 'Open keyboard shortcut help'),
    ('e', 'Archive note'),
    ('#', 'Trash note'),
    ('f', 'Pin or unpin notes'),
    ('Esc', 'Finish editing / Quit'),
]

class Line(urwid.Columns):
    def __init__(self, key, doc):
        super(Line, self).__init__([
            (urwid.WEIGHT, 2, urwid.Text(doc)),
            urwid.Text(', '.join(key) if isinstance(key, tuple) else key),
        ], dividechars=1)

class Border(urwid.AttrMap):
    def __init__(self, original_widget, title=''):
        super(Border, self).__init__(urwid.LineBox(
            urwid.AttrMap(urwid.Padding(original_widget, left=1, right=1), 'modal'),
            tlcorner='█', trcorner='█',
            blcorner='█', brcorner='█',
            tline='▀', lline='█', rline='█', bline='▄'
        ), 'border')

class Help(Border):
    def __init__(self, app: 'application.Application'):
        self.application = app
        super(Help, self).__init__(
            urwid.Pile((Line(key, doc) for key, doc in keys))
        )

    def selectable(self):
        return True

    def keypress(self, size, key):
        key = super(Help, self).keypress(size, key)
        if key == 'esc':
            self.application.overlay(None)
            key = None
        return key
