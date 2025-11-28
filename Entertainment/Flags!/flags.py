#!/usr/bin/env python3

# Standard library imports
from os.path import exists
from zipfile import ZipFile

# Third-party library imports
from requests import get    # pip install requests

base_url = "https://codeby.games"
path = "game_api/files/download"
folder = "parts_eea8f7b2-d17f-4720-9f32-91f4d3857c54_data"
filename = "task"
filetype = "zip"


def download_zip() -> None:
    """
    Downloads a zip file from the task page to the current directory.
    """

    url = f"{base_url}/{path}?folder={folder}&name={filename}&type={filetype}"

    response = get(url=url)

    try:
        with open(f"Flags!/{filename}.{filetype}", "wb") as f:
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
        with ZipFile(f"Flags!/{filename}.{filetype}") as zf:
            zf.extractall(path="Flags!/")
    except FileNotFoundError:
        with ZipFile(f"{filename}.{filetype}") as zf:
            zf.extractall(path='.')


def get_flag() -> str:
    """
    Returns the challenge flag https://codeby.games/en/categories/misc/eea8f7b2-d17f-4720-9f32-91f4d3857c54

    References:
        1. Signal Flags — http://www.quadibloc.com/other/flaint.htm
        2. Signal flags of NATO fleets — http://www.vexillographia.ru/signal_nt.htm
        3. Navy Signals Code — https://www.dcode.fr/maritime-signals-code

    :return: Flag
    """

    if not exists("task.png"):
        unzip()

    # TODO: Find Unicode symbols of signal flags and add them to the dictionary.
    mapping = {
        48: '0', 49: '1', 50: '2', 51: '3', 52: '4', 53: '5',
        54: '6', 55: '7', 56: '8', 57: '9', 65: 'A', 66: 'B',
        67: 'C', 68: 'D', 69: 'E', 70: 'F', 71: 'G', 72: 'H',
        73: 'I', 74: 'J', 75: 'K', 76: 'L', 77: 'M', 78: 'N',
        79: 'O', 80: 'P', 81: 'Q', 82: 'R', 83: 'S', 84: 'T',
        85: 'U', 86: 'V', 87: 'W', 88: 'X', 89: 'Y', 90: 'Z'
    }

    encrypted_message = [67, 79, 68, 69, 66, 89, 70, 76, 52, 71, 48, 50, 55, 57]

    flag_chars = []

    for item in encrypted_message:
        flag_chars.append(mapping[item])

    flag = ''.join(flag_chars[:6]) + '{' + ''.join(flag_chars[6:10]) + '_' + ''.join(flag_chars[10:]) + '}'

    return flag


if __name__ == "__main__":
    print(get_flag())
