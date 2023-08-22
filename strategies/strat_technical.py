# @Project:     Crypto-Bot
# @Filename:    strat_technical.py
# @Author:      Daksh Gaur
# @Email:       hi@daksh.fyi
# @Time:        22-08-2023 02:48 pm


import typing
import logging

logger = logging.getLogger()


from strategies.base import Strategy
from connectors.models import Balance, Candle, Contract, OrderStatus

class TechnicalStrategy(Strategy):
    # the params of technical strategy is passed as a other_params dict
    def __init__(self, contract: Contract, exchange: str, timeframe: str, balance_pct: float, take_profit: float,
                stop_loss: float, other_params: typing.Dict):
        super().__int__(contract, exchange, timeframe, balance_pct, take_profit, stop_loss)

        self._ema_fast = other_params['ema_fast']
        self._ema_slow = other_params['ema_slow']
        self._ema_signal = other_params['ema_signal']

        print(f"Activated TS for {contract.symbol}")