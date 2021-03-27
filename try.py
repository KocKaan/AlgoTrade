import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt

api_key= 'K83K1D6UT8N973SA'


ts= TimeSeries(key=api_key,output_format='pandas')
data_ts,meta_data_ts= ts.get_intraday(symbol= 'AAPL', interval='1min',outputsize= 'full')

#60 means an hour
period=60
ti= TechIndicators(key=api_key, output_format='pandas')
data_ti,meta_data_ti= ti.get_sma(symbol='AAPL', interval='1min', time_period=period, series_type='close')

data_ts[1:1,['close']]=50
print(data_ts.head)

print(data_ti.tail(3))
