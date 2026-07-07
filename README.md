---
title: Game
emoji: ⚡
colorFrom: indigo
colorTo: pink
sdk: streamlit
sdk_version: 1.34.0
app_file: app.py
pinned: false
---

# Bitcoin Price Tracker

A Streamlit web app for tracking Bitcoin prices, displaying trading signals, and running simple predictive models.

## Features

- **Live Bitcoin price** in USD, EUR, or GBP via the CoinDesk API
- **Tehran time** display in the sidebar
- **Trading signals** based on RSI and MACD indicators
- **Historical price chart** (last 30 days)
- **Tabular regression** price prediction (`pytest.py`)
- **Custom Bitcoin trading environment** for simulation (`pytest.py`)

## Files

- `app.py` — Main Streamlit app (price tracker, RSI/MACD signals, chart)
- `pytest.py` — Experimental app with linear regression and a custom trading environment
- `requirements.txt` — Python dependencies

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Usage

1. Select a currency from the sidebar.
2. View the current Bitcoin price and trading signals.
3. Use the **Refresh** button to fetch the latest data.

## APIs

- [CoinDesk Bitcoin Price Index](https://www.coindesk.com/coindesk-api)
- [WorldTimeAPI](https://worldtimeapi.org/) for Tehran time

## License

Copyright © 2023 Taha Tehrani Nasab. All rights reserved.
