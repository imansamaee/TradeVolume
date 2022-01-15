import json


class Token:
    def __init__(self, name_symbol, price=0, market_cap=0, market_volume=0):
        self.name_symbol = name_symbol
        self.volume_24h = 0
        self.price = price
        self.market_percentage = 0
        self.market_change = 0
        self.market_cap = market_cap
        self.market_volume = market_volume
        self.data_objects = {}
        self.learner = {}

    @property
    def total_value_24h(self):
        return self.volume_24h * self.price

    def to_json(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__,
                                     sort_keys=True, indent=4))
