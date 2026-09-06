---
title: Bitcoin Price Tracker
emoji: 📈
colorFrom: indigo
colorTo: pink
sdk: streamlit
sdk_version: 1.34.0
app_file: app.py
pinned: false
---

# Bitcoin Price Tracker

A lightweight **Streamlit** web app for tracking Bitcoin prices in real time, generating simple RSI/MACD trading signals, and experimenting with basic price prediction and trading simulation.

## ✨ Features

- **Live Bitcoin price** in USD, EUR, or GBP (via the CoinDesk API)
- **Tehran time** displayed in the sidebar (via WorldTimeAPI)
- **Trading signals** based on RSI and MACD indicators
- **Historical price chart** for the last 30 days
- **Tabular regression** forecast of the next 7 days using linear regression (`pytest.py`)
- **Custom Bitcoin trading environment** for simple buy/sell/hold simulations with a $1,000 starting portfolio (`pytest.py`)

## 📁 Project Structure

| File | Description |
|------|-------------|
| `app.py` | Main Streamlit app: live price, RSI/MACD signals, 30-day chart |
| `pytest.py` | Experimental app: 7-day linear-regression forecast + custom trading environment (despite the name, nothing to do with the pytest test framework) |
| `requirements.txt` | Python dependencies |

## 🚀 Getting Started

### Prerequisites

- Python 3.8+

### Installation

```bash
git clone https://github.com/tahatehran/Bitcoin-Price-Tracker.git
cd Bitcoin-Price-Tracker
pip install -r requirements.txt
```

### Running the App

```bash
# Main app: price tracker, signals, and chart
streamlit run app.py

# Experimental version: regression forecast and trading simulation
streamlit run pytest.py
```

The app opens in your browser at `http://localhost:8501` by default.

## 📖 Usage

1. Pick a currency (**USD / EUR / GBP**) from the sidebar.
2. View the current Bitcoin price and the buy/sell signal counts.
3. Use the **Refresh** button to fetch the latest data.
4. In `pytest.py`, you can also switch the displayed time zone (Tehran / UTC / Local).

## 📊 How the Signals Work

A signal fires only when **both** conditions align:

| Indicator | Buy Signal | Sell Signal |
|-----------|------------|-------------|
| RSI (14-day) | RSI < 30 (oversold) | RSI > 70 (overbought) |
| MACD (12/26/9) | MACD above the signal line | MACD below the signal line |

## 🛰️ APIs Used

- [CoinDesk Bitcoin Price Index API](https://www.coindesk.com/coindesk-api) — current and historical BTC prices
- [WorldTimeAPI](https://worldtimeapi.org/) — current Tehran time

## ☁️ Deploying to Hugging Face Spaces

The YAML block at the top of this file contains the [Hugging Face Spaces](https://huggingface.co/spaces) configuration (Streamlit SDK). Fork the repo, create a new Space from it, and the app deploys automatically.

## ⚠️ Disclaimer

This project is for **educational purposes only**. The indicators and predictions are naive and must not be used as the basis for real investment decisions.

## 📄 License

Copyright © 2023 Taha Tehrani Nasab. All rights reserved.
