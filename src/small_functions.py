from datetime import datetime as dt
from json import load
from typing import Optional

from src.hash_dict import HashableDict

__all__ = ['closed_by_brackets', 'json_to_dict', 'read_file',
           'remove_brackets', 'remove_empty_looks', 'today_str',
           'valid_groups', 'make_filename']


def today_str() -> str:
    """Return today's date as a string in ISO hyphen-separated format."""
    return str(dt.now().isoformat("-", "seconds")).replace(":", "-")


def read_file(file: str) -> list[str]:
    """Read file and return its contents as a list of strings."""
    with open(file, encoding="utf-8") as f: return f.readlines()


def json_to_dict(json_file: Optional[str]) -> Optional[HashableDict]:
    """Open a JSON file and return its contents as a HashableDict."""
    if json_file is None: return None
    with open(json_file, encoding="utf-8") as j: return HashableDict(load(j))


def remove_empty_looks(x: str) -> str:
    """Remove regex's lookahead and lookbehind if empty."""
    return x.removeprefix("(?<=)").removesuffix("(?=)")


def start_end_with(x: str, start: str, end: str) -> bool:
    """Return whether a string starts and ends with ``start`` and ``end``."""
    return x.startswith(start) and x.endswith(end)


def closed_by_brackets(x: str) -> bool:
    """Return whether a string starts and ends with square brackets."""
    return start_end_with(x, "[", "]")


def valid_groups(x: str, y: str) -> bool:
    """Return whether ``x`` and ``y`` are valid groups (enclosed by square brackets and equal size)."""
    return closed_by_brackets(x) and closed_by_brackets(y) and len(x) == len(y)


def remove_brackets(x: str) -> str:
    """Remove starting and ending square brackets of a string."""
    return x.removeprefix("[").removesuffix("]")


def make_filename() -> str:
    """Create a name for the sound change file."""
    return f"sound-change-{today_str()}"
