import urwid
import constants
import gkeepapi
import widget.note
import widget.grid

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
                widget.grid.Grid(note_widgets, 20, 1, 1, urwid.LEFT),
            valign=urwid.TOP),
            constants.Palette
        )

        loop.screen.set_terminal_properties(colors=256)
        loop.run()
