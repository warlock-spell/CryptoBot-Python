# @Project:     Crypto-Bot
# @Filename:    main.py
# @Author:      Daksh Gaur
# @Email:       hi@daksh.fyi
# @Time:        06-07-2023 11:55 am

import tkinter as tk
import logging
import os
from dotenv import load_dotenv

from components.root_component import Root

from connectors.binance_futures import BinanceFuturesClient
from connectors.bitmex import BitmexClient

load_dotenv()

BINANCE_TESTNET_PUBLIC_KEY = os.environ.get("BINANCE_TESTNET_PUBLIC_KEY")
BINANCE_TESTNET_SECRET_KEY = os.environ.get("BINANCE_TESTNET_SECRET_KEY")
BITMEX_TESTNET_PUBLIC_KEY = os.environ.get("BITMEX_TESTNET_PUBLIC_KEY")
BITMEX_TESTNET_SECRET_KEY = os.environ.get("BITMEX_TESTNET_SECRET_KEY")

logger = logging.getLogger()

logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s :: %(message)s')
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler('info.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

if __name__ == "__main__":
    binance_client = BinanceFuturesClient(public_key=BINANCE_TESTNET_PUBLIC_KEY, secret_key=BINANCE_TESTNET_SECRET_KEY,
                                          testnet=True)

    bitmex_client = BitmexClient(public_key=BITMEX_TESTNET_PUBLIC_KEY, secret_key=BITMEX_TESTNET_SECRET_KEY,
                                 testnet=True)

    root = Root(binance_client, bitmex_client) # To access logs from these clients

    root.mainloop()
