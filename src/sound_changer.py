import re
from functools import singledispatchmethod
from typing import Optional, Union

from src.hash_dict import HashableDict

__all__ = ['PhonRule', 'PhonRules']


class InvalidPhonRule(Exception):
    pass


class InvalidSoundClass(Exception):
    pass


class PhonRule:
    """
    A phological rule.

    Valid ways of writing phonological rules:
    ```
    x > y / a_b
    x -> y / a_b
    x => y / a_b
    ```
    where `x` becomes `y` when `x` is between `a` and `b`.

    Raise `InvalidPhonRule` if the rule isn't considered valid.
    Raise `InvalidSoundClass` if any key of the `sound_classes`
    argument isn't an uppercase single-character string.
    """
    def __init__(self, rule_str: str,
                 sound_classes: Optional[HashableDict]=None):
        self._rule_str: str = rule_str

        match = re.match(
            r"^(?P<before>\S+) [-=]?> (?P<after>\S+) / (?P<where>\S*_\S*)$",
            self._rule_str
        )
        if match is None:
            raise InvalidPhonRule(
                f"{self._rule_str} is not a valid phonological rule notation."
            )

        self._before: str = match["before"]
        self._after: str = match["after"]
        self._where: str = match["where"]
        self._rule_list: list[str] = self._complex_rule()

        if len(invalids := _invalid_sound_classes(sound_classes)) != 0:
            raise InvalidSoundClass(
                f"{str(invalids)[1:-1]} are not valid sound classes"
            )

        self._sound_classes: HashableDict = sound_classes \
            if sound_classes is not None \
            else HashableDict({
                "V": "aeiou", "C": "bcdfghjklmnpqrstvwxyz",
                "S": "sz", "P": "pbtdkg", "F": "fvsz", "N": "mn",
            })


    @property
    def rule(self) -> str:
        """Get the rule as a string."""
        return self._rule_str

    @property
    def sound_classes(self) -> HashableDict:
        """Get the sound classes as a `HashableDict`."""
        return self._sound_classes

    @singledispatchmethod
    def apply(self, words: Union[str, list[str]]) -> Union[str, list[str]]:
        """Apply a phonological rule to word(s)."""
        raise NotImplementedError

    @apply.register
    def _(self, word: str) -> str:
        return self._changes_word(word)

    @apply.register
    def _(self, words: list) -> list[str]:
        return [self.apply(w) for w in words]

    def _complex_rule(self) -> list[str]:
        before_groups = _bracket_group(self._before)
        after_groups = _bracket_group(self._after)

        if before_groups is None or after_groups is None:
            return [self._rule_str]

        len_pre, len_post = len(before_groups[1]), len(after_groups[1])
        if len_pre == len_post and len_post != 0:
            zip_list = zip(before_groups[1], after_groups[1])
            pre_bg, pre_ag = before_groups[0], after_groups[0]
            post_bg, post_ag = before_groups[2], after_groups[2]

            return [
                f"{pre_bg}{x}{post_bg} -> {pre_ag}{y}{post_ag} / {self._where}"
                for x, y in zip_list
            ]
        else:
            return [self._rule_str]

    def _convert_to_regex(self):
        # "#a_b#" -> "#a_b$"
        where = re.sub("#$", "$", self._where)
        # "#a_b$" -> "^a_b$"
        where = re.sub("^#", "^", where)
        # "^a_b$" -> ["^a", "b$"]
        where = where.split("_")
        # ["^a", "b$"] -> ["(?<=^a)", "(?=b$)"]
        where = (f"(?<={where[0]})", f"(?={where[1]})")
        # ["(?<=^a)", "(?=b$)"] -> "(?<=^a)_(?=b$)"
        where = "_".join(where)

        for group, phones in self._sound_classes.items():
            where = re.sub(group, f"[{phones}]", where)

        where = where.replace("_", self._before, 1)

        return _remove_empty_looks(where), self._after.replace("_", "", 1)

    def _change_word(self, word: str) -> str:
        return re.sub(*self._convert_to_regex(), word)

    def _changes_word(self, word: str):
        for r in self._rule_list:
            word = PhonRule(r)._change_word(word)
        return word

    def __repr__(self):
        return f"PhonRule('{self._rule_str}', {self._sound_classes})"


class PhonRules:
    """
    A list of phonological rules.

    Valid ways of writing phonological rules:
    ```
    x > y / a_b
    x -> y / a_b
    x => y / a_b
    ```
    where `x` becomes `y` when `x` is between `a` and `b`.

    Raise `InvalidPhonRule` if any rule isn't considered valid.
    Raise `InvalidSoundClass` if any key of the `sound_classes`
    argument isn't an uppercase single-character string.
    """
    def __init__(self, rules: list[str],
                 sound_classes: Optional[HashableDict] = None):
        self._rules: list[str] = rules

        self._phonrules_list: list[PhonRule] = [
            PhonRule(rule, sound_classes) for rule in rules]

        self._sound_classes: HashableDict = sound_classes \
            if sound_classes is not None \
            else HashableDict({
                "V": "aeiou", "C": "bcdfghjklmnpqrstvwxyz",
                "S": "sz", "P": "pbtdkg", "F": "fvsz", "N": "mn",
            })

        if len(invalids := _invalid_sound_classes(self._sound_classes)) != 0:
            raise InvalidSoundClass(
                f"{str(invalids)[1:-1]} are not valid sound classes"
            )

    @property
    def rules(self) -> list[str]:
        """Get the rules as a list of strings."""
        return self._rules

    @property
    def phonrules_list(self) -> list[PhonRule]:
        """Get the rules as a list of `PhonRule`s."""
        return self._phonrules_list

    @property
    def sound_classes(self) -> HashableDict:
        """Get the sound classes as a `HashableDict`."""
        return self._sound_classes

    def apply(self, word: Union[str, list[str]]) -> Union[str, list[str]]:
        """Apply phonological rules to word(s)."""
        for r in self._phonrules_list:
            word = r.apply(word)
        return word

    def __repr__(self):
        return f"PhonRules({self._rules}, {self._sound_classes})"


def _remove_empty_looks(x: str) -> str:
    """Remove regex's lookahead and lookbehind if they are empty."""
    return x.removeprefix("(?<=)").removesuffix("(?=)")


def _bracket_group(x: str) -> Optional[tuple[str, str, str]]:
    """
    Divide a string in three parts: before, inside, and after the first bracket group.

    Return `None` if the square brackets never close or open.
    """
    depth = 0
    bef, whi, aft = "", "", ""
    place = "before_bracket"
    ended_bracket = False

    for char in x:

        if char == "[" and not ended_bracket:
            depth += 1
            place = "inside_bracket"

        elif char == "]":
            if ended_bracket:
                aft += char
            depth -= 1
            if depth == 0:
                place = "after_bracket"
                ended_bracket = True

        elif depth >= 0:
            if place == "before_bracket":
                bef += char
            elif place == "inside_bracket":
                whi += char
            else:
                aft += char

        elif depth < 0 and not ended_bracket:
            break

        else:
            continue

    return (bef, whi, aft) if (depth == 0 or ended_bracket) else None


def _invalid_sound_classes(d: HashableDict) -> list[str]:
    """
    Return a list of sound classes that are considered invalid.

    Sound classes are invalid if they are not a single-character
    string or are not uppercase.
    """
    invalid = filter(lambda x: not _is_upper_char(x), d.keys())
    return list(invalid)


def _is_upper_char(x: str) -> bool:
    """Return `True` if `x` is an uppercase single-character string, otherwise `False`."""
    return len(x) == 1 and x.isupper()
