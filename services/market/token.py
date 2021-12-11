class Token:
    def __init__(self, name_symbol):
        self.name_symbol = name_symbol
        self.volume_24h = 0
        self.price = 0
        self.market_percentage = 0
        self.market_change = 0

    @property
    def total_value_24h(self):
        return self.volume_24h * self.price

