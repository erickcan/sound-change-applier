import argparse
from sys import argv

from src.hash_dict import HashableDict


def parse_cmd_args(args_to_parse) -> HashableDict:
    """Parse command line arguments for the sound changer."""
    parser = argparse.ArgumentParser(prog="sound-changer")

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("-f", "--file-based-sound-change",
                       help="applies sound changes through files",
                       type=str, nargs=2,
                       metavar=("rules-file", "words-file"))
    group.add_argument("-n", "--named-sound-change",
                       help="applies a named sound change defined in a JSON file",
                       type=str, nargs=3,
                       metavar=("named-rules-file", "named-rule", "words"))

    parser.add_argument("--csv-output", help="creates a CSV file as output (default: txt)",
                        required=False, action="store_true")
    parser.add_argument("sound-classes-file",
                        help="JSON file where the sound classes are defined",
                        type=str)

    return HashableDict(parser.parse_args(args_to_parse).__dict__)
