from time import sleep

import schedule


def scheduled(duration):
    def decorator(function):
        def new_function(*args, **kwargs):
            d = int(duration[:-1])
            d_l = duration[-1]
            d_l_c = ""
            if d_l == "s":
                d_l_c = "seconds"
            elif d_l == "m":
                d_l_c = "minutes"
            elif d_l == "h":
                d_l_c = "hour"
            elif d_l == "d":
                d_l_c = "day"
            sch = getattr(schedule.every(d) ,d_l_c)
            sch.do(function)
            return function(*args, **kwargs)
        return new_function
    return decorator