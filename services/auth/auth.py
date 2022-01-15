# init
import time

import requests
import win32api
from binance.client import Client

api_key = 'XoY2Jy39Y51gYMt1niywbOXsHSQEemtJI70naqxssk9payH7w1KKyvYjcgtMU36u'
api_secret = 'quyLDj59OcOAVsFhOMxEptITeR9fcBucGIynLErZVO1HpCVkR4nljAWmKYsDOW4D'
try:
    client = Client(api_key, api_secret)
    server_time = client.get_server_time()
    gmtime = time.gmtime(int((server_time["serverTime"]) / 1000))
    win32api.SetSystemTime(gmtime[0], gmtime[1], 0, gmtime[2], gmtime[3], gmtime[4], gmtime[5], 0)
except requests.exceptions.ReadTimeout:
    print("Binance not responding!")
    client = None


