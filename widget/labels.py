# -*- coding: utf-8 -*-
import urwid
import gkeepapi
import logging

from typing import List

class Label(urwid.Text):
    def __init__(self, label: gkeepapi.node.Label, color: gkeepapi.node.ColorValue):
        super(Label, self).__init__(('l' + color.value, label.name))

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key

class Labels(urwid.Columns):
    def __init__(self):
        super(Labels, self).__init__([], dividechars=1)

    def setLabels(self, labels: List[gkeepapi.node.Label], color: gkeepapi.node.ColorValue):
        self.contents = [
            (Label(label, color), self.options(urwid.PACK)) for label in labels
        ]
