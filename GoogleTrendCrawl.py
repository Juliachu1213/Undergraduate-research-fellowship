from pytrends.request import TrendReq
from pprint import pprint
import pytrends
import pandas as pd
import time
import datetime
from datetime import datetime, date, time

pytrend = TrendReq(hl='en-US', tz=360)
keywords = ['五峰旗瀑布']
pytrend.build_payload(kw_list=keywords,cat=0,timeframe='2020-1-1 2020-12-31',geo='TW',gprop='')
pytrend.interest_over_time()

df = pd.DataFrame()
for i in range(1,6):
    print(i)
    if i== 1 or i==3 or i==5:
        gotr_1 = pytrend.get_historical_interest(keywords, year_start=2021, month_start=i, day_start=1, hour_start=0, year_end=2021, month_end=i, day_end=31, hour_end=23, cat=3, sleep=0)
        df = pd.concat([df,gotr_1])
    elif i==4 :
        gotr_2 = pytrend.get_historical_interest(keywords, year_start=2021, month_start=i, day_start=1, hour_start=0, year_end=2021, month_end=i, day_end=30, hour_end=23, cat=0, sleep=0)
        df = pd.concat([df,gotr_2])
    else:
        gotr_3 = pytrend.get_historical_interest(keywords, year_start=2021, month_start=i, day_start=1, hour_start=0, year_end=2021, month_end=i, day_end=28, hour_end=23, cat=0, sleep=0)
        df = pd.concat([df,gotr_3])
