# @Project:     Crypto-Bot
# @Filename:    base.py
# @Author:      Daksh Gaur
# @Email:       hi@daksh.fyi
# @Time:        22-08-2023 02:30 pm

import logging

from connectors.models import Balance, Candle, Contract, OrderStatus

logger = logging.getLogger()


class Strategy:
    def __int__(self, contract: Contract, exchange: str, timeframe: str, balance_pct: float, take_profit: float,
                stop_loss: float):

        self.contract = contract
        self.exchange = exchange
        self.tf = timeframe
        self.balance_pct = balance_pct
        self.take_profit = take_profit
        self.stop_loss = stop_loss

