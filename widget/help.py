# -*- coding: utf-8 -*-
import urwid
import constants
import gkeepapi
import logging

from typing import List

class Help(urwid.Pile):
    def __init__(self):
        super(Help, self).__init__([
            urwid.Filler(urwid.Text(u'jkhl Move')),
            urwid.Filler(urwid.Text(u'f Pin')),
            urwid.Filler(urwid.Text(u'e Archive')),
        ])

    def keypress(self, size, key):
        key = super(Help, self).keypress(size, key)
        if key == 'esc':
            self.application.pop()
            key = None
        return key
