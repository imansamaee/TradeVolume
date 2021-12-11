from binance.exceptions import BinanceAPIException

from services import logger
from services.scheduleJob.schedule_job import scheduled
from services.state.state import State


class BOT:
    def __init__(self, time_frame="5m", test=False, init=False):
        self.time_frame = time_frame
        self.state = State(time_frame=time_frame, test=test, init=init)


TRADING_BOT = BOT(time_frame="1h", test=True, init=False)
STATE = TRADING_BOT.state


@scheduled(TRADING_BOT.time_frame)
def scalping():
    from main import STATE
    for symbol, data in STATE.data_objects.items():
        try:
            position = TRADING_BOT.state.get_position(data.symbol)
            position.closed_price = data.training_data_df['close'].iloc[-1]
            position.check_sells()
            if data.strategy.broken_out(1.5):
                # position.add_to_buy()
                data.draw_chart()
        except BinanceAPIException as e:
            logger.error(f"Binance error for symbol {data.symbol} : {e}")

    TRADING_BOT.state.update()


def run():
    # STATE.create_learner_df()
    STATE.update()
    STATE.get_overall_df()
    # print(STATE.best_to_buy.symbol)
    # # print(STATE.best_to_buy.last, STATE.best_to_buy.next_close, STATE.best_to_buy.real_last)
    # # for i, l in STATE.learner.items():
    # #     print(l.data_object.symbol, l.data_object.lost)
    STATE.create_learner_df()


if __name__ == "__main__":
    run()
