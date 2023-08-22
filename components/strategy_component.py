# @Project:     Crypto-Bot
# @Filename:    strategy_component.py
# @Author:      Daksh Gaur
# @Email:       hi@daksh.fyi
# @Time:        18-07-2023 05:35 pm

import tkinter as tk
import typing

import components.styles as st
from connectors.binance_futures import BinanceFuturesClient
from connectors.bitmex import BitmexClient
from strategies.strat_breakout import BreakoutStrategy
from strategies.strat_technical import TechnicalStrategy


class StrategyEditor(tk.Frame):
    def __init__(self, root, binance: BinanceFuturesClient, bitmex: BitmexClient, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.root = root  # to access the logger

        self._exchanges = {"Binance": binance, "Bitmex": bitmex}

        self._all_contracts = []
        for exchange, client in self._exchanges.items():
            for symbol, contract in client.contracts.items():
                self._all_contracts.append(f"{symbol}_{exchange.capitalize()}")

        self._all_timeframes = ["1m", "5m", "15m", "1h", "4h"]

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

        self._additional_params = dict()
        self._extra_input = dict()

        self._base_params = [
            {"code_name": "strategy_type",
             "widget": tk.OptionMenu,
             "data_type": str,
             "values": ["Technical", "Breakout"],
             "width": 10},

            {"code_name": "contract",
             "widget": tk.OptionMenu,
             "data_type": str,
             "values": self._all_contracts,
             "width": 15},

            {"code_name": "timeframe",
             "widget": tk.OptionMenu,
             "data_type": str,
             "values": self._all_timeframes,
             "width": 7},

            {"code_name": "balance_pct",
             "widget": tk.Entry,
             "data_type": float,
             "width": 7},

            {"code_name": "take_profit",
             "widget": tk.Entry,
             "data_type": float,
             "width": 7},

            {"code_name": "stop_loss",
             "widget": tk.Entry,
             "data_type": float,
             "width": 7},

            {"code_name": "parameters",
             "widget": tk.Button,
             "data_type": float,
             "text": "Parameters",
             "bg": st.BG_COLOR_2,
             "command": self._show_popup},

            {"code_name": "activation",
             "widget": tk.Button,
             "data_type": float,
             "text": "OFF",
             "bg": st.BG_COLOR_3,
             "command": self._switch_strategy},

            {"code_name": "delete",
             "widget": tk.Button,
             "data_type": float,
             "text": "X",
             "bg": st.BG_COLOR_3,
             "command": self._delete_row},
        ]

        self._extra_params = {
            "Technical": [
                {"code_name": "ema_fast", "name": "MACD Fast Length", "widget": tk.Entry, "data_type": int},
                {"code_name": "ema_slow", "name": "MACD Slow Length", "widget": tk.Entry, "data_type": int},
                {"code_name": "ema_signal", "name": "MACD Signal Length", "widget": tk.Entry, "data_type": int},
            ],
            "Breakout": [
                {"code_name": "min_volume", "name": "Minimum Volume", "widget": tk.Entry, "data_type": float},
            ]
        }

        for index, val in enumerate(self._headers):
            header = tk.Label(self._table_frame,
                              text=val,
                              bg=st.BG_COLOR_1,
                              fg=st.FG_COLOR_1,
                              font=st.BOLD_FONT)
            header.grid(row=0, column=index)

        for val in self._base_params:
            self.body_widgets[val['code_name']] = dict()
            if val['widget'] == tk.OptionMenu:
                self.body_widgets[f'{val["code_name"]}_var'] = dict()

        self._body_index = 1

    def _add_strategy_row(self):
        b_index = self._body_index

        for col, base_param in enumerate(self._base_params):
            code_name = base_param['code_name']
            if base_param['widget'] == tk.OptionMenu:
                self.body_widgets[code_name + "_var"][b_index] = tk.StringVar()
                self.body_widgets[code_name + "_var"][b_index].set(base_param['values'][0])  # setting default values
                self.body_widgets[code_name][b_index] = tk.OptionMenu(self._table_frame,
                                                                      self.body_widgets[code_name + "_var"][b_index],
                                                                      *base_param['values'], )
                self.body_widgets[code_name][b_index].config(width=base_param['width'])

            elif base_param['widget'] == tk.Entry:
                self.body_widgets[code_name][b_index] = tk.Entry(self._table_frame,
                                                                 justify=tk.CENTER, )

            elif base_param['widget'] == tk.Button:
                self.body_widgets[code_name][b_index] = tk.Button(self._table_frame,
                                                                  text=base_param['text'],
                                                                  bg=base_param['bg'],
                                                                  fg=st.FG_COLOR_1,
                                                                  command=lambda frozen_command=base_param[
                                                                      'command']: frozen_command(b_index))
            else:
                # do nothing
                continue

            # place the widget
            self.body_widgets[code_name][b_index].grid(row=b_index, column=col)

        self._additional_params[b_index] = dict()

        for strategy, parameters in self._extra_params.items():
            for param in parameters:
                self._additional_params[b_index][param['code_name']] = None

        self._body_index += 1

    def _show_popup(self, b_index: int):

        x = self.body_widgets['parameters'][b_index].winfo_rootx()
        y = self.body_widgets['parameters'][b_index].winfo_rooty()

        self._popup_window = tk.Toplevel(self)
        self._popup_window.wm_title("Parameters")

        self._popup_window.config(bg=st.BG_COLOR_1)
        self._popup_window.attributes('-topmost', 'true')

        self._popup_window.geometry(f"+{x - 80}+{y + 30}")

        strat_selected = self.body_widgets['strategy_type_var'][b_index].get()

        row_no = 0

        for param in self._extra_params[strat_selected]:
            code_name = param['code_name']

            temp_label = tk.Label(self._popup_window, bg=st.BG_COLOR_1, fg=st.FG_COLOR_1, text=param['name'],
                                  font=st.BOLD_FONT)
            temp_label.grid(row=row_no, column=0)

            if param['widget'] == tk.Entry:
                self._extra_input[code_name] = tk.Entry(self._popup_window, justify=tk.CENTER, bg=st.BG_COLOR_2,
                                                        fg=st.FG_COLOR_1, insertbackground=st.FG_COLOR_1)

                # if parametric value is already set, then set the entry to that value
                if self._additional_params[b_index][code_name] is not None:
                    # set the entry to the value
                    self._extra_input[code_name].insert(tk.END, str(self._additional_params[b_index][code_name]))

            else:
                # do nothing
                continue

            self._extra_input[code_name].grid(row=row_no, column=1)
            row_no += 1

        # Validation
        validation_button = tk.Button(self._popup_window, text="Validate", bg=st.BG_COLOR_2, fg=st.FG_COLOR_1,
                                      command=lambda: self._validate_popup(b_index))
        validation_button.grid(row=row_no, column=0, columnspan=2)

    def _validate_popup(self, b_index: int):

        strat_selected = self.body_widgets['strategy_type_var'][b_index].get()

        for param in self._extra_params[strat_selected]:
            code_name = param['code_name']

            if self._extra_input[code_name].get() == "":
                self._additional_params[b_index][code_name] = None
            else:
                self._additional_params[b_index][code_name] = param['data_type'](
                    self._extra_input[code_name].get())  # convert to the correct data type from string

        self._popup_window.destroy()  # destroy the popup window when validation is done

    def _switch_strategy(self, b_index: int):

        for param in ["balance_pct", "take_profit", "stop_loss"]:
            if self.body_widgets[param][b_index].get() == "":
                self.root.logging_frame.add_log(f"Missing {param} parameter for strategy at row {b_index}")
                return

        strat_selected = self.body_widgets['strategy_type_var'][b_index].get()

        for param in self._extra_params[strat_selected]:
            if self._additional_params[b_index][param['code_name']] is None:
                self.root.logging_frame.add_log(f"Missing {param['code_name']} parameter for strategy at row {b_index}")
                return

        # if all parameters are set, then switch the strategy
        # save the current strategy
        symbol = self.body_widgets['contract_var'][b_index].get().split("_")[
            0]  # contract is in the format of "Symbol_Exchange"
        exchange = self.body_widgets['contract_var'][b_index].get().split("_")[1]
        timeframe = self.body_widgets['timeframe_var'][b_index].get()
        balance_pct = float(self.body_widgets['balance_pct'][b_index].get())  # entry box value is always string
        take_profit = float(self.body_widgets['take_profit'][b_index].get())
        stop_loss = float(self.body_widgets['stop_loss'][b_index].get())

        contract = self._exchanges[exchange].contracts[symbol]

        # switch the strategy
        if self.body_widgets['activation'][b_index].cget("text") == "OFF":

            if strat_selected == "Technical":
                new_strategy = TechnicalStrategy(contract, exchange, timeframe, balance_pct, take_profit, stop_loss,
                                                 self._additional_params[b_index])

            elif strat_selected == "Breakout":
                new_strategy = BreakoutStrategy(contract, exchange, timeframe, balance_pct, take_profit, stop_loss,
                                                 self._additional_params[b_index])

            else:
                return

            # deactivate the widgets to prevent user from changing the parameters while the strategy is running
            for param in self._base_params:
                code_name = param['code_name']

                if code_name != "activation" and "_var" not in code_name:
                    self.body_widgets[code_name][b_index].config(state=tk.DISABLED)  # disable the widget

            self.body_widgets['activation'][b_index].config(bg=st.GREEN, text="ON")
            self.root.logging_frame.add_log(f"{strat_selected} strategy on {symbol} / {timeframe} started")

        else:
            for param in self._base_params:
                code_name = param['code_name']

                if code_name != "activation" and "_var" not in code_name:
                    self.body_widgets[code_name][b_index].config(state=tk.NORMAL)  # enable the widget

            self.body_widgets['activation'][b_index].config(bg=st.RED, text="OFF")
            self.root.logging_frame.add_log(f"{strat_selected} strategy on {symbol} / {timeframe} stopped")

    def _delete_row(self, b_index: int):

        for element in self._base_params:
            self.body_widgets[element['code_name']][b_index].grid_forget()

            del self.body_widgets[element['code_name']][b_index]
