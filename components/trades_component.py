# @Project:     Crypto-Bot
# @Filename:    trades_component.py
# @Author:      Daksh Gaur
# @Email:       hi@daksh.fyi
# @Time:        17-07-2023 10:46 pm

import tkinter as tk
import typing

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

    def add_trade(self, data: typing.Dict):

        b_index = self._body_index

        t_index = data['time'] # Unique identifier for each trade

        # Time

        self.body_widgets["time"][t_index] = tk.Label(self._table_frame,
                                                      text=data["time"],
                                                      bg=st.BG_COLOR_1,
                                                      fg=st.FG_COLOR_2,
                                                      font=st.GLOBAL_FONT)
        self.body_widgets["time"][t_index].grid(row=b_index, column=0)

        # Symbol

        self.body_widgets["symbol"][t_index] = tk.Label(self._table_frame,
                                                      text=data["symbol"],
                                                      bg=st.BG_COLOR_1,
                                                      fg=st.FG_COLOR_2,
                                                      font=st.GLOBAL_FONT)
        self.body_widgets["symbol"][t_index].grid(row=b_index, column=1)

        # Exchange

        self.body_widgets["exchange"][t_index] = tk.Label(self._table_frame,
                                                      text=data["exchange"],
                                                      bg=st.BG_COLOR_1,
                                                      fg=st.FG_COLOR_2,
                                                      font=st.GLOBAL_FONT)
        self.body_widgets["exchange"][t_index].grid(row=b_index, column=2)

        # Strategy

        self.body_widgets["strategy"][t_index] = tk.Label(self._table_frame,
                                                          text=data["strategy"],
                                                          bg=st.BG_COLOR_1,
                                                          fg=st.FG_COLOR_2,
                                                          font=st.GLOBAL_FONT)
        self.body_widgets["strategy"][t_index].grid(row=b_index, column=3)

        # Side

        self.body_widgets["side"][t_index] = tk.Label(self._table_frame,
                                                          text=data["side"],
                                                          bg=st.BG_COLOR_1,
                                                          fg=st.FG_COLOR_2,
                                                          font=st.GLOBAL_FONT)
        self.body_widgets["side"][t_index].grid(row=b_index, column=4)

        # Quantity

        self.body_widgets["quantity"][t_index] = tk.Label(self._table_frame,
                                                            text=data["quantity"],
                                                            bg=st.BG_COLOR_1,
                                                            fg=st.FG_COLOR_2,
                                                            font=st.GLOBAL_FONT)
        self.body_widgets["quantity"][t_index].grid(row=b_index, column=5)

        # Status

        self.body_widgets["status_var"][t_index] = tk.StringVar()
        self.body_widgets["status"][t_index] = tk.Label(self._table_frame,
                                                          textvariable=self.body_widgets["status_var"][t_index],
                                                          bg=st.BG_COLOR_1,
                                                          fg=st.FG_COLOR_2,
                                                          font=st.GLOBAL_FONT)
        self.body_widgets["status"][t_index].grid(row=b_index, column=6)

        # PnL

        self.body_widgets["pnl_var"][t_index] = tk.StringVar()
        self.body_widgets["pnl"][t_index] = tk.Label(self._table_frame,
                                                        textvariable=self.body_widgets["pnl_var"][t_index],
                                                        bg=st.BG_COLOR_1,
                                                        fg=st.FG_COLOR_2,
                                                        font=st.GLOBAL_FONT)
        self.body_widgets["pnl"][t_index].grid(row=b_index, column=7)


        self._body_index += 1

