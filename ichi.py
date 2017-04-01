#!/usr/bin/env python

import pandas as pd
import numpy as np
import plotly.plotly as py
import plotly.figure_factory as FF
from datetime import datetime
from plotly.graph_objs import *

def printCharts(df):

    fig = FF.create_candlestick(df.Open, df.High, df.Low, df.Close, dates=df.index)

    ts_line = Scatter(
        x=df.index, 
        y=df.tenkan_sen, 
        name= 'Tenkan Sen', 
        line=Line(color='Red')
    )
    fig['data'].extend([ts_line])
    
    ks_line = Scatter(
        x=df.index, 
        y=df.kijun_sen,
        name= 'Kijun Sen', 
        line=Line(color='Blue')
    )    
    fig['data'].extend([ks_line])
    
    cs_line = Scatter(
        x=df.index, 
        y=df.chikou_span,
        name= 'Chikou Span', 
        line=Line(color='Black')
    )    
    fig['data'].extend([cs_line])
    
    ssA_line = Scatter(
        x=df.index, 
        y=df.senkou_span_a,
        name= 'senkou_span_a', 
        line=Line(color='Grean')
    )    
    fig['data'].extend([ssA_line])

    ssB_line = Scatter(
        x=df.index, 
        y=df.senkou_span_b,
        name= 'senkou_span_b', 
        line=Line(color='Orange')
    )    
    fig['data'].extend([ssB_line])
    
    
    
    py.plot(fig, filename='KGHM', validate=False)

def process(file):
    print('Start')
    df = pd.read_csv(file, parse_dates=True, index_col=[1])
    df = df['2016-01-1':'2017-02-28']

    hiP = df['High']
    clP = df['Close']
    loP = df['Low']
    
    # Tenkan-sen (Conversion Line): (9-period high + 9-period low)/2))
    period9_high = pd.rolling_max(hiP, window=9)
    period9_low = pd.rolling_min(loP, window=9)
    tenkan_sen = (period9_high + period9_low) / 2

    # Kijun-sen (Base Line): (26-period high + 26-period low)/2))
    period26_high = pd.rolling_max(hiP, window=26)
    period26_low = pd.rolling_min(loP, window=26)
    kijun_sen = (period26_high + period26_low) / 2

    # Senkou Span A (Leading Span A): (Conversion Line + Base Line)/2))
    senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(26)

    # Senkou Span B (Leading Span B): (52-period high + 52-period low)/2))
    period52_high = pd.rolling_max(hiP, window=52)
    period52_low = pd.rolling_min(loP, window=52)
    senkou_span_b = ((period52_high + period52_low) / 2).shift(26)

    # The most current closing price plotted 22 time periods behind (optional)
    chikou_span = clP.shift(-26) # 22 according to investopedia
    
    df['tenkan_sen'] = tenkan_sen
    df['kijun_sen']  = kijun_sen
    df['senkou_span_a'] = senkou_span_a
    df['senkou_span_b']  = senkou_span_b
    df['chikou_span']  = chikou_span
    
    print(df)
    printCharts(df)

def main():
    process('download/pl/KGHM.txt')
    print('Done');

main()
