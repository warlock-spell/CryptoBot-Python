# @Project:     Crypto-Bot
# @Filename:    models.py
# @Author:      Daksh Gaur
# @Email:       hi@daksh.fyi
# @Time:        09-07-2023 02:07 pm


class Balance:
    def __init__(self, info):
        self.initial_margin = float(info['initialMargin'])
        self.maintenance_margin = float(info['maintMargin'])
        self.margin_balance = float(info['marginBalance'])
        self.wallet_balance = float(info['walletBalance'])
        self.unrealised_pnl = float(info['unrealizedProfit'])