import talib


class Pattern:
    def __init__(self, df, pattern):
        self.df = df
        self.df[pattern] = getattr(talib, pattern).\
            df(['open'], df['high'], df['low'], df['close'])
