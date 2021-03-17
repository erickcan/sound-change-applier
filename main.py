import os
from sys import argv
from csv import writer

from src import *


def before_after_csv(before: list[str], after: list[str], filename: str):
    """Create a CSV file with two columns in the cwd and print that the file was created."""
    filename = f"{os.path.join(os.getcwd(), filename)}.csv"
    with open(filename, newline="", encoding="utf-8", mode="w") as f:
        for w in zip(before, after):
            writer(f).writerow(u.strip() for u in w)

    created_file(filename)


def try_changes_words(rules: list[str], words: list[str], sound_classes: HashableDict) -> list[str]:
    """Try to change words, raise NotPhonRule if any rule is not valid."""
    try:
        changed_words = changes_words(rules, words, sound_classes)
    except NotPhonRule as e:
        exit(e)

    return changed_words


def main(args):
    args_dict = parse_cmd_args(args)

    sound_classes_filename = args_dict['sound-classes-file']
    sound_classes = HashableDict({
        "V": "aeiou", "C": "bcdfghjklmnpqrstvwxyz",
        "P": "pbtdkg", "F": "fvsz", "N": "mn", "S": "sz"
        }) if sound_classes_filename == "-"\
        else try_open_json(sound_classes_filename, "sound-classes-file")

    if (nsc := args_dict['named_sound_change']) is not None:

        named_rules = try_open_json(nsc[0], "named-rules-file")
        chosen_rule = named_rules[nsc[1]]
        words = nsc[2].split()

        changed_words = try_changes_words([chosen_rule], words, sound_classes)

        if args_dict['csv_output']:
            filename = make_filename()
            before_after_csv(words, changed_words, filename)

        else:
            for w in changed_words:
                print(w)

    if (fbsc := args_dict['file_based_sound_change']) is not None:

        rules = try_open_txt(fbsc[0], "rules-file")
        words = try_open_txt(fbsc[1], "words-file")

        changed_words = try_changes_words(rules, words, sound_classes)

        filename = make_filename()

        if args_dict['csv_output']:
            before_after_csv(words, changed_words, filename)

        else:
            filename = f"{os.path.join(os.getcwd(), filename)}.txt"
            with open(filename, encoding="utf-8", mode="w") as f:
                f.writelines(word + '\n' for word in changed_words)
            created_file(filename)


if __name__ == '__main__':
    main(argv[1:])
