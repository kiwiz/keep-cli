import os
import json
import logging
import gkeepapi


def load(config_dir: str, username: str) -> dict:
    cache_file = os.path.join(config_dir, "%s.json" % username)

    try:
        fh = open(cache_file, "r")
    except FileNotFoundError:
        logging.warning("Unable to find state file: %s", cache_file)
        return None

    try:
        state = json.load(fh)
    except json.decoder.JSONDecodeError:
        logging.warning("Unable to load state file: %s", cache_file)
        return None
    finally:
        fh.close()

    return state


def save(keep: gkeepapi.Keep, config_dir: str, username: str):
    cache_file = os.path.join(config_dir, "%s.json" % username)

    state = keep.dump()
    fh = open(cache_file, "w")
    json.dump(state, fh)
    fh.close()
