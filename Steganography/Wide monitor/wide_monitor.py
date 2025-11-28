#!/usr/bin/env python3

# Standard library imports
from base64 import b64decode
from os.path import exists

# Third-party library imports
from requests import get    # pip install requests

base_url = "https://codeby.games"
path = "game_api/files/download"
folder = "parts_a1e6e8a9-0ea3-4605-880e-c7cf528d2980_data"
filename = "file"
filetype = "txt"


def download_file() -> None:
    """
    Downloads a text file from the task page to the current directory.
    """

    url = f"{base_url}/{path}?folder={folder}&name={filename}&type={filetype}"

    response = get(url=url)

    try:
        with open(f"Wide monitor/{filename}.{filetype}", "wb") as f:
            f.write(response.content)
    except FileNotFoundError:
        with open(f"{filename}.{filetype}", "wb") as f:
            f.write(response.content)


def get_flag() -> str:
    """
    Returns the challenge flag https://codeby.games/en/categories/steganography/a1e6e8a9-0ea3-4605-880e-c7cf528d2980

    References:
        1. ASCII to Image Converter — https://onlinetools.com/ascii/convert-ascii-to-image
        2. Image to ASCII — https://www.asciiart.eu/image-to-ascii

    :return: Flag
    """

    if not exists(f"{filename}.{filetype}"):
        download_file()

    # Encoded the flag in base64 to avoid spoilers.
    flag = b64decode("Q09ERUJZe0dPT0RfSk9CX01ZX0ZSMUVORCF9").decode()

    return flag


if __name__ == "__main__":
    print(get_flag())
