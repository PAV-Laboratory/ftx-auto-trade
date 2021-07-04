# ---------------------------------------------------------------------------------------- #

import requests
import pandas as pd
import datetime
from datetime import timezone
import numpy as np

#import plotly.graph_objects as go

# ---------------------------------------------------------------------------------------- #

# 顯示所有欄位
pd.set_option('display.max_column', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_seq_items', None)
pd.set_option('display.max_colwidth', 1000)
pd.set_option('expand_frame_repr', False)

# ---------------------------------------------------------------------------------------- #

# 定義K棒時間
resolution_1M = 60
resolution_15M = 900
resolution_1H = 3600
resolution_4H = 14400
resolution_1D = 86400

# ---------------------------------------------------------------------------------------- #

# Datetime轉Unix
def start_dt_to_unix(y,m,d):
    start_dt = datetime.datetime(y, m, d)
    start_unix_ts = int(start_dt.timestamp())
    return(start_unix_ts)

def end_dt_to_unix(y,m,d):
    end_dt = datetime.datetime(y, m, d)
    end_unix_ts = int(end_dt.timestamp())
    return(end_unix_ts)

# ---------------------------------------------------------------------------------------- #

def get_ftx_historial_market(symbol, kline, start_time, end_time):
    
    market_url = 'https://ftx.com/api/markets/{}/candles?resolution={}&start_time={}&end_time={}'.format(symbol, kline, start_time, end_time) # 設定URL
    
    try: # 除錯
        request_data = requests.get(market_url, timeout = 15) # 對API要求資訊

    except Exception as e:

        print('ERROR', e)

        return None
    
    historical_data = None

    if request_data.status_code == 200: # 除錯

        request_data_json = request_data.json() # 資訊轉成JSON

        if 'error' in request_data_json: # 除錯
            print ("ERROR MESSAGE:{}".format(request_data_json['error']))

        else: # 沒出現錯誤繼續程序

            historical_data = pd.DataFrame(request_data_json['result']) # 從API裡面拿出叫做'result'裡面的資料

            historical_data['time'] = pd.to_datetime(historical_data['time'], unit='ms') # 校正UNIX顯示時間   

            historical_data.drop(['startTime'], axis = 1, inplace=True) # 把開始時間拿掉

            historical_data['volume'] = historical_data['volume'].apply(lambda x: '{:.5f}'.format(x)) # 完整顯示volume float

            historical_data.set_index('time', inplace=True) # 把time當索引

            historical_data.insert(5,'market',symbol)

            # historical_data.head(5) # 顯示最一開始的幾筆資料

            # historical_data.tail(5) # 顯示最後的幾筆資料
    else:
        print ("ERROR MESSAGE:{}".format(request_data.status_code))
    
    return historical_data

# ---------------------------------------------------------------------------------------- #

def main():

    symbol = "BTC/USD"
    kline = resolution_15M
    start_time = start_dt_to_unix(2021,7,4)
    end_time = end_dt_to_unix(2021,7,5)

    historical_data = get_ftx_historial_market(symbol, kline, start_time, end_time)

    print(historical_data)

    historical_data.to_csv('./history/test.csv', index = False)

# ---------------------------------------------------------------------------------------- #

main()