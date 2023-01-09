# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 15:22:40 2023

@author: WEIJUN
"""

import time
from datetime import datetime
import requests
import json
import pandas as pd

# 取得今天日期 
ts = time.time()
dt = datetime.fromtimestamp(ts).strftime("%m%d")
# print(dt)

# 發送請求，並解析氣象局API
url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001'
params = {'Authorization':'CWB-C30B0FE2-8DB4-430D-9FCC-7921B72ADA6C'}
web = requests.get(url, params=params)
# print(web.status_code)

tmr = {"城市":[],
       "日期":[],
       "白天天氣現象":[],
       "白天降雨機率":[],
       "白天最低溫度":[],
       "白天舒適度":[],
       "白天最高溫度":[],
       "晚上天氣現象":[],
       "晚上降雨機率":[],
       "晚上最低溫度":[],
       "晚上舒適度":[],
       "晚上最高溫度":[]}

if web.status_code == 200 :
    data = json.loads(web.text)
    # print(data)
    loc = data["records"]["location"]
    for i in loc:
        city = i["locationName"] # 城市
        date = i["weatherElement"][0]["time"][1]["startTime"] # 日期
        d_wx = i["weatherElement"][0]["time"][1]["parameter"]["parameterName"] # 白天天氣現象
        d_pop = i["weatherElement"][1]["time"][1]["parameter"]["parameterName"] # 白天降雨機率
        d_minT = i["weatherElement"][2]["time"][1]["parameter"]["parameterName"] # 白天最低溫度
        d_ci = i["weatherElement"][3]["time"][1]["parameter"]["parameterName"] # 白天舒適度
        d_maxT = i["weatherElement"][4]["time"][1]["parameter"]["parameterName"] # 白天最高溫度
        n_wx = i["weatherElement"][0]["time"][2]["parameter"]["parameterName"] # 晚上天氣現象
        n_pop = i["weatherElement"][1]["time"][2]["parameter"]["parameterName"] # 晚上降雨機率
        n_minT = i["weatherElement"][2]["time"][2]["parameter"]["parameterName"] # 晚上最低溫度
        n_ci = i["weatherElement"][3]["time"][2]["parameter"]["parameterName"] # 晚上舒適度
        n_maxT = i["weatherElement"][4]["time"][2]["parameter"]["parameterName"] # 晚上最高溫度
        tmr["城市"].append(city)
        tmr["日期"].append(date.split(' ')[0])
        tmr["白天天氣現象"].append(d_wx)
        tmr["白天降雨機率"].append(d_pop)
        tmr["白天最低溫度"].append(d_minT)
        tmr["白天舒適度"].append(d_ci)
        tmr["白天最高溫度"].append(d_maxT)
        tmr["晚上天氣現象"].append(n_wx)
        tmr["晚上降雨機率"].append(n_pop)
        tmr["晚上最低溫度"].append(n_minT)
        tmr["晚上舒適度"].append(n_ci)
        tmr["晚上最高溫度"].append(n_maxT)

df = pd.DataFrame(tmr)
df.to_csv(dt+"weather.csv",encoding="utf-8",index=False)

# -----------------------------
# 設定notify
def notify(message, token):
    url = "https://notify-api.line.me/api/notify" # Notify網址
    headers = {"Authorization":"Bearer " + token} # https表頭
    payload = {"message":message, # https內容
               "stickerPackageId" : 8525, # 該組貼圖編號
               "stickerId" : 16581294} # 指定貼圖編號
    requests.post(url, headers = headers,
                  params = payload) # 提出post請求
    
# 發送訊息
token = "tRSiYCZpWIOnZkAltHHIeH4lGLk7iMI771XG8DCr2OO" # 景家群組
#"QhvfrfVnF4YWSgSX35Fs1UDbzaf7gQOqlzTTZjIeaxy" # 個人
message = "\n安安，明天(%s)的白天天氣為%s\n溫度：%s~%s\n降雨機率：%s \n感覺為%s" %(tmr["日期"][1],tmr["白天天氣現象"][1],tmr["白天最低溫度"][1],tmr["白天最高溫度"][1],tmr["白天降雨機率"][1],tmr["白天舒適度"][1])
notify(message, token)