# @Project:     Crypto-Bot
# @Filename:    test.py.py
# @Author:      Daksh Gaur
# @Email:       hi@daksh.fyi
# @Time:        07-07-2023 12:54 am

from connectors.binance_futures import BinanceFuturesClient
from connectors.bitmex import BitmexClient
from dotenv import load_dotenv
import os

load_dotenv()

BINANCE_TESTNET_PUBLIC_KEY = os.environ.get("BINANCE_TESTNET_PUBLIC_KEY")
BINANCE_TESTNET_SECRET_KEY = os.environ.get("BINANCE_TESTNET_SECRET_KEY")
BITMEX_TESTNET_PUBLIC_KEY = os.environ.get("BITMEX_TESTNET_PUBLIC_KEY")
BITMEX_TESTNET_SECRET_KEY = os.environ.get("BITMEX_TESTNET_SECRET_KEY")

# binance_client = BinanceFuturesClient(public_key=BINANCE_TESTNET_PUBLIC_KEY, secret_key=BINANCE_TESTNET_SECRET_KEY,
#                                       testnet=True)

bitmex_client = BitmexClient(public_key=BITMEX_TESTNET_PUBLIC_KEY, secret_key=BITMEX_TESTNET_SECRET_KEY, testnet=True)


# for contract in binance_client.get_contract():
    # print(contract)

# print(binance_client.get_bid_ask('BTCUSDT'))
# print(binance_client.get_historical_candles('BTCUSDT', '1m', 10))
# assert 10 == len(binance_client.get_historical_candles('BTCUSDT', '1m', 10))
# assert 20 == len(binance_client.get_historical_candles('BTCUSDT', '1m', 20))

# print(binance_client.get_balance())

def test_place_and_cancel_order_binance():
    print(f"Current Balance: {binance_client.get_balance()}")
    order = binance_client.place_order('BTCUSDT', 'BUY', 0.01, "LIMIT", 20000, "GTC")
    print(order)
    print(f"New Balance: {binance_client.get_balance()}")
    print(binance_client.get_order_status('BTCUSDT', order['orderId']))
    print(binance_client.cancel_order('BTCUSDT', order['orderId']))
    print(f"Balance after cancellation: {binance_client.get_balance()}")
    return None

# test_place_and_cancel_order_binance()


def get_balance_bitmex():
    print(bitmex_client.contracts['XBTUSD'].base_asset, bitmex_client.contracts['XBTUSD'].price_decimals)
    # Bitmex returns XBt (the symbol for satoshi) instead of XBT (the symbol for bitcoin)
    print(bitmex_client.balances['XBt'].wallet_balance)

    return None

# get_balance_bitmex()

def test_place_and_cancel_order_bitmex():
    order1 = bitmex_client.place_order(bitmex_client.contracts['XBTUSD'], 'Limit', 101, 'Buy', price=20000, tif='GoodTillCancel')
    print(order1)
    # print(bitmex_client.get_order_status(order1['orderID'], bitmex_client.contracts['XBTUSD']))
    # print(bitmex_client.cancel_order(order1['orderID']))

    return None

# test_place_and_cancel_order_bitmex()