import pandas as pd
import numpy as np
from alpha_vantage.timeseries import TimeSeries
import time
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', None)
api_key= 'K83K1D6UT8N973SA'
stock_symbol = input("Enter stock shortcut:")
stock_symbol.upper()

ts= TimeSeries(key=api_key,output_format='pandas')
data_ts,meta_data_ts= ts.get_intraday(symbol= stock_symbol, interval='1min',outputsize= 'full')

#60 means an hour
period=60
ti= TechIndicators(key=api_key, output_format='pandas')
data_ti,meta_data_ti= ti.get_sma(symbol=stock_symbol, interval='1min', time_period=period, series_type='close')


data_frame1=data_ti
#as we cant have the simple moving average of first interval
data_frame2= data_ts['4. close'].iloc[period-1::]

data_frame2.index= data_frame1.index

total_data_frame = pd.concat([data_frame1,data_frame2],axis =1)


total_data_frame.loc[total_data_frame['SMA']+1<total_data_frame['4. close'], 'Signal']=1.0
total_data_frame.loc[total_data_frame['SMA']>total_data_frame['4. close']+1, 'Signal']=0.0
total_data_frame.loc[(total_data_frame['SMA']+1>total_data_frame['4. close']) & (total_data_frame['SMA']<total_data_frame['4. close']+1), 'Signal']=np.nan
total_data_frame['position']= total_data_frame['Signal'].diff()

#option_data_frame['position']=option_data_frame['Option'].diff()

print(total_data_frame)
#total_data_frame.plot()

#plt.title( stock_symbol + " simple moving average")
#plt.show()
