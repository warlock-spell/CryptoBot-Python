# @Project:     Crypto-Bot
# @Filename:    main.py
# @Author:      Daksh Gaur
# @Email:       hi@daksh.fyi
# @Time:        06-07-2023 11:55 am

import tkinter as tk
import logging
from bitmex import get_contracts


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


logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")


if __name__ == "__main__":

    bitmex_contracts = get_contracts()

    root = tk.Tk()

    row_count, col_count = 0, 0

    for contract in bitmex_contracts:
        # label -> window, text
        label_widget = tk.Label(root, text=contract)
        # pack -> add to window
        # grid -> add to window
        label_widget.grid(row=row_count, column=col_count)

        if row_count == 4:
            col_count+=1
            row_count = 0
        else:
            row_count+=1

    # Start event loop, it avoids the termination of program
    root.mainloop()