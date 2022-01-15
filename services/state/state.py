import pandas as pd

from services.data.api_data import APIData
from services.data.data_object import DataObject
# from services.deep.learner import DeepLearner
# noinspection PyTypeChecker
from services.market.symbol import Symbol


class State:
    def __init__(self, quoted_asset="USDT", time_frame="1m", test=False, init=False):
        self.init = init
        self.quoted_asset = quoted_asset
        self.time_frame = time_frame
        self.data_objects = {}
        # self.pnl = PNL(self.quoted_asset)
        # self.pnl.update()
        self.learner = {}
        self.positions = {}
        self.symbols = {}
        self.trades = {}
        self.limit = 400
        self.api_data = APIData(quoted_asset)
        self.test = test
        self.best_to_buy: DataObject

    def update(self):
        self.api_data.update()
        self.update_df()

    def update_df(self, since=None, limit=800, params={}):
        timeframe = self.time_frame
        print('updating assets...')
        symbols = self.api_data.get_big_symbols(1)
        print(symbols)
        for symbol in symbols:
            if symbol not in self.symbols:
                self.symbols[symbol] = {}
            exchange_data = self.api_data.exchange_data
            market = self.api_data.exchange_data.market(symbol)
            # binance docs say that the default limit 500, max 1500
            # for futures, max 1000 for spot markets
            # the reality is that the time range wider than 500 candles won't work right
            defaultLimit = 500
            maxLimit = 1500
            limit = defaultLimit if (limit is None) else min(limit, maxLimit)
            request = {
                'symbol': market['id'],
                'interval': exchange_data.timeframes[timeframe],
                'limit': limit,
            }
            duration = exchange_data.parse_timeframe(timeframe)
            if since is not None:
                request['startTime'] = since
                if since > 0:
                    endTime = exchange_data.sum(since, limit * duration * 1000 - 1)
                    now = exchange_data.milliseconds()
                    request['endTime'] = min(now, endTime)
            method = 'publicGetKlines'
            if market['linear']:
                method = 'fapiPublicGetKlines'
            elif market['inverse']:
                method = 'dapiPublicGetKlines'
            response = getattr(exchange_data, method)(exchange_data.extend(request, params))
            #
            #     [
            #         [1591478520000,"0.02501300","0.02501800","0.02500000","0.02500000","22.19000000",1591478579999,"0.55490906",40,"10.92900000","0.27336462","0"],
            #         [1591478580000,"0.02499600","0.02500900","0.02499400","0.02500300","21.34700000",1591478639999,"0.53370468",24,"7.53800000","0.18850725","0"],
            #         [1591478640000,"0.02500800","0.02501100","0.02500300","0.02500800","154.14200000",1591478699999,"3.85405839",97,"5.32300000","0.13312641","0"],
            #     ]
            #
            bars = exchange_data.parse_ohlcvs(response, market, timeframe, since, limit)
            df = pd.DataFrame(bars, columns=["time", "open", "high", "low", "close", "volume"])
            df.title = df.symbol = symbol
            data = DataObject(Symbol(symbol, market, df, timeframe))
            data.last = data.symbol.price = df.iloc[-1]['close']
            self.data_objects[symbol] = data

    def get_token_by_symbol_name(self, name_symbol):
        return next((i for i in self.api_data.tokens if i.name_symbol == name_symbol), None)

    def get_token_info(self, name_symbol):
        token = self.get_token_by_symbol_name(name_symbol)
        for index, item in self.data_objects.items():
            if name_symbol == item.symbol.market['info']['baseAsset'] or \
                    name_symbol == item.symbol.market['info']['quoteAsset']:
                token.data_objects[item.symbol.name] = item
                print(item.symbol.market['info']['quoteAsset'])
        return token

    def get_overall_df(self):

        for symbol, data_object in self.data_objects.items():
            df = pd.DataFrame()
            df['time'] = data_object.df['time']
            df['close'] = data_object.df['close']
            df['volume'] = data_object.df['volume']
            s = Symbol(data_object.symbol, data_object.df)

    def create_learner_df(self):
        numpy_data = []
        for i, l in self.learner.items():
            d: DataObject = l.data_object
            numpy_data.append(
                [d.symbol, d.last, d.real_last, d.next_close, d.anticipated_percentage_increase, d.profit, d.lost,
                 d.test_accuracy, d.sma_200, d.rsi_14])

        df = pd.DataFrame(numpy_data,
                          columns=['symbol', 'last', 'real_last', 'next_close', 'anticipated_percentage_increase',
                                   'profit', 'lost', 'test_accuracy', 'sma_200', 'rsi_14'])
        df.to_csv("test.csv")

    # def get_overall_df_deep(self):
    #     highest_increase = -100
    #     counter = 0
    #     trade_df = pd.DataFrame()
    #     for symbol, data_object in self.data_objects.items():
    #         trade_df[symbol + "_trade"] = data_object.df['close'] * data_object.df['volume']
    #     for symbol, data_object in self.data_objects.items():
    #         df = pd.DataFrame()
    #         df['time'] = data_object.df['time']
    #         df['close'] = data_object.df['close']
    #         df['volume'] = data_object.df['volume']
    #         df['sma_200'] = SMAIndicator(close=df['close'], window=200).sma_indicator()
    #         df['rsi_14'] = RSIIndicator(close=df['close']).rsi()
    #         sma_200 = df.iloc[-1]['sma_200']
    #         rsi_14 = df.iloc[-1]['rsi_14']
    #
    #         # if df.iloc[1]['close'] is None or df.iloc[-1]['close'] < sma_200 or \
    #         #         rsi_14 < 50 or \
    #         #         abs((df.iloc[-1]['close'] / df.iloc[1]['close'])) > 1.5:
    #
    #         #     continue
    #         df = df.drop(columns=["sma_200", "rsi_14"])
    #         df = pd.concat([df, trade_df], axis=1)
    #         df['next_close'] = data_object.df.shift(-1)['close']
    #         df = df.fillna(0)
    #         df.to_csv(f"data/deep/overall/{symbol}.csv", index=False)
    #         new_data: DataObject = data_object
    #         new_data.df = df
    #         new_data.rsi_14 = rsi_14
    #         new_data.sma_200 = sma_200
    #         learner = DeepLearner(new_data, self.init)
    #         learner.data_object.next_close = learner.predict_next_close()
    #         if highest_increase < learner.data_object.anticipated_percentage_increase:
    #             highest_increase = learner.data_object.anticipated_percentage_increase
    #             self.best_to_buy = learner.data_object
    #         self.learner[symbol] = learner
    #         counter += 1
    #         print(counter)
    #         # if counter % 3 == 0:
    #         #     break
