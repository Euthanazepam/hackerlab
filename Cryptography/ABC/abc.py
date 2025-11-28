#!/usr/bin/env python3

# Standard library imports
from os.path import exists
from zipfile import ZipFile

# Third-party library imports
from requests import get    # pip install requests

base_url = "https://codeby.games"
path = "game_api/files/download"
folder = "parts_87811258-949b-48f1-8d0e-719c69db4f65_data"
filename = "task"
filetype = "zip"


def download_zip() -> None:
    """
    Downloads a zip file from the task page to the current directory.
    """

    url = f"{base_url}/{path}?folder={folder}&name={filename}&type={filetype}"

    response = get(url=url)

    try:
        with open(f"ABC/{filename}.{filetype}", "wb") as f:
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
        with ZipFile(f"ABC/{filename}.{filetype}") as zf:
            zf.extractall(path="ABC/")
            return zf.namelist()[0]
    except FileNotFoundError:
        with ZipFile(f"{filename}.{filetype}") as zf:
            zf.extractall(path='.')
            return zf.namelist()[0]


def get_flag() -> str:
    """
    Returns the challenge flag https://codeby.games/en/categories/cryptography/87811258-949b-48f1-8d0e-719c69db4f65
    Need to count the number of hyphens, not the number of characters in a line.
    А space has been added at the end of the sixth line.
    So, the word 'know' is formed incorrectly ('koow' instead of 'know').

    :return: Flag
    """

    file_name = unzip()

    try:
        with open(f"ABC/{file_name}", 'r') as f:
            task = f.readlines()
    except FileNotFoundError:
        with open(f"{file_name}", 'r') as f:
            task = f.readlines()

    alphabet = {
        1:  'a', 2:  'b', 3:  'c', 4:  'd', 5:  'e', 6:  'f', 7:  'g', 8:  'h', 9:  'i', 10: 'j',
        11: 'k', 12: 'l', 13: 'm', 14: 'n', 15: 'o', 16: 'p', 17: 'q', 18: 'r', 19: 's', 20: 't',
        21: 'u', 22: 'v', 23: 'w', 24: 'x', 25: 'y', 26: 'z'
    }

    flag_chars = []

    for line in task:
        flag_chars.append(alphabet[len([i for i in line if i == '-'])])

    flag = "CODEBY{" + ''.join(flag_chars) + '}'

    return flag


if __name__ == "__main__":
    print(get_flag())
