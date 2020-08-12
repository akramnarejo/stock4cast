import streamlit as st
import datetime as dt
import pandas as pd
import pandas_datareader as reader
from fbprophet import Prophet
from PIL import Image


choice = st.sidebar.selectbox('Select company', ('Company','Apple','Google','Amazon','Microsoft','Tesla'))
input_periods = st.sidebar.slider(label='Select months to forecast for', min_value=1, max_value=24)
action = st.sidebar.button(label='forecast')
st.sidebar.text('tweet me @akramnarejo')
company = {
    'Company':'',
    'Apple':'AAPL',
    'Google':'GOOG',
    'Amazon':'AMZN',
    'Microsoft':'MSFT',
    'Tesla':'TSLA'
}

st.markdown("# Welcome to Stock4Cast!")
st.write('Stock4cast lets you forecast the stock prices of top companies for the next 2 years.')
image = Image.open('stock.jpg')
st.image(image, use_column_width=True)

if action:
    if len(company[choice]) > 1:
        end = dt.datetime.now()
        start = end.year-1
        df = reader.get_data_yahoo(company[choice],start,end)
        st.markdown(f'## {choice} statistics')
        st.write(df.sort_index(ascending=False))
        df.reset_index(inplace=True)
        df = df[['Date','Close']]
        df = df.rename(columns={'Date':'ds','Close':'y'})
        # create prophet model
        model = Prophet(yearly_seasonality=True, daily_seasonality=True)
        model.fit(df)
        future_dates = model.make_future_dataframe(periods=input_periods, freq='MS')
        forecast = model.predict(future_dates)
        st.markdown(f'## {choice} close price forecast')
        model.plot(forecast, uncertainty=True)
        st.pyplot()
        model.plot_components(forecast)
        st.pyplot()

    