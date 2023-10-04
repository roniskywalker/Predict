import streamlit as st
from datetime import date

import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go

START = "2006-01-01"
TODAY = date.today().strftime("%y-%m-%d")

st.title("Stock Prediction App")

stocks = ("AAPL", "GOOG", "MSFT")
selected_stocks = st.selectbox("Select dataset for prediction", stocks)

n_years = st.slider("Years of prediction:", 1, 3)
period = n_years * 365