# sound-change-applier
A command-line sound change applier written in Python.

## Setup
To begin using this sound change applier, you just need to download the executable (`.exe`) file in the [Releases page](https://github.com/erickcan/sound-change-applier/releases) and use it through the command-line prompt:
```
$ sca sca-options
```
You can also clone this repo and use the `sca.bat` or `sca.sh` file:
```sh
$ git clone https://github.com/erickcan/sound-change-applier.git
$ sca sca-options       # if Windows
$ ./sca.sh sca-options  # if Linux
```

## Command line
```
sca (-f rules-file words-file | -n named-rules-json named-rule words)
    [--csv-output] [-s sound-classes-json | --no-sound-classes]
```
### Usage
- `--file-based-sound-change` | `-f` to apply a set of rules to a set of words, each defined in a separate file, creating a text file with the changed words;
  - `rules-file`: text file with the rules
  - `words-file`: text file with the words
- `--named-sound-change` | `-n` to apply a named sound change to words passed on the command line, and then prints the words after the change;
  - `named-rules-json`: JSON file where sound classes are defined
  - `named-rule`: name of the rule to apply (defined in `named-rules-json`)
  - `words`: words to apply the sound change
- `--csv-output` to create a before and after of the changed words;
- `--sound-classes-file` | `-s` to specify the JSON file where the sound classes are defined (see also [Default sound classes](#default-sound-classes));
- `--no-sound-classes` to not make use of sound classes.

### Examples
Suppose the following files:
> named_rules.json
```json
{
  "terminal-devoicing": "[bdgz] > [ptks] /  _#",
  "h-dropping":          "h    -> _      /  _",
  "z-rhotacization":     "z    -> r      / V_V",
  "l-vocalization":      "l    => w      /  _!V",
  "/æ/-raising":         "æ    => eə     /  _N",
  "th-fronting":         "[θð] -> [fv]   /  _"
}
```
> rules.txt
```
d    => ð   /    V_V
[gk] -> _   /    #_n
a    -> ə   /     _#
l    -> w   /     _!V
[aou]e>[æøy]/     _
sw    > s   /     _[ou]
[ao]N > [ãõ]/     _
s    => z   /[bdg]_
e    -> _   /   CC_#
```
> words.txt
```
aeon
beds
clue
daemon
knowledge
laterals
media
sand
swords
```

If this were passed to the command line,
```
$ sca -f rules.txt words.txt --csv-output
```
the following file would be created:
> sound-change-YYYY-MM-DD-HH-MM-SS.csv
```csv
aeon,æõ
beds,bedz
clue,cly
daemon,dæmõ
knowledge,nowledg
laterals,lateraws
media,meðiə
sand,sãd
swords,sordz
```

And if the following were passed into the command line,
```
$ sca -n named_rules.json h-dropping "here he had hallucinated"
```
it would print:
```
ere e ad allucinated
```

## Rule notation
The rules can be written in any of the following forms:
```
x  > y / a_b
x -> y / a_b
x => y / a_b
```
where `x` becomes `y` when `x` is between `a` and `b`. (Spaces between `>`, `->`, `=>` and `/` are insignificant.)

### Symbols
| symbol  | meaning          | example                                     |
| ------- | ---------------- | ------------------------------------------- |
| `#`     | word boundary    | `_#`: end of word, `#_`: start of word      |
| `A..Z`  | sound class      | `Gt`: class `G` followed by `t`             |
| `[xyz]` | ad-hoc class     | `u[rl]`: `u` followed by `r` or `l`         |
| `> _`   | sound-eraser     | `h -> _`: deletes `h`                       |
| `_`     | everywhere, when | `_x`: when followed by `x`, `_`: everywhere |
| `!_`    | not preceded by  | `u!_`: when not preceded by `u`             |
| `_!`    | not followed by  | `_!n`: when not followed by `n`             |

## Appendix

### Default sound classes
If neither `--sound-classes-file` nor `--no-sound-classes` are used, the following sound classes are used:
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
