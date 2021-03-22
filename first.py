import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt

api_key= 'K83K1D6UT8N973SA'

ts= TimeSeries(key=api_key,output_format='pandas')
data_ts,meta_data_ts= ts.get_intraday(symbol='MSFT', interval='1min',outputsize= 'full')

#60 means an hour
period=60
ti= TechIndicators(key=api_key, output_format='pandas')
data_ti,meta_data_ti= ti.get_sma(symbol='MSFT', interval='1min', time_period=period, series_type='close')


data_frame1=data_ti
#as we cant have the simple moving average of first interval
data_frame2= data_ts['4. close'].iloc[period-1::]

data_frame2.index= data_frame1.index

total_data_frame = pd.concat([data_frame1,data_frame2],axis =1)
print(total_data_frame)

total_data_frame.plot()
plt.show()
