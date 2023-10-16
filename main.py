import streamlit as st
from datetime import date

import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go

START = "2015-01-01"
TODAY = date.today().strftime("%y-%m-%d")

st.title("Predict")

selected_stock = st.text_input('Enter Stock Ticker', 'GOOG')

n_years = st.slider("Years of prediction:", 1, 10)
period = n_years * 365

@st.cache_data
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

data = load_data(selected_stock)

st.subheader('Raw Data:')
st.write(data.tail())

def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name = 'stock_open'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name = 'stock_close'))
    fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()

df_train = data[['Date', "Close"]]
df_train = df_train.rename(columns={"Date":"ds", "Close":"y"})

model = Prophet()
model.fit(df_train)
future = model.make_future_dataframe(periods=period)
forecast = model.predict(future)

st.subheader('Forecast Data:')
st.write(forecast.tail())

fig1 = plot_plotly(model, forecast)
st.plotly_chart(fig1)

st.write('Forecast Components')
fig2 = model.plot_components(forecast)
st.write(fig2)
