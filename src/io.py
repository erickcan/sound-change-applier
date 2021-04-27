import argparse
from csv import writer
from datetime import datetime as dt
from json import load
from typing import Optional

from src.hash_dict import HashableDict

__all__ = ["today_str", "read_file", "write_txt", "json_to_dict", "before_after_csv", "ScaArgs"]


def today_str() -> str:
    """Return today's date as a string in ISO hyphen-separated format."""
    return str(dt.now().isoformat("-", "seconds")).replace(":", "-")


def read_file(file: str) -> list[str]:
    """Read file and return its contents as a list of strings."""
    with open(file, encoding="utf-8") as f:
        return [line.strip() for line in f]


def write_txt(filename: str, contents: list[str]):
    """Write a list of strings to a text file."""
    filename += ".txt"
    with open(filename, encoding="utf-8", mode="w") as f:
        f.writelines(x + "\n" for x in contents)


def json_to_dict(json_file: Optional[str]) -> Optional[HashableDict]:
    """
    Open a JSON file and return its contents as `HashableDict`.

    Return `None` if `json_file` is `None`.
    """
    if json_file is None:
        return None
    else:
        with open(json_file, encoding="utf-8") as j:
            return HashableDict(load(j))


def before_after_csv(before: list[str], after: list[str], filename: str):
    """Create a two-column CSV file with `before` and `after` as columns."""
    filename += ".csv"
    with open(filename, newline="", encoding="utf-8", mode="w") as f:
        writer(f).writerows(zip(before, after))


class NotJsonFile(Exception):
    ...


def _open_sc_file(file: Optional[str]) -> Optional[HashableDict]:
    """
    Open the sound classes JSON file.

    Return `None` if `file` is `None`, otherwise return the contents of `file`
    as `HashableDict`. Raise `NotJsonFile` if `file` doesn't end with '.json'.
    """
    if file is not None:
        if not file.lower().endswith(".json"):
            raise NotJsonFile("sound-classes-json should be a JSON file")
    return json_to_dict(file)


def _parse_cmd_args(args_to_parse: list[str]) -> HashableDict:
    """Parse command line arguments for the sound change applier."""
    parser = argparse.ArgumentParser(
        prog="sound-change-applier-v2.0",
        description="A program that applies phonological rules to words.",
        epilog="For more information see README.md at <https://github.com/erickcan/sound-change-applier#readme>.",
    )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "-f",
        "--file-based-sound-change",
        help="applies sound changes through files",
        type=str,
        nargs=2,
        metavar=("rules-file", "words-file"),
    )
    group.add_argument(
        "-n",
        "--named-sound-change",
        type=str,
        nargs=3,
        help="applies a named sound change defined in a JSON file",
        metavar=("named-rules-json", "named-rule", "words"),
    )

    parser.add_argument(
        "--csv-output",
        action="store_true",
        help="creates a CSV file as output with the before and after of the words",
    )

    sc_file = parser.add_mutually_exclusive_group(required=False)

    sc_file.add_argument(
        "-s",
        "--sound-classes-json",
        metavar="sound-classes-json",
        type=str,
        help="JSON file with sound classes",
    )
    sc_file.add_argument("--no-sound-classes", action="store_true", help="do not use sound classes")

    return HashableDict(parser.parse_args(args_to_parse).__dict__)


class ScaArgs:
    def __init__(self, args: list[str]):
        self.args_dict: HashableDict = _parse_cmd_args(args)

    @property
    def ndsc(self) -> Optional[list[str]]:
        return self.args_dict["named_sound_change"]

    @property
    def fbsc(self) -> Optional[list[str]]:
        return self.args_dict["file_based_sound_change"]

    @property
    def sound_classes(self) -> Optional[HashableDict]:
        return (
            HashableDict({})
            if self.args_dict["no_sound_classes"]
            else _open_sc_file(self.args_dict["sound_classes_json"])
        )

    @property
    def csv_output(self) -> bool:
        return self.args_dict["csv_output"]
