#!/usr/bin/python
# -*- coding: utf-8 -*-

import gkeepapi
import enum

class Attribute(enum.Enum):
    Title = 'title'
    Text = 'text'

TextColor = ('', '#222')

ColorMap = {
    gkeepapi.node.ColorValue.White: ('white', 'h231'),
    gkeepapi.node.ColorValue.Red: ('dark red', 'h210'),
    gkeepapi.node.ColorValue.Orange: ('dark red', 'h222'),
    gkeepapi.node.ColorValue.Yellow: ('brown', 'h228'),
    gkeepapi.node.ColorValue.Green: ('dark green', 'h192'),
    gkeepapi.node.ColorValue.Teal: ('dark cyan', 'h159'),
    gkeepapi.node.ColorValue.Blue: ('dark blue', 'h117'),
    gkeepapi.node.ColorValue.DarkBlue: ('dark blue', 'h111'),
    gkeepapi.node.ColorValue.Purple: ('dark magenta', 'h141'),
    gkeepapi.node.ColorValue.Pink: ('dark magenta', 'h218'),
    gkeepapi.node.ColorValue.Brown: ('brown', '#dcc'),
    gkeepapi.node.ColorValue.Gray: ('light gray', 'h188'),
    'SELECTED': ('', 'h59'),
}

Palette = [
    (Attribute.Title.value, '', '', '', '#ff6', '#123'),
    (Attribute.Text.value, '', '', '', 'g37', 'g1'),
    ('underline', 'bold,underline', '', ''),
]

for k, v in ColorMap.items():
    Palette.append((k, 'black', v[0], '', TextColor[1], v[1]))
    Palette.append(('b' + str(k), 'black', v[0], '', TextColor[1], v[1]))
