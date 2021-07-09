from nsepy import get_history
from datetime import date
import os
import pandas as pd
import streamlit as st
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator,DayLocator, MONDAY
#from matplotlib import quotes_historical_yahoo_ohlc, candlestick_ohlc
from mpl_finance import candlestick_ohlc
import mplfinance as mpf
from matplotlib import gridspec
import numpy as np
import matplotlib.ticker as ticker
import yfinance as yf 
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import SessionState


os.chdir('/home/rohit/Documents/Python/Project_stocks')

stock_names=pd.read_csv('Equity.csv')
stock_names=stock_names.reset_index()
filtered_stock = st.sidebar.selectbox("Select stock", stock_names["Security Id"].unique())
stock=stock_names['Issuer Name'].loc[(stock_names["Security Id"] == filtered_stock)]
stock=stock.to_string(index=False)
stock=stock.strip()

#start=st.sidebar.date_input('Start Date')
#end=st.sidebar.date_input('End Date')

#start=pd.Timestamp('2021-01-01')
#end=pd.Timestamp('2021-05-21')

mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
alldays = DayLocator()
months = mdates.MonthLocator()
years = mdates.YearLocator()
yearFormatter=   DateFormatter('%Y')        # minor ticks on the days
weekFormatter = DateFormatter('%b %Y')  # e.g., Jan 12
dayFormatter = DateFormatter('%d-%b-%Y')      # e.g., 12
#df = get_history(symbol=stock, start=start, end=end)
stock_name = yf.Ticker(stock+'.NS')
#msft.info
df = stock_name.history(period='max')

df["Date"] = pd.to_datetime(df.index)
df.Date = mdates.date2num(df.Date.dt.to_pydatetime())
df.index = pd.DatetimeIndex(df['Date'])
mav=st.sidebar.number_input('Enter Moving average number')
mav=int(mav)
#mav=8
df=df[df['Close']!=0]
df["MA"]=df["Close"].rolling(mav).mean()   #days
vma=50
df["VMA"]=df["Volume"].rolling(vma).mean()
#l=len(df)
#df3=df2.iloc[-94:,:]

period=st.sidebar.select_slider('Slide to select', options=['5d','1mo','3mo','6mo','1y','2y','5y','10y','max'])

if (period=='5d'):
    df=df.iloc[-5:,:]
    
    quotes = [tuple(x) for x in df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].to_records(index=False)]
    if len(quotes) == 0:
        st.error('Check dates')
        st.stop()

    ticks = np.linspace(min(df['Volume']), max(df['Volume']), 5 )
    
    fig = plt.figure(figsize=(12,10))
    # set height ratios for subplots
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1]) 
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1], sharex = ax1)
    
    #fig.subplots_adjust(bottom=0.2)
    #mpf.plot(df,type='candle',mav=9,volume=True)
    ax1.xaxis.set_major_locator(mondays)
    ax1.xaxis.set_minor_locator(alldays)
    # ax1.xaxis.set_minor_formatter(dayFormatter)
    # ax1.xaxis.set_major_formatter(dayFormatter)
    ax1.xaxis.set_major_locator(MultipleLocator(1))
    ax1.xaxis.set_major_formatter(dayFormatter)
    #plot_day_summary(ax, quotes, ticksize=3)
    candlestick_ohlc(ax1, quotes, width=0.6)
    ax1.plot(df['Date'],df["MA"],linewidth=0.4,color='g')
    ax1.xaxis_date()
    ax1.autoscale_view()
    ax1.set_ylabel('Price', fontweight='bold')
    ax1.set_title(stock, fontweight='bold')
    plt.xticks(rotation=45)
    #plt.ylabel('Price', fontweight='bold')
    #plt.title(stock,fontweight="bold")
    ax1.xaxis.set_tick_params(labelsize=1)
    ax1.yaxis.set_tick_params(labelsize=10)
    yticks = ax1.yaxis.get_major_ticks()
    yticks[-1].label1.set_visible(False)
    
    #ax2 = ax.twinx()
    ax2.bar(df['Date'],df['Volume'])
    ax2.plot(df['Date'],df["VMA"],linewidth=0.4,color='g')
    ax2.set_ylabel('Volume', fontweight='bold')
    ax2.set_yticks(ticks)
    ax2.xaxis.set_tick_params(labelsize=6)
    ax2.yaxis.set_tick_params(labelsize=6)
    yticks = ax2.yaxis.get_major_ticks()
    yticks[-1].label1.set_visible(False)
    
    plt.subplots_adjust(hspace=.0)
    ax1.grid(color = 'green', linestyle = '--', linewidth = 0.2)
    ax2.grid(color = 'green', linestyle = '--', linewidth = 0.2)
    #plt.show()
    st.pyplot(fig)
    
