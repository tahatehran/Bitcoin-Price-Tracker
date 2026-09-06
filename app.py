import ipaddress
import socket
from urllib.parse import urlparse

import streamlit as st
import requests
import pandas as pd
from datetime import datetime

ALLOWED_CURRENCIES = ['USD', 'EUR', 'GBP']

# Fetch a URL only when it points at a public http/https host
def safe_get(url):
    parsed = urlparse(url)
    if parsed.scheme not in ('http', 'https'):
        raise ValueError(f'Unsupported URL scheme: {parsed.scheme}')
    host = parsed.hostname or ''
    try:
        addr_infos = socket.getaddrinfo(host, None)
    except socket.gaierror as exc:
        raise ValueError(f'Cannot resolve host: {host}') from exc
    for info in addr_infos:
        ip = ipaddress.ip_address(info[4][0])
        if ip.is_loopback or ip.is_private or ip.is_reserved or ip.is_link_local or ip.is_multicast or ip.is_unspecified:
            raise ValueError(f'Host resolves to a non-public address: {host}')
    return requests.get(url, allow_redirects=False)

# Function to get current Bitcoin price
@st.cache_data
def get_current_price(currency='USD'):
    if currency not in ALLOWED_CURRENCIES:
        raise ValueError(f'Unsupported currency: {currency}')
    url = f'https://api.coindesk.com/v1/bpi/currentprice/{currency}.json'
    response = safe_get(url)
    data = response.json()
    price = data['bpi'][currency]['rate_float']
    return price

# Function to get current time in Tehran
@st.cache_data
def get_tehran_time():
    response = safe_get('https://worldtimeapi.org/api/timezone/Asia/Tehran')
    time_data = response.json()
    return time_data['datetime']

# Function to get historical Bitcoin price data
@st.cache_data
def get_historical_prices(currency='USD', days=30):
    if currency not in ALLOWED_CURRENCIES:
        raise ValueError(f'Unsupported currency: {currency}')
    url = f'https://api.coindesk.com/v1/bpi/historical/close.json?currency={currency}&start={datetime.now().strftime("%Y-%m-%d")}&end={datetime.now().strftime("%Y-%m-%d")}'
    response = safe_get(url)
    data = response.json()
    if 'bpi' in data:
        historical_prices = pd.Series(data['bpi']).sort_index()
        df = pd.DataFrame({'price': historical_prices.values, 'date': historical_prices.index})
        return df.tail(days)
    else:
        return pd.DataFrame()

# Calculate RSI
def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)
    average_gain = gains.rolling(window=period).mean()
    average_loss = losses.rolling(window=period).mean()
    rs = average_gain / average_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Calculate MACD
def calculate_macd(prices, fast_window=12, slow_window=26, signal_window=9):
    ema_fast = prices.ewm(span=fast_window, adjust=False).mean()
    ema_slow = prices.ewm(span=slow_window, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    hist = macd - signal
    return macd, signal, hist

# Set page configuration
st.set_page_config(page_title='Bitcoin Price Tracker', page_icon=':moneybag:', layout='wide')

# Page header
st.header('Bitcoin Price Tracker :chart_with_upwards_trend:')

# Display current time in Tehran
tehran_time = get_tehran_time()
st.sidebar.write('Current time in Tehran:', tehran_time)

# Display current Bitcoin price
currency = st.sidebar.selectbox('Select Currency', ALLOWED_CURRENCIES)
current_price = get_current_price(currency)
st.write(f'Current Bitcoin Price in {currency}: **{current_price}**')

# Refresh button
if st.button('Refresh'):
    st.experimental_rerun()

# Trading signals section
st.subheader('Trading Signals :signal_strength:')

# Get Bitcoin price data
historical_df = get_historical_prices(currency, days=30)
df = pd.DataFrame({'close': historical_df['price']})

# Calculate RSI and MACD
df['rsi'] = calculate_rsi(df['close'])
macd, signal, _ = calculate_macd(df['close'])
df['macd'] = macd
df['signal'] = signal

# Generate trading signals
df['buy_signal'] = (df['rsi'] < 30) & (df['macd'] > df['signal'])
df['sell_signal'] = (df['rsi'] > 70) & (df['macd'] < df['signal'])

# Display trading signals
st.write('Buy Signals:', df['buy_signal'].sum())
st.write('Sell Signals:', df['sell_signal'].sum())

# Display historical Bitcoin price chart
st.subheader('Historical Bitcoin Price')
st.line_chart(historical_df, x='date')
