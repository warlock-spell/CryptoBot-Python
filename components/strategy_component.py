# @Project:     Crypto-Bot
# @Filename:    strategy_component.py
# @Author:      Daksh Gaur
# @Email:       hi@daksh.fyi
# @Time:        18-07-2023 05:35 pm

import tkinter as tk
import typing


import components.styles as st
from connectors.models import Contract


class StrategyEditor(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._commands_frame = tk.Frame(self, bg=st.BG_COLOR_1)
        self._commands_frame.pack(side=tk.TOP)

        self._table_frame = tk.Frame(self, bg=st.BG_COLOR_1)
        self._table_frame.pack(side=tk.TOP)

        self._add_button = tk.Button(self._commands_frame,
                                     text="Add Strategy",
                                     font=st.GLOBAL_FONT,
                                     command=self._add_strategy_row,
                                     bg=st.BG_COLOR_2,
                                     fg=st.FG_COLOR_1)
        self._add_button.pack(side=tk.TOP)

        self.body_widgets = dict()

        self._headers = ["Strategy", "Contract", "Timeframe", "Balance %", "TP %", "SL %"]

        for index, val in enumerate(self._headers):
            header = tk.Label(self._table_frame,
                              text=val,
                              bg=st.BG_COLOR_1,
                              fg=st.FG_COLOR_1,
                              font=st.BOLD_FONT)
            header.grid(row=0, column=index)

        for val in self._headers:
            self.body_widgets[val] = dict()

        self._body_index = 1

    def _add_strategy_row(self):
        return