from re import sub
from functools import cache

from src.small_functions import flatten, search_prn, remove_empty_looks, remove_brackets, valid_groups
from src.hash_dict import HashableDict
from src.errs import NotPhonRule

__all__ = ['changes_words']


@cache
def convert_to_regex(rule, sound_classes) -> tuple[str, str]:
    """
    Convert a phonological rule notation string into a regex string.

    Returns a tuple consisting of a regex string representing the
    sound change and a string with the sound it changes to.

    Sound classes are defined in a HashableDict. The key defined at
    ``sound_classes`` dict is substituted by its respective value as
    a regex set of characters.

    Raise NotPhonRule if ``rule`` is not a valid phonological rule
    notation.

    :param str rule: sound change in phonological rule notation
    :param HashableDict sound_classes: sound classes
    :return: regex string, sound after change
    """

    match = search_prn(rule)
    if match is None:
        raise NotPhonRule(rule)

    where = sub("^#", "^", sub("#$", "$", match[3]))  # "#a_b#" -> "^a_b$"
    where = where.split("_")                          # "^a_b$" -> ["^a", "b$"]
    where = (f"(?<={where[0]})", f"(?={where[1]})")   # ["^a", "b$"] -> ["(?<=^a)", "(?=b$)"]
    where = "_".join(where)                           # ["(?<=^a)", "(?=b$)"] -> "(?<=^a)_(?=b$)"

    # convert dictionary to regex set
    for group, phones in sound_classes.items():
        where = sub(group, f"[{phones}]", where)

    where = where.replace("_", match[1], 1)

    return remove_empty_looks(where), match[2].replace("_", "", 1)


@cache
def change_word(rule: str, word: str, sound_classes: HashableDict) -> str:
    """Apply a sound change to a word."""
    return sub(*convert_to_regex(rule, sound_classes), word)


@cache
def complex_rule(rule: str) -> list[str]:
    """
    Convert a complex sound change (many-to-many) into a list of simpler ones.

    For example, ``complex_rule("[eo] -> [iu] / _#")`` evaluates to
    ["e -> i / _#", "o -> u / _#"].

    Raise NotPhonRule if ``rule`` is not a valid phonological rule notation.
    """

    match = search_prn(rule)
    if match is None:
        raise NotPhonRule(rule)

    before, after, where = match[1], match[2], match[3]

    if valid_groups(before, after):
        zip_list = zip(remove_brackets(before), remove_brackets(after))

        return [f"{x} -> {y} / {where}" for x, y in zip_list]
    else:
        return [rule]


def changes_word(rules: list[str], word: str, sound_classes: HashableDict) -> str:
    """Apply a list of sound changes to a word."""
    for rule in rules:
        word = change_word(rule, word, sound_classes)

    return word


def changes_words(rules: list[str], words: list[str], sound_classes: HashableDict) -> list[str]:
    """Apply a list of sound changes to a list of words."""
    rules = flatten(complex_rule(rule) for rule in rules)

    return [changes_word(rules, word, sound_classes) for word in words]
