import numpy as np
import pandas as pd
import talib

from services.market.level import Level
from services.ta.hill import Hill


class Symbol:
    def __init__(self, name, market, df, timeframe):
        self.name = name
        self.market = market
        self.json_df = df.to_json()
        self.price = 0.0
        # if self.df:
        #     self.price = self.df.iloc[-1]['close']
        self.timeframe = timeframe
        self.levels: [Level] = []
        self.hills: [Hill] = []

        self.get_hills()

    def add_pattern(self, pattern):
        df = pd.read_json(self.json_df)
        df[pattern] = getattr(talib, pattern)(df['open'], df['high'], df['low'], df['close'])
        self.json_df = df.to_json()

    def get_levels(self):
        pass

    def is_support(self, i):
        df = pd.read_json(self.json_df)
        return df['low'][i] < df['low'][i - 1] < df['low'][i - 2] \
               and df['low'][i] < df['low'][i + 1] < df['low'][i + 2]

    def is_resistance(self, i):
        df = pd.read_json(self.json_df)
        return df['high'][i] > df['high'][i - 1] > df['high'][i - 2] \
               and df['high'][i] > df['high'][i + 1] > df['high'][i + 2]

    def is_far_from_level(self, levels, l):
        df = pd.read_json(self.json_df)
        s = np.mean(df['high'] - df['low'])
        return np.sum([abs(l - x) < s for x in levels]) == 0

    def get_hills(self):
        df = pd.read_json(self.json_df)
        current_high = df.iloc[0]['high']
        hill_df: pd.DataFrame = {}
        hill = Hill()
        going_up = False
        going_down = False

        for index, candle in df.iterrows():
            if not going_down and not going_up and candle['high'] > current_high:
                going_up = True
                hill = Hill(btm_start=candle['low'])
                hill_df = pd.DataFrame(candle).transpose()

            if going_up and candle['high'] > current_high:
                hill_df = hill_df.append(candle, ignore_index=True)
                hill.top = current_high

            if going_up and candle['high'] < current_high:
                going_down = True
                going_up = False
                hill.top = current_high

            if going_down and candle['high'] < current_high:
                hill_df = hill_df.append(candle, ignore_index=True)

            if going_down and candle['high'] > current_high:
                hill.btm_end = candle['low']
                if hill_df.shape[0] > 5:
                    hill.json_df = hill_df.to_json()
                self.hills.append(hill)
                hill_df = None
                going_down = False

            current_high = candle['high']
