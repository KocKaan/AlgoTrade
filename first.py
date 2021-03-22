import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time

api_key= 'K83K1D6UT8N973SA'

ts= TimeSeries(key=api_key,output_format='pandas')
data,meta_data= ts.get_intraday(symbol='MSFT', interval='1min',outputsize= 'full')
print(data)

i=1

while i==1:
    data,meta_data= ts.get_intraday(symbol='MSFT', interval='1min',outputsize= 'full')
    data.to_excel("output.xlsx")
    time.sleep(60)
