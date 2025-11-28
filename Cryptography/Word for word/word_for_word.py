#!/usr/bin/env python3

# Standard library imports
from os.path import exists
from zipfile import ZipFile

# Third-party library imports
from requests import get    # pip install requests

base_url = "https://codeby.games"
path = "game_api/files/download"
folder = "parts_bedc74ff-5cd2-4ed5-b825-602b95797f1b_data"
filename = "word for word"
filetype = "zip"


def download_zip() -> None:
    """
    Downloads a zip file from the task page to the current directory.
    """

    url = f"{base_url}/{path}?folder={folder}&name={filename}&type={filetype}"

    response = get(url=url)

    try:
        with open(f"Word for word/{filename}.{filetype}", "wb") as f:
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
        with ZipFile(f"Word for word/{filename}.{filetype}") as zf:
            zf.extractall(path="Word for word/")
            return zf.namelist()[0]
    except FileNotFoundError:
        with ZipFile(f"{filename}.{filetype}") as zf:
            zf.extractall(path='.')
            return zf.namelist()[0]


def get_flag() -> str:
    """
    Returns the challenge flag https://codeby.games/en/categories/cryptography/bedc74ff-5cd2-4ed5-b825-602b95797f1b

    References:
        1. Reverse hash decoder — https://md5hashing.net/hash

    :return: Flag
    """

    file_name = unzip()

    try:
        with open(f"Word for word/{file_name}", 'r') as f:
            task = f.read()
    except FileNotFoundError:
        with open(f"{file_name}", 'r') as f:
            task = f.read()

    hashes = task.split(' ')

    flag = ''

    for n in range(len(hashes)):
        flag += f"https://md5hashing.net/hash/md5/{hashes[n]}\n"

    return flag


if __name__ == "__main__":
    print(get_flag())
