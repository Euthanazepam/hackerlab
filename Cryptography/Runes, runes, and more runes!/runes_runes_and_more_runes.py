#!/usr/bin/env python3

# Standard library imports
from os.path import exists

# Third-party library imports
from requests import get    # pip install requests

base_url = "https://codeby.games"
path = "game_api/files/download"
folder = "parts_e8df895a-64d0-48fb-8db7-6e6a6a17ac59_data"
filename = "task"
filetype = "png"


def download_image() -> None:
    """
    Downloads an image from the task page to the current directory.
    """

    url = f"{base_url}/{path}?folder={folder}&name={filename}&type={filetype}"

    response = get(url=url)

    try:
        with open(f"Runes, runes, and more runes!/{filename}.{filetype}", "wb") as f:
            f.write(response.content)
    except FileNotFoundError:
        with open(f"{filename}.{filetype}", "wb") as f:
            f.write(response.content)


def get_flag() -> str:
    """
    Returns the challenge flag https://codeby.games/en/categories/cryptography/e8df895a-64d0-48fb-8db7-6e6a6a17ac59

    References:
        1. Elder Futhark Decoder — https://www.dcode.fr/elder-futhark

    :return: Flag
    """

    if not exists(f"{filename}.{filetype}"):
        download_image()

    runes = "ᚱᚢᚾᛖᛋ ᚫᚱᛖ ᛏᛟᛟ ᚺᚫᚱᛞ"

    mapping = {
        'ᚫ': 'a',
        'ᛒ': 'b',
        'ᛞ': 'd',
        'ᛖ': 'e',
        'ᛓ': 'f',
        'ᚷ': 'g',
        'ᚺ': 'h',
        'ᛁ': 'i',
        'ᛃ': 'j',
        'ᚲ': 'k',
        'ᛚ': 'l',
        'ᛗ': 'm',
        'ᚾ': 'n',
        'ᛟ': 'o',
        'ᛈ': 'p',
        'ᚱ': 'r',
        'ᛋ': 's',
        'ᛏ': 't',
        'ᚢ': 'u',
        'ᚹ': 'w',
        'ᛇ': 'y',
        'ᛉ': 'z',
        ' ': '_'
    }

    flag = "CODEBY{" + ''.join(mapping[o] for o in runes) + '}'

    return flag


if __name__ == "__main__":
    print(get_flag())
