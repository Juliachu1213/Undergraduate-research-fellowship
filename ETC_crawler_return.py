#!/usr/bin/env python
# coding: utf-8

# In[3]:


#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import xml.etree.ElementTree as ET
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
import time,times
import gzip
from multiprocessing.dummy import Pool as ThreadPool
#from tqdm import tqdm_notebook
import os
import numpy as np
import requests


# In[2]:

driverpath = '../chromedriver'
#downloadpath = '/Users/office_macmini/Downloads/'
downloadpath = './'
destFile = r"../error_april/error_message.txt"


# In[3]:

chrome_options = Options() # 啟動無頭模式
chrome_options.add_argument('--headless')  #規避google bug
chrome_options.add_argument('--disable-gpu')


year_list = ['2018','2019','2020']
day31 = ['01','03','05','07','08','10','12']
month = ['01','02','03','04','05','06','07','08','09','10','11','12']
day = []
for i in range(31):
    if i < 9:
        day.append('0'+str(i+1))
    else:
        day.append(str(i+1))
date_list = []
for d in day:
    for y in year_list:
        if int(d) < 29:
            for m in month:
                date_list.append(y+m+d)
        elif d == '30':
            for m in month:
                if m != '02':
                    date_list.append(y+m+d)
                else:
                    pass
        elif d == '31':
            for m in day31:
                date_list.append(y+m+d)
        else:
            if y =='2020':
                for m in month:
                    date_list.append(y+m+d)
            else:
                for m in month:
                    if m != '02':
                        date_list.append(y+m+d)
                    else:
                        pass


# In[4]:


def read_xml(file):
    df = gzip.open(downloadpath+file, 'r')
    tree = ET.parse(df)
    root = tree.getroot()
    vdid,status,datacollecttime,vsrdir,vsrid,speed,laneoccupy,carid,volume = [],[],[],[],[],[],[],[],[]
    for level1 in root.iter('Info'):
        for level2 in level1.iter('lane'):
            for level3 in level2.iter('cars'):
                vdid.append(level1.attrib['vdid'])
                status.append(level1.attrib['status'])
                datacollecttime.append(level1.attrib['datacollecttime'])
                vsrdir.append(level2.attrib['vsrdir'])
                vsrid.append(level2.attrib['vsrid'])
                speed.append(level2.attrib['speed'])
                laneoccupy.append(level2.attrib['laneoccupy'])
                carid.append(level3.attrib['carid'])
                volume.append(level3.attrib['volume'])

    data = list(zip(vdid,status,datacollecttime,vsrdir,vsrid,speed,laneoccupy,carid,volume))
    data_df =  pd.DataFrame(data,columns=['vdid','status','datacollecttime','vsrdir','vsrid','speed','laneoccupy','carid','volume'])
    return data_df


# In[5]:


def get_dataframe(file_list):
    final_df = pd.DataFrame(columns=['vdid','status','datacollecttime','vsrdir','vsrid','speed','laneoccupy','carid','volume'])
    driver = webdriver.Chrome(executable_path=driverpath,chrome_options=chrome_options)
    #final_df = pd.DataFrame(columns=['vdid','status','datacollecttime','vsrdir','vsrid','speed','laneoccupy','carid','volume'])
    for f in file_list:
        try:
            os.remove(downloadpath+f)
        except:
            pass
        f = f.replace(' ','')
        url2 = url+'/'+f
        driver.get(url2)
        time.sleep(40)
        try:
            df = read_xml(f)
        except:
            try:
                time.sleep(30)
                df = read_xml(f)
            except:
                with open(destFile, 'a') as file:
                    file.write(f+' is error \n')
                print(f,'is error')
                continue
        final_df = pd.concat([final_df,df],0)
        os.remove(downloadpath+f)

    driver.close()
    return final_df

# In[6]:


# file_1m = []
# file_5m = []


# In[7]:


for i in range(0, len(date_list)): 
    date_list[i] = int(date_list[i])

date_list.sort()

date_list2 = list(filter(lambda x: x>=20190101 and x<=20190131, date_list))

for i in range(0, len(date_list2)): 
    date_list2[i] = str(date_list2[i])


# In[8]:


#len(date_list2)


# In[9]:


# date_list_lv1 = date_list2[:194]
# date_list_lv2 = date_list2[194:388]
# date_list_lv3 = date_list2[388:581]
# date_list_lv4 = date_list2[581:775]
# date_list_lv5 = date_list2[775:]








# In[ ]:


# In[11]:

for date in date_list2:
    driver = webdriver.Chrome(executable_path=driverpath,chrome_options=chrome_options)
    file_list = []
    try:
        url='https://tisvcloud.freeway.gov.tw/history/vd/'+date
        driver.get(url)
    except:
        continue
    
    with open(destFile, 'a') as f:
        f.write("-------------------------\n")
        f.write(date+"\n")
        
    print('-------------------------')
    print(date)
    soup=BeautifulSoup(driver.page_source,"html.parser")
    table = soup.find_all("tbody")
    name = table[0].find_all('a',target="_blank")
    for i in range(len(name)-1): 
        file = driver.find_element_by_xpath('//*[@id="form1"]/div[3]/div/section[2]/table/tbody/tr['+str(i+2)+']/td[1]/a').text
        if len(file)== 21:
            #file_5m.append(date+'/'+file)
            file_list.append(file)
        else:
            #file_1m.append(date+'/'+file)
            pass
        
    if len(file_list) != 288:
        with open(destFile, 'a') as f:
            f.write(date+"無288筆資料 \n")
        print(date+'無288筆資料')
    else:
        pass
    driver.close()
    
    urls = np.array_split(np.array(file_list),10)
    pool = ThreadPool(10)
    all_pool = pool.map(get_dataframe, urls)
    pool.close()
    pool.join()

    final_df = all_pool.reset_index(drop=True)
    final_df['datacollecttime'] = pd.to_datetime(final_df['datacollecttime'], format='%Y-%m-%d %H:%M:%S')
    final_df.to_csv('../data_all/data_april/etc_'+date+'.csv', encoding='utf-8',index=False)


# In[ ]:


# In[ ]:




