#!/usr/bin/env python3

# Standard library imports
from os.path import exists
from zipfile import ZipFile

# Third-party library imports
from requests import get    # pip install requests

base_url = "https://codeby.games"
path = "game_api/files/download"
folder = "parts_1f91f3d3-a500-4442-82fe-09b462020929_data"
filename = "task"
filetype = "zip"


def download_zip() -> None:
    """
    Downloads a zip file from the task page to the current directory.
    """

    url = f"{base_url}/{path}?folder={folder}&name={filename}&type={filetype}"

    response = get(url=url)

    try:
        with open(f"Letter/{filename}.{filetype}", "wb") as f:
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
        with ZipFile(f"Letter/{filename}.{filetype}") as zf:
            zf.extractall(path="Letter/")
            return zf.namelist()[0]
    except FileNotFoundError:
        with ZipFile(f"{filename}.{filetype}") as zf:
            zf.extractall(path='.')
            return zf.namelist()[0]


def get_flag() -> str:
    """
    Returns the challenge flag https://codeby.games/en/categories/cryptography/1f91f3d3-a500-4442-82fe-09b462020929

    :return: Flag
    """

    file_name = unzip()

    try:
        with open(f"Letter/{file_name}", 'r') as f:
            cypher = f.readlines()
    except FileNotFoundError:
        with open(f"{file_name}", 'r') as f:
            cypher = f.readlines()

    flag_string = cypher[48]

    # Mapping was done manually.
    mapping = {
        'a': 't',
        'b': 'n',
        'c': 'w',
        'd': 'b',
        'e': 'f',
        'g': 'c',
        'i': 'k',
        'j': 'm',
        'k': 'i',
        'l': 's',
        'm': 'g',
        'n': 'e',
        'o': 'u',
        'p': 'p',
        'q': 'y',
        'r': 'd',
        's': 'r',
        't': 'm',
        'u': 'h',
        'w': 'o',
        'x': 'a',
        'y': 'l',
        '{': '{',
        '}': '}',
        '_': '_',
        '0': '0',
        '1': '1',
        '6': '6',
        '8': '8'
    }

    flag_chars = []

    for char in flag_string:
        flag_chars.append(mapping[char])

    flag = ''.join(flag_chars[:6]).upper() + ''.join(flag_chars[6:])

    return flag


if __name__ == "__main__":
    print(get_flag())
