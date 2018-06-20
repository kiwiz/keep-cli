# -*- coding: utf-8 -*-
import urwid
import gkeepapi
import logging

from typing import List

class Labels(urwid.Columns):
    def __init__(self):
        super(Labels, self).__init__([], dividechars=1)

    def setLabels(self, labels: List[gkeepapi.node.Label], color: gkeepapi.node.ColorValue):
        self.contents = [
            (urwid.Text(('l' + color.value, label.name)), self.options(urwid.PACK)) for label in labels
        ]
