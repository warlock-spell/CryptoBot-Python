# @Project:     Crypto-Bot
# @Filename:    binance_futures.py.py
# @Author:      Daksh Gaur
# @Email:       hi@daksh.fyi
# @Time:        06-07-2023 05:48 pm

import logging
import requests
import pprint

logger = logging.getLogger()

def get_contracts():
    response_obj = requests.get("https://fapi.binance.com/fapi/v1/exchangeInfo")
    print(response_obj.status_code)
    return [contract['pair'] for contract in response_obj.json()['symbols']]

print(get_contracts())