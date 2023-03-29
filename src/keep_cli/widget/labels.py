# -*- coding: utf-8 -*-
import urwid
import gkeepapi
import logging

from typing import List

class Label(urwid.AttrMap):
    def __init__(self, label: gkeepapi.node.Label, color: gkeepapi.node.ColorValue, selected=False):
        self.label = label
        self.color = color
        self.selected = selected

        super(Label, self).__init__(
            urwid.Text(label.name),
            'l' + color.value,
            'lu' + color.value,
        )

    def update(self):
        self.set_attr_map({None: ('lb' if self.selected else 'l') + self.color.value})
        self.set_focus_map({None: ('lub' if self.selected else 'lu') + self.color.value})

    def selectable(self):
        return True

    def keypress(self, size, key):
        if key == ' ':
            self.selected = not self.selected
            self.update()
            key = None
        return key

class Labels(urwid.Columns):
    def __init__(self):
        super(Labels, self).__init__([], dividechars=1)

    def setLabels(self, labels: List[gkeepapi.node.Label], color: gkeepapi.node.ColorValue):
        self.contents = [
            (Label(label, color), self.options(urwid.PACK)) for label in labels
        ]

    def getSelected(self) -> List[gkeepapi.node.Label]:
        return [item.label for item, _ in self.contents if item.selected]

