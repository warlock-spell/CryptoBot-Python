# @Project:     Crypto-Bot
# @Filename:    root_component.py
# @Author:      Daksh Gaur
# @Email:       hi@daksh.fyi
# @Time:        14-07-2023 03:25 pm

import tkinter as tk

import components.styles as st
from components.logging_component import Logging
from connectors.binance_futures import BinanceFuturesClient
from connectors.bitmex import BitmexClient
from components.watchlist_component import Watchlist


class Root(tk.Tk):
    def __init__(self, binance: BinanceFuturesClient, bitmex: BitmexClient):
        super().__init__()

        self.binance = binance
        self.bitmex = bitmex

        self.title("Crypto Bot")
        self.configure(bg=st.BG_COLOR_1)

        # Component style: 2 frames -> left and right
        # Left frame: 2 frames -> top and bottom -> top_left and bottom_left
        # Right frame: 2 frames -> top and bottom -> top_right and bottom_right
        self._left_frame = tk.Frame(self, bg=st.BG_COLOR_1)
        self._left_frame.pack(side=tk.LEFT)

        self._right_frame = tk.Frame(self, bg=st.BG_COLOR_1)
        self._right_frame.pack(side=tk.LEFT)

        self._watchlist_frame = Watchlist(self.binance.contracts, self.bitmex.contracts,self._left_frame, bg=st.BG_COLOR_1)
        self._watchlist_frame.pack(side=tk.TOP)

        self._logging_frame = Logging(self._left_frame, bg=st.BG_COLOR_1)
        self._logging_frame.pack(side=tk.TOP)

        self._update_ui()

    def _update_ui(self):
        # log is a dictionary with 2 keys: log and displayed
        for log in self.binance.logs:
            if not log['displayed']:
                self._logging_frame.add_log(log['log'])
                log['displayed'] = True

        for log in self.bitmex.logs:
            if not log['displayed']:
                self._logging_frame.add_log(log['log'])
                log['displayed'] = True

        self.after(1500, self._update_ui) # call this method again after 1500ms