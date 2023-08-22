# @Project:     Crypto-Bot
# @Filename:    strat_technical.py
# @Author:      Daksh Gaur
# @Email:       hi@daksh.fyi
# @Time:        22-08-2023 02:48 pm


from typing import *
import pandas as pd
import logging

logger = logging.getLogger()


from strategies.base import Strategy
from connectors.models import Balance, Candle, Contract, OrderStatus

class TechnicalStrategy(Strategy):
    # the params of technical strategy is passed as a other_params dict
    def __init__(self, contract: Contract, exchange: str, timeframe: str, balance_pct: float, take_profit: float,
                stop_loss: float, other_params: Dict):
        super().__int__(contract, exchange, timeframe, balance_pct, take_profit, stop_loss)

        self._ema_fast = other_params['ema_fast']
        self._ema_slow = other_params['ema_slow']
        self._ema_signal = other_params['ema_signal']

        self._rsi_length = other_params['rsi_length']

        # print(f"Activated TS for {contract.symbol}")

    def _rsi(self) -> float:
        # rsi -> relative strength index

        close_list = []
        for candle in self.candles:
            close_list.append(candle.close)

        closes = pd.Series(close_list)

        delta = closes.diff().dropna()

        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0

        avg_gain = up.ewm(com=(self._rsi_length - 1), min_periods=self._rsi_length).mean()
        avg_loss = down.abs().ewm(com=(self._rsi_length - 1), min_periods=self._rsi_length).mean()

        rs = avg_gain / avg_loss  # relative strength

        rsi = 100 - 100 / (1 + rs)
        rsi = rsi.round(2)

        return rsi.iloc[-2]

    def _macd(self) -> Tuple[float, float]:
        # moving average convergence divergence

        close_list = []
        for candle in self.candles:
            close_list.append(candle.close)

        closes = pd.Series(close_list)
        ema_fast = closes.ewm(span=self._ema_fast).mean()
        ema_slow = closes.ewm(span=self._ema_slow).mean()

        macd_line = ema_fast - ema_slow
        macd_signal = macd_line.ewm(span=self._ema_signal).mean()

        return macd_line.iloc[-2], macd_signal.iloc[-2]

    def _check_signal(self):

        macd_line, macd_signal = self._macd()
        rsi = self._rsi()

        print(rsi, macd_signal, macd_line)

        if rsi < 30 and macd_line > macd_signal:
            # Long signal
            return 1
        elif rsi > 70 and macd_line < macd_signal:
            # Short signal
            return -1
        else:
            # no signal
            return 0
