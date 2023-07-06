# @Project:     Crypto-Bot
# @Filename:    main.py
# @Author:      Daksh Gaur
# @Email:       hi@daksh.fyi
# @Time:        06-07-2023 11:55 am

import tkinter as tk
import logging
from connectors.binance_futures import BinanceFuturesClient

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

    binance_client = BinanceFuturesClient(testnet=True)

    root = tk.Tk()

    APP_BACKGROUND = 'gray12'
    CONTRACTS_FOREGROUND = 'SteelBlue1'

    root.configure(bg=APP_BACKGROUND)

    calibri_font = ("Calibri", 12, "normal")

    row_count, col_count = 0, 0

    for contract in binance_client.get_contract():
        label_widget = tk.Label(root, text=contract, bg=APP_BACKGROUND, fg=CONTRACTS_FOREGROUND, width=14, font=calibri_font)
        label_widget.grid(row=row_count, column=col_count,
                          sticky="ew")  # sticky="ew" makes the widget expand horizontally

        if row_count == 4:
            col_count += 1
            row_count = 0
        else:
            row_count += 1

    root.mainloop()
