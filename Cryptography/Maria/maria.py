#!/usr/bin/env python3

# Standard library imports
from os.path import exists

# Third-party library imports
from requests import get    # pip install requests

base_url = "https://codeby.games"
path = "game_api/files/download"
folder = "parts_0c99ff07-4ef9-4dd4-80cd-8eeb6f6ddb3b_image"
filename = "Mary"
filetype = "png"


def download_image() -> None:
    """
    Downloads an image from the task page to the current directory.
    """

    url = f"{base_url}/{path}?folder={folder}&name={filename}&type={filetype}"

    response = get(url=url)

    try:
        with open(f"Maria/{filename}.{filetype}", "wb") as f:
            f.write(response.content)
    except FileNotFoundError:
        with open(f"{filename}.{filetype}", "wb") as f:
            f.write(response.content)


def get_flag() -> str:
    """
    Returns the challenge flag https://codeby.games/en/categories/cryptography/0c99ff07-4ef9-4dd4-80cd-8eeb6f6ddb3b

    References:
        1. Character table — https://www.dcode.fr/tools/mary-stuart/images/alphabet.png
        2. Mary Stuart code decipherer — https://www.dcode.fr/mary-stuart-code

    :return: Flag
    """

    if not exists(f"{filename}.{filetype}"):
        download_image()

    # The encrypted text uses similarly written symbols.
    encrypted_message = "ⴷ🜄ᚒ⧜‡8⌐ɱO‡🜄Cε∞⧜Oᚒ⏗"

    mapping = {
        'O': 'A',
        '‡': 'B',
        'ⴷ': 'C',
        'ᚒ': 'D',
        '⧜': 'E',
        '∞': 'H',
        '🜄': 'O',
        'ε': 'T',
        'C': 'U',
        '8': 'Y',
        'ɱ': "WHAT",
        '⌐': '',
        '⏗': ''
    }

    flag_chars = []

    for item in encrypted_message:
        flag_chars.append(mapping[item])

    flag = ''.join(flag_chars)[:6] + '{' + ''.join(flag_chars)[6:].lower() + '}'

    return flag


if __name__ == "__main__":
    print(get_flag())
