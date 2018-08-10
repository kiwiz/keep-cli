# -*- coding: utf-8 -*-
import urwid

class Border(urwid.AttrMap):
    def __init__(self, original_widget):
        super(Border, self).__init__(urwid.LineBox(
            urwid.AttrMap(urwid.Padding(original_widget, left=1, right=1), 'TEXT'),
            tlcorner='█', trcorner='█',
            blcorner='█', brcorner='█',
            tline='▀', lline='█', rline='█', bline='▄'
        ), 'BORDER')
