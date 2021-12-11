from enum import Enum

import numpy as np
from ccxt import ExchangeError

from services import logger
# from services.auth.auth import exchange_data
from services.helper.helper import get_profit


class Position:
    def __init__(self, symbol, profit=0.35, loss=-1.0):
        self.symbol = symbol
        from bot.bot import TRADING_BOT
        self.quoted_asset = TRADING_BOT.state.quoted_asset
        self.base_asset = self.symbol.replace(self.quoted_asset, "")
        self.price = None
        self.amount = None
        self.quoted_price = None
        self.quoted_amount = TRADING_BOT.state.quoted_asset_amount_for_every_trade
        self.status = OrderStatus.START
        self.aimed_profit = profit
        self.max_loss = loss
        self.closed_price = None
        self.sold_price = None
        self.bought_price = None

    @property
    def profit(self):
        return get_profit(self.sold_price, self.bought_price)

    @property
    def pnl_status(self):
        return np.where(self.profit < 0, "LOST", "WIN")

    def add_to_buy(self):
        if not self.check_balance():
            return
        amount = self.quoted_amount
        price = self.closed_price
        if self.status in [OrderStatus.SOLD, OrderStatus.START]:
            self.price = exchange_data.price_to_precision(self.symbol, price * 1.01)
            self.amount = exchange_data.amount_to_precision(self.symbol, amount / price)
            self.status = OrderStatus.BUY_APPROVED

    def check_balance(self):
        from bot.bot import STATE
        available_quoted_amount = STATE.pnl.get_balance(self.quoted_asset)
        if available_quoted_amount < self.quoted_amount:
            print("available quoted amount is not enough.")
            return False
        return True

    def add_all_to_sell(self):
        from bot.bot import STATE
        price = self.closed_price
        if self.status in [OrderStatus.BOUGHT, OrderStatus.START]:
            amount = STATE.pnl.get_balance(self.base_asset)
            self.price = exchange_data.price_to_precision(self.symbol, price * (1 + self.aimed_profit / 100))
            self.amount = exchange_data.amount_to_precision(self.symbol, amount)
            self.status = OrderStatus.SELL_APPROVED


    def buy(self):
        try:
            if not self.check_balance():
                print("Error with buy balance!")
                return
            if self.status == OrderStatus.BUY_APPROVED:
                print(f"trade {self.symbol} approved!")
                exchange_data.create_limit_buy_order(self.symbol, self.amount, self.price)
                self.status = OrderStatus.OPEN_BUY
        except ExchangeError as e:
            logger.error(e)

    def sell(self):
        try:
            if self.status == OrderStatus.SELL_APPROVED:
                print(f" sell amount is: {self.amount}")
                exchange_data.create_limit_sell_order(self.symbol, self.amount, self.price)
                self.status = OrderStatus.OPEN_SELL
        except ExchangeError as e:
            logger.error(e)

    def check_open_orders(self):
        try:
            if self.status == OrderStatus.BOUGHT:
                print(f"adding {self.symbol} to sell...")
                self.add_all_to_sell()
        except ExchangeError as e:
            logger.error(f"Sell error: {e}")
        try:
            if self.status not in [OrderStatus.OPEN_SELL, OrderStatus.OPEN_BUY]:
                return
            orders = exchange_data.fetch_open_orders(self.symbol)
            if len(orders) == 0:
                if self.status is OrderStatus.OPEN_SELL:
                    self.status = OrderStatus.SOLD
                    order = exchange_data.fetch_closed_orders(symbol=self.symbol, limit=1)[0]
                    if order['info']['side'] == "SELL":
                        self.sold_price = order['average']
                        self.close()
                    else:
                        print("please don't")
                if self.status is OrderStatus.OPEN_BUY:
                    self.status = OrderStatus.BOUGHT
                    order = exchange_data.fetch_closed_orders(symbol=self.symbol, limit=1)[0]
                    if order['info']['side'] == "BUY":
                        self.bought_price = order['average']
                        print(f"average bought price: {self.bought_price}")
                    else:
                        print("please don't")

            if len(orders) > 1:
                print("Too many Orders. Please fix manually.")
        except ExchangeError as e:
            logger.error(e)



    def check_sells(self):
        if self.profit < self.max_loss:
            self.sell_with_loss()
            self.status = OrderStatus.SOLD

    def sell_with_loss(self):
        try:
            exchange_data.cancel_all_orders(self.symbol)
            amount = exchange_data.fetch_balance()[self.base_asset]['free']
            print(amount)
            exchange_data.create_market_sell_order(self.symbol, amount)
        except ExchangeError as e:
            logger.error(e)

    def close(self):
        msg = f"{self.pnl_status} -- Trading {self.symbol} Completed with {self.profit} profit."
        print(msg)
        from bot.bot import TRADING_BOT
        TRADING_BOT.state.get_trade(self.symbol).append(self)
        self.__init__(self.symbol, self.aimed_profit, self.max_loss)
        logger.info(msg)


class OrderStatus(Enum):
    START = 0
    SELL_APPROVED = 1
    BUY_APPROVED = 2
    SELL_FAILED = 3
    BUY_FAILED = 4
    OPEN_SELL = 5
    OPEN_BUY = 6
    SOLD = 7
    BOUGHT = 8
