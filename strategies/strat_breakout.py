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

        print(f"Activated BS for {contract.symbol}")
