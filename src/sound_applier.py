import os
from csv import writer
from functools import cache
from re import sub, search
from typing import Callable

from src.small_functions import *

# sound classes defined in a JSON file
sound_classes = json_to_dict(os.path.abspath("./sound_classes.json"))

# rules whose names are defined in a JSON file
named_rules = json_to_dict(os.path.abspath("./named_rules.json"))

__all__ = ['call_named_rule', 'files_apply']


@cache
def interpret_rule(phonological_rule) -> Callable[[str], str]:
    """
    Convert a PRN string into a function.

    The string applied to this function should be in phonological
    rule notation (PRN), i.e., "before -> after / environment". The
    function returned applies this rule to a string.

    Sound classes are defined in the sound_classes.json file; one
    can define ad-hoc classes using square brackets.

    To delete a sound use a underscore after the arrow.

    :param str phonological_rule: phonological rule notation string
    :return: function that applies the sound change
    """

    def _rule_to_regex(x: str) -> str:
        x = sub("^#", "^", sub("#$", "$", x))  # "#a_b#" -> "^a_b$"
        x = x.split("_")                       # "^a_b$" -> ["^a", "b$"]
        x = (f"(?<={x[0]})", f"(?={x[1]})")    # ["^a", "b$"] -> ["(?<=^a)", "(?=b$)"]
        x = "_".join(x)                        # ["(?<=^a)", "(?=b$)"] -> "(?<=^a)_(?=b$)"

        # convert dictionary to regex classes
        for group, phones in sound_classes.items():
            x = sub(group, f"[{phones}]", x)

        return remove_empty_looks(x)

    if match := search(r"^(\S+) -> (\S+) / (\S*(_)\S*)$", phonological_rule):
        # before-sound, after-sound, where to change, underscore
        sound, changes_to, environment, location = regex_groups(match)

        # convert the environment string to regex
        regex_environ = _rule_to_regex(environment) \
            .replace(location, sound, 1)  # underscore becomes the sound being changed

        # function that applies the sound change
        return lambda word: sub(regex_environ, changes_to, word) \
            .replace("_", "", 1)  # delete the sound if it is an underscore
    else:
        raise Exception(f'"{phonological_rule}" is not a valid phonological rule notation.')


def files_apply(rules_file, words_file, csv_file=False) -> None:
    """
    Apply rules to words in specified in their own files and creates another.

    The first parameter to be passed is the name of the file where
    the rules are defined; each rule should be in its own line. The
    second parameter is the file where the words to change are.

    The optional parameter ``csv_file`` is whether to create a CSV
    file (True) with the before and after of the words or a text file
    (False) with only the words after the changes.

    :param str rules_file: file where the rules are
    :param str words_file: file where the words are
    :param bool csv_file: whether to create a .txt or CSV file.
    """

    rules = tuple(read_file(rules_file)[::-1])
    words = tuple(read_file(words_file))

    applied_words = apply_sound_change(rules)(words)

    filename = f"sound_change_{today_str()}.{'csv' if csv_file else 'txt'}"

    with open(filename, encoding="utf-8", mode="w", newline="") as f:
        if csv_file:
            for w in zip(words, applied_words):
                writer(f).writerow(u.strip() for u in w)
        else:
            f.writelines(applied_words)


@cache
def complex_rule(rule) -> list[str]:
    """
    Transform a complex rule into a list of simpler ones.

    Rules are considered 'complex' if they are a many-to-many
    change, e.g., "[xy] -> [zw] / _#". This function makes
    them a series of simpler rules, e.g., ["x -> z / _#",
    "y -> w / _#"].

    Only works if the before and after sounds consist solely
    of classes surrounded by square brackets, and nothing else.

    If the rule can't be further simplified, just returns the
    original argument as a list.

    :param str rule: phonological rule notation string
    :return: list of simplified rules
    """

    if match := search(r"^(\S+) -> (\S+) / (\S*(_)\S*)$", rule):
        before, after, where = regex_groups(match)[:3]

        if valid_groups(before, after):
            zip_list = zip(remove_brackets(before), remove_brackets(after))

            return [f"{ante} -> {post} / {where}" for ante, post in zip_list]
    return [rule]


def compose_rules(rules_list: list[str]) -> Callable[[str], str]:
    """Transform a list of rules into a function applying them right-to-left."""
    return compose(*map(interpret_rule, rules_list))


def call_named_rule(rule_name: str) -> Callable[[str], str]:
    """Calls a function applying the specified rule in the named_rules.json file."""
    return compose_rules(complex_rule(named_rules[rule_name]))


@cache
def apply_sound_change(rules) -> Callable[[list[str]], list[str]]:
    """
    Transform a sequence of rules into a function.

    A sequence of strings in phonological rule notation
    should be passed to this function; then this function
    returns another function that applies these sound
    changes to strings, representing the words to alter.

    The sound changes are read right-to-left.

    :param list[str] rules: sound changes to apply
    :return: function that applies these rules
    """

    list_list_func = map(complex_rule, rules)
    list_func = map(compose_rules, list_list_func)

    return lambda words: list(map(compose(*list_func), words))
