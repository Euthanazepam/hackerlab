#!/usr/bin/env python3

# Standard library imports
from os.path import exists
from zipfile import ZipFile

# Third-party library imports
from requests import get    # pip install requests

base_url = "https://codeby.games"
path = "game_api/files/download"
folder = "parts_597a5e9a-5b74-4f1d-b3ed-7782b568ac55_data"
filename = "task"
filetype = "zip"


def download_zip() -> None:
    """
    Downloads a zip file from the task page to the current directory.
    """

    url = f"{base_url}/{path}?folder={folder}&name={filename}&type={filetype}"

    response = get(url=url)

    try:
        with open(f"Bookworm/{filename}.{filetype}", "wb") as f:
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
        with ZipFile(f"Bookworm/{filename}.{filetype}") as zf:
            zf.extractall(path="Bookworm/")
            return zf.namelist()[0]
    except FileNotFoundError:
        with ZipFile(f"{filename}.{filetype}") as zf:
            zf.extractall(path='.')
            return zf.namelist()[0]


def get_flag() -> str:
    """
    Returns the challenge flag https://codeby.games/en/categories/cryptography/597a5e9a-5b74-4f1d-b3ed-7782b568ac55
    Dictionary 'mapping' is based on the original story https://www.eapoe.org/works/tales/goldbga2.htm
    You can also use the decryptor https://www.dcode.fr/gold-bug-poe

    :return: Flag
    """

    file_name = unzip()

    try:
        with open(f"Bookworm/{file_name}", 'r') as f:
            task = f.read().rstrip()    # rstrip() is used to remove the '\n' character from the end of a string.
    except FileNotFoundError:
        with open(f"{file_name}", 'r') as f:
            task = f.read().rstrip()    # rstrip() is used to remove the '\n' character from the end of a string.

    mapping = {
        '8': 'e',
        ';': 't',
        '4': 'h',
        '‡': 'o',
        ')': 's',
        '*': 'n',
        '5': 'a',
        '6': 'i',
        '(': 'r',
        '1': 'f',
        '†': 'd',
        '0': 'l',
        '9': 'm',
        '2': 'b',
        ':': 'y',
        '3': 'g',
        '?': 'u',
        '¶': 'v',
        '—': 'c',
        '.': 'p'
    }

    flag_chars = []

    for char in task:
        flag_chars.append(mapping[char])

    flag = "CODEBY{" + ''.join(flag_chars) + '}'

    return flag


if __name__ == "__main__":
    print(get_flag())
