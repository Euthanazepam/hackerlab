#!/usr/bin/env python3

# Standard library imports
from os.path import exists
from zipfile import ZipFile

# Third-party library imports
from requests import get    # pip install requests

base_url = "https://codeby.games"
path = "game_api/files/download"
folder = "parts_a7676d01-1141-4788-a4b2-4bd8b546897b_data"
filename = "task"
filetype = "zip"


def download_zip() -> None:
    """
    Downloads a zip file from the task page to the current directory.
    """

    url = f"{base_url}/{path}?folder={folder}&name={filename}&type={filetype}"

    response = get(url=url)

    try:
        with open(f"Flags/{filename}.{filetype}", "wb") as f:
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
        with ZipFile(f"Flags/{filename}.{filetype}") as zf:
            zf.extractall(path="Flags/")
    except FileNotFoundError:
        with ZipFile(f"{filename}.{filetype}") as zf:
            zf.extractall(path='.')


def get_flag() -> str:
    """
    Returns the challenge flag https://codeby.games/en/categories/cryptography/a7676d01-1141-4788-a4b2-4bd8b546897b
    A useful resource with country flags — https://flagpedia.net

    :return: Flag
    """

    if not exists("task.jpg"):
        unzip()

    flags = {
        "🇦🇱": "Albania",
        "🇧🇷": "Brazil",
        "🇨🇾": "Cyprus",
        "🇩🇲": "Dominica",
        "🇪🇨": "Ecuador",
        "🇪🇬": "Egypt",
        "🇪🇪": "Estonia",
        "🇮🇳": "India",
        "🇮🇹": "Italy",
        "🇳🇪": "Niger",
        "🇳🇬": "Nigeria",
        "🇴🇲": "Oman",
        "🇷🇴": "Romania",
        "🇹🇷": "Turkey",
        "🇺🇬": "Uganda",
        "🇻🇪": "Venezuela",
        "🇻🇳": "Vietnam",
        "🇾🇪": "Yemen"
    }

    # Take the first letter of the country's name.
    message = [
        flags["🇨🇾"][0],
        flags["🇴🇲"][0],
        flags["🇩🇲"][0],
        flags["🇪🇬"][0],
        flags["🇧🇷"][0],
        flags["🇾🇪"][0],
        "{",
        flags["🇾🇪"][0].lower(),
        flags["🇴🇲"][0].lower(),
        flags["🇺🇬"][0].lower(),
        "_",
        flags["🇦🇱"][0].lower(),
        flags["🇷🇴"][0].lower(),
        flags["🇪🇪"][0].lower(),
        "_",
        flags["🇮🇳"][0].lower(),
        flags["🇳🇪"][0].lower(),
        flags["🇻🇳"][0].lower(),
        flags["🇪🇨"][0].lower(),
        flags["🇳🇬"][0].lower(),
        flags["🇹🇷"][0].lower(),
        flags["🇮🇹"][0].lower(),
        flags["🇻🇪"][0].lower(),
        flags["🇪🇪"][0].lower(),
        "}"
    ]

    flag = ''.join(item for item in message)

    return flag


if __name__ == "__main__":
    print(get_flag())
