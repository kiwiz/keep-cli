#!/usr/bin/python
# -*- coding: utf-8 -*-

import gkeepapi
import enum


class Attribute(enum.Enum):
    Title = "title"
    Text = "text"
    Selected = "selected"


TextColor = ("", "#222")
MutedColor = ("", "#666")

ColorMap = {
    gkeepapi.node.ColorValue.White: ("white", "h231"),
    gkeepapi.node.ColorValue.Red: ("dark red", "h210"),
    gkeepapi.node.ColorValue.Orange: ("light red", "h222"),
    gkeepapi.node.ColorValue.Yellow: ("yellow", "h228"),
    gkeepapi.node.ColorValue.Green: ("dark green", "h192"),
    gkeepapi.node.ColorValue.Teal: ("dark cyan", "h159"),
    gkeepapi.node.ColorValue.Blue: ("light blue", "h117"),
    gkeepapi.node.ColorValue.DarkBlue: ("dark blue", "h111"),
    gkeepapi.node.ColorValue.Purple: ("dark magenta", "h141"),
    gkeepapi.node.ColorValue.Pink: ("light magenta", "h218"),
    gkeepapi.node.ColorValue.Brown: ("brown", "h181"),
    gkeepapi.node.ColorValue.Gray: ("light gray", "h188"),
}


def _(*attrs):
    return ",".join(attrs)


Palette = [
    (Attribute.Selected.value, "black", "dark gray", "", TextColor[1], "h242"),
    ("BORDER", "light gray", "white", "", "h254", "h231"),
    ("TEXT", "black", "white", "", TextColor[1], "h231"),
    (
        "buTEXT",
        _("black", "underline", "bold"),
        "white",
        "",
        _(TextColor[1], "underline", "bold"),
        "h231",
    ),
    ("bTEXT", _("black", "bold"), "white", "", _(TextColor[1], "bold"), "h231"),
    ("mTEXT", "dark gray", "white", "", MutedColor[1], "h231"),
    ("STATUS", "black", "yellow", "", TextColor[1], "h214"),
]

for k, v in ColorMap.items():
    Palette.append((k.value, "black", v[0], "", TextColor[1], v[1]))

    # Bold variant
    Palette.append(
        ("b" + k.value, "black", v[0], "", _(TextColor[1], "underline", "bold"), v[1])
    )
    # Italicized variant
    Palette.append(("i" + k.value, "black", v[0], "", _(TextColor[1], "italics"), v[1]))
    # Label variant
    Palette.append(
        ("l" + k.value, "black", v[0], "", _(TextColor[1], "standout"), v[1])
    )
    # Underlined label variant
    Palette.append(
        (
            "lu" + k.value,
            "black",
            v[0],
            "",
            _(TextColor[1], "underline", "standout"),
            v[1],
        )
    )
    # Bold label variant
    Palette.append(
        ("lb" + k.value, "black", v[0], "", _(TextColor[1], "standout", "bold"), v[1])
    )
    # Underlined bold label variant
    Palette.append(
        (
            "lub" + k.value,
            "black",
            v[0],
            "",
            _(TextColor[1], "underline", "standout", "bold"),
            v[1],
        )
    )
    # Color variant
    Palette.append(("c" + k.value, v[0], v[0], "", TextColor[1], v[1]))
    # Underlined color variant
    Palette.append(("cu" + k.value, v[0], v[0], "", _(TextColor[1], "underline"), v[1]))
