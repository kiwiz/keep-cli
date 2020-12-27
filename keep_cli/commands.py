import logging
import sys
import argparse
import gkeepapi
import os
import glob
import re
import io
import random
import itertools
from typing import List, Dict, Tuple, Optional
from . import application
from . import util


logger = logging.getLogger(__name__)


NONWORD_RE = re.compile(r"\W")
FILE_RE = re.compile(r"^.+ \((.+?)\)\.md$")
TITLE_RE = re.compile(r"^# (.*)$")
OPTION_RE = re.compile(r"^<!-- (.*) -->$")
LISTITEM_RE = re.compile(r"^(    )?- \[(x| )\] (.*)$")


def _ensure_note(keep: gkeepapi.Keep, note_id: str) -> gkeepapi.node.TopLevelNode:
    note = keep.get(note_id)
    if note is None:
        logger.error("Note not found")
        sys.exit(2)
    return note


def _sync(args: argparse.Namespace, keep: gkeepapi.Keep, config: dict, save: bool):
    if not args.offline:
        keep.sync()

    if save:
        util.save(keep, args.config_dir, config["username"])


def tui(args: argparse.Namespace, keep: gkeepapi.Keep, config: dict):
    app = application.Application(keep, config, args.config_dir, args.offline)
    app.run()


def find(args: argparse.Namespace, keep: gkeepapi.Keep, config: dict):
    _sync(args, keep, config, True)
    notes = keep.find(
        query=args.query,
        labels=args.labels,
        colors=args.colors,
        pinned=args.pinned,
        archived=args.archived,
        trashed=args.trashed,
    )
    for note in notes:
        print(note.id)


def get(args: argparse.Namespace, keep: gkeepapi.Keep, config: dict):
    _sync(args, keep, config, True)
    note = _ensure_note(keep, args.note)
    none = not (
        args.title or args.text or args.unchecked or args.checked or args.labels
    )

    if none or args.title:
        print(note.title)

    if none or args.text:
        if isinstance(note, gkeepapi.node.List):
            none_completion = not (args.unchecked or args.checked)
            entries = []
            if none_completion or args.unchecked:
                entries += note.unchecked
            if none_completion or args.checked:
                entries += note.checked
            for entry in entries:
                print(entry)

        else:
            print(note.text)

    if none or args.labels:
        for label in note.labels.all():
            print(label)


def set_(args: argparse.Namespace, keep: gkeepapi.Keep, config: dict):
    _sync(args, keep, config, False)
    note = _ensure_note(keep, args.note)

    if args.title is not None:
        note.title = args.title

    if args.text is not None:
        note.text = args.text

    # FIXME: Handle list items

    _sync(args, keep, config, True)


def sync(args: argparse.Namespace, keep: gkeepapi.Keep, config: dict):
    _sync(argparse.Namespace(offline=False), keep, config, True)


def _init_export_dir(root: str):
    os.makedirs(root, exist_ok=True)
    os.makedirs(os.path.join(root, "archived"), exist_ok=True)
    os.makedirs(os.path.join(root, "trashed"), exist_ok=True)
    os.makedirs(os.path.join(root, "deleted"), exist_ok=True)


def _get_export_path(note: gkeepapi.node.TopLevelNode, root: str) -> str:
    title = note.title.strip()
    if title:
        title = NONWORD_RE.sub("-", title.lower())
    else:
        title = "untitled"

    fn = "%s (%s).md" % (title, note.id)

    path_parts = [root]
    if note.trashed:
        path_parts.append("trashed")
    elif note.archived:
        path_parts.append("archived")
    path_parts.append(fn)
    return os.path.join(*path_parts)


def _enum_export_fns(
    root: str, keep: gkeepapi.Keep
) -> Tuple[List[str], List[str], Dict]:
    new_files = []
    untracked_files = []
    existing_files = {}

    # Enumerate existing files
    for path in itertools.chain(
        glob.glob(
            os.path.join(root, "*.md"),
        ),
        glob.glob(
            os.path.join(root, "{archived,trashed}", "*.md"),
        ),
    ):
        fn = os.path.basename(path)
        m = FILE_RE.search(fn)
        if not m:
            # If filename format doesn't match, assume new file
            new_files.append(path)
            continue

        note = keep.get(m.group(1))
        if not note:
            # If note id doesn't exist, assume deleted file
            untracked_files.append(path)
        else:
            # Otherwise, the file maps to an existing note
            if note.id in existing_files:
                logger.warning("Multiple files found for note with id: %s", note.id)
            existing_files[note.id] = path

    return new_files, untracked_files, existing_files