elif (period=='1mo'):
    df=df.iloc[-30:,:]
    
    quotes = [tuple(x) for x in df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].to_records(index=False)]
    if len(quotes) == 0:
        st.error('Check dates')
        st.stop()

    ticks = np.linspace(min(df['Volume']), max(df['Volume']), 5 )
    
    fig = plt.figure(figsize=(12,10))
    # set height ratios for subplots
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1]) 
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1], sharex = ax1)
    
    #fig.subplots_adjust(bottom=0.2)
    #mpf.plot(df,type='candle',mav=9,volume=True)
    ax1.xaxis.set_major_locator(mondays)
    #ax1.xaxis.set_minor_locator(mondays)
    # ax1.xaxis.set_major_formatter(dayFormatter)
    ax1.xaxis.set_major_formatter(dayFormatter)
    #ax1.xaxis.set_minor_formatter(dayFormatter)
    #plot_day_summary(ax, quotes, ticksize=3)
    candlestick_ohlc(ax1, quotes, width=0.6)
    ax1.plot(df['Date'],df["MA"],linewidth=0.4,color='g')
    ax1.xaxis_date()
    #ax1.autoscale_view()
    ax1.set_ylabel('Price', fontweight='bold')
    ax1.set_title(stock, fontweight='bold')
    #plt.xticks(rotation=45)
    #plt.ylabel('Price', fontweight='bold')
    #plt.title(stock,fontweight="bold")
    #ax1.xaxis.set_tick_params(labelsize=1)
    #ax2.xaxis.set_tick_params(labelsize=1)
    ax1.yaxis.set_tick_params(labelsize=10)
    yticks = ax1.yaxis.get_major_ticks()
    yticks[-1].label1.set_visible(False)
    
    #ax2 = ax.twinx()
    ax2.bar(df['Date'],df['Volume'])
    ax2.plot(df['Date'],df["VMA"],linewidth=0.4,color='g')
    ax2.set_ylabel('Volume', fontweight='bold')
    ax2.set_yticks(ticks)
    ax2.xaxis.set_tick_params(labelsize=6)
    ax2.yaxis.set_tick_params(labelsize=6)
    yticks = ax2.yaxis.get_major_ticks()
    yticks[-1].label1.set_visible(False)
    ax1.tick_params(axis="x", which="both", rotation=45,labelsize=6,direction='out')
    ax2.tick_params(axis="x", which="both", rotation=45,labelsize=6,direction='out')
    plt.subplots_adjust(hspace=.0)
    ax1.grid(color = 'green', linestyle = '--', linewidth = 0.2)
    ax2.grid(color = 'green', linestyle = '--', linewidth = 0.2)
    plt.show()
    st.pyplot(fig)
    
