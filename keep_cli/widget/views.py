# -*- coding: utf-8 -*-
import urwid
from . import util

from typing import Union

class Views(util.Border):
    def __init__(self, app: 'application.Application'):
        self.application = app

        views = app.config.get('views')
        super(Views, self).__init__(urwid.Pile([
            urwid.Text(('buTEXT', 'Views'), align=urwid.CENTER),
            urwid.Divider(),
            urwid.Pile([urwid.Button(('TEXT', view.get('name', key))) for key, view in views.items()]),
        ]))

    def selectable(self):
        return True

    def keypress(self, size, key):
        key = super(Views, self).keypress(size, key)
        if key == 'esc':
            self.application.overlay(None)
            key = None
        return key
