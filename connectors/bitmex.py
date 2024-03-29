# @Project:     Crypto-Bot
# @Filename:    bitmex.py
# @Author:      Daksh Gaur
# @Email:       hi@daksh.fyi
# @Time:        06-07-2023 07:54 pm

import logging
import requests
import time
import hmac
import hashlib
import websocket
import threading
import json
import typing
import dateutil.parser
from urllib.parse import urlencode

from connectors.models import Balance, Candle, Contract, OrderStatus
from strategies.strat_technical import TechnicalStrategy
from strategies.strat_breakout import BreakoutStrategy

logger = logging.getLogger()

TESTNET_BITMEX_BASE_URL = "https://testnet.bitmex.com"
BITMEX_BASE_URL = "https://www.bitmex.com"
TESTNET_BITMEX_STREAM_URL = "wss://testnet.bitmex.com/realtime"
BITMEX_STREAM_URL = "wss://www.bitmex.com/realtime"


class BitmexClient:
    def __init__(self, public_key: str, secret_key: str, testnet: bool = True):
        self._base_url = TESTNET_BITMEX_BASE_URL if testnet else BITMEX_BASE_URL
        self._stream_url = TESTNET_BITMEX_STREAM_URL if testnet else BITMEX_STREAM_URL

        self._public_key = public_key
        self._secret_key = secret_key

        self._ws = None

        self.strategies: typing.Dict[int, typing.Union[TechnicalStrategy, BreakoutStrategy]] = dict()

        self.contracts = self.get_contracts()
        self.balances = self.get_balances()

        self.prices = {}

        self.logs = []

        t = threading.Thread(target=self._start_websocket)
        t.start()

        logger.info("Bitmex Client Successfully Initialised")

    def _add_log(self, msg: str):
        logger.info(msg)
        self.logs.append({"log": msg, "displayed": False})

    def _generate_signature(self, method: str, endpoint: str, expires: str, data: typing.Dict) -> str:
        message = method + endpoint + "?" + urlencode(data) + expires if len(data) > 0 else method + endpoint + expires
        return hmac.new(self._secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()

    def _make_request(self, method: str, endpoint: str, data: typing.Dict):

        # For each request, generate a new header
        # header has api-key, signature, expires

        headers = dict()
        expires = str(int(time.time()) + 5)
        headers['api-expires'] = expires
        headers['api-key'] = self._public_key
        headers['api-signature'] = self._generate_signature(method, endpoint, expires, data)

        if method == "GET":
            try:
                response = requests.get(self._base_url + endpoint, params=data, headers=headers)
            except Exception as e:
                logger.error(f"Connection error while making {method} request to {endpoint}: {e}")
                return None

        elif method == "POST":
            try:
                response = requests.post(self._base_url + endpoint, params=data, headers=headers)
            except Exception as e:
                logger.error(f"Connection error while making {method} request to {endpoint}: {e}")
                return None

        elif method == "DELETE":
            try:
                response = requests.delete(self._base_url + endpoint, params=data, headers=headers)
            except Exception as e:
                logger.error(f"Connection error while making {method} request to {endpoint}: {e}")
                return None
        else:
            raise ValueError

        if response.status_code == 200:
            return response.json()
        else:
            logger.error(
                f"Error while making {method} request to {endpoint}: {response.json()} (error code {response.status_code})")
            return None

    def get_contracts(self) -> typing.Dict[str, Contract]:

        instruments = self._make_request("GET", "/api/v1/instrument/active", dict())

        contracts = dict()

        if instruments is not None:
            for s in instruments:
                contracts[s['symbol']] = Contract(s, "bitmex")

        return contracts

    def get_balances(self) -> typing.Dict[str, Balance]:
        data = dict()
        data['currency'] = "all"

        margin_data = self._make_request("GET", "/api/v1/user/margin", data)

        balances = dict()

        if margin_data is not None:
            for a in margin_data:
                balances[a['currency']] = Balance(a, "bitmex")

        return balances

    def get_historical_candles(self, contract: Contract, timeframe: str) -> typing.List[Candle]:
        data = dict()

        data['symbol'] = contract.symbol
        data['partial'] = True
        data['binSize'] = timeframe
        data['count'] = 500
        data['reverse'] = True

        raw_candles = self._make_request("GET", "/api/v1/trade/bucketed", data)

        candles = []

        if raw_candles is not None:
            for c in reversed(raw_candles):
                candles.append(Candle(c, timeframe, "bitmex"))

        return candles

    def place_order(self, contract: Contract, order_type: str, quantity: int, side: str, price=None,
                    tif=None) -> OrderStatus:
        data = dict()

        data['symbol'] = contract.symbol
        data['side'] = side.capitalize()
        data['orderQty'] = round(quantity / contract.lot_size) * contract.lot_size
        data['ordType'] = order_type.capitalize()

        if price is not None:
            data['price'] = round(round(price / contract.tick_size) * contract.tick_size, 8)

        if tif is not None:
            data['timeInForce'] = tif

        order_status = self._make_request("POST", "/api/v1/order", data)

        if order_status is not None:
            order_status = OrderStatus(order_status, "bitmex")

        return order_status

    def cancel_order(self, order_id: str) -> OrderStatus:
        data = dict()
        data['orderID'] = order_id

        order_status = self._make_request("DELETE", "/api/v1/order", data)

        if order_status is not None:
            # cancel 1st order in list
            order_status = OrderStatus(order_status[0], "bitmex")

        return order_status

    def get_order_status(self, order_id: str, contract: Contract) -> OrderStatus:

        data = dict()
        data['symbol'] = contract.symbol
        data['reverse'] = True

        order_status = self._make_request("GET", "/api/v1/order", data)

        if order_status is not None:
            # order status is a list of all orders with the supplied symbol
            for order in order_status:
                if order['orderID'] == order_id:
                    return OrderStatus(order, "bitmex")

    def _start_websocket(self):
        self._ws = websocket.WebSocketApp(self._stream_url, on_open=self._on_open, on_close=self._on_close,
                                          on_error=self._on_error, on_message=self._on_message)

        while True:
            try:
                self._ws.run_forever()
            except Exception as e:
                logger.error(f"Bitmex error in websocket run_forever() method: {e}")
            time.sleep(2)

    def _on_open(self, ws):
        logger.info("Websocket connection opened for Bitmex")

        self.subscribe_channel("instrument")
        self.subscribe_channel("trade")

    def _on_close(self, ws):
        logger.warning("Websocket connection closed for Bitmex")

    def _on_error(self, ws, error: str):
        logger.error(f"Error received on Bitmex: {error}")

    def _on_message(self, ws, msg: str):

        data = json.loads(msg)

        if "table" in data:
            if data['table'] == "instrument":

                for d in data['data']:

                    symbol = d['symbol']

                    if symbol not in self.prices:
                        self.prices[symbol] = {'bid': None, 'ask': None}

                    if 'bidPrice' in d:
                        self.prices[symbol]['bid'] = d['bidPrice']
                    if 'askPrice' in d:
                        self.prices[symbol]['ask'] = d['askPrice']

                    # print(symbol, self.prices[symbol])
                    # if symbol == "XBTUSD":
                    #     self._add_log(
                    #         f"{symbol} "
                    #         + str(self.prices[symbol]['bid'])
                    #         + " /"
                    #         + str(self.prices[symbol]['ask'])
                    #     )
            if data['table'] == "trade":

                for d in data['data']:
                    symbol = d['symbol']
                    # timestamp is in YYYY-MM-DDTHH:MM:SSZ
                    ts = int(dateutil.parser.isoparse(d['timestamp']).timestamp() * 1000)
                    for key, strat in self.strategies.items():
                        if strat.contract.symbol == symbol:
                            strat.parse_trades(float(d['price']), float(d['size']), ts)  # price, size, timestamp

    def subscribe_channel(self, topic: str):
        data = dict()
        data['op'] = "subscribe"
        data['args'] = []
        data['args'].append(topic)

        try:
            self._ws.send(json.dumps(data))
        except Exception as e:
            logger.error(f"Websocket error while subscribing to {topic} updates: {e}")
