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


ti= TechIndicators(key=api_key, output_format='pandas')
#60 means hour
data_ti_short,meta_data_ts_short= ti.get_sma(symbol=stock_symbol, interval='1min', time_period=60, series_type='close')
data_ti_long,meta_data_ts_long= ti.get_sma(symbol=stock_symbol, interval='1min', time_period=120, series_type='close')

#change the column name
data_ti_short.rename(columns={'SMA': 'SMA 60min'}, inplace=True)
data_ti_long.rename(columns={'SMA': 'SMA 120min'}, inplace=True)

total_data_frame = pd.concat([data_ti_short,data_ti_long],axis =1)
#adds the closing price of the stocks.
total_data_frame['close']=data_ts['4. close']
#starting from 120th row becasue sma120 wouldnt work.
total_data_frame= total_data_frame.iloc[120:]

#1 if SMA 60 is more than SMA 120 otherwise 0
total_data_frame['signal'] = np.where(total_data_frame['SMA 60min']
                                   > total_data_frame['SMA 120min'], 1.0, 0.0)

#writes the difference meaning sognaling when there is a buy or sell situation
total_data_frame['position'] = total_data_frame['signal'].diff()

# Initialize the plot figure
fig = plt.figure()

# Add a subplot and label for y-axis
ax1 = fig.add_subplot(111,  ylabel='Price in $')

# Plot the short and long moving averages
total_data_frame[['SMA 60min', 'SMA 120min','close']].plot(ax=ax1, lw=2.)


# Plot the buy signals
print(total_data_frame.loc[total_data_frame.position == 1.0].index,
         total_data_frame['SMA 60min'][total_data_frame.position== 1.0])

# Plot the sell signals
#ax1.plot(signals.loc[signals.positions == -1.0].index,signals.short_mavg[signals.positions == -1.0],
#         'v', markersize=10, color='k')
plt.show()

#print(total_data_frame.head(200))