elif (period=='3mo'):
    df=df.iloc[-90:,:]
    
    quotes = [tuple(x) for x in df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].to_records(index=False)]
    if len(quotes) == 0:
        st.error('Check dates')
        st.stop()

    ticks = np.linspace(min(df['Volume']), max(df['Volume']), 5 )
    
    fig = plt.figure(figsize=(12,10))
    # set height ratios for subplots
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1]) 
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1], sharex = ax1)
    
    #fig.subplots_adjust(bottom=0.2)
    #mpf.plot(df,type='candle',mav=9,volume=True)
    ax1.xaxis.set_major_locator(mondays)
    #ax1.xaxis.set_minor_locator(mondays)
    # ax1.xaxis.set_major_formatter(dayFormatter)
    ax1.xaxis.set_major_formatter(dayFormatter)
    #ax1.xaxis.set_minor_formatter(dayFormatter)
    #plot_day_summary(ax, quotes, ticksize=3)
    candlestick_ohlc(ax1, quotes, width=0.6)
    ax1.plot(df['Date'],df["MA"],linewidth=0.4,color='g')
    ax1.xaxis_date()
    #ax1.autoscale_view()
    ax1.set_ylabel('Price', fontweight='bold')
    ax1.set_title(stock, fontweight='bold')
    #plt.xticks(rotation=45)
    #plt.ylabel('Price', fontweight='bold')
    #plt.title(stock,fontweight="bold")
    #ax1.xaxis.set_tick_params(labelsize=1)
    #ax2.xaxis.set_tick_params(labelsize=1)
    ax1.yaxis.set_tick_params(labelsize=10)
    yticks = ax1.yaxis.get_major_ticks()
    yticks[-1].label1.set_visible(False)
    
    #ax2 = ax.twinx()
    ax2.bar(df['Date'],df['Volume'])
    ax2.plot(df['Date'],df["VMA"],linewidth=0.4,color='g')
    ax2.set_ylabel('Volume', fontweight='bold')
    ax2.set_yticks(ticks)
    ax2.xaxis.set_tick_params(labelsize=6)
    ax2.yaxis.set_tick_params(labelsize=6)
    yticks = ax2.yaxis.get_major_ticks()
    yticks[-1].label1.set_visible(False)
    ax1.tick_params(axis="x", which="both", rotation=45,labelsize=6,direction='out')
    ax2.tick_params(axis="x", which="both", rotation=45,labelsize=6,direction='out')
    plt.subplots_adjust(hspace=.0)
    ax1.grid(color = 'green', linestyle = '--', linewidth = 0.2)
    ax2.grid(color = 'green', linestyle = '--', linewidth = 0.2)
    #plt.show()
    st.pyplot(fig)
elif (period=='6mo'):
    df=df.iloc[-180:,:]
    
    quotes = [tuple(x) for x in df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].to_records(index=False)]
    if len(quotes) == 0:
        st.error('Check dates')
        st.stop()

    ticks = np.linspace(min(df['Volume']), max(df['Volume']), 5 )
    
    fig = plt.figure(figsize=(12,10))
    # set height ratios for subplots
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1]) 
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1], sharex = ax1)
    
    #fig.subplots_adjust(bottom=0.2)
    #mpf.plot(df,type='candle',mav=9,volume=True)
    ax1.xaxis.set_major_locator(months)
    #ax1.xaxis.set_minor_locator(mondays)
    # ax1.xaxis.set_major_formatter(dayFormatter)
    ax1.xaxis.set_major_formatter(dayFormatter)
    #ax1.xaxis.set_minor_formatter(dayFormatter)
    #plot_day_summary(ax, quotes, ticksize=3)
    candlestick_ohlc(ax1, quotes, width=0.6)
    ax1.plot(df['Date'],df["MA"],linewidth=0.4,color='g')
    ax1.xaxis_date()
    #ax1.autoscale_view()
    ax1.set_ylabel('Price', fontweight='bold')
    ax1.set_title(stock, fontweight='bold')
    #plt.xticks(rotation=45)
    #plt.ylabel('Price', fontweight='bold')
    #plt.title(stock,fontweight="bold")
    #ax1.xaxis.set_tick_params(labelsize=1)
    #ax2.xaxis.set_tick_params(labelsize=1)
    ax1.yaxis.set_tick_params(labelsize=10)
    yticks = ax1.yaxis.get_major_ticks()
    yticks[-1].label1.set_visible(False)
    
    #ax2 = ax.twinx()
    ax2.bar(df['Date'],df['Volume'])
    ax2.plot(df['Date'],df["VMA"],linewidth=0.4,color='g')
    ax2.set_ylabel('Volume', fontweight='bold')
    ax2.set_yticks(ticks)
    ax2.xaxis.set_tick_params(labelsize=6)
    ax2.yaxis.set_tick_params(labelsize=6)
    yticks = ax2.yaxis.get_major_ticks()
    yticks[-1].label1.set_visible(False)
    ax1.tick_params(axis="x", which="both", rotation=45,labelsize=6,direction='out')
    ax2.tick_params(axis="x", which="both", rotation=45,labelsize=6,direction='out')
    plt.subplots_adjust(hspace=.0)
    ax1.grid(color = 'green', linestyle = '--', linewidth = 0.2)
    ax2.grid(color = 'green', linestyle = '--', linewidth = 0.2)
    #plt.show()
    st.pyplot(fig)
