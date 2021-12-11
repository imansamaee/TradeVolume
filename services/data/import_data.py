import duka.app.app as import_ticks_method
from duka.core.utils import TimeFrame
import datetime

start_date = datetime.date(2019,1,1)
end_date = datetime.date(2019,2,1)
Assets = ["EURUSD"]

import_ticks_method(Assets,
                    start_date,
                    end_date,
                    1,
                    TimeFrame.TICK,
                    ".",
                    True)