def _read_export_file(
    keep: gkeepapi.Keep,
    fh: io.IOBase,
    note: Optional[gkeepapi.node.TopLevelNode] = None,
) -> gkeepapi.node.TopLevelNode:
    lines = fh.readlines()

    title = ""
    color = gkeepapi.node.ColorValue.White
    pinned = False
    archived = False
    labels = set()
    items = []

    # Extract the title
    i = 0
    m = TITLE_RE.search(lines[i])
    if m:
        title = m.group(1)
        i += 1

    # Extract all the options
    options = []
    while i < len(lines):
        m = OPTION_RE.search(lines[i])
        if not m:
            break
        options.append(m.group(1))
        i += 1

    # Process the options
    for option in options:
        parts = option.split(" ", 1)
        if parts[0] == "pinned":
            pinned = True
        elif parts[0] == "archived":
            archived = True
        elif parts[0] == "color":
            if len(parts) == 2:
                try:
                    color = gkeepapi.node.ColorValue(parts[1].upper())
                except ValueError:
                    logger.warning("Unknown color option: %s", parts[1])
        elif parts[0] == "label":
            labels.add(parts[1])
        else:
            logger.warning("Unknown option: %s", parts[0])

    # Initialize note (if necessary)
    if note is None:
        labels.add(args.label)
        if len(lines) > i and LISTITEM_RE.search(lines[i]):
            note = gkeepapi.node.List()
        else:
            note = gkeepapi.node.Note()

    # Extract content
    if isinstance(note, gkeepapi.node.List):
        # Extract list items
        first = True
        item = []
        indented = False
        checked = False
        while i < len(lines):
            m = LISTITEM_RE.search(lines[i])
            if not m:
                if first:
                    logger.warning("Invalid listitem entry: %s", lines[i])
                else:
                    item.append(lines[i])
            else:
                if not first:
                    items.append((indented, checked, "\n".join(item)))
                    item = []

                indented_str, checked_str, content = m.groups()
                indented = bool(indented_str)
                checked = " " != checked_str
                item.append(content)

            first = False
            i += 1

        if not first:
            items.append((indented, checked, "\n".join(item)))

        # Sync up items to the list
        i = 0
        list_items = note.items
        sort = random.randint(1000000000, 9999999999)

        while True:
            a_ok = i < len(items)
            b_ok = i < len(list_items)

            # Update an existing item
            if a_ok and b_ok:
                indented, checked, content = items[i]
                list_item = list_items[i]
                if indented != list_item.indented:
                    list_item.indented = indented
                if checked != list_item.checked:
                    list_item.checked = checked
                if content != list_item.text:
                    list_item.text = content
                sort = int(list_item.sort)
            # Create a new item
            elif a_ok:
                indented, checked, content = items[i]
                list_item = note.add(content, checked, sort)
                if indented:
                    list_item.indent()
                sort -= gkeepapi.node.List.SORT_DELTA
            # Remove a deleted item
            elif b_ok:
                list_items[i].delete()
            else:
                break
            i += 1
    else:
        text = "\n".join(lines[i:])
        if note.text != text:
            note.text = text

    # Apply labels
    note_labels = set((label.name for label in note.labels.all()))
    new_labels = labels - note_labels
    del_labels = note_labels - labels
    for label in new_labels:
        note.labels.add(keep.findLabel(label, True))
    for label in del_labels:
        note.labels.remove(keep.findLabel(label))

    # Apply all other changes
    if note.title != title:
        note.title = title
    if note.pinned != pinned:
        note.pinned = pinned
    if note.archived != archived:
        note.archived = archived
    if note.color != color:
        note.color = color

    return note


def import_(args: argparse.Namespace, keep: gkeepapi.Keep, config: dict):
    _sync(args, keep, config, False)
    _init_export_dir(args.dir)

    new_files, untracked_files, existing_files = _enum_export_fns(args.dir, keep)

    # Process notes to update
    for note_id, path in existing_files.items():
        note = keep.get(note_id)

        # Read in the markdown file
        with open(path, "r") as fh:
            note = _read_export_file(keep, fh, note)

    # Process notes to create
    for path in new_files:
        # Read in the markdown file
        with open(path, "r") as fh:
            note = _read_export_file(keep, fh)
            keep.add(note)
            new_path = _get_export_path(note, args.dir)
            os.rename(path, new_path)
            logger.info("Created new note: %s", new_path)

    # Process notes to delete
    if args.delete:
        for note in keep.all():
            path = _get_export_path(note, args.dir)
            if os.path.exists(path):
                continue
            note.delete()
            logger.warning("Removed deleted note: %s", path)

    _sync(args, keep, config, True)


def _write_export_file(fh: io.IOBase, note: gkeepapi.node.TopLevelNode):
    # Write title
    fh.write("# %s\n" % note.title)

    # Write all options
    if note.pinned:
        fh.write("<!-- pinned -->\n")
    if note.color:
        fh.write("<!-- color %s -->\n" % note.color.value.lower())
    for label in note.labels.all():
        fh.write("<!-- label %s -->\n" % label.name)

    # Write content
    if isinstance(note, gkeepapi.node.List):
        # Write out each list item
        for item in note.items:
            fh.write(
                "%s- [%s] %s\n"
                % (
                    "    " if item.indented else "",
                    "x" if item.checked else " ",
                    item.text,
                )
            )
    else:
        # Write out the text
        fh.write(note.text)


def export(args: argparse.Namespace, keep: gkeepapi.Keep, config: dict):
    _sync(args, keep, config, True)
    _init_export_dir(args.dir)

    _, untracked_files, existing_files = _enum_export_fns(args.dir, keep)

    # Move deleted files to the "deleted" directory
    for deleted_file in untracked_files:
        fn = os.path.basename(deleted_file)
        os.rename(deleted_file, os.path.join(args.dir, "deleted", fn))
        logger.warning("Removed deleted note: %s", deleted_file)

    # Sync down existing notes
    for note in keep.all():
        # Determine target filename
        path = _get_export_path(note, args.dir)

        # Move existing file to new location if necessary
        if note.id in existing_files and path != existing_files[note.id]:
            os.rename(existing_files[note.id], path)

        # Write out the markdown file
        with open(path, "w") as fh:
            _write_export_file(fh, note)
