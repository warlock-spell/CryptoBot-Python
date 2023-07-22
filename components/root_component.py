# @Project:     Crypto-Bot
# @Filename:    root_component.py
# @Author:      Daksh Gaur
# @Email:       hi@daksh.fyi
# @Time:        14-07-2023 03:25 pm

import tkinter as tk
import logging

import components.styles as st
from components.logging_component import Logging
from connectors.binance_futures import BinanceFuturesClient
from connectors.bitmex import BitmexClient
from components.watchlist_component import Watchlist
from components.trades_component import TradesWatch
from components.strategy_component import StrategyEditor

logger = logging.getLogger()


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

        self._strategy_frame = StrategyEditor(self._right_frame, bg=st.BG_COLOR_1)
        self._strategy_frame.pack(side=tk.TOP)

        self._trades_frame = TradesWatch(self._right_frame, bg=st.BG_COLOR_1)
        self._trades_frame.pack(side=tk.TOP)

        self._update_ui()

    def _update_ui(self):

        # Logs

        # log is a dictionary with 2 keys: log and displayed
        for log in self.binance.logs:
            if not log['displayed']:
                self._logging_frame.add_log(log['log'])
                log['displayed'] = True

        for log in self.bitmex.logs:
            if not log['displayed']:
                self._logging_frame.add_log(log['log'])
                log['displayed'] = True


        # Watchlist prices

        try:
            for key, value in self._watchlist_frame.body_widgets['symbol'].items():
                symbol = self._watchlist_frame.body_widgets['symbol'][key].cget("text") # Get the symbol from the label
                exchange = self._watchlist_frame.body_widgets['exchange'][key].cget("text") # Get the exchange from the label
                # print(symbol, exchange)

                if exchange in ["Binance", "binance"]:
                    if symbol not in self.binance.contracts:
                        # print(symbol, "not in contracts")
                        continue
                    if symbol not in self.binance.prices:
                        # print(f"Fetching bid ask for, {symbol}")
                        self.binance.get_bid_ask(self.binance.contracts[symbol])
                        continue

                    precision = self.binance.contracts[symbol].price_decimals
                    prices = self.binance.prices[symbol]

                elif exchange in ["Bitmex", "bitmex"]:
                    if symbol not in self.bitmex.contracts:
                        # print("Not in contracts")
                        continue
                    if symbol not in self.bitmex.prices:
                        # print("Not in prices")
                        continue

                    precision = self.bitmex.contracts[symbol].price_decimals
                    prices = self.bitmex.prices[symbol]

                else:
                    continue

                if prices['bid'] is not None:
                    price_str = f"{prices['bid']:.{precision}f}"
                    self._watchlist_frame.body_widgets['bid_var'][key].set(price_str)

                if prices['ask'] is not None:
                    price_str = f"{prices['ask']:.{precision}f}"
                    self._watchlist_frame.body_widgets['ask_var'][key].set(price_str)

        except RuntimeError as e:
            # Errors might occur if the watchlist dict is updated while the loop is running
            # for example, if a new symbol is added to the watchlist
            # or if a symbol is removed from the watchlist
            logger.error(f"error while iterating over watchlist dict: {RuntimeError}")

        self.after(1500, self._update_ui) # call this method again after 1500ms