import urwid
import logging

class Grid(urwid.GridFlow):
    def keypress(self, size, key):
        if key == 'j':
            key = 'down'
        elif key == 'k':
            key = 'up'
        elif key == 'h':
            key = 'left'
        elif key == 'l':
            key = 'right'
        super(Grid, self).keypress(size, key)
        return key
