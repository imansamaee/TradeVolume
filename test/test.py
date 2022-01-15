from main import BOT

TRADING_BOT = BOT(time_frame="1h", test=True, init=False)
STATE = TRADING_BOT.state
STATE.update()

print(STATE)