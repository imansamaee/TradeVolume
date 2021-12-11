# from services.auth.auth import exchange_data
from services.helper.helper import get_profit


class PNL:
    def __init__(self, quoted_asset="BUSD"):
        self.tickers = None
        self.balances = None
        self.quoted_asset = quoted_asset
        self.init_quoted_balance = None
        self.init_total_balance = self.total_balance

    @property
    def profit(self):
        return get_profit(self.init_total_balance, self.total_balance)

    @property
    def total_balance(self):
        _all_asset_in_quoted_value = 0
        for balance in self.balances:
            if balance['free'] == 0:
                continue
            _all_asset_in_quoted_value += float(balance['free']) * self.last_price(balance['asset'])
        return _all_asset_in_quoted_value

    def last_price(self, asset):
        if asset == self.quoted_asset:
            return 1
        symbol = asset + "/" + self.quoted_asset
        if symbol in self.tickers:
            return float(self.tickers[asset + "/" + self.quoted_asset]['info']['lastPrice'])
        return 0.0

    def get_balance(self, asset):
        balances = [b['free'] for b in self.balances if b['asset'] == asset]
        if len(balances) == 1:
            return float(balances[0])
        else:
            print(f"asset {asset} not in market.")
            return 0.0

    def update(self):
        from main import STATE
        self.tickers = STATE.exchange_data.fetch_tickers()
        self.balances = STATE.exchange_data.fetch_balance()['info']['balances']

    def get_current_row(self, asset):
        return self.tickers[asset + "/" + self.quoted_asset]


if __name__ == '__main__':
    pnl = PNL()
    print(pnl.get_balance("BUSD") * 10)
    # for i in range(1,100):
    #     print(exchange_data.price_to_precision("BTCBUSD", 47000.324234234234))
