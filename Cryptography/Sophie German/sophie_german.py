#!/usr/bin/env python3

# Standard library imports
import re
from os.path import exists
from zipfile import ZipFile

# Third-party library imports
from factordb.factordb import FactorDB  # pip install factordb-python
from requests import get    # pip install requests

base_url = "https://hackerlab.pro"
path = "game_api/files/download"
folder = "parts_eb2e709d-0d17-4fb5-8268-c0de89ce9b5a_data"
filename = "sophie_and_german"
filetype = "zip"


def download_zip() -> None:
    """
    Downloads a zip file from the task page to the current directory.
    """

    url = f"{base_url}/{path}?folder={folder}&name={filename}&type={filetype}"

    response = get(url=url)

    try:
        with open(f"Sophie German/{filename}.{filetype}", "wb") as f:
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
        with ZipFile(f"Sophie German/{filename}.{filetype}") as zf:
            zf.extractall(path="Sophie German/")
            return zf.namelist()[0]
    except FileNotFoundError:
        with ZipFile(f"{filename}.{filetype}") as zf:
            zf.extractall(path='.')
            return zf.namelist()[0]


def get_flag() -> str:
    """
    Returns the challenge flag https://hackerlab.pro/en/categories/cryptography/eb2e709d-0d17-4fb5-8268-c0de89ce9b5a

    :return: Flag
    """

    file_name = unzip()

    try:
        with open(f"Sophie German/{file_name}", 'r') as f:
            task = f.readlines()
    except FileNotFoundError:
        with open(f"{file_name}", 'r') as f:
            task = f.readlines()

    n = int(task[0][4:])
    e = int(task[1][4:])
    c = int(task[2][4:])

    # Use http://factordb.com to factorize n.
    f = FactorDB(n)
    f.connect()
    p, q = f.get_factor_list()

    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)

    decrypted_message = pow(c, d, n)

    # Convert number to plain text.
    plain_text = decrypted_message.to_bytes(c.bit_length() // 8, "big").decode()

    # Find the task flag.
    flag = re.findall("CODEBY{.*}", plain_text)[0]

    return flag


if __name__ == "__main__":
    print(get_flag())
