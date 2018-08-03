#!/usr/bin/python
# -*- coding: utf-8 -*-

import gkeepapi
import enum

class Attribute(enum.Enum):
    Title = 'title'
    Text = 'text'
    Selected = 'selected'

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
    gkeepapi.node.ColorValue.Brown: ('brown', 'h181'),
    gkeepapi.node.ColorValue.Gray: ('light gray', 'h188'),
}

Palette = [
    (Attribute.Selected.value, '', '', '', TextColor[1], 'h242'),

    ('border', '', '', '', 'h254', 'h231'),
    ('modal', '', '', '', TextColor[1], 'h231'),
]

for k, v in ColorMap.items():
    Palette.append((k.value, 'black', v[0], '', TextColor[1], v[1]))

    # Bold variant
    Palette.append(('b' + k.value, 'black', v[0], '', ','.join([TextColor[1], 'underline', 'bold']), v[1]))
    # Italicized variant
    Palette.append(('i' + k.value, 'black', v[0], '', ','.join([TextColor[1], 'italics']), v[1]))
    # Label variant
    Palette.append(('l' + k.value, 'black', v[0], '', ','.join([TextColor[1], 'standout']), v[1]))
    # Color variant
    Palette.append(('c' + k.value, v[0], v[0], '', v[1], v[1]))
