# -*- coding: utf-8 -*-
import urwid
from . import util

from typing import Union

class Item(urwid.AttrMap):
    def __init__(self, key, label):
        self.key = key
        super(Item, self).__init__(
            urwid.Text(label),
            'TEXT', 'bTEXT'
        )

    def keypress(self, size, key):
        return key

    def selectable(self):
        return True

class Views(util.Border):
    def __init__(self, app: 'application.Application'):
        self.application = app

        views = app.config.get('views')
        self.w_list = urwid.Pile([
            (urwid.PACK, Item(key, view.get('name', key)))
        for key, view in views.items()])


        super(Views, self).__init__(urwid.Pile([
            urwid.Text(('buTEXT', 'Views'), align=urwid.CENTER),
            urwid.Divider(),
            self.w_list,
        ]))

    def selectable(self):
        return True

    def keypress(self, size, key):
        key = super(Views, self).keypress(size, key)
        if key == 'enter':
            view = self.w_list.focus.key
            w_view = self.application.hydrateView(view)
            self.application.replace(w_view)
            self.application.overlay(None)
            self.application.refresh()
            key = None
        return key
