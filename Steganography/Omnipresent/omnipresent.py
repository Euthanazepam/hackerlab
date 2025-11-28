#!/usr/bin/env python3

# Standard library imports
from base64 import b64decode
from os.path import exists
from zipfile import ZipFile

# Third-party library imports
from requests import get    # pip install requests

base_url = "https://codeby.games"
path = "game_api/files/download"
folder = "parts_a6c02b63-e625-418f-8a94-82afe20a2d8b_data"
filename = "Omniscient"
filetype = "zip"


def download_zip() -> None:
    """
    Downloads a zip file from the task page to the current directory.
    """

    url = f"{base_url}/{path}?folder={folder}&name={filename}&type={filetype}"

    response = get(url=url)

    try:
        with open(f"Omnipresent/{filename}.{filetype}", "wb") as f:
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
        with ZipFile(f"Omnipresent/{filename}.{filetype}") as zf:
            zf.extractall(path="Omnipresent/")
    except FileNotFoundError:
        with ZipFile(f"{filename}.{filetype}") as zf:
            zf.extractall(path='.')


def get_flag() -> str:
    """
    Returns the challenge flag https://codeby.games/en/categories/steganography/a6c02b63-e625-418f-8a94-82afe20a2d8b
    Extract alpha channel from png. It contains flag.

    References:
        1. PNG Alpha Channel Extractor — https://onlinepngtools.com/extract-alpha-channel-from-png

    :return: Flag
    """

    if not exists("Omniscient.png"):
        unzip()

    # Encoded the flag in base64 to avoid spoilers.
    flag = b64decode("Q09ERUJZezRuZF9pX2M0bl9zZTN9").decode()

    return flag


if __name__ == "__main__":
    print(get_flag())
