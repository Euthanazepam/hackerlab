#!/usr/bin/env python3

# Standard library imports
from os.path import exists
from zipfile import ZipFile

# Third-party library imports
from requests import get    # pip install requests

base_url = "https://codeby.games"
path = "game_api/files/download"
folder = "parts_f1c174bf-475e-43e9-af96-3c2f2a44c408_data"
filename = "task"
filetype = "zip"


def download_zip() -> None:
    """
    Downloads a zip file from the task page to the current directory.
    """

    url = f"{base_url}/{path}?folder={folder}&name={filename}&type={filetype}"

    response = get(url=url)

    try:
        with open(f"Musical accompaniment/{filename}.{filetype}", "wb") as f:
            f.write(response.content)
    except FileNotFoundError:
        with open(f"{filename}.{filetype}", "wb") as f:
            f.write(response.content)


def unzip() -> None:
    """
    Unpacks a zip file into the current directory.
    """

    if not exists(f"{filename}.{filetype}"):
        download_zip()

    try:
        with ZipFile(f"Musical accompaniment/{filename}.{filetype}") as zf:
            zf.extractall(path="Musical accompaniment/")
    except FileNotFoundError:
        with ZipFile(f"{filename}.{filetype}") as zf:
            zf.extractall(path='.')


def get_flag() -> str:
    """
    Returns the challenge flag https://codeby.games/en/categories/cryptography/f1c174bf-475e-43e9-af96-3c2f2a44c408

    References:
        1. Music Sheets Decoder — https://www.dcode.fr/music-sheet-cipher

    :return: Flag
    """

    if not exists("music.png"):
        unzip()

    # TODO: Rewrite the dictionary using musical notation.
    mapping = {
        "do1":      'o',
        "do11":     'a',
        "re1":      'p',
        "re11":     'b',
        "fa1":      'r',
        "sol11":    'e',
        "re2":      'w',
        "fa2":      'y',
        "sol21":    'l'
    }

    cipher = ["re2", "sol11", "sol21", "sol21", "re1", "sol21", "do11", "fa2", "re11", "fa1", "do1"]

    flag = "CODEBY{" + ''.join(mapping[note] for note in cipher) + '}'

    return flag


if __name__ == "__main__":
    print(get_flag())
