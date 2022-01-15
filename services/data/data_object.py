import json


class DataObject:
    def __init__(self, symbol):
        self.symbol = symbol
        self.last = 0
        self.real_last = 0
        self.next_close = 0
        self.rsi_14 = 0
        self.sma_200 = 0

    @property
    def anticipated_percentage_increase(self):
        return (self.next_close - self.last) / self.last * 100

    @property
    def test_accuracy(self):
        increase = (self.real_last - self.last) / self.last * 100
        return self.anticipated_percentage_increase - increase

    @property
    def lost(self):
        if self.anticipated_percentage_increase > 0 and self.last > self.real_last:
            return (self.last - self.real_last) / self.last * 100
        else:
            return False

    @property
    def profit(self):
        if self.anticipated_percentage_increase > 0 and self.last < self.real_last:
            return (self.last - self.real_last) / self.last * 100
        else:
            return False

    def to_json(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__,
                                     sort_keys=True, indent=4))
