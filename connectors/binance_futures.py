# @Project:     Crypto-Bot
# @Filename:    binance_futures.py.py
# @Author:      Daksh Gaur
# @Email:       hi@daksh.fyi
# @Time:        06-07-2023 05:48 pm

import logging
import requests

logger = logging.getLogger()

TESTNET_BINANCE_BASE_URL = "https://testnet.binancefuture.com"
BINANCE_BASE_URL = "https://fapi.binance.com"


class BinanceFuturesClient:
    def __init__(self, testnet=True):
        self.base_url = TESTNET_BINANCE_BASE_URL if testnet else BINANCE_BASE_URL
        self.prices = {}  # key: contract_name, value: {bid: 0, ask: 0}
        logger.info("Binance Futures Client Initialised")

    def make_request(self, method, endpoint, data):
        if method == "GET":
            response = requests.get(f"{self.base_url}{endpoint}", params=data)
        else:
            raise ValueError

        if response.status_code == 200:
            return response.json()
        else:
            logger.error(
                f"Request failed with "
                f"status code: {response.status_code}, "
                f"method: {method}, "
                f"endpoint: {endpoint}, "
                f"{response.json()}")

            return None

    def get_contract(self):
        exchange_info = self.make_request("GET", "/fapi/v1/exchangeInfo", None)
        contracts = {}
        if exchange_info is not None:
            for contract_data in exchange_info['symbols']:
                contracts[contract_data['pair']] = contract_data

        return contracts

    def get_bid_ask(self, symbol):
        data = {'symbol': symbol}
        orderbook_data = self.make_request("GET", "/fapi/v1/ticker/bookTicker", data)

        if orderbook_data is not None:
            if symbol not in self.prices:
                self.prices[symbol] = {'bid': float(orderbook_data['bidPrice']),
                                       'ask': float(orderbook_data['askPrice'])}
            else:
                self.prices[symbol]['bid'] = float(orderbook_data['bidPrice'])
                self.prices[symbol]['ask'] = float(orderbook_data['askPrice'])

        return self.prices[symbol]

    def get_historical_candles(self, symbol, interval, limit=1000):
        data = {'symbol': symbol, 'interval': interval, 'limit': limit}
        raw_candle_data = self.make_request("GET", "/fapi/v1/klines", data)
        candles = []
        if raw_candle_data is not None:
            for candle_data in raw_candle_data:
                candles.append({
                    'open_time': candle_data[0],
                    'open': float(candle_data[1]),
                    'high': float(candle_data[2]),
                    'low': float(candle_data[3]),
                    'close': float(candle_data[4]),
                    'volume': float(candle_data[5]),
                    'close_time': candle_data[6],
                    'quote_asset_volume': float(candle_data[7]),
                    'number_of_trades': candle_data[8],
                    'taker_buy_base_asset_volume': float(candle_data[9]),
                    'taker_buy_quote_asset_volume': float(candle_data[10]),
                    'ignore': float(candle_data[11])
                })
        return candles