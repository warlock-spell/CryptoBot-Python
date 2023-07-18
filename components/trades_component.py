# @Project:     Crypto-Bot
# @Filename:    trades_component.py
# @Author:      Daksh Gaur
# @Email:       hi@daksh.fyi
# @Time:        17-07-2023 10:46 pm

import tkinter as tk

import components.styles as st

class TradesWatch(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.body_widgets = dict()

        self._headers = ["time", "symbol", "exchange", "strategy", "side", "quantity", "status", "pnl"]

        self._table_frame = tk.Frame(self, bg=st.BG_COLOR_1)
        self._table_frame.pack(side=tk.TOP)


        for index, val in enumerate(self._headers):
            header = tk.Label(self._table_frame,
                              text=val.capitalize(),
                              bg=st.BG_COLOR_1,
                              fg=st.FG_COLOR_1,
                              font=st.BOLD_FONT)
            header.grid(row=0, column=index)

        for val in self._headers:
            self.body_widgets[val] = dict()
            if val in ["status", "pnl"]:
                self.body_widgets[f"{val}_var"] = dict()

        self._body_index = 1  # Start from 1 because 0 is the header