elif (period=='1y'):
    df=df.iloc[-253:,:]
    
    quotes = [tuple(x) for x in df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].to_records(index=False)]
    if len(quotes) == 0:
        st.error('Check dates')
        st.stop()

    ticks = np.linspace(min(df['Volume']), max(df['Volume']), 5 )
    
    fig = plt.figure(figsize=(12,10))
    # set height ratios for subplots
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1]) 
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1], sharex = ax1)
    
    #fig.subplots_adjust(bottom=0.2)
    #mpf.plot(df,type='candle',mav=9,volume=True)
    ax1.xaxis.set_major_locator(months)
    #ax1.xaxis.set_minor_locator(mondays)
    # ax1.xaxis.set_major_formatter(dayFormatter)
    ax1.xaxis.set_major_formatter(dayFormatter)
    #ax1.xaxis.set_minor_formatter(dayFormatter)
    #plot_day_summary(ax, quotes, ticksize=3)
    candlestick_ohlc(ax1, quotes, width=0.6)
    ax1.plot(df['Date'],df["MA"],linewidth=0.4,color='g')
    ax1.xaxis_date()
    #ax1.autoscale_view()
    ax1.set_ylabel('Price', fontweight='bold')
    ax1.set_title(stock, fontweight='bold')
    #plt.xticks(rotation=45)
    #plt.ylabel('Price', fontweight='bold')
    #plt.title(stock,fontweight="bold")
    #ax1.xaxis.set_tick_params(labelsize=1)
    #ax2.xaxis.set_tick_params(labelsize=1)
    ax1.yaxis.set_tick_params(labelsize=10)
    yticks = ax1.yaxis.get_major_ticks()
    yticks[-1].label1.set_visible(False)
    
    #ax2 = ax.twinx()
    ax2.bar(df['Date'],df['Volume'])
    ax2.plot(df['Date'],df["VMA"],linewidth=0.4,color='g')
    ax2.set_ylabel('Volume', fontweight='bold')
    ax2.set_yticks(ticks)
    ax2.xaxis.set_tick_params(labelsize=6)
    ax2.yaxis.set_tick_params(labelsize=6)
    yticks = ax2.yaxis.get_major_ticks()
    yticks[-1].label1.set_visible(False)
    ax1.tick_params(axis="x", which="both", rotation=45,labelsize=6,direction='out')
    ax2.tick_params(axis="x", which="both", rotation=45,labelsize=6,direction='out')
    plt.subplots_adjust(hspace=.0)
    ax1.grid(color = 'green', linestyle = '--', linewidth = 0.2)
    ax2.grid(color = 'green', linestyle = '--', linewidth = 0.2)
    #plt.show()
    st.pyplot(fig)
elif (period=='2y'):
    df=df.iloc[-506:,:]
    
    quotes = [tuple(x) for x in df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].to_records(index=False)]
    if len(quotes) == 0:
        st.error('Check dates')
        st.stop()

    ticks = np.linspace(min(df['Volume']), max(df['Volume']), 5 )
    
    fig = plt.figure(figsize=(12,10))
    # set height ratios for subplots
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1]) 
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1], sharex = ax1)
    
    #fig.subplots_adjust(bottom=0.2)
    #mpf.plot(df,type='candle',mav=9,volume=True)
    ax1.xaxis.set_major_locator(months)
    #ax1.xaxis.set_minor_locator(mondays)
    # ax1.xaxis.set_major_formatter(dayFormatter)
    ax1.xaxis.set_major_formatter(dayFormatter)
    #ax1.xaxis.set_minor_formatter(dayFormatter)
    #plot_day_summary(ax, quotes, ticksize=3)
    candlestick_ohlc(ax1, quotes, width=0.6)
    ax1.plot(df['Date'],df["MA"],linewidth=0.4,color='g')
    ax1.xaxis_date()
    #ax1.autoscale_view()
    ax1.set_ylabel('Price', fontweight='bold')
    ax1.set_title(stock, fontweight='bold')
    #plt.xticks(rotation=45)
    #plt.ylabel('Price', fontweight='bold')
    #plt.title(stock,fontweight="bold")
    #ax1.xaxis.set_tick_params(labelsize=1)
    #ax2.xaxis.set_tick_params(labelsize=1)
    ax1.yaxis.set_tick_params(labelsize=10)
    yticks = ax1.yaxis.get_major_ticks()
    yticks[-1].label1.set_visible(False)
    
    #ax2 = ax.twinx()
    ax2.bar(df['Date'],df['Volume'])
    ax2.plot(df['Date'],df["VMA"],linewidth=0.4,color='g')
    ax2.set_ylabel('Volume', fontweight='bold')
    ax2.set_yticks(ticks)
    ax2.xaxis.set_tick_params(labelsize=6)
    ax2.yaxis.set_tick_params(labelsize=6)
    yticks = ax2.yaxis.get_major_ticks()
    yticks[-1].label1.set_visible(False)
    ax1.tick_params(axis="x", which="both", rotation=45,labelsize=6,direction='out')
    ax2.tick_params(axis="x", which="both", rotation=45,labelsize=6,direction='out')
    plt.subplots_adjust(hspace=.0)
    ax1.grid(color = 'green', linestyle = '--', linewidth = 0.2)
    ax2.grid(color = 'green', linestyle = '--', linewidth = 0.2)
    #plt.show()
    st.pyplot(fig)
