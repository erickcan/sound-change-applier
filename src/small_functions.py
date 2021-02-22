from datetime import date
from functools import reduce
from json import load
from re import search
from itertools import chain

from src.hash_dict import HashableDict

__all__ = ['closed_by_brackets', 'flatten', 'json_to_dict', 'read_file', 'remove_brackets',
           'remove_empty_looks', 'search_prn', 'today_str', 'valid_groups']


def today_str() -> str:
    """Return today's date as a string in ISO underscore-separated format."""
    return str(date.today().isoformat()).replace("-", "_")


def read_file(file: str) -> list[str]:
    """Read file and return its contents as a list of strings."""
    with open(file, encoding="utf-8") as f: return f.readlines()


def json_to_dict(json_file: str) -> HashableDict:
    """Open a JSON file and return its contents as a HashableDict."""
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


def search_prn(x: str):
    """Search for a phonological rule notation string. Returns a Match object or None."""
    return search(r"^(\S+) -> (\S+) / (\S*_\S*)$", x)


def flatten(xs: list[list]) -> list:
    """Transform a list of lists into a list."""
    return list(chain.from_iterable(xs))
