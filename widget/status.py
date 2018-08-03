# -*- coding: utf-8 -*-
import urwid

class Status(urwid.AttrMap):
    def __init__(self, app: 'application.Application'):
        self.application = app

        super(Status, self).__init__(urwid.Columns([
            urwid.Text('Press ? for help')
        ]), 'STATUS')
