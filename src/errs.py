from sys import exit
from src.small_functions import search_prn, read_file, json_to_dict
from src.hash_dict import HashableDict

__all__ = ['try_open_txt', 'try_open_json']


class NotPhonRule(Exception):
    def __init__(self, rule):
        self.rule = rule
        self.message = f"'{rule}' is not a valid phonological rule notation"
        super().__init__(self.message)


class NotJSONFile(Exception): pass


def raise_not_json_file(file: str) -> str:
    """Raise NotJSONFile if ``file`` doesn't end with '.json', else return ``file``."""
    if not file.endswith(".json"):
        raise NotJSONFile
    else:
        return file


class NotTxtFile(Exception): pass


def raise_not_txt_file(file: str) -> str:
    """Raise NotTxtFile if ``file`` doesn't end with '.txt', else return ``file``."""
    if not file.endswith(".txt"):
        raise NotTxtFile
    else:
        return file


def try_open_txt(filename: str, arg_name: str) -> list[str]:
    """Try to open a txt file, raise NotTxtFile if not a txt file."""
    try:
        contents = list(map(str.strip, read_file(raise_not_txt_file(filename))))
    except NotTxtFile:
        exit(f"`{arg_name}` should be a txt file")
    except Exception as e:
        exit(f"error opening '{filename}': {e}")

    return contents


def try_open_json(filename: str, arg_name: str) -> HashableDict:
    """Try to open a JSON file, raise NotJSON if not a JSON file."""
    try:
        contents = json_to_dict(raise_not_json_file(filename))
    except NotJSONFile:
        exit(f"`{arg_name}` should be a JSON file")
    except Exception as e:
        exit(f"error opening '{filename}': {e}")

    return contents
