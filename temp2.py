# -*- coding:utf-8 -*-
import cv2 as cv
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import dload
from googletrans import Translator
import os
import csv

HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"} # User Agent를 지정해줍니다

one_link = "https://weather.com/weather/tenday/l/5996d79cd18699103ac958cfd7f51ef5c26ecc4224f22fc6d4ea4bec1ae9a80d"

res2 = requests.get(one_link,headers=HEADERS)   # 링크에 접속합니다 
res2.raise_for_status()  # 에러 체크
soup = BeautifulSoup(res2.text, 'html.parser')
main_content = soup.find('main',attrs={'id':'MainContent'}).find('div',attrs={'class':'DaybreakLargeScreen--gridWrapper--3sleb'}).find('main',attrs={'class':"region-main regionMain DaybreakLargeScreen--regionMain--1FzNI"})
in_cont = main_content.find('div',attrs={'id':'WxuDailyCard-main-a43097e1-49d7-4df7-9d1a-334b29628263'}).find('div',attrs={'class','Card--content--1GQMr DailyForecast--CardContent--2YlvT'}).find('div',attrs={'class','DailyForecast--DisclosureList--nosQS'})
columns = in_cont.find_all('details')
dates = []
percs = []
temps_1 = []
temps_2 = []
for ind,i in enumerate(columns):
    summary = i.find('summary').find('div',attrs={'class':'DetailsSummary--DetailsSummary--1DqhO DetailsSummary--fadeOnOpen--KnNyF'})
    date = summary.find('h3').get_text()
    dates.append(date)
    perc = summary.find('div',attrs={'data-testid':'Precip'}).find('span').get_text()
    percs.append(perc)
    temp_1 = summary.find('div',attrs={'data-testid':'detailsTemperature'}).find('span').get_text() # 디그리로 바꾸기 (온도단위)
    temps_1.append(temp_1) 
    temp_2 = summary.find('div',attrs={'data-testid':'detailsTemperature'}).find('span',attrs={'data-testid':'lowTempValue'}).find('span').get_text()
    temps_2.append(temp_2)
    
r = zip(dates,percs,temps_1,temps_2)
header = ['Date','PSR','Day_Temp','Night_Temp']
with open('PSR_Temp.csv', 'w+', newline ='',encoding='UTF-8') as file:
    w = csv.writer(file)
    dw = csv.DictWriter(file,delimiter=',',fieldnames=header)
    dw.writeheader()
    for row in r:
        w.writerow(row)