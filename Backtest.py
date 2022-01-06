import datetime
import requests
import numpy as np
import pandas as pd
import pandas_ta as ta
import yfinance as yf
import streamlit as st
import plotly.graph_objects as go


def download_data(symbol, s_date="2019-04-05", e_date="2021-12-30"):
    return yf.download(symbol, start=s_date, end=e_date, group_by="ticker")

def mk_pickle():
    pass

def EMA(df):
    moving_averages = ta.Strategy(name="moving indicators", ta=[{"kind": "ema", "length": 9},{"kind": "ema", "length": 26},])
    df.ta.cores = 0  
    return df.ta.strategy(moving_averages)

def sup_trend(h, l, c, p, mul):
    return ta.supertrend(high=h, low=l, close=c, period=p, multiplier=mul)['SUPERT_7_3.0']

#sidebar
st.title("Test")
option = st.sidebar.selectbox("Select Dashboard", ("Default", "Fetch data"))
if option=="Default":
    
    #pickle data
    data = pd.read_pickle('./pickle_data')
    
    #strategy input
    strategy = st.sidebar.selectbox('Select strategy', ('EMA', 'Supertrend'))
    if strategy =='EMA':
        moving_averages = ta.Strategy(name="moving indicators", ta=[{"kind": "ema", "length": 9},{"kind": "ema", "length": 26},])
        data.ta.cores = 0  
        data.ta.strategy(moving_averages)
        
        data['favor'] = np.where(data['EMA_9'] > data['EMA_26'], 1, 0)
        data['N_F'] = np.where(data['EMA_9'] < data['EMA_26'], 1, 0)
        
        buy = list()
        sell = list()
        investment=0
        for i in range(len(data)):
            if data['favor'][i] == 1:
                buy.append(data['EMA_9'][i])
                stop_loss = data['EMA_9'][i]- data['EMA_9'][i]*0.05
                investment+=data['EMA_9'][i]

            if data['N_F'][i]==1:
                sell.append(data['EMA_9'][i])

        def ty(x):
            price=0
            for i in x:
                price+=i
            return price
        SELL= ty(sell)
        BUY = ty(buy)
        profit = SELL-BUY
        loss = BUY-SELL
        st.write('profit',profit,'loss',loss,'investment',investment)
        
        #candle plot
        fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'],
                close=data['Close'], increasing_line_color='#ff9900', decreasing_line_color='black', showlegend=False,),])
        layout = go.Layout(plot_bgcolor='#efefef', font_family='Monospace', font_color='#000000', font_size=20,
                xaxis=dict(rangeslider=dict(visible=False)))
        fig.update_layout(layout)
        #EMA plot
        fig.add_trace(go.Scatter(x=data.index, y=data['EMA_9'], line=dict(color='#008000', width=2), name='EMA_9'))
        fig.add_trace(go.Scatter(x=data.index, y=data['EMA_26'], line=dict(color='#FF5733', width=2), name='EMA_26'))
        fig.show()
        
        
        st.write('Number of Trade :',)
    
    if strategy =='Supertrend':
        data['sup']=ta.supertrend(high=data['High'], low=data['Low'], close=data['Close'], period=10, multiplier=3)['SUPERT_7_3.0']
        
        data['buy']=0
        data['sell']=0

        for i in range(10,len(data)):
            if data['Close'][i-1] <= data['sup'][i-1] and data['Close'][i] > data['sup'][i]:
                data['buy'][i] =1
            if data['Close'][i-1] >= data['sup'][i-1] and data['Close'][i] < data['sup'][i]:
                data['sell'][i] = 1
        
        fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'],
                close=data['Close'], increasing_line_color='#ff9900', decreasing_line_color='black', showlegend=False,),])
        layout = go.Layout(plot_bgcolor='#efefef', font_family='Monospace', font_color='#000000', font_size=20,
                xaxis=dict(rangeslider=dict(visible=False)))
        fig.update_layout(layout)
        fig.add_trace(go.Scatter(x=data.index, y=data['sup'], line=dict(color='#EE4B2B', width=2), name='sup'))
        fig.show()
    
if option=="Fetch data":
    symbol = st.sidebar.text_input("Enter Symbol", value='', max_chars=None, key=None, type='default')
    
    #date input 
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    start_date = st.sidebar.date_input('Start date', today)
    end_date = st.sidebar.date_input('End date', tomorrow)
    
    if start_date < end_date: pass
        #st.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
    else: pass
        #st.error('Error: End date must fall after start date.')
    
    #download data
    data = download_data(symbol, start_date, end_date)
    
    #strategy input
    strategy = st.sidebar.selectbox('Select strategy', ('EMA', 'Supertrend'))
    if strategy =='EMA':
        
        moving_averages = ta.Strategy(name="moving indicators", ta=[{"kind": "ema", "length": 9},{"kind": "ema", "length": 26},])
        data.ta.cores = 0  
        data.ta.strategy(moving_averages)
        
        data['favor'] = np.where(data['EMA_9'] > data['EMA_26'], 1, 0)
        data['N_F'] = np.where(data['EMA_9'] < data['EMA_26'], 1, 0)
        
        buy = list()
        sell = list()
        investment=0
        for i in range(len(data)):
            if data['favor'][i] == 1:
                buy.append(data['EMA_9'][i])
                stop_loss = data['EMA_9'][i]- data['EMA_9'][i]*0.05
                investment+=data['EMA_9'][i]

            if data['N_F'][i]==1:
                sell.append(data['EMA_9'][i])

        def ty(x):
            price=0
            for i in x:
                price+=i
            return price
        SELL= ty(sell)
        BUY = ty(buy)
        profit = SELL-BUY
        loss = BUY-SELL
        st.write('profit',profit,'loss',loss,'investment',investment)
        
        #candle plot
        fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'],
                close=data['Close'], increasing_line_color='#ff9900', decreasing_line_color='black', showlegend=False,),])
        layout = go.Layout(plot_bgcolor='#efefef', font_family='Monospace', font_color='#000000', font_size=20,
                xaxis=dict(rangeslider=dict(visible=False)))
        fig.update_layout(layout)
        #EMA plot
        fig.add_trace(go.Scatter(x=data.index, y=data['EMA_9'], line=dict(color='#008000', width=2), name='EMA_9'))
        fig.add_trace(go.Scatter(x=data.index, y=data['EMA_26'], line=dict(color='#FF5733', width=2), name='EMA_26'))
        fig.show()
        
    if strategy =='Supertrend':
        data['sup']=ta.supertrend(high=data['High'], low=data['Low'], close=data['Close'], period=10, multiplier=3)['SUPERT_7_3.0']
        
        data['buy']=0
        data['sell']=0

        for i in range(10,len(data)):
            if data['Close'][i-1] <= data['sup'][i-1] and data['Close'][i] > data['sup'][i]:
                data['buy'][i] =1
            if data['Close'][i-1] >= data['sup'][i-1] and data['Close'][i] < data['sup'][i]:
                data['sell'][i] = 1
        
        ig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'],
                close=data['Close'], increasing_line_color='#ff9900', decreasing_line_color='black', showlegend=False,),])
        layout = go.Layout(plot_bgcolor='#efefef', font_family='Monospace', font_color='#000000', font_size=20,
                xaxis=dict(rangeslider=dict(visible=False)))
        fig.update_layout(layout)
        
        fig.add_trace(go.Scatter(x=data.index, y=data['sup'], line=dict(color='#EE4B2B', width=2), name='sup'))
        fig.show()
