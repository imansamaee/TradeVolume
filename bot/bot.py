from binance.exceptions import BinanceAPIException

from services import logger
# from services.data.strategy import Strategy
from services.deep.learner import DeepLearner
from services.scheduleJob.schedule_job import scheduled
from services.state.state import State


class BOT:
    def __init__(self, time_frame="5m", limit=200, test=False):
        self.time_frame = time_frame
        self.limit = limit
        self.state = State(time_frame=time_frame, test=test)


