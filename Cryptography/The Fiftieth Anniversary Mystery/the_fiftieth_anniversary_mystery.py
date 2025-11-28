#!/usr/bin/env python3

# Standard library imports
from os.path import exists
from zipfile import ZipFile

# Third-party library imports
from requests import get    # pip install requests

base_url = "https://codeby.games"
path = "game_api/files/download"
folder = "parts_3082faf3-0f68-4293-be23-a6676abce9b7_data"
filename = "task"
filetype = "zip"


def download_zip() -> None:
    """
    Downloads a zip file from the task page to the current directory.
    """

    url = f"{base_url}/{path}?folder={folder}&name={filename}&type={filetype}"

    response = get(url=url)

    try:
        with open(f"The Fiftieth Anniversary Mystery/{filename}.{filetype}", "wb") as f:
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
        with ZipFile(f"The Fiftieth Anniversary Mystery/{filename}.{filetype}") as zf:
            zf.extractall(path="The Fiftieth Anniversary Mystery/")
    except FileNotFoundError:
        with ZipFile(f"{filename}.{filetype}") as zf:
            zf.extractall(path='.')


def get_flag() -> str:
    """
    Returns the challenge flag https://codeby.games/en/categories/cryptography/3082faf3-0f68-4293-be23-a6676abce9b7

    References:
        1. https://zodiackiller.com/Letters.html
        2. Resource for searching similar Unicode symbols — http://shapecatcher.com/index.html

    :return: Flag
    """

    if not exists("task.jpg"):
        unzip()

    # The encrypted text uses similarly written symbols.
    encrypted_message = "OXHJπYO⌖🞎ꟼI"

    mapping = {
        'O': 'N',
        'X': 'O',
        'H': 'T',
        'J': 'F',
        'π': 'O',
        'Y': 'U',
        '⌖': 'D',
        '🞎': 'Y',
        'ꟼ': 'E',
        'I': 'T'
    }

    flag_chars = []

    for item in encrypted_message:
        flag_chars.append(mapping[item])

    flag = "CODEBY{" + ''.join(flag_chars) + '}'

    return flag


if __name__ == "__main__":
    print(get_flag())
