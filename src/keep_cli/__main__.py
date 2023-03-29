#!/usr/bin/env python3
import sys
import os
import re
import argparse
import getpass
import logging
import yaml
import keyring
import gkeepapi
from keep_cli import commands
from keep_cli import util

logger = logging.getLogger("keep-cli")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("[%(levelname)s] %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


def path_type(path: str):
    return os.path.expanduser(path)


def re_type(exp: str):
    try:
        return re.compile(exp)
    except re.error as e:
        raise argparse.ArgumentTypeError(e.msg)


def bool_type(b: str):
    if b.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif b.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected")


def main():
    parser = argparse.ArgumentParser("Keep-CLI")
    parser.add_argument(
        "--config-dir",
        type=path_type,
        default="~/.keep",
        help="Configuration directory",
    )
    parser.add_argument("--offline", action="store_true", help="Offline mode")
    subparsers = parser.add_subparsers(help="Command", dest="command", required=True)

    parent_note_parser = argparse.ArgumentParser(add_help=False)
    parent_note_parser.add_argument("--note", type=str, help="Note id", required=True)

    tui_parser = subparsers.add_parser("tui", help="TUI interface")
    tui_parser.add_argument("--note", type=str, help="Note id")
    tui_parser.set_defaults(func=commands.tui)

    find_parser = subparsers.add_parser("find", help="Find all matching notes")
    find_parser.add_argument(
        "--query", type=re_type, help="Regular expression match on title & text"
    )
    find_parser.add_argument(
        "--colors", type=str, nargs="*", help="List of colors to match. Comma separated"
    )
    find_parser.add_argument(
        "--labels", type=str, nargs="*", help="List of labels to match. Comma separated"
    )
    find_parser.add_argument("--pinned", type=bool_type, help="Pinned status to match")
    find_parser.add_argument(
        "--archived", type=bool_type, help="Archived status to match"
    )
    find_parser.add_argument(
        "--trashed", type=bool_type, help="Trashed status to match"
    )
    find_parser.set_defaults(func=commands.find)

    get_parser = subparsers.add_parser(
        "get", help="Get data on a note", parents=[parent_note_parser]
    )
    get_parser.add_argument(
        "--title", action="store_true", help="Display title of a note"
    )
    get_parser.add_argument(
        "--text", action="store_true", help="Display body of a note"
    )
    get_parser.add_argument(
        "--checked", action="store_true", help="Display list checked items on a list"
    )
    get_parser.add_argument(
        "--unchecked", action="store_true", help="Display unchecked items on a list"
    )
    get_parser.add_argument(
        "--labels", action="store_true", help="Display labels on a note"
    )
    get_parser.set_defaults(func=commands.get)

    set_parser = subparsers.add_parser(
        "set", help="Set data on a note", parents=[parent_note_parser]
    )
    set_parser.add_argument("--title", type=str, help="Set title of a note")
    set_parser.add_argument("--text", type=str, help="Set body of a note")
    set_parser.set_defaults(func=commands.set_)

    sync_parser = subparsers.add_parser("sync", help="Manually sync keep notes")
    sync_parser.set_defaults(func=commands.sync)

    import_parser = subparsers.add_parser(
        "import", help="Import notes from a file or directory"
    )
    import_parser.add_argument(
        "--label", type=str, help="Label to add to imported notes"
    )
    import_parser.add_argument(
        "--delete", action="store_true", help="Delete missing notes"
    )
    import_parser.add_argument(
        "--dir", type=str, default="notes", help="Source directory"
    )
    import_parser.set_defaults(func=commands.import_)

    export_parser = subparsers.add_parser("export", help="Export notes to a directory")
    export_parser.add_argument(
        "--dir", type=str, default="notes", help="Target directory"
    )
    export_parser.set_defaults(func=commands.export)

    args = parser.parse_args()

    if not os.path.isdir(args.config_dir):
        os.makedirs(args.config_dir)

    config_file = os.path.join(args.config_dir, "config.yml")
    config = {}
    if os.path.isfile(config_file):
        with open(config_file, "r") as fh:
            config = yaml.load(fh, Loader=yaml.Loader)
    else:
        config = {
            "username": input("Username: "),
            "views": {
                "default": {
                    "name": "Default",
                    "type": "grid",
                },
            },
        }
        with open(config_file, "w") as fh:
            yaml.dump(config, fh, default_flow_style=False)

    keep = gkeepapi.Keep()

    logged_in = False

    if args.offline:
        logger.info("Offline mode")
        state = util.load(args.config_dir, config["username"])
        keep.load(None, state, False)
        logged_in = True

    token = keyring.get_password("google-keep-token", config["username"])
    if not logged_in and token:
        logger.info("Authenticating with token")
        state = util.load(args.config_dir, config["username"])

        try:
            keep.resume(config["username"], token, state=state, sync=False)
            logged_in = True
            logger.info("Success")
        except gkeepapi.exception.LoginException:
            logger.info("Invalid token")

    if not logged_in:
        password = getpass.getpass()
        try:
            keep.login(config["username"], password, sync=False)
            logged_in = True
            del password
            token = keep.getMasterToken()
            keyring.set_password("google-keep-token", config["username"], token)
            logger.info("Success")
        except gkeepapi.exception.LoginException:
            logger.info("Login failed")

    if not logged_in:
        logger.error("Failed to authenticate")
        sys.exit(1)

    args.func(args, keep, config)


if __name__ == "__main__":
    main()
