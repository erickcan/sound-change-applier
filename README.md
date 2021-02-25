# sound-change-applier
A command-line sound change applier written in Python.

## Setup
To start using this sound change applier, you just need to clone this repo:
```
$ git clone https://github.com/erickcan/sound-change-applier.git
```

## Command line
There are two ways of applying sound changes using the command line: `--file-based-sound-change` and `--named-sound-change`.

- `--file-based-sound-change` (or `-f`) applies a set of rules to a set of words, each defined in their own files, and creates a text file with the changed words.
- `--named-sound-change` (or `-n`) applies a named sound change to words passed on the command line, and then prints the words after the change.

### Usage
For `--file-based-sound-change`:
```
$ sca sound-classes-file -f rules-file words-file [--csv-output]
```
where:
- `sca` is the sound change applier;
- `sound-classes-file` is a JSON file where sound classes are defined;
- `rules-file` is text file where the rules to apply are;
- `words-file` is text file where the words to which the rules will be applied;
- `--csv-output` is an optional argument that, if selected, creates a CSV file with the before and after of the words instead of a text file.

---

For `--named-sound-change`:
```
$ sca sound-classes-file -n named-rules-file named-rule words [--csv-output]
```
where:
- `sca` is the sound change applier;
- `sound-classes-file` is a JSON file where sound classes are defined;
- `named-rules-file` is a JSON file where sound changes and their names are defined;
- `named-rule` name of the rule to apply (should be defined in the `named-rules-file` file);
- `words` is a string with the words to change (if more than one word, should be inside quotes and separed by spaces);
- `--csv-output` is an optional argument that, if selected, creates a CSV file with the before and after of the words instead of just printing the words.

### Examples
Suppose the following files:

> sound_classes.json
```json
{
  "V": "aeiou",
  "C": "bcdfghjklmnpqrstvwxyz",
  "P": "pbtdkg",
  "F": "fvsz",
  "N": "mn",
  "S": "sz"
}
```
> named_rules.json
```json
{
  "terminal-devoicing": "[bdgz] -> [ptks] / _#",
  "h-dropping": "h -> _ / _",
  "z-rhotacization": "z -> r / V_V",
  "/æ/-raising": "æ -> eə / _N"
}
```

> rules.txt
```
d -> ð / V_V
[ae] -> [ãẽ] / _N
[aou] -> [äöü] / _e
l -> w / _#
s -> z / [bdg]_
```

> words.txt
```
ada
beds
clue
daemon
sand
vowel
```

If this were passed to the command line:
```
$ sca sound_classes.json -f rules.txt words.txt --csv-output
```
The following file would be created:

> sound-change-YYYY-MM-DD-HH-MM-SS.csv
```csv
ada,aða
beds,bedz
clue,clüe
daemon,daẽmon
sand,sãnd
vowel,vowew
```

And if the following were passed into the command line:
```
$ sca sound_classes.json -n named_rules.json h-dropping "here he had hallucinated"
```
It would print:
```
ere
e
ad
alluciated
```

## Rule notation
The rules should be written in the form `a -> b / x_y`, where `a` becomes `b` when `a` is between `x` and `y`.

### Symbols
| symbol  | meaning       | example                                   |
| ------- | ------------- | ----------------------------------------- |
| `#`     | word boundary | `_#` : end of word                        |
| `A..Z`  | sound class   | `Gt` : class `G` followed by `t`          |
| `[xyz]` | ad-hoc class  | `u[rl]` : `u` followed by `r` or `l`      |
| `_`     | everywhere    | `ð -> d / _` : `ð` becomes `d` everywhere |
| `_`     | sound-eraser  | `h -> _` : deletes `h`                    |


## Dependencies
This project has no dependencies. It only uses modules of the Python Standard Library.
