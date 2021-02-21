from datetime import date
from functools import reduce
from json import load
from re import search
from itertools import chain

__all__ = ['closed_by_brackets', 'compose', 'json_to_dict', 'read_file', 'regex_groups', 'remove_brackets',
           'remove_empty_looks', 'today_str', 'valid_groups', 'search_prn', 'flatten']


def compose(*funcs):
    """Compose functions."""
    return reduce(lambda f, g: lambda *a, **kw: f(g(*a, **kw)), funcs)


def today_str() -> str:
    """Return today's date as a string in ISO underscore-separated format."""
    return str(date.today().isoformat()).replace("-", "_")


def read_file(file: str) -> list[str]:
    """Read file and return its contents as a list of strings."""
    with open(file, encoding="utf-8") as f: return f.readlines()


def json_to_dict(json_file: str) -> dict:
    """Open a JSON file and return its contents as a dictionary."""
    with open(json_file, encoding="utf-8") as j: return load(j)


def remove_empty_looks(x: str) -> str:
    """Remove regex's lookahead and lookbehind if empty."""
    return x.removeprefix("(?<=)").removesuffix("(?=)")


def regex_groups(match) -> tuple[str, str, str, str]:
    """Return the first four groups of a regex search"""
    return match[1], match[2], match[3], match[4]


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
    return list(chain.from_iterable(xs))
