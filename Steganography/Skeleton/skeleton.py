#!/usr/bin/env python3

# Standard library imports
from base64 import b64decode
from os.path import exists
from zipfile import ZipFile

# Third-party library imports
from requests import get    # pip install requests

base_url = "https://codeby.games"
path = "game_api/files/download"
folder = "parts_7ebaf2d5-a03c-44ed-9f77-7adea3e4834f_data"
filename = "task"
filetype = "zip"


def download_zip() -> None:
    """
    Downloads a zip file from the task page to the current directory.
    """

    url = f"{base_url}/{path}?folder={folder}&name={filename}&type={filetype}"

    response = get(url=url)

    try:
        with open(f"Skeleton/{filename}.{filetype}", "wb") as f:
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
        with ZipFile(f"Skeleton/{filename}.{filetype}") as zf:
            zf.extractall(path="Skeleton/")
    except FileNotFoundError:
        with ZipFile(f"{filename}.{filetype}") as zf:
            zf.extractall(path='.')


def get_flag() -> str:
    """
    Returns the challenge flag https://codeby.games/en/categories/steganography/7ebaf2d5-a03c-44ed-9f77-7adea3e4834f
    The flag is contained in frame 53 of the gif.

    References:
        1. GIF frame extractor (splitter) — https://ezgif.com/split
        2. GIMP — https://www.gimp.org/downloads

    :return: Flag
    """

    if not exists("task.gif"):
        unzip()

    # Encoded the flag in base64 to avoid spoilers.
    flag = b64decode("Q09ERUJZezRfUzNDUjM3XzFOXzdIM19TSzNMM1QwTl9XNFNfRjBVTkR9").decode()

    return flag


if __name__ == "__main__":
    print(get_flag())