elif (period=='5y'):
    df=df.iloc[-1265:,:]
    
    quotes = [tuple(x) for x in df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].to_records(index=False)]
    if len(quotes) == 0:
        st.error('Check dates')
        st.stop()

    ticks = np.linspace(min(df['Volume']), max(df['Volume']), 5 )
    
    fig = plt.figure(figsize=(12,10))
    # set height ratios for subplots
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1]) 
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1], sharex = ax1)
    
    #fig.subplots_adjust(bottom=0.2)
    #mpf.plot(df,type='candle',mav=9,volume=True)
    ax1.xaxis.set_major_locator(years)
    #ax1.xaxis.set_minor_locator(mondays)
    # ax1.xaxis.set_major_formatter(dayFormatter)
    ax1.xaxis.set_major_formatter(dayFormatter)
    #ax1.xaxis.set_minor_formatter(dayFormatter)
    #plot_day_summary(ax, quotes, ticksize=3)
    candlestick_ohlc(ax1, quotes, width=0.6)
    ax1.plot(df['Date'],df["MA"],linewidth=0.4,color='g')
    ax1.xaxis_date()
    #ax1.autoscale_view()
    ax1.set_ylabel('Price', fontweight='bold')
    ax1.set_title(stock, fontweight='bold')
    #plt.xticks(rotation=45)
    #plt.ylabel('Price', fontweight='bold')
    #plt.title(stock,fontweight="bold")
    #ax1.xaxis.set_tick_params(labelsize=1)
    #ax2.xaxis.set_tick_params(labelsize=1)
    ax1.yaxis.set_tick_params(labelsize=10)
    yticks = ax1.yaxis.get_major_ticks()
    yticks[-1].label1.set_visible(False)
    
    #ax2 = ax.twinx()
    ax2.bar(df['Date'],df['Volume'])
    ax2.plot(df['Date'],df["VMA"],linewidth=0.4,color='g')
    ax2.set_ylabel('Volume', fontweight='bold')
    ax2.set_yticks(ticks)
    ax2.xaxis.set_tick_params(labelsize=6)
    ax2.yaxis.set_tick_params(labelsize=6)
    yticks = ax2.yaxis.get_major_ticks()
    yticks[-1].label1.set_visible(False)
    ax1.tick_params(axis="x", which="both", rotation=45,labelsize=6,direction='out')
    ax2.tick_params(axis="x", which="both", rotation=45,labelsize=6,direction='out')
    plt.subplots_adjust(hspace=.0)
    ax1.grid(color = 'green', linestyle = '--', linewidth = 0.2)
    ax2.grid(color = 'green', linestyle = '--', linewidth = 0.2)
    #plt.show()
    st.pyplot(fig)
