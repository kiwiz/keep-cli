#!/usr/bin/python
# -*- coding: utf-8 -*-

import gkeepapi
import enum

class Attribute(enum.Enum):
    Title = 'title'
    Text = 'text'

TextColor = ('', '#222')

ColorMap = {
    gkeepapi.node.ColorValue.White: ('', 'h231'),
    gkeepapi.node.ColorValue.Red: ('', 'h210'),
    gkeepapi.node.ColorValue.Orange: ('', 'h222'),
    gkeepapi.node.ColorValue.Yellow: ('', 'h228'),
    gkeepapi.node.ColorValue.Green: ('', 'h192'),
    gkeepapi.node.ColorValue.Teal: ('', 'h159'),
    gkeepapi.node.ColorValue.Blue: ('', 'h117'),
    gkeepapi.node.ColorValue.DarkBlue: ('', 'h111'),
    gkeepapi.node.ColorValue.Purple: ('', 'h141'),
    gkeepapi.node.ColorValue.Pink: ('', 'h218'),
    gkeepapi.node.ColorValue.Brown: ('', '#dcc'),
    gkeepapi.node.ColorValue.Gray: ('', 'h188'),
    'SELECTED': ('', 'h59'),
}

Palette = [
    (gkeepapi.node.ColorValue.Green, '', '', '', TextColor[1], 'h192'),
    (Attribute.Title.value, '', '', '', '#ff6', '#123'),
    (Attribute.Text.value, '', '', '', 'g37', 'g1'),
    ('underline', 'bold,underline', '', ''),
]
