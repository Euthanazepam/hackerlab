#!/usr/bin/env python3

# Standard library imports
import re
from os.path import exists
from zipfile import ZipFile

# Third-party library imports
from requests import get    # pip install requests

base_url = "https://hackerlab.pro"
path = "game_api/files/download"
folder = "parts_8eeacb32-2132-46d3-bd89-8238594558f0_data"
filename = "confused_cipher"
filetype = "zip"


def download_zip() -> None:
    """
    Downloads a zip file from the task page to the current directory.
    """

    url = f"{base_url}/{path}?folder={folder}&name={filename}&type={filetype}"

    response = get(url=url)

    try:
        with open(f"A confusing cipher/{filename}.{filetype}", "wb") as f:
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
        with ZipFile(f"A confusing cipher/{filename}.{filetype}") as zf:
            zf.extractall(path="A confusing cipher/")
            return zf.namelist()[0]
    except FileNotFoundError:
        with ZipFile(f"{filename}.{filetype}") as zf:
            zf.extractall(path='.')
            return zf.namelist()[0]


def get_flag() -> str:
    """
    Returns the challenge flag https://hackerlab.pro/en/categories/cryptography/8eeacb32-2132-46d3-bd89-8238594558f0

    References:
        1. Morse Code Converter — https://symbl.cc/en/tools/morse
        2. International Morse Code — https://morsecode.world/international/morse2.html

    :return: Flag
    """

    file_name = unzip()

    try:
        with open(f"A confusing cipher/{file_name}", 'r') as f:
            task = f.readline().rstrip()
    except FileNotFoundError:
        with open(f"{file_name}", 'r') as f:
            task = f.readline().rstrip()

    # Remove all Cyrillic characters using regex.
    # See https://stackoverflow.com/questions/15175142/how-can-i-do-multiple-substitutions-using-regex
    clear_text = re.sub(r"([абвгдеёжзийклмнопрстуфхцчшщъыьэюя])", "", task).split(' ')

    morse_code_mapping = {
        ".-": 'A',
        "-...": 'B',
        "-.-.": 'C',
        "-..": 'D',
        ".": 'E',
        "..-.": 'F',
        "--.": 'G',
        "....": 'H',
        "..": 'I',
        ".---": 'J',
        "-.-": 'K',
        ".-..": 'L',
        "--": 'M',
        "-.": 'N',
        "---": 'O',
        ".--.": 'P',
        "--.-": 'Q',
        ".-.": 'R',
        "...": 'S',
        "-": 'T',
        "..-": 'U',
        "...-": 'V',
        ".--": 'W',
        "-..-": 'X',
        "-.--": 'Y',
        "--..": 'Z',
        "-----": '0',
        ".----": '1',
        "..---": '2',
        "...--": '3',
        "....-": '4',
        ".....": '5',
        "-....": '6',
        "--...": '7',
        "---..": '8',
        "----.": '9',
        "..--..": '?',
        "..--.-": '_',
        "{": '{',
        "}": '}',
    }

    flag = ''.join(morse_code_mapping[item] for item in clear_text)

    return flag


if __name__ == "__main__":
    print(get_flag())
