import argparse
from sys import argv

from src.hash_dict import HashableDict


def parse_cmd_args(args_to_parse: list[str]) -> HashableDict:
    """Parse command line arguments for the sound change applier."""
    parser = argparse.ArgumentParser(
        prog="sound-change-applier v1.1",
        description="A program that applies phonological rules to words."
    )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("-f", "--file-based-sound-change",
                       help="applies sound changes through files",
                       type=str, nargs=2,
                       metavar=("rules-file", "words-file"))
    group.add_argument("-n", "--named-sound-change", type=str, nargs=3,
                       help="applies a named sound change defined in a JSON file",
                       metavar=("named-rules-file", "named-rule", "words"))

    parser.add_argument("--csv-output", required=False, action="store_true",
                        help="creates a CSV file as output with the before and after of the words")
    parser.add_argument("sound-classes-file", type=str,
                        help="JSON file with sound classes ('-' for default sound classes)")

    return HashableDict(parser.parse_args(args_to_parse).__dict__)
