import os

from sys import argv
from csv import writer

from src import *


def before_after_csv(before: list[str], after: list[str], filename: str):
    """Create a CSV file with two columns. Return the name of the file."""
    with open(f"{filename}.csv", newline="", encoding="utf-8", mode="w") as f:
        for w in zip(before, after):
            writer(f).writerow(u.strip() for u in w)


def main(args):
    args_dict = parse_cmd_args(args)

    sound_classes = json_to_dict(args_dict['sound-classes-file'])

    if (nsc := args_dict['named_sound_change']) is not None:
        named_rules = json_to_dict(nsc[0])
        chosen_rule = named_rules[nsc[1]]
        words = nsc[2].split()

        changed_words = changes_words([chosen_rule], words, sound_classes)

        if args_dict['csv_output'] == True:
            filename = make_filename()
            before_after_csv(words, changed_words, filename)
            created_file(filename + ".csv")

        else:
            for w in changed_words:
                print(w)

    if (fbsc := args_dict['file_based_sound_change']) is not None:
        rules = read_file(fbsc[0])
        words = list(map(lambda k: k.strip(), read_file(fbsc[1])))

        changed_words = changes_words(rules, words, sound_classes)

        filename = make_filename()

        if args_dict['csv_output'] == True:
            before_after_csv(words, changed_words, filename)
            created_file(filename + ".csv")

        else:
            filename += ".txt"
            with open(filename, encoding="utf-8", mode="w") as f:
                f.writelines(word + '\n' for word in changed_words)
            created_file(filename)


if __name__ == '__main__':
    main(argv[1:])
