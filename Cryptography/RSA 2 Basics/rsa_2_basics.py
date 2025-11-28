#!/usr/bin/env python3

# Standard library imports
from os.path import exists
from zipfile import ZipFile

# Third-party library imports
from factordb.factordb import FactorDB  # pip install factordb-python
from requests import get    # pip install requests

base_url = "https://codeby.games"
path = "game_api/files/download"
folder = "parts_b0967cfb-8c27-4491-b9a4-4278635c2ccd_data"
filename = "task"
filetype = "zip"


def download_zip() -> None:
    """
    Downloads a zip file from the task page to the current directory.
    """

    url = f"{base_url}/{path}?folder={folder}&name={filename}&type={filetype}"

    response = get(url=url)

    try:
        with open(f"RSA 2 Basics/{filename}.{filetype}", "wb") as f:
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
        with ZipFile(f"RSA 2 Basics/{filename}.{filetype}") as zf:
            zf.extractall(path="RSA 2 Basics/")
    except FileNotFoundError:
        with ZipFile(f"{filename}.{filetype}") as zf:
            zf.extractall(path='.')


def get_flag() -> str:
    """
    Returns the challenge flag https://codeby.games/en/categories/cryptography/b0967cfb-8c27-4491-b9a4-4278635c2ccd

    References:
        1. RSA Decoder — https://www.dcode.fr/rsa-cipher
        2. FactorDB — http://factordb.com

    :return: Flag
    """

    if not exists("data.txt") or not exists("flag.txt"):
        unzip()

    try:
        with open("RSA 2 Basics/data.txt", 'r') as f:
            data = f.readlines()
    except FileNotFoundError:
        with open("data.txt", 'r') as f:
            data = f.readlines()

    try:
        with open("RSA 2 Basics/flag.txt", "rb") as f:
            flag_txt = f.read()
    except FileNotFoundError:
        with open("flag.txt", "rb") as f:
            flag_txt = f.read()

    c = int.from_bytes(flag_txt)
    n = int(data[0][2:].strip(',\n'))
    e = int(data[1][2:].strip('\n'))

    # Use http://factordb.com to factorize n.
    f = FactorDB(n)
    f.connect()
    p, q = f.get_factor_list()

    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)

    decrypted_message = pow(c, d, n)

    # The flag is at the end of the message.
    flag = decrypted_message.to_bytes(c.bit_length() // 8, "big")[-41:].decode()

    return flag


if __name__ == "__main__":
    print(get_flag())
