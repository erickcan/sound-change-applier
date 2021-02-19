from sys import stdout, exit, argv

from src import *


def main(args):
    def first_arg(name: str, short: str) -> bool:
        return (f"--{name}" == args[0]) or (f"-{short}" == args[0])

    if first_arg("help", "h"):
        print("""
--help | -h\n\tshow this message\n
--named-rule | -n rule-name word [word [···]]\n\tapplies a named sound change to word(s)\n
--file-based-sound-change | -f rules-filepath words-filepath [--csv-output]\n\tapplies \
sound changes to words (each defined in their own files), and creates a .txt or .csv file \
with these words\n
""")

    elif first_arg("named-rule", "n"):
        for word in args[2:]:
            print(call_named_rule(args[1])(word))

    elif first_arg("file-based-sound-change", "f"):
        files_apply(args[1], args[2], "--csv-output" in args)

    else:
        print("Invalid command.", file=stdout)
        exit(1)

    return None


if __name__ == '__main__':
    main(argv[1:])
    exit(0)
