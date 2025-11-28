#!/usr/bin/env python3

# Standard library imports
from os.path import exists
from zipfile import ZipFile

# Third-party library imports
from requests import get    # pip install requests

base_url = "https://codeby.games"
path = "game_api/files/download"
folder = "parts_627d29d1-0e5f-4bec-ae88-e29888f0d72b_data"
filename = "task"
filetype = "zip"


def download_zip() -> None:
    """
    Downloads a zip file from the task page to the current directory.
    """

    url = f"{base_url}/{path}?folder={folder}&name={filename}&type={filetype}"

    response = get(url=url)

    try:
        with open(f"Art of War/{filename}.{filetype}", "wb") as f:
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
        with ZipFile(f"Art of War/{filename}.{filetype}") as zf:
            zf.extractall(path="Art of War/")
    except FileNotFoundError:
        with ZipFile(f"{filename}.{filetype}") as zf:
            zf.extractall(path='.')


def get_flag() -> str:
    """
    Returns the challenge flag https://codeby.games/en/categories/cryptography/627d29d1-0e5f-4bec-ae88-e29888f0d72b

    References:
        1. Chinese Remainder Calculator — https://www.dcode.fr/chinese-remainder

    :return: Flag
    """

    if not exists("task.txt"):
        unzip()

    cipher_text = 25183524468752482838730336135334402772668615375346038
    a = 3339

    flag = bytes.fromhex(hex(cipher_text ^ a)[2:]).decode("utf-8")

    return flag


if __name__ == "__main__":
    print(get_flag())
