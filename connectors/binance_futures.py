# @Project:     Crypto-Bot
# @Filename:    binance_futures.py.py
# @Author:      Daksh Gaur
# @Email:       hi@daksh.fyi
# @Time:        06-07-2023 05:48 pm

import logging
import requests
import time
import hmac
import hashlib
import websocket
import threading
import json
import typing

from models import Balance, Candle, Contract, OrderStatus

logger = logging.getLogger()

TESTNET_BINANCE_BASE_URL = "https://testnet.binancefuture.com"
BINANCE_BASE_URL = "https://fapi.binance.com"
TESTNET_BINANCE_FUTURES_STREAM_URL = "wss://stream.binancefuture.com/ws"
BINANCE_FUTURES_STREAM_URL = "wss://fstream.binance.com/ws"


class BinanceFuturesClient:
    def __init__(self, public_key: str, secret_key: str, testnet: bool = True):
        self.base_url = TESTNET_BINANCE_BASE_URL if testnet else BINANCE_BASE_URL
        self.stream_url = TESTNET_BINANCE_FUTURES_STREAM_URL if testnet else BINANCE_FUTURES_STREAM_URL
        self.prices = {}  # key: contract_name, value: {bid: 0, ask: 0}
        self.public_key = public_key
        self.secret_key = secret_key
        self.websocket_id = 1
        self.ws = None

        self.contracts = self.get_contract()
        self.balances = self.get_balances()

        self.headers = {'X-MBX-APIKEY': self.public_key}

        t = threading.Thread(target=self.start_websocket)
        t.start()

        logger.info("Binance Futures Client Initialised")

    def generate_signature(self, data: typing.Dict) -> str:
        # generate signature from data and secret key to be sent in header
        query_string = '&'.join([f"{d}={data[d]}" for d in data])
        # encode it to bytes using UTF-8
        # another way to do same is: urlencode(data).encode('utf-8')
        return hmac.new(self.secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    def make_request(self, method: str, endpoint: str, data: typing.Dict):

        if method == "GET":
            try:
                response = requests.get(f"{self.base_url}{endpoint}", params=data, headers=self.headers)
            except Exception as e:
                logger.error(f"Connection error while making {method} request to {endpoint}: {e}")
                return None

        elif method == "POST":
            try:
                response = requests.post(f"{self.base_url}{endpoint}", params=data, headers=self.headers)
            except Exception as e:
                logger.error(f"Connection error while making {method} request to {endpoint}: {e}")
                return None

        elif method == "DELETE":
            try:
                response = requests.delete(f"{self.base_url}{endpoint}", params=data, headers=self.headers)
            except Exception as e:
                logger.error(f"Connection error while making {method} request to {endpoint}: {e}")
                return None
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

    def get_contract(self) -> typing.Dict[str, Contract]:
        exchange_info = self.make_request("GET", "/fapi/v1/exchangeInfo", dict())
        contracts = {}
        if exchange_info is not None:
            for contract_data in exchange_info['symbols']:
                contracts[contract_data['pair']] = Contract(contract_data)

        return contracts

    def get_bid_ask(self, contract: Contract) -> typing.Dict[str, float]:
        data = {'symbol': contract.symbol}
        orderbook_data = self.make_request("GET", "/fapi/v1/ticker/bookTicker", data)

        if orderbook_data is not None:
            if contract.symbol not in self.prices:
                self.prices[contract.symbol] = {'bid': float(orderbook_data['bidPrice']),
                                                'ask': float(orderbook_data['askPrice'])}
            else:
                self.prices[contract.symbol]['bid'] = float(orderbook_data['bidPrice'])
                self.prices[contract.symbol]['ask'] = float(orderbook_data['askPrice'])

            return self.prices[contract.symbol]

    def get_historical_candles(self, contract: Contract, interval: str, limit: int = 1000) -> typing.List[Candle]:
        data = {'symbol': contract.symbol, 'interval': interval, 'limit': limit}
        raw_candle_data = self.make_request("GET", "/fapi/v1/klines", data)
        candles = []
        if raw_candle_data is not None:
            for candle_data in raw_candle_data:
                candles.append(Candle(candle_data))

        return candles

    def get_balances(self) -> typing.Dict[str, Balance]:
        data = {}
        data['timestamp'] = int(time.time() * 1000)  # LONG format required, therefore int()
        data['signature'] = self.generate_signature(data)

        balances = {}

        account_data = self.make_request("GET", "/fapi/v1/account", data)

        if account_data is not None:
            for a in account_data['assets']:
                balances[a['asset']] = Balance(a)

        return balances

    def place_order(self, contract: Contract, side: str, quantity: float, order_type: str, price=None,
                    time_in_force=None) -> OrderStatus:
        # Symbol, side & type are mandatory
        # quantity and timestamp are mandatory
        # timeInForce, price, newClientOrderId, stopPrice, recvWindow are optional
        data = {}
        data['symbol'] = contract.symbol
        data['side'] = side
        data['quantity'] = quantity
        data['type'] = order_type

        if price is not None:
            data['price'] = price

        if time_in_force is not None:
            data['timeInForce'] = time_in_force

        data['timestamp'] = int(time.time() * 1000)
        data['signature'] = self.generate_signature(data)

        order_status = self.make_request("POST", "/fapi/v1/order", data)

        if order_status is None:
            order_status = OrderStatus(order_status)

        return order_status

    def cancel_order(self, contract: Contract, order_id: int) -> OrderStatus:
        # Binance may send "order does not exist" when market fluctuates a lot
        # GET /fapi/v1/order will work anyway
        data = {}
        data['symbol'] = contract.symbol
        data['orderId'] = order_id
        data['timestamp'] = int(time.time() * 1000)
        data['signature'] = self.generate_signature(data)

        order_status = self.make_request("DELETE", "/fapi/v1/order", data)

        if order_status is None:
            order_status = OrderStatus(order_status)

        return order_status

    def get_order_status(self, contract: Contract, order_id: int) -> OrderStatus:
        data = {}
        data['timestamp'] = int(time.time() * 1000)
        data['symbol'] = contract.symbol
        data['orderId'] = order_id
        data['signature'] = self.generate_signature(data)

        order_status = self.make_request("GET", "/fapi/v1/order", data)

        if order_status is None:
            order_status = OrderStatus(order_status)

        return order_status

    def start_websocket(self):
        self.ws = websocket.WebSocketApp(self.stream_url,
                                         on_open=self.on_open,
                                         on_close=self.on_close,
                                         on_error=self.on_error,
                                         on_message=self.on_message)
        while True: # reconnect on disconnect after 3 seconds
            try:
                self.ws.run_forever()
            except Exception as e:
                logger.error(f"Binance error in websocket run_forever() method: {e}")
            time.sleep(3)

    def on_open(self, ws):
        logger.info("Websocket connection opened for Binance")
        # Subscribe to symbol when connection is established
        self.subscribe_channel("BTCUSDT")

    def on_close(self, ws):
        logger.warning("Websocket connection closed for Binance")

    def on_error(self, ws, error: str):
        logger.error(f"Error received {error}")

    def on_message(self, ws, message: str):
        # convert received message from string to dict
        data = json.loads(message)

        if "e" in data:
            if data["e"] == "bookTicker":
                symbol = data['s']
                if symbol not in self.prices:
                    self.prices[symbol] = {'bid': float(data['b']),
                                           'ask': float(data['a'])}
                else:
                    self.prices[symbol]['bid'] = float(data['b'])
                    self.prices[symbol]['ask'] = float(data['a'])

                print(self.prices[symbol])

    def subscribe_channel(self, contract: Contract):
        data = {}
        data['method'] = "SUBSCRIBE"
        data['params'] = []
        data['params'].append(f"{contract.symbol.lower()}@bookTicker")
        data['id'] = self.websocket_id

        # convert from dict to string and send
        try:
            self.ws.send(json.dumps(data))
        except Exception as e:
            logger.error(f"Websocket error while subscribing to {contract.symbol}: {e}")

        self.websocket_id += 1
