#!/usr/bin/env python3

# Standard library imports
from os.path import exists
from zipfile import ZipFile

# Third-party library imports
from requests import get    # pip install requests

base_url = "https://hackerlab.pro"
path = "game_api/files/download"
folder = "parts_8ae16126-a115-4247-9c6e-087c8bf5ea79_data"
filename = "dna"
filetype = "zip"


def download_zip() -> None:
    """
    Downloads a zip file from the task page to the current directory.
    """

    url = f"{base_url}/{path}?folder={folder}&name={filename}&type={filetype}"

    response = get(url=url)

    try:
        with open(f"DNA/{filename}.{filetype}", "wb") as f:
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
        with ZipFile(f"DNA/{filename}.{filetype}") as zf:
            zf.extractall(path="DNA/")
            return zf.namelist()[0]
    except FileNotFoundError:
        with ZipFile(f"{filename}.{filetype}") as zf:
            zf.extractall(path='.')
            return zf.namelist()[0]


def get_flag() -> str:
    """
    Returns the challenge flag https://hackerlab.pro/en/categories/cryptography/8ae16126-a115-4247-9c6e-087c8bf5ea79

    References:
        1. Codons (Genetic Code) — https://www.dcode.fr/codons-genetic-code

    :return: Flag
    """

    file_name = unzip()

    try:
        with open(f"DNA/{file_name}", 'r') as f:
            dna_txt = f.readline().rstrip()
    except FileNotFoundError:
        with open(f"{file_name}", 'r') as f:
            dna_txt = f.readline().rstrip()

    dna_codons_mapping = {
        "GCT": 'A', "GCC": 'A', "GCA": 'A', "GCG": 'A',
        "AAT": 'B', "AAC": 'B', "GAT": 'B', "GAC": 'B',
        "TGT": 'C', "TGC": 'C',
        "GAT": 'D', "GAC": 'D',
        "GAA": 'E', "GAG": 'E',
        "TTT": 'F', "TTC": 'F',
        "GGT": 'G', "GGC": 'G', "GGA": 'G', "GGG": 'G',
        "CAC": 'H', "CAT": 'H',
        "ATT": 'I', "ATC": 'I', "ATA": 'I',
        "AAA": 'K', "AAG": 'K',
        "TTA": 'L', "TTG": 'L', "CTT": 'L', "CTC": 'L', "CTA": 'L', "CTG": 'L',
        "ATG": 'M',
        "AAT": 'N', "AAC": 'N',
        'O': 'O',
        "CCT": 'P', "CCC": 'P', "CCA": 'P', "CCG": 'P',
        "CAA": 'Q', "CAG": 'Q',
        "CGT": 'R', "CGC": 'R', "CGA": 'R', "CGG": 'R', "AGA": 'R', "AGG": 'R',
        "TCT": 'S', "TCC": 'S', "TCA": 'S', "TCG": 'S', "AGT": 'S', "AGC": 'S',
        "ACT": 'T', "ACC": 'T', "ACA": 'T', "ACG": 'T',
        "GTT": 'V', "GTC": 'V', "GTA": 'V', "GTG": 'V',
        "TGG": 'W',
        "TAT": 'Y', "TAC": 'Y'
        }

    # Split 'dna_txt' using the letter 'O' as a separator.
    split_dna_txt = dna_txt.split('O')

    # Split text into blocks of 3 characters.
    n = 3
    before_separator = ' '.join([split_dna_txt[0][i:i+n] for i in range(0, len(split_dna_txt[0]), n)]).split(' ')
    after_separator = ' '.join([split_dna_txt[1][i:i+n] for i in range(0, len(split_dna_txt[1]), n)]).split(' ')

    # Remap codons into letters.   
    flag_1 = ''.join([dna_codons_mapping[item] for item in before_separator])
    flag_2 = dna_codons_mapping['O']
    flag_3 = ''.join([dna_codons_mapping[item] for item in after_separator])
    
    flag = "CODEBY{" + f"{flag_1}{flag_2}{flag_3}" + "}"

    return flag


if __name__ == "__main__":
    print(get_flag())
