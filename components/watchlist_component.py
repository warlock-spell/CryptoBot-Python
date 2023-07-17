# @Project:     Crypto-Bot
# @Filename:    watchlist_component.py
# @Author:      Daksh Gaur
# @Email:       hi@daksh.fyi
# @Time:        14-07-2023 04:44 pm

import tkinter as tk
import typing

import components.styles as st
from connectors.models import Contract


class Watchlist(tk.Frame):
    def __init__(self, binance_contracts: typing.Dict[str, Contract], bitmex_contracts: typing.Dict[str, Contract],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.binance_symbols = list(binance_contracts.keys())
        self.bitmex_symbols = list(bitmex_contracts.keys())

        # print(self.binance_symbols)
        # print("/n")
        # print(self.bitmex_symbols)

        self._commands_frame = tk.Frame(self, bg=st.BG_COLOR_1)
        self._commands_frame.pack(side=tk.TOP)

        self._table_frame = tk.Frame(self, bg=st.BG_COLOR_1)
        self._table_frame.pack(side=tk.TOP)

        self._binance_label = tk.Label(self._commands_frame,
                                       text="Binance",
                                       bg=st.BG_COLOR_1,
                                       fg=st.FG_COLOR_1,
                                       font=st.BOLD_FONT)
        self._binance_label.grid(row=0, column=0)

        self._binance_entry = tk.Entry(self._commands_frame,
                                       fg=st.FG_COLOR_1,
                                       justify=tk.CENTER,
                                       insertbackground=st.FG_COLOR_1,
                                       bg=st.BG_COLOR_2)
        self._binance_entry.bind("<Return>", self._add_binance_symbol)  # Bind the return key to the entry
        self._binance_entry.grid(row=1, column=0)

        self._bitmex_label = tk.Label(self._commands_frame,
                                      text="Bitmex",
                                      bg=st.BG_COLOR_1,
                                      fg=st.FG_COLOR_1,
                                      font=st.BOLD_FONT)
        self._bitmex_label.grid(row=0, column=1)

        self._bitmex_entry = tk.Entry(self._commands_frame,
                                      fg=st.FG_COLOR_1,
                                      justify=tk.CENTER,
                                      insertbackground=st.FG_COLOR_1,
                                      bg=st.BG_COLOR_2)
        self._bitmex_entry.bind("<Return>", self._add_bitmax_symbol)
        self._bitmex_entry.grid(row=1, column=1)

        self.body_widgets = dict()

        self._headers = ["symbol", "exchange", "bid", "ask", "remove"]

        for index, val in enumerate(self._headers):
            header = tk.Label(self._table_frame,
                              text=val.capitalize() if val != "remove" else "",
                              bg=st.BG_COLOR_1,
                              fg=st.FG_COLOR_1,
                              font=st.BOLD_FONT)
            header.grid(row=0, column=index)

        for val in self._headers:
            self.body_widgets[val] = dict()
            if val in ["bid", "ask"]:
                self.body_widgets[f"{val}_var"] = dict()  # create bid_var and ask_var

        self._body_index = 1  # Start from 1 because 0 is the header

    def _remove_symbol(self, body_index: int):

        for val in self._headers:
            self.body_widgets[val][body_index].grid_forget()
            del self.body_widgets[val][body_index]


    def _add_binance_symbol(self, event):
        symbol = event.widget.get()

        if symbol in self.binance_symbols:
            self._add_symbol(symbol, "Binance")
            event.widget.delete(0, tk.END)  # Clear the entry

    def _add_bitmax_symbol(self, event):
        symbol = event.widget.get()

        if symbol in self.bitmex_symbols:
            self._add_symbol(symbol, "Bitmex")
            event.widget.delete(0, tk.END)  # Clear the entry

    def _add_symbol(self, symbol: str, exchange: str):
        b_index = self._body_index

        self.body_widgets["symbol"][b_index] = tk.Label(self._table_frame,
                                                        text=symbol,
                                                        bg=st.BG_COLOR_1,
                                                        fg=st.FG_COLOR_2,
                                                        font=st.GLOBAL_FONT)
        self.body_widgets["symbol"][b_index].grid(row=b_index, column=0)

        self.body_widgets["exchange"][b_index] = tk.Label(self._table_frame,
                                                          text=exchange,
                                                          bg=st.BG_COLOR_1,
                                                          fg=st.FG_COLOR_2,
                                                          font=st.GLOBAL_FONT)
        self.body_widgets["exchange"][b_index].grid(row=b_index, column=1)

        self.body_widgets['bid_var'][b_index] = tk.StringVar()
        self.body_widgets["bid"][b_index] = tk.Label(self._table_frame,
                                                     textvariable=self.body_widgets['bid_var'][b_index],
                                                     bg=st.BG_COLOR_1,
                                                     fg=st.FG_COLOR_2,
                                                     font=st.GLOBAL_FONT)
        self.body_widgets["bid"][b_index].grid(row=b_index, column=2)

        self.body_widgets['ask_var'][b_index] = tk.StringVar()
        self.body_widgets["ask"][b_index] = tk.Label(self._table_frame,
                                                     textvariable=self.body_widgets['ask_var'][b_index],
                                                     bg=st.BG_COLOR_1,
                                                     fg=st.FG_COLOR_2,
                                                     font=st.GLOBAL_FONT)
        self.body_widgets["ask"][b_index].grid(row=b_index, column=3)

        self.body_widgets["remove"][b_index] = tk.Button(self._table_frame,
                                                         text="X",  # X for cancel or remove
                                                         bg=st.RED,
                                                         fg=st.FG_COLOR_1,
                                                         font=st.GLOBAL_FONT,
                                                         # lambda to pass the index, and avoiding callback to trigger immediately
                                                         command=lambda: self._remove_symbol(b_index))
        self.body_widgets["remove"][b_index].grid(row=b_index, column=4)

        self._body_index += 1
