# 엑셀 파일 데이터 수식화
# 강수량 0~25, 26~50, 51~75, 76~100 / 변동 상수 페이퍼 참고
# 강수량으로 인한 변동성 변수: Occupancy(0~1)/ {여유로움, 다소 혼잡함, 혼잡함}
### 시간대로 인한 차량 점유율 관계

import pandas as pd
from datetime import datetime 
from datetime import timedelta
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

nw = datetime.now()
hrs = nw.hour
mins = nw.minute 
secs = nw.second 
zero = timedelta(seconds = secs+mins*60+hrs*3600)
st = nw - zero
time1 = st + timedelta(seconds=9*3600) # 9시
time2 = st + timedelta(seconds=18*3600) #18시

# 변수 선언
PSR_cof = 0.073
Temp_cof = -0.00728
Temp_avg = 22

# indexing
###  
index_1 = ['QC','MC']
index_2 = ['PD']
index_23= ['Occ','CS']
index_3 = ['35min','1h','2h','=2h','3h','4h','8h','=8h']

index = [('QC','Occ'), ('QC', 'PD', '>35min'), ('QC', 'PD','>1h'), ('QC', 'PD','>2h'), ('QC', 'PD','>=2h'), ('QC','CS'), \
         ('MC','Occ'), ('MC','PD','>1h'), ('MC','PD','>2h'), ('MC','PD','>3h'), ('MC','PD','>4h'), ('MC','PD','>8h'), ('MC','PD','>=8h'), ('MC','CS')]
# Data 
###
data = {'NDO':[0.2, 0.7, 0.9, 0.95, 1, 0.1, 0.9, 0.1 ,0.15, 0.2, 0.25, 0.9, 1, 0.3], \
        'NDN':[0.6, 0.75, 0.95, 1, 1, 0.3, 0.4, 0.1, 0.4, 0.9, 1, 1, 1, 0.3], \
        'NE':[0.9, 0.85, 0.95, 1, 1, 0.6, 0.7, 0.1, 0.4, 0.9, 1, 1, 1, 0.4], \
        'Rday':[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}

df = pd.DataFrame(data, index = index)
df_c = df.columns

psr = pd.read_csv('PSR_Temp.csv')

# change Null data

if psr['Day_Temp'][0] == '--':
     psr['Day_Temp'][0] = psr['Day_Temp'][1] 

psr['Day_Temp'] = psr['Day_Temp'].str[:-1]
psr['Night_Temp'] = psr['Night_Temp'].str[:-1] # change to int 
psr['PSR'] = psr['PSR'].str[:-1]
psr['Day_Temp'] = psr['Day_Temp'].apply(int)
psr['Night_Temp'] = psr['Night_Temp'].apply(int)
psr['PSR'] = psr['PSR'].apply(int)

psr['Day_CT'] = round((psr['Day_Temp'] - 32) * (5/9), 1)
psr['Night_CT'] = round((psr['Night_Temp'] - 32) * (5/9) ,1)
psr['PSR'] = psr['PSR']/100

if 'Sun' or 'Mon' in psr['Date'][1]:
    df['Rday'] = df['NE']
elif nw > time1 and nw < time2:
    df['Rday'] = df['NDO']
else:
    df['Rday'] = df['NDN']

# add coefficient 
### 낮 온도, 밤 온도, 주말 평균 온도
### 날자 주중인지 주말인지 확인 
### 강수량은 날자 매칭만시켜서 선 온도 후 강수량 

if 'Sun' or 'Mon' in psr['Date'][1]:
    temp = (psr['Day_CT'][0] + psr['Night_CT'][0])/2
elif nw > time1 and nw < time2:
    temp = psr['Day_CT'][0]
else:
    temp = psr['Night_CT'][0]

rain = psr['PSR'][0]

# output
# 혼잡도 어떻게 출력할지 생각하기 (퍼센테이지)

df.iloc[0:6,3] = df.iloc[0:6,3] * (1 - (Temp_cof * (Temp_avg - temp))) #QC
df.iloc[0:6,3] = round(df.iloc[0:6,3] * (1 - (PSR_cof * rain)),2)

df.iloc[6:14,3] = df.iloc[6:14,3] * (1 - (Temp_cof * (Temp_avg - temp))) #MC
df.iloc[6:14,3] = round(df.iloc[6:14,3] * (1 - (PSR_cof * rain)),2)

df[df > 1] = 1


QC_Occ = (df.iloc[0,3] * 100).astype(int)
MC_Occ = (df.iloc[6,3] * 100).astype(int)
PP = (rain * 100).astype(int)

print(df)
print(df_c)
print(psr.head())

print('Current Quick Charger\'s Occupancy is {}%'.format(QC_Occ))
print('Current Medium Charger\'s Occupancy is {}%'.format(MC_Occ))
print('Current Tempreature is {}°C, and Precipitation probability is {}%'.format(temp,PP))

QC = df.iloc[1:5,0:4]
QC.plot()
MC = df.iloc[8:13,0:4]
MC.plot()
plt.show()

#index label
#index_name = df.index.name
#df.index.name = ['Type', 'Data', 'Data']
