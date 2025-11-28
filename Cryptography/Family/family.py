#!/usr/bin/env python3

# Standard library imports
from os.path import exists
from zipfile import ZipFile

# Third-party library imports
from requests import get    # pip install requests

base_url = "https://codeby.games"
path = "game_api/files/download"
folder = "parts_74035f68-c4d6-4d40-a9c0-ea969c660a2b_data"
filename = "family"
filetype = "zip"


def download_zip() -> None:
    """
    Downloads a zip file from the task page to the current directory.
    """

    url = f"{base_url}/{path}?folder={folder}&name={filename}&type={filetype}"

    response = get(url=url)

    try:
        with open(f"Family/{filename}.{filetype}", "wb") as f:
            f.write(response.content)
    except FileNotFoundError:
        with open(f"{filename}.{filetype}", "wb") as f:
            f.write(response.content)


def unzip() -> str:
    """
    Unpacks a zip file into the current directory.

    :return: Name of file
    """

    if not exists(f"{filename}.{filetype}"):
        download_zip()

    try:
        with ZipFile(f"Family/{filename}.{filetype}") as zf:
            zf.extractall(path="Family/")
            return zf.namelist()[0]
    except FileNotFoundError:
        with ZipFile(f"{filename}.{filetype}") as zf:
            zf.extractall(path='.')
            return zf.namelist()[0]


def get_flag() -> str:
    """
    Returns the challenge flag https://codeby.games/en/categories/cryptography/74035f68-c4d6-4d40-a9c0-ea969c660a2b
    References:
        1. ASCII Chart — https://python-reference.readthedocs.io/en/latest/docs/str/ASCII.html
        2. String Encoder / Decoder — https://dencode.com/en/string/unicode-escape

    :return: Flag
    """

    file_name = unzip()

    try:
        with open(f"Family/{file_name}", 'r') as f:
            family = f.read()
    except FileNotFoundError:
        with open(f"{file_name}", 'r') as f:
            family = f.read()

    # I haven't figured out yet how to elegantly turn "U+73 U+79 U+73 U+74 U+33 U+6D U+73 U+7D"
    # into "\u0073\u0079\u0073\u0074\u0033\u006D\u0073\u007D".
    #
    # I tried f"{family[101:]}".replace('U+', r'\u00').replace(' ', '') but it didn't work.
    #
    # Maybe Python has a built-in function or a third-party library to handle Unicode.
    # I've searched for a long time (2 hours) but found nothing.
    # So I decided to use a dict.

    mapping = {
        "U+33": "\u0033",
        "U+73": "\u0073",
        "U+74": "\u0074",
        "U+79": "\u0079",
        "U+6D": "\u006D",
        "U+7D": "\u007D"
    }

    flag = (f"""{bytes.fromhex(family[:11]).decode("utf-8")}"""                                     # hex to utf-8
            f"{''.join((chr(int(i, 2)) for i in family[12:38].split(' ')))}"                        # binary to ascii
            f"{''.join(chr(int(o, 8)) for o in family[39:75].split(' '))}"                          # octal to ascii
            f"{''.join(chr(int(o)) for o in family[76:100].split(' '))}"                            # int to ascii
            f"{''.join(mapping[o] for o in family[101:].rstrip().split(' ')).encode().decode()}")   # unicode escape

    return flag


if __name__ == "__main__":
    print(get_flag())
