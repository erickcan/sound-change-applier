from sys import argv

from src import sound_changer as sc
from src import io


def main(args: list[str]):
    sca_args = io.ScaArgs(args)

    if sca_args.ndsc is not None:
        named_rules = io.json_to_dict(sca_args.ndsc[0])
        chosen_rule = named_rules[sca_args.ndsc[1]]
        words = sca_args.ndsc[2].split()

        phon_rule = sc.PhonRule(chosen_rule, sca_args.sound_classes)
        changed_words = list(map(phon_rule.apply, words))

        if not sca_args.csv_output:
            print(' '.join(changed_words))

    else:
        rules = io.read_file(sca_args.fbsc[0])
        words = io.read_file(sca_args.fbsc[1])

        phon_rules = sc.PhonRules(rules, sca_args.sound_classes)
        changed_words = list(map(phon_rules.apply, words))

        if not sca_args.csv_output:
            filename = f"sound-change-{io.today_str()}"
            io.write_txt(filename, changed_words)

    if sca_args.csv_output:
        filename = f"sound-change-{io.today_str()}"
        io.before_after_csv(words, changed_words, filename)


if __name__ == '__main__':
    try:
        main(argv[1:])
    except Exception as e:
        exit(f"{type(e).__name__}: {e}")
