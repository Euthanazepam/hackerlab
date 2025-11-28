#!/usr/bin/env python3

# Standard library imports
from os.path import exists
from xml.etree.ElementTree import parse
from zipfile import ZipFile

# Third-party library imports
from requests import get    # pip install requests

base_url = "https://codeby.games"
path = "game_api/files/download"
folder = "parts_e73e49dc-f033-4af4-9daa-004f0afb1c90_data"
filename = "task"
filetype = "zip"


def download_zip() -> None:
    """
    Downloads a zip file from the task page to the current directory.
    """

    url = f"{base_url}/{path}?folder={folder}&name={filename}&type={filetype}"

    response = get(url=url)

    try:
        with open(f"Ward/{filename}.{filetype}", "wb") as f:
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
        with ZipFile(f"Ward/{filename}.{filetype}") as zf:
            zf.extractall(path="Ward/")
            return zf.namelist()[0]
    except FileNotFoundError:
        with ZipFile(f"{filename}.{filetype}") as zf:
            zf.extractall(path='.')
            return zf.namelist()[0]


def get_flag() -> str:
    """
    Returns the challenge flag https://codeby.games/en/categories/steganography/e73e49dc-f033-4af4-9daa-004f0afb1c90

    References:
        1. Anatomy of a WordProcessingML File — http://www.officeopenxml.com/anatomyofOOXML.php

    :return: Flag
    """

    file_name = unzip()

    xml_document = "word/document.xml"

    try:
        with ZipFile(f"Ward/{file_name}") as zf:
            zf.extract(xml_document)
    except FileNotFoundError:
        with ZipFile(f"{file_name}") as zf:
            zf.extract(xml_document)

    tree = parse(xml_document)
    root = tree.getroot()

    # The flag is located in the 'w:bottom' attribute of the 'w:document > w:body > w:sectPr > w:pgMar' object.
    flag = root[0][-1][2].attrib["{http://schemas.openxmlformats.org/wordprocessingml/2006/main}bottom"]

    return flag


if __name__ == "__main__":
    print(get_flag())
