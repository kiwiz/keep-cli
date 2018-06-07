# -*- coding: utf-8 -*-
import urwid
import constants

class Note(urwid.AttrMap):
    def __init__(self, note):
        w_text = urwid.Text(note.text)
        w_title = urwid.Text(('underline', note.title), wrap='clip')

        super(Note, self).__init__(
            urwid.Frame(
                urwid.Filler(
                    w_text,
                    valign='top'
                ),
                header=w_title
            ),
            note.color
        )


    """
    def render(self):
        w, h = self.getSize()
        min_y, max_y = self.borders[0], h - self.borders[1]
        min_x, max_x = self.borders[2], w - self.borders[3]
    self.win.addstr(
        y, x,
        ('📥' if self.note.archived else '  ') +
        ('📍' if self.note.pinned else '  ')
    )


        # Fill background
        for i in range(h):
            try:
                self.win.addstr(i, 0, ' ' * w)
            except curses.error:
                pass

        self._renderTray(w - 4, 0)

        text_width = max_x - min_x
        text_index = min_y
        if self.note.title:
            text_index += 1
            try:
                self.win.addstr(
                    min_y, min_x,
                    abbreviate(self.note.title, text_width).encode('UTF-8'),
                    curses.A_UNDERLINE
                )
            except curses.error:
                pass

        if max_y > text_index:
            if type(self.note) == gkeepapi.node.Note:
                entries = [abbreviate(line, text_width) for line in self.note.text.split("\n")]
            else:
                entries = [
                    (u'☒' if item.checked else u'☐') + abbreviate(item.text, max_x - min_x - 1) for item in self.note.items
                ]
            for i in range(min(max_y - text_index, len(entries))):
                try:
                    self.win.addstr(
                        i + text_index, min_x,
                        entries[i].encode('UTF-8'),
                    )
                except curses.error:
                    pass
        self.win.noutrefresh()
    """
