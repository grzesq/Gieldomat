#!/usr/bin/env python

import pandas as pd
import numpy as np
import plotly.plotly as py
import plotly.figure_factory as FF
import datetime
from plotly.graph_objs import *
import os


Period_1 = 9
Period_2 = 26
Period_3 = 52


tenkan_sen = 0
kijun_sen  = 0
senkou_span_a = 0
senkou_span_b = 0
chikou_span   = 0

def printCharts(df):
    delta = datetime.timedelta(days=190)
    end = datetime.date.today()
    start = end - delta
    e = end.strftime("%Y %m %d")
    s = start.strftime("%Y %m %d")
    df = df[s:e]
    
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
        fill='none',
        name= 'senkou_span_a', 
        line=Line(color='Grean')
    )    
    fig['data'].extend([ssA_line])

    ssB_line = Scatter(
        x=df.index, 
        y=df.senkou_span_b,
        name= 'senkou_span_b', 
        fill='tonexty',
        line=Line(color='Orange')
    )    
    fig['data'].extend([ssB_line])
        
    py.plot(fig, filename='KGHM', validate=False)
    

def calcIchi(file):
    df = pd.read_csv(file, parse_dates=True, index_col=[1])

    hiP = df['High']
    clP = df['Close']
    loP = df['Low']
    
    # Tenkan-sen (Conversion Line): (9-period high + 9-period low)/2))
    period9_high = hiP.rolling(window=Period_1).max()
    period9_low  = loP.rolling(window=Period_1).min()
    tenkan_sen = (period9_high + period9_low) / 2

    # Kijun-sen (Base Line): (26-period high + 26-period low)/2))
    period26_high = hiP.rolling(window=Period_2).max()
    period26_low  = loP.rolling(window=Period_2).min()
    kijun_sen = (period26_high + period26_low) / 2

    # Senkou Span A (Leading Span A): (Conversion Line + Base Line)/2))
    senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(Period_2)

    # Senkou Span B (Leading Span B): (52-period high + 52-period low)/2))
    period52_high = hiP.rolling(window=Period_3).max()
    period52_low = loP.rolling(window=Period_3).min()
    senkou_span_b = ((period52_high + period52_low) / 2).shift(Period_2)

    # The most current closing price plotted 22 time periods behind (optional)
    chikou_span = clP.shift(-Period_2)
    
    
    df['tenkan_sen'] = tenkan_sen
    df['kijun_sen']  = kijun_sen
    df['senkou_span_a'] = senkou_span_a
    df['senkou_span_b']  = senkou_span_b
    df['chikou_span']  = chikou_span

    return df
    
def addSignal(df):
    # 0 Brak 1 Slaby Up 2 Up 3 Mocny UP
    ts = df.tenkan_sen;
    ks = df.kijun_sen
    sygnal = 0
        
    df["sygnal"] = np.where((ts.shift(1) <= ks.shift(1)) & (ts > ks), 1, 0)
    df["sygnal"] = np.where((ts.shift(1) >= ks.shift(1)) & (ts < ks), -1, 0)
    df["sygnal"] = df["sygnal"] * \
                   np.where((df['chikou_span'] > df['Close'].shift(-Period_2)), 2, 1 )
    df["sygnal"] = df["sygnal"] * \
                   np.where((df['Close'] > df['senkou_span_a']) & \
                            (df['Close'] > df['senkou_span_b']), 2, 1 )
    df["sygnal"] = df["sygnal"] * np.where((df['Volume'] > 4999), 1, 0)
        
        
        
    return df
    
def main():
    print('Start\n')
    for file in os.listdir("download/pl"):
        if (file.endswith(".csv") or file.endswith(".txt")):
            data = calcIchi("download/pl/"+file)
            data = addSignal(data)
            sg = data.iloc[-1].sygnal
            if (sg != 0):
                print(file + "  Sygnal: ")
                print(sg)
                print("-----------------------------------\n")
    print('Done')
    #    printCharts(df)

main()
