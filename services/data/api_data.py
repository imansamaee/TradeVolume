import operator

import ccxt
import requests

from services.auth.auth import api_secret, api_key
from services.auth.auth import client
from services.market.token import Token


class APIData:
    def __init__(self, base_symbol="USDT"):
        if not client:
            return
        self.base_symbol = base_symbol
        self.exchange_info = client.get_exchange_info()
        self.symbol_list_info = self.exchange_info['symbols']
        self.trade_symbols = self.init_trade_symbols()
        self.products = None
        self.exchange_data = ccxt.binance({'apiKey': api_key,
                                           'secret': api_secret})
        self.market_data = self.exchange_data.load_markets()
        self.tokens = []
        self.market_cap = 0

    def get_tokens(self):
        self.market_cap = 0
        self.tokens = []
        for token in self.products:
            if token["q"] == "USDT" and token["cs"] and token["c"]:
                token = Token(name_symbol=token["b"], price=float(token["c"]), market_volume=token["cs"])
                token.market_cap = token.price * token.market_volume
                self.tokens.append(token)
                self.market_cap += token.market_cap
        for i, token in enumerate(self.tokens):
            self.tokens[i].market_percentage = 100 * token.market_cap / self.market_cap
        self.tokens = sorted(self.tokens, key=operator.attrgetter('market_percentage'), reverse=True)

    def update(self) -> object:
        self.market_data = self.exchange_data.load_markets()
        self.products = requests.get(
            "https://www.binance.com/exchange-api/v2/public/asset-service/product/get-products").json()['data']
        self.get_tokens()

    def init_trade_symbols(self):
        ts = [ts['symbol'] for ts in self.trading_spot_symbols_info if ts['symbol'].endswith(self.base_symbol)]
        return ts

    def get_big_symbols(self, limit=10):
        symbols = []
        count = 0
        for token in self.tokens:
            if token.name_symbol + self.base_symbol in self.trade_symbols:
                symbols.append(token.name_symbol + self.base_symbol)
                count += 1
            if count > limit:
                break
        return symbols

    @property
    def trading_spot_symbols_info(self):
        return [s for s in self.symbol_list_info if s['status'] == "TRADING" and "SPOT" in s['permissions']]
