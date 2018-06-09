import urwid
import constants
import widget.note
import widget.grid

import gkeepapi
class Label(object):
    def __init__(self, name):
        self.name = name
class _Note(object):
    def __init__(self):
        self.title = 'Title' * 30
        self.text = ' '.join(['Text'] * 50)
        self.color = gkeepapi.node.ColorValue.Green
        self.labels = [Label('todo'), Label('nobo')]

class Application(object):
    """
    Entrypoint class
    """
    def __init__(self, keep: gkeepapi.Keep):
        self.keep = keep

    def run(self):
        """
        Run keep-cli
        """
        notes = self.keep.find(archived=False)
        note_widgets = [urwid.BoxAdapter(widget.note.Note(n), 10) for n in notes]

        loop = urwid.MainLoop(
            urwid.Filler(
                widget.grid.Grid(note_widgets, 20, 1, 1, 'left'),
            valign='top'),
            constants.Palette
        )

        loop.screen.set_terminal_properties(colors=256)
        loop.run()
