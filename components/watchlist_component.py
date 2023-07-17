# @Project:     Crypto-Bot
# @Filename:    watchlist_component.py
# @Author:      Daksh Gaur
# @Email:       hi@daksh.fyi
# @Time:        14-07-2023 04:44 pm

import tkinter as tk

import components.styles as st


class Watchlist(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        self._bitmex_entry.grid(row=1, column=1)
