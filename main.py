from csv import writer
from sys import argv
from typing import Optional

from src.cmd_args import parse_cmd_args
from src.hash_dict import HashableDict
from src.small_functions import json_to_dict, read_file, make_filename
from src.sound_changer import PhonRule, PhonRules


def main(args: list[str]):
    args_dict = parse_cmd_args(args)

    sound_classes: Optional[HashableDict] = _open_sc_file(args_dict["sound_classes_file"])

    ndsc = args_dict["named_sound_change"]
    fbsc = args_dict["file_based_sound_change"]

    if ndsc is not None:
        named_rules = json_to_dict(ndsc[0])
        chosen_rule = named_rules[ndsc[1]]
        words = ndsc[2].split()

        phon_rule = PhonRule(chosen_rule, sound_classes)
        changed_words = phon_rule.apply(words)

        if not args_dict["csv_output"]:
            for w in changed_words:
                print(w)

    else:
        rules = _open_txt(fbsc[0])
        words = _open_txt(fbsc[1])

        phon_rules = PhonRules(rules, sound_classes)
        changed_words = phon_rules.apply(words)

        if not args_dict["csv_output"]:
            filename = make_filename() + ".txt"
            with open(filename, encoding="utf-8", mode="w") as f:
                f.writelines(word + '\n' for word in changed_words)

    if args_dict["csv_output"]:
        _before_after_csv(words, changed_words, make_filename())


def _open_txt(filename: str) -> list[str]:
    return list(map(str.strip, read_file(filename)))


def _before_after_csv(before: list[str], after: list[str], filename: str):
    filename += ".csv"
    with open(filename, newline="", encoding="utf-8", mode="w") as f:
        for w in zip(before, after):
            writer(f).writerow(u.strip() for u in w)


def _open_sc_file(file: Optional[str]) -> Optional[HashableDict]:
    if file is not None:
        if not file.lower().endswith(".json"):
            raise TypeError(
                "sound-classes-file should be a JSON file"
            )
    return json_to_dict(file)


if __name__ == '__main__':
    try:
        main(argv[1:])
    except Exception as e:
        exit(f"{type(e).__name__}: {e}")
