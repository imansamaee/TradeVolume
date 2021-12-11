import collections
import operator

from services.db.db import Ticker
from services.market.token import Token


class Market:
    def __init__(self):
        self.info = None
        self.sorted_symbols = []
        self.tokens: [Token] = []
        self.symbol_list = []
        self.last_hr_tokens = []

    def update(self):
        self.tokens = self.get_tokens_from_db()
        self.get_token_price()
        self.update_token_market_percentage()
        self.last_hr_tokens = self.get_historical_tokens(2)
        self.get_market_change()

    def update_tokens(self, data_list=None):
        from main import STATE
        for symbol, data_object in STATE.data_objects.items():
            for q in ["USDT", "BTC", "ETH", "BNB"]:
                if symbol.endswith(q):
                    token = Token(symbol.replace(q, ""))

        if not data_list:
            data_list = Ticker.objects.order_by('-id').first()['info']
        self.info = data_list
        self.symbol_list = [i[0] for i in self.info]
        print("-" * 50)
        token_list = []
        for info in data_list:
            # info = list of [symbol, baseVolume, quoteVolume, last']
            symbol = info[0]
            tokens = symbol.split('/')
            token_list.append(tokens[0])
            token_list.append(tokens[1])
        counter = collections.Counter(token_list).most_common()
        for symbol, count in counter:
            self.sorted_symbols.append((symbol, [t for t in data_list if symbol in t[0].split('/')]))
        for sorted_symbol in self.sorted_symbols:
            token: Token = Token(sorted_symbol[0])
            for db_list_data in sorted_symbol[1]:
                # if it is base
                if token.name_symbol == db_list_data[0].split("/")[0]:
                    volume = db_list_data[1]
                else:
                    volume = db_list_data[2]
                token.volume_24h += volume
                self.tokens.append(token)
        self.tokens = list(dict.fromkeys(self.tokens))
        return_list = []
        self.get_token_price()
        for token in self.tokens:
            return_list.append([token.name_symbol, token.volume_24h, token.price])
        return return_list

    def get_tokens_from_db(self, id_index=0):
        tokens = []
        db_token_list = Ticker.objects.order_by('-id')[id_index]['volume']
        self.info = Ticker.objects.order_by('-id').first()['info']
        self.symbol_list = [i[0] for i in self.info]
        for db_token in db_token_list:
            token = Token(db_token[0])
            token.volume_24h = db_token[1]
            tokens.append(token)
        return tokens

    def get_token_price(self):
        new_token_list = []
        if not self.info:
            return
        for token in self.tokens:
            if token.name_symbol == "USDT":
                token.price = 1
            elif token.name_symbol + '/USDT' in self.symbol_list:
                token.price = next(x[-1] for x in self.info if x[0] == token.name_symbol + '/USDT')
            elif token.name_symbol + '/BTC' in self.symbol_list:
                token.price = next(x[-1] for x in self.info if x[0] == token.name_symbol + '/BTC') * \
                              next(x[-1] for x in self.info if x[0] == 'BTC/USDT')
            elif token.name_symbol + '/ETH' in self.symbol_list:
                token.price = next(x[-1] for x in self.info if x[0] == token.name_symbol + '/ETH') * \
                              next(x[-1] for x in self.info if x[0] == 'ETH/USDT')
            elif token.name_symbol + '/BNB' in self.symbol_list:
                token.price = next(x[-1] for x in self.info if x[0] == token.name_symbol + '/BNB') * \
                              next(x[-1] for x in self.info if x[0] == 'BNB/USDT')
            # else:
            #     print(f"{token.name_symbol} is not in any category.")
            new_token_list.append(token)
        self.tokens = new_token_list

    def get_token(self, name_symbol) -> Token:
        result = [i for i in self.tokens if i.name_symbol == name_symbol]
        if len(result) == 1:
            return result[0]
        else:
            # print('No token available with this name symbol.')
            return None

    @property
    def trade_value_24h(self):
        _trade_value_24h = 0
        for token in self.tokens:
            _trade_value_24h += token.volume_24h * token.price
        return _trade_value_24h

    def get_historical_tokens(self, depth=60):
        _historical_tokens = []
        for i in range(0, 120):
            _historical_tokens.append(self.get_tokens_from_db(i))
        return _historical_tokens

    def get_market_change(self, historical_tokens=None):
        if not historical_tokens:
            historical_tokens = self.last_hr_tokens
        for tokens in historical_tokens:
            for token in tokens:
                if max_power[token.name_symbol] < token.volume_24h:
                    max_power[token.name_symbol] = token.volume_24h

        for i, token in enumerate(self.tokens):
            if token.name_symbol not in max_power.keys():
                continue
            self.tokens[i].market_change = (max_power[token.name_symbol] - min_power[token.name_symbol]) / min_power[
                token.name_symbol]

        self.tokens = sorted(self.tokens, key=operator.attrgetter("market_change"), reverse=True)

    def update_token_market_percentage(self):
        _trade_value_24h = self.trade_value_24h
        for i, token in enumerate(self.tokens):
            token.market_percentage = token.total_value_24h / _trade_value_24h
            self.tokens[i] = token
