# 清理資料用
import pandas as pd 
import numpy as np

# 爬蟲用
import requests,json
import urllib.parse
import ssl #給對方知道連線安全
from bs4 import BeautifulSoup as bs
from time import sleep #每跑一下休息
from requests.adapters import HTTPAdapter #安全網域
from requests.packages.urllib3.util.retry import Retry  #對方擋住爬蟲 所以要一直重複跑
from selenium import webdriver #控制網頁機器人
import pytz
from datetime import datetime
import instaloader
from bs4 import BeautifulSoup as bs
from dateutil import parser
from datetime import datetime
from itertools import dropwhile, takewhile
import pickle
import instaloader

L = instaloader.Instaloader()
session = requests.Session()
retry = Retry(connect=3)
adapter = HTTPAdapter(max_retries=retry)
session.mount('https://', adapter)
HASHTAG = '五峰旗瀑布'
L.login('', '')
post_iterator = instaloader.NodeIterator(
    L.context, "9b498c08113f1e09617a1703c22b2f32",
    lambda d: d['data']['hashtag']['edge_hashtag_to_media'],
    lambda n: instaloader.Post(L.context, n),
    {'tag_name': HASHTAG},
    f"https://www.instagram.com/explore/tags/{HASHTAG}/"
)

data=[]
SINCE = datetime(2020, 1, 1)
UNTIL = datetime(2020, 12, 31)
for post in post_iterator:
    postdate = post.date
    print(postdate)
    if postdate <= UNTIL and postdate>=SINCE:
        data.append(postdate)
df = pd.DataFrame(data)
df.columns=['hashtag']
df['hashtag'] = pd.to_datetime(df['hashtag'])
df['Date'] = df['hashtag'].dt.strftime('%Y-%m-%d')
df['Time'] = df['hashtag'].dt.strftime('%H:%M:%S')
df['hashtag']=1
     