import json

# from services.plotting.candlestick import draw_chart
from services.state.state import State


class BOT:
    def __init__(self, time_frame="5m", test=False, init=False):
        self.time_frame = time_frame
        self.state = State(time_frame=time_frame, test=test, init=init)

    def to_json(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__,
                                     sort_keys=True, indent=4))


# TRADING_BOT = BOT(time_frame="1h", test=True, init=False)
# STATE = TRADING_BOT.state

#
# @scheduled(TRADING_BOT.time_frame)
# def scalping():
#     from main import STATE
#     for symbol, data in STATE.data_objects.items():
#         try:
#             position = TRADING_BOT.state.get_position(data.symbol)
#             position.closed_price = data.training_data_df['close'].iloc[-1]
#             position.check_sells()
#             if data.strategy.broken_out(1.5):
#                 # position.add_to_buy()
#                 data.draw_chart()
#         except BinanceAPIException as e:
#             logger.error(f"Binance error for symbol {data.symbol} : {e}")
#
#     TRADING_BOT.state.update()

#
# def run_services():
#     draw_chart("a")
#     # STATE.update()
#     print("done!")
#     draw_chart(list(STATE.data_objects.values())[0])
#     print("OK")

#
# if __name__ == "__main__":
#     run_services()
#

# 137788  variant and clear
# 1800675368 covid hotline