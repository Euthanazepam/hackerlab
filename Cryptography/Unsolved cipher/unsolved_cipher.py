#!/usr/bin/env python3

# Standard library imports
from os.path import exists
from zipfile import ZipFile

# Third-party library imports
from requests import get    # pip install requests

base_url = "https://codeby.games"
path = "game_api/files/download"
folder = "parts_92e6a4b9-1899-4584-9780-2312da201665_data"
filename = "notsolvedcipher"
filetype = "zip"


def download_zip() -> None:
    """
    Downloads a zip file from the task page to the current directory.
    """

    url = f"{base_url}/{path}?folder={folder}&name={filename}&type={filetype}"

    response = get(url=url)

    try:
        with open(f"Unsolved cipher/{filename}.{filetype}", "wb") as f:
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
        with ZipFile(f"Unsolved cipher/{filename}.{filetype}") as zf:
            zf.extractall(path="Unsolved cipher/")
            return zf.namelist()[0]
    except FileNotFoundError:
        with ZipFile(f"{filename}.{filetype}") as zf:
            zf.extractall(path='.')
            return zf.namelist()[0]


def vigenere_decrypt(cipher_text, key) -> str:
    """
    Decryption function for the Vigenère cipher.

    Source: https://thepythoncode.com/article/implementing-the-vigenere-cipher-in-python

    :param cipher_text: Encrypted text
    :param key: Encryption key
    :return: Decrypted text
    """

    decrypted_text = ''

    key_repeated = (key * (len(cipher_text) // len(key))) + key[:len(cipher_text) % len(key)]

    for i in range(len(cipher_text)):
        if cipher_text[i].isalpha():
            shift = ord(key_repeated[i].upper()) - ord('A')
            if cipher_text[i].isupper():
                decrypted_text += chr((ord(cipher_text[i]) - shift - ord('A')) % 26 + ord('A'))
            else:
                decrypted_text += chr((ord(cipher_text[i]) - shift - ord('a')) % 26 + ord('a'))
        else:
            decrypted_text += cipher_text[i]

    return decrypted_text


def get_flag() -> str:
    """
    Returns the challenge flag https://codeby.games/en/categories/cryptography/92e6a4b9-1899-4584-9780-2312da201665

    :return: Flag
    """

    file_name = unzip()

    try:
        with open(f"Unsolved cipher/{file_name}", 'r') as f:
            not_solved_cipher = f.readlines()
    except FileNotFoundError:
        with open(f"{file_name}", 'r') as f:
            not_solved_cipher = f.readlines()

    cipher_text = not_solved_cipher[0][6:].replace('{', '').replace('}', '').rstrip()
    key = not_solved_cipher[1][6:].rstrip()

    plain_text = vigenere_decrypt(cipher_text, key)

    flag = plain_text[:6] + '{' + plain_text[6:] + '}'

    return flag


if __name__ == "__main__":
    print(get_flag())
