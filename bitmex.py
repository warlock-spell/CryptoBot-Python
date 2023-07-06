# @Project:     Crypto-Bot
# @Filename:    bitmex.py
# @Author:      Daksh Gaur
# @Email:       hi@daksh.fyi
# @Time:        06-07-2023 07:54 pm

import requests

def get_contracts():
    response_obj = requests.get("https://www.bitmex.com/api/v1/instrument/active")
    return [contract['symbol'] for contract in response_obj.json()]

# print(get_contracts())