import urwid
import constants
import widget.note
import widget.grid

import gkeepapi
class _Note(object):
    def __init__(self):
        self.title = 'Title' * 30
        self.text = ' '.join(['Text'] * 50)
        self.color = gkeepapi.node.ColorValue.Green

class Application(object):
    """
    Entrypoint class
    """
    def __init__(self):
        pass

    def run(self):
        """
        Run keep-cli
        """
        loop = urwid.MainLoop(
            urwid.Filler(
                widget.grid.Grid([
                    urwid.BoxAdapter(widget.note.Note(_Note()), 10),
                    urwid.BoxAdapter(widget.note.Note(_Note()), 10),
                    urwid.BoxAdapter(widget.note.Note(_Note()), 10),
                    urwid.BoxAdapter(widget.note.Note(_Note()), 10),
                    urwid.BoxAdapter(widget.note.Note(_Note()), 10),
                ], 15, 1, 1, 'left'),
            valign='top'),
            constants.Palette
        )

        loop.screen.set_terminal_properties(colors=256)
        loop.run()
