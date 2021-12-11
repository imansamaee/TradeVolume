import collections
import os

import ccxt as ccxt
from binance.client import Client

# init
import time
import win32api


api_key = 'XoY2Jy39Y51gYMt1niywbOXsHSQEemtJI70naqxssk9payH7w1KKyvYjcgtMU36u'
api_secret = 'quyLDj59OcOAVsFhOMxEptITeR9fcBucGIynLErZVO1HpCVkR4nljAWmKYsDOW4D'

client = Client(api_key, api_secret)
server_time = client.get_server_time()
gmtime=time.gmtime(int((server_time["serverTime"])/1000))
win32api.SetSystemTime(gmtime[0],gmtime[1],0,gmtime[2],gmtime[3],gmtime[4],gmtime[5],0)