elif (period=='10y'):
    df=df.iloc[-2530:,:]
    
    quotes = [tuple(x) for x in df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].to_records(index=False)]
    if len(quotes) == 0:
        st.error('Check dates')
        st.stop()

    ticks = np.linspace(min(df['Volume']), max(df['Volume']), 5 )
    
    fig = plt.figure(figsize=(12,10))
    # set height ratios for subplots
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1]) 
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1], sharex = ax1)
    
    #fig.subplots_adjust(bottom=0.2)
    #mpf.plot(df,type='candle',mav=9,volume=True)
    ax1.xaxis.set_major_locator(years)
    #ax1.xaxis.set_minor_locator(mondays)
    # ax1.xaxis.set_major_formatter(dayFormatter)
    ax1.xaxis.set_major_formatter(dayFormatter)
    #ax1.xaxis.set_minor_formatter(dayFormatter)
    #plot_day_summary(ax, quotes, ticksize=3)
    candlestick_ohlc(ax1, quotes, width=0.6)
    ax1.plot(df['Date'],df["MA"],linewidth=0.4,color='g')
    ax1.xaxis_date()
    #ax1.autoscale_view()
    ax1.set_ylabel('Price', fontweight='bold')
    ax1.set_title(stock, fontweight='bold')
    #plt.xticks(rotation=45)
    #plt.ylabel('Price', fontweight='bold')
    #plt.title(stock,fontweight="bold")
    #ax1.xaxis.set_tick_params(labelsize=1)
    #ax2.xaxis.set_tick_params(labelsize=1)
    ax1.yaxis.set_tick_params(labelsize=10)
    yticks = ax1.yaxis.get_major_ticks()
    yticks[-1].label1.set_visible(False)
    
    #ax2 = ax.twinx()
    ax2.bar(df['Date'],df['Volume'])
    ax2.plot(df['Date'],df["VMA"],linewidth=0.4,color='g')
    ax2.set_ylabel('Volume', fontweight='bold')
    ax2.set_yticks(ticks)
    ax2.xaxis.set_tick_params(labelsize=6)
    ax2.yaxis.set_tick_params(labelsize=6)
    yticks = ax2.yaxis.get_major_ticks()
    yticks[-1].label1.set_visible(False)
    ax1.tick_params(axis="x", which="both", rotation=45,labelsize=6,direction='out')
    ax2.tick_params(axis="x", which="both", rotation=45,labelsize=6,direction='out')
    plt.subplots_adjust(hspace=.0)
    ax1.grid(color = 'green', linestyle = '--', linewidth = 0.2)
    ax2.grid(color = 'green', linestyle = '--', linewidth = 0.2)
    #plt.show()
    st.pyplot(fig)
elif (period=='max'):
    df=df
    
    quotes = [tuple(x) for x in df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].to_records(index=False)]
    if len(quotes) == 0:
        st.error('Check dates')
        st.stop()

    ticks = np.linspace(min(df['Volume']), max(df['Volume']), 5 )
    
    fig = plt.figure(figsize=(12,10))
    # set height ratios for subplots
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1]) 
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1], sharex = ax1)
    
    #fig.subplots_adjust(bottom=0.2)
    #mpf.plot(df,type='candle',mav=9,volume=True)
    ax1.xaxis.set_major_locator(years)
    #ax1.xaxis.set_minor_locator(mondays)
    # ax1.xaxis.set_major_formatter(dayFormatter)
    ax1.xaxis.set_major_formatter(dayFormatter)
    #ax1.xaxis.set_minor_formatter(dayFormatter)
    #plot_day_summary(ax, quotes, ticksize=3)
    candlestick_ohlc(ax1, quotes, width=0.6)
    ax1.plot(df['Date'],df["MA"],linewidth=0.4,color='g')
    ax1.xaxis_date()
    #ax1.autoscale_view()
    ax1.set_ylabel('Price', fontweight='bold')
    ax1.set_title(stock, fontweight='bold')
    #plt.xticks(rotation=45)
    #plt.ylabel('Price', fontweight='bold')
    #plt.title(stock,fontweight="bold")
    #ax1.xaxis.set_tick_params(labelsize=1)
    #ax2.xaxis.set_tick_params(labelsize=1)
    ax1.yaxis.set_tick_params(labelsize=10)
    yticks = ax1.yaxis.get_major_ticks()
    yticks[-1].label1.set_visible(False)
    
    #ax2 = ax.twinx()
    ax2.bar(df['Date'],df['Volume'])
    ax2.plot(df['Date'],df["VMA"],linewidth=0.4,color='g')
    ax2.set_ylabel('Volume', fontweight='bold')
    ax2.set_yticks(ticks)
    ax2.xaxis.set_tick_params(labelsize=6)
    ax2.yaxis.set_tick_params(labelsize=6)
    yticks = ax2.yaxis.get_major_ticks()
    yticks[-1].label1.set_visible(False)
    ax1.tick_params(axis="x", which="both", rotation=45,labelsize=6,direction='out')
    ax2.tick_params(axis="x", which="both", rotation=45,labelsize=6,direction='out')
    plt.subplots_adjust(hspace=.0)
    ax1.grid(color = 'green', linestyle = '--', linewidth = 0.2)
    ax2.grid(color = 'green', linestyle = '--', linewidth = 0.2)
    #plt.show()
    st.pyplot(fig)

