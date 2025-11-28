#!/usr/bin/env python3

# Standard library imports
import re
from os.path import exists
from zipfile import ZipFile

# Third-party library imports
from requests import get    # pip install requests

base_url = "https://hackerlab.pro"
path = "game_api/files/download"
folder = "parts_f05dfc0f-d1ea-491d-825f-33f846ae14c0_data"
filename = "task_garland"
filetype = "zip"


def download_zip() -> None:
    """
    Downloads a zip file from the task page to the current directory.
    """

    url = f"{base_url}/{path}?folder={folder}&name={filename}&type={filetype}"

    response = get(url=url)

    try:
        with open(f"Garland/{filename}.{filetype}", "wb") as f:
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
        with ZipFile(f"Garland/{filename}.{filetype}") as zf:
            zf.extractall(path="Garland/")
    except FileNotFoundError:
        with ZipFile(f"{filename}.{filetype}") as zf:
            zf.extractall(path='.')


def get_flag() -> str:
    """
    Returns the challenge flag https://hackerlab.pro/en/categories/cryptography/f05dfc0f-d1ea-491d-825f-33f846ae14c0

    References:
        1. https://stackoverflow.com/questions/48691121/converting-bases-using-int
        2. https://stackoverflow.com/questions/180606/how-do-i-convert-a-list-of-ascii-values-to-a-string-in-python

    :return: Flag
    """

    if not exists("Гирлянда"):
        unzip()

    try:
        with open(f"Garland/Гирлянда", 'r') as f:
            task = f.readline().rstrip()
    except FileNotFoundError:
        with open(f"Гирлянда", 'r') as f:
            task = f.readline().rstrip()

    # Convert emoji to ninary.
    emoji_map = {
        '🟢': '0',
        '🟣': '1',
        '⚫': '2',
        '🔴': '3',
        '🟡': '4',
        '🟠': '5',
        '🔵': '6',
        '⚪': '7',
        '🟤': '8',
        ' ': ' ',
        '️': ''
        }

    ninary_numbers = ''.join(emoji_map[item] for item in task).split(' ')

    # Convert ninary to decimal.
    decimal_numbers = [int(i, 9) for i in ninary_numbers]

    # Convert decimal to ASCII.
    ascii_text = ''.join(chr(i) for i in decimal_numbers)

    # Find the task flag.
    flag = re.findall("CODEBY{.*}", ascii_text)[0]

    return flag


if __name__ == "__main__":
    print(get_flag())
