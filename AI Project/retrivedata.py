
#Import the Yahoo finance to get the stock data
import yfinance as yf

#Import the plotting library
import matplotlib.pyplot as plt

import pandas as pd
import csv
import numpy as np

#Ticker is used for the series of stocks that we are intrested in
stocks = ['MSFT', 'AAPl' , 'TSLA' , 'FB' , 'AMZN' , 'NVDA' , 'AMD' , 'MA', 'PYPL' , 'GOOG' , 'V' , 'CRM' , 'NFLX']

#Get the data of the stocks
df = yf.download(stocks, start = '2019-01-01', end = '2020-12-01')

#Ordered the stocks alphabetically and saved them in a csv file
df.stack().reset_index().rename(index=str, columns={"level_1": "Symbol"}).sort_values(['Symbol','Date'])
df.to_csv('Stocks1.csv')

#Plot the close price
df.Close.plot()
plt.show()

