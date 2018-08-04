# -*- coding: utf-8 -*-
import urwid

class Status(urwid.AttrMap):
    def __init__(self, app: 'application.Application'):
        self.application = app

        super(Status, self).__init__(urwid.Columns([
            urwid.Text(self.application.config['username']),
            urwid.Text('Press ? for help', align=urwid.RIGHT),
        ]), 'STATUS')
