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


class Candle:
    def __init__(self, info):
        self.open_time = info[0] # already an int
        self.open = float(info[1])
        self.high = float(info[2])
        self.low = float(info[3])
        self.close = float(info[4])
        self.volume = float(info[5])
        self.close_time = info[6]
        self.quote_asset_volume = float(info[7])
        self.number_of_trades = float(info[8])
        self.taker_buy_base_asset_volume = float(info[9])
        self.taker_buy_quote_asset_volume = float(info[10])
        self.ignore = float(info[11])
