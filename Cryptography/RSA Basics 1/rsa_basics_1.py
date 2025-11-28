#!/usr/bin/env python3

# Standard library imports
import tarfile
from os.path import exists

# Third-party library imports
from requests import get    # pip install requests

base_url = "https://codeby.games"
path = "game_api/files/download"
folder = "parts_173db536-19e0-4510-8516-624e74ff619f_data"
filename = "task"
filetype = "tar"


def download_tar() -> None:
    """
    Downloads a tar file from the task page to the current directory.
    """

    url = f"{base_url}/{path}?folder={folder}&name={filename}&type={filetype}"

    response = get(url=url)

    try:
        with open(f"RSA Basics 1/{filename}.{filetype}", "wb") as f:
            f.write(response.content)
    except FileNotFoundError:
        with open(f"{filename}.{filetype}", "wb") as f:
            f.write(response.content)


def unpack() -> None:
    """
    Unpacks a tar file into the current directory.
    """

    if not exists(f"{filename}.{filetype}"):
        download_tar()

    try:
        with tarfile.open(f"RSA Basics 1/{filename}.{filetype}", 'r:*') as tar:
            tar.extractall(path=f"RSA Basics 1/")
    except FileNotFoundError:
        with tarfile.open(f"{filename}.{filetype}", 'r:*') as tar:
            tar.extractall(path='.')


def get_flag() -> str:
    """
    Returns the challenge flag https://codeby.games/en/categories/cryptography/173db536-19e0-4510-8516-624e74ff619f
    A bit of theory:
        m — message (plain text)
        c — cipher text

        n = p * q
        φ(n) = (p - 1) * (q - 1)

        d — secret exponent
        d = e⁻¹ mod φ(n)

        Public key:     (n, e)
        Private key:    (n, d)

        Encryption:     c = mᵉ mod n
        Decryption:     m = cᵈ mod n

    References:
        1. RSA Decoder — https://www.dcode.fr/rsa-cipher

    :return: Flag
    """

    if not exists("data.txt") or not exists("flag.txt"):
        unpack()

    try:
        with open("RSA Basics 1/data.txt", 'r') as f:
            data = f.readlines()
    except FileNotFoundError:
        with open("data.txt", 'r') as f:
            data = f.readlines()

    try:
        with open("RSA Basics 1/flag.txt", "rb") as f:
            flag_txt = f.read()
    except FileNotFoundError:
        with open("flag.txt", "rb") as f:
            flag_txt = f.read()

    n = int(data[0][2:].replace(',', '').replace('\n', ''))
    e = int(data[1][2:].replace(',', '').replace('\n', ''))
    p = int(data[2][2:].replace(',', '').replace('\n', ''))
    q = n // p
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    c = int.from_bytes(flag_txt)

    decrypted_message = pow(c, d, n)

    # The flag is at the end of the message.
    flag = decrypted_message.to_bytes(c.bit_length() // 8, "big")[-29:].decode()

    return flag


if __name__ == "__main__":
    print(get_flag())
