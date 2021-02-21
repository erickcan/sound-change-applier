from re import sub
from functools import cache
import cProfile
import timeit

from src.small_functions import *
from src.hash_dict import HashableDict

__all__ = ['apply_rules_to_word', 'sound_changes_to_words']


@cache
def convert_to_regex(rule: str, sound_classes: HashableDict) -> tuple[str, str]:

    match = search_prn(rule)
    if match is None:
        raise Exception(f'"{rule}" is not a valid phonological rule notation')

    where = sub("^#", "^", sub("#$", "$", match[3]))  # "#a_b#" -> "^a_b$"
    where = where.split("_")                          # "^a_b$" -> ["^a", "b$"]
    where = (f"(?<={where[0]})", f"(?={where[1]})")   # ["^a", "b$"] -> ["(?<=^a)", "(?=b$)"]
    where = "_".join(where)                           # ["(?<=^a)", "(?=b$)"] -> "(?<=^a)_(?=b$)"

    # convert dictionary to regex classes
    for group, phones in sound_classes.items():
        where = sub(group, f"[{phones}]", where)

    where = where.replace("_", match[1], 1)

    return remove_empty_looks(where), match[2].replace("_", "", 1)


@cache
def change_sounds(rule: str, word: str, sound_classes: HashableDict) -> str:
    return sub(*convert_to_regex(rule, sound_classes), word)


@cache
def complex_rule(rule: str) -> list[str]:

    match = search_prn(rule)
    if match is None:
        raise Exception(f'"{rule}" is not a valid phonological rule notation')

    before, after, where = match[1], match[2], match[3]

    if valid_groups(before, after):
        zip_list = zip(remove_brackets(before), remove_brackets(after))

        return [f"{x} -> {y} / {where}" for x, y in zip_list]
    else:
        return [rule]


def compose_rules(rules: list[str]) -> list[str]:
    return flatten(complex_rule(rule) for rule in rules)


def apply_rules_to_word(rules: list[str], word: str, sound_classes: HashableDict) -> str:
    """Apply a list of sound changes to a word."""
    for rule in rules:
        word = change_sounds(rule, word, sound_classes)

    return word


def sound_changes_to_words(rules: list[str], words: list[str], sound_classes: HashableDict) -> list[str]:
    """Apply a list of rules to a list of words."""
    rules = compose_rules(rules)

    return [apply_rules_to_word(rules, word, sound_classes) for word in words]
