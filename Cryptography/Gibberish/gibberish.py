#!/usr/bin/env python3

# Standard library imports
from os.path import exists
from zipfile import ZipFile

# Third-party library imports
from requests import get    # pip install requests

base_url = "https://codeby.games"
path = "game_api/files/download"
folder = "parts_173c3580-34f9-45cb-aedc-5e5d06b83d80_data"
filename = "task"
filetype = "zip"


def download_zip() -> None:
    """
    Downloads a zip file from the task page to the current directory.
    """

    url = f"{base_url}/{path}?folder={folder}&name={filename}&type={filetype}"

    response = get(url=url)

    try:
        with open(f"Gibberish/{filename}.{filetype}", "wb") as f:
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
        with ZipFile(f"Gibberish/{filename}.{filetype}") as zf:
            zf.extractall(path="Gibberish/")
            return zf.namelist()[0]
    except FileNotFoundError:
        with ZipFile(f"{filename}.{filetype}") as zf:
            zf.extractall(path='.')
            return zf.namelist()[0]


def decode_message() -> str:
    """
    Returns the challenge flag https://codeby.games/en/categories/cryptography/173c3580-34f9-45cb-aedc-5e5d06b83d80
    Useful resource for determining text encoding — https://www.online-decoder.com/ru

    :return: Flag
    """

    file_name = unzip()

    try:
        with open(f"Gibberish/{file_name}", 'r') as f:
            task = f.readlines()
    except FileNotFoundError:
        with open(f"{file_name}", 'r') as f:
            task = f.readlines()

    decoded_message = (f"""{task[0].rstrip().encode(encoding="koi8-r").decode("utf-8")}\n"""
                       f"""{task[2].rstrip().encode(encoding="cp1251").decode("utf-8")}\n"""
                       f"""{task[4].rstrip().encode(encoding="gb18030").decode("utf-8")}""")

    return decoded_message


if __name__ == "__main__":
    print(decode_message())
