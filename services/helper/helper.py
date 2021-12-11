def get_profit(init_price, current_price):
    try:
        return 100 * round((float(current_price) - float(init_price)) / float(init_price), 4)
    except TypeError as e:
        return 0