##############################################################################

data = yf.download(tickers=stock+'.NS', period="1d", interval="1m") 
data.reset_index(inplace=True)
data['Datetime1']=data['Datetime'].apply(lambda x: x.strftime('%d-%b, %H:%M'))
#data['Time']=data['Datetime'].apply(lambda x: x.strftime('%H'))

fig1, ax = plt.subplots(figsize=(8,2))
ax.plot(data['Datetime1'],data['Close'])
ax.set_ylabel('Price', fontsize=10)
ax.xaxis.set_major_locator(MultipleLocator(12))
#ax.set_xticks(data['Time'])
ax.tick_params(axis="x", which="both", rotation=45,labelsize=6,direction='out')
ax.tick_params(axis="y", which="both", rotation=45,labelsize=6,direction='out')
fig1.suptitle("Live chart", fontsize=12)
st.pyplot(fig1)

##############################################################################
st.markdown('____')
st.subheader("**Technicals**")
##############################################################################
holders=stock_name.major_holders
holders = holders.rename(columns={0: "%",
                                  1: "Holders"})
holders.set_index('%', inplace=True)
st.subheader("*Major holders*")
st.table(holders)

quat_earnings1=stock_name.quarterly_earnings
quat_earnings1['%']=quat_earnings1['Earnings'].pct_change()
quat_earnings1['Revenue1'] = '₹' + (quat_earnings1['Revenue'].astype(float)/10000000).astype(str) + ' crores'
quat_earnings1['Earnings1'] = '₹' + (quat_earnings1['Earnings'].astype(float)/10000000).astype(str) + ' crores'
st.subheader("*Quarterly earnings and Yearly earnings*")

earnings=stock_name.earnings
earnings['%']=earnings['Earnings'].pct_change()
earnings['Revenue1'] = '₹' + (earnings['Revenue'].astype(float)/10000000).astype(str) + ' crores'
earnings['Earnings1'] = '₹' + (earnings['Earnings'].astype(float)/10000000).astype(str) + ' crores'

b=stock_name.quarterly_financials

fig3, (ax3, ax4) = plt.subplots(1,2, figsize=(10,3))
ax3.bar(quat_earnings1.index, (quat_earnings1['Earnings'].astype(float)/10000000))
ax4.bar(earnings.index.astype(str), (earnings['Earnings'].astype(float)/10000000))
ax3.tick_params(axis="x", which="both", rotation=45,labelsize=6,direction='out')
ax4.tick_params(axis="x", which="both", rotation=45,labelsize=6,direction='out')
ax3.set_ylabel('Earnings (in crores)', fontsize=7,fontdict=dict(weight='bold'))
ax4.set_ylabel('Earnings (in crores)', fontsize=7,fontdict=dict(weight='bold'))
ax3.bar_label(ax3.containers[0])
ax4.bar_label(ax4.containers[0])
ax3.get_yaxis().set_ticks([])
ax4.get_yaxis().set_ticks([])
ax3.set_title('Quarterly Earnings',fontweight='bold')
ax4.set_title('Yearly Earnings',fontweight='bold')
ax3.spines["top"].set_visible(False)
ax3.spines["right"].set_visible(False)
ax3.spines["left"].set_visible(False)
ax4.spines["top"].set_visible(False)
ax4.spines["right"].set_visible(False)
ax4.spines["left"].set_visible(False)
plt.show()
st.pyplot(fig3)


info=stock_name.info



    
 
