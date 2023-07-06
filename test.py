# @Project:     Crypto-Bot
# @Filename:    test.py.py
# @Author:      Daksh Gaur
# @Email:       hi@daksh.fyi
# @Time:        07-07-2023 12:54 am

from connectors.binance_futures import BinanceFuturesClient
binance_client = BinanceFuturesClient(testnet=True)
for contract in binance_client.get_contract():
    # print(contract)
    pass
print(binance_client.get_bid_ask('BTCUSDT'))
print(binance_client.get_historical_candles('BTCUSDT', '1m', 10))
assert 10 == len(binance_client.get_historical_candles('BTCUSDT', '1m', 10))
assert 20 == len(binance_client.get_historical_candles('BTCUSDT', '1m', 20))