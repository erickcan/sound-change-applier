from sys import argv
from csv import writer
from os import getcwd

from src.sound_changer import changes_words
from src.cmd_args import parse_cmd_args
from src.small_functions import json_to_dict, read_file, today_str


def before_after_csv(before: list[str], after: list[str]) -> str:
    """Create a CSV file with two columns. Return the filename."""
    filename = f"sound_change_{today_str()}.csv"
    with open(filename, newline="", encoding="utf-8", mode="w") as f:
        for w in zip(before, after):
            writer(f).writerow(u.strip() for u in w)

    return filename


def main(args):
    args_dict = parse_cmd_args(args)

    sound_classes = json_to_dict(args_dict['sound-classes-file'])

    if (nss := args_dict['named_sound_change']) is not None:
        named_rules = json_to_dict(nss[0])
        chosen_rule = named_rules[nss[1]]
        words = nss[2].split()

        changed_words = changes_words([chosen_rule], words, sound_classes)

        if args_dict['csv_output'] == True:
            filename = before_after_csv(words, changed_words)
            print(f"created {filename} in:", getcwd())

        else:
            for w in changed_words:
                print(w)

    if (fbsc := args_dict['file_based_sound_change']) is not None:
        rules = read_file(fbsc[0])
        words = list(map(lambda k: k.strip(), read_file(fbsc[1])))

        changed_words = changes_words(rules, words, sound_classes)

        if args_dict['csv_output'] == True:
            filename = before_after_csv(words, changed_words)
            print(f"created {filename} in:", getcwd())

        else:
            filename = f"sound_change_{today_str()}.txt"
            with open(filename, encoding="utf-8", mode="w") as f:
                f.writelines(word + '\n' for word in changed_words)
            print(f"created {filename} in:", getcwd())


if __name__ == '__main__':
    main(argv[1:])
