# @Project:     Crypto-Bot
# @Filename:    models.py
# @Author:      Daksh Gaur
# @Email:       hi@daksh.fyi
# @Time:        09-07-2023 02:07 pm


class Balance:
    def __init__(self, balance_info):
        self.initial_margin = float(balance_info['initialMargin'])
        self.maintenance_margin = float(balance_info['maintMargin'])
        self.margin_balance = float(balance_info['marginBalance'])
        self.wallet_balance = float(balance_info['walletBalance'])
        self.unrealised_pnl = float(balance_info['unrealizedProfit'])


class Candle:
    def __init__(self, candle_info):
        self.open_time = candle_info[0] # already an int
        self.open = float(candle_info[1])
        self.high = float(candle_info[2])
        self.low = float(candle_info[3])
        self.close = float(candle_info[4])
        self.volume = float(candle_info[5])
        self.close_time = candle_info[6]
        self.quote_asset_volume = float(candle_info[7])
        self.number_of_trades = float(candle_info[8])
        self.taker_buy_base_asset_volume = float(candle_info[9])
        self.taker_buy_quote_asset_volume = float(candle_info[10])
        self.ignore = float(candle_info[11])


class Contract:
    def __init__(self, contract_info):
        self.symbol = contract_info['symbol']
        self.base_asset = contract_info['baseAsset']
        self.quote_asset = contract_info['quoteAsset']
        self.price_decimals = contract_info['pricePrecision']
        self.quantity_decimals = contract_info['quantityPrecision']
