import logging
import sys
import argparse
import gkeepapi
from . import application

logger = logging.getLogger(__name__)

def _ensure_note(keep: gkeepapi.Keep, note: str) -> gkeepapi.node.TopLevelNode:
    note = keep.get(note)
    if note is None:
        logger.error('Note not found')
        sys.exit(2)
    return note

def _ensure_sync(args: argparse.Namespace, keep: gkeepapi.Keep):
    if args.sync:
        keep.sync()


def tui(args: argparse.Namespace, keep: gkeepapi.Keep, config: dict):
    app = application.Application(keep, config, args.config_dir, args.offline)
    app.run()

def find(args: argparse.Namespace, keep: gkeepapi.Keep, config: dict):
    _ensure_sync(args, keep)
    notes = keep.find(
        query=args.query,
        labels=args.labels,
        colors=args.colors,
        pinned=args.pinned,
        archived=args.archived,
        trashed=args.trashed
    )
    for note in notes:
        print(note.id)

def sync(args: argparse.Namespace, keep: gkeepapi.Keep, config: dict):
    keep.sync()

def get(args: argparse.Namespace, keep: gkeepapi.Keep, config: dict):
    _ensure_sync(args, keep)
    note =_ensure_note(keep, args.note)
    none = not (args.title or args.text or args.unchecked or args.checked or args.labels)
    if none or args.title:
        print(note.title)
    if none or args.text:
        if isinstance(note, gkeepapi.node.List):
            entries = []
            if none or args.unchecked:
                entries += note.unchecked
            if none or args.checked:
                entries += note.checked
            for entry in entries:
                print(entry)
        else:
            print(note.text)
    if none or args.labels:
        for label in note.labels.all():
            print(label)

def set(args: argparse.Namespace, keep: gkeepapi.Keep, config: dict):
    _ensure_sync(args, keep)
    note =_ensure_note(keep, args.note)
