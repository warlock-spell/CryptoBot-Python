# @Project:     Crypto-Bot
# @Filename:    strat_breakout.py
# @Author:      Daksh Gaur
# @Email:       hi@daksh.fyi
# @Time:        22-08-2023 02:57 pm

import typing
import logging

logger = logging.getLogger()


from strategies.base import Strategy
from connectors.models import Balance, Candle, Contract, OrderStatus

class BreakoutStrategy(Strategy):
    # the params of breakout strategy is passed as a other_params dict
    def __init__(self, contract: Contract, exchange: str, timeframe: str, balance_pct: float, take_profit: float,
                stop_loss: float, other_params: typing.Dict):
        super().__int__(contract, exchange, timeframe, balance_pct, take_profit, stop_loss)

        self._min_volume = other_params['min_volume']

        # print(f"Activated BS for {contract.symbol}")

    def _check_signal(self) -> int:

        # at index -1 -> current bar, -2 -> Inside/outside bar depending upon pattern, -3 -> mother bar

        if self.candles[-1].close > self.candles[-2].high and self.candles[-1].volume > self._min_volume:
            # Long Signal
            return 1
        elif self.candles[-1].close < self.candles[-2].low and self.candles[-1].volume > self._min_volume:
            # Short signal
            return -1
        else:
            # no signal
            return 0

        # if self.candles[-2].high < self.candles[-3].high and self.candles[-2].low > self.candles[-3].low:
        #     if self.candles[-1].close > self.candles[-3].high:
        #         # Upside Breakout
        #         pass
        #     elif self.candles[-1].close < self.candles[-3].low:
        #         # Downside Breakout
        #         pass