# 📈 Trading Bot: Automated Signal Generation and Alert System

A fully automated trading signal pipeline that uses RSI and EMA crossover strategies to generate and broadcast real-time trading alerts. Designed to demonstrate robust Data Engineering practices in financial data processing and automation.

---

## 🚀 Project Overview

This bot processes intraday and historical market data, generates entry/exit signals based on technical indicators, and delivers real-time alerts to Telegram.

- **Project Type**: Personal Project
- **Domain**: Algo Trading / Quantitative Finance
- **Focus Area**: Data Engineering, Code Modularity, Technical Analysis/Signal Processing, Automation, Chat Bot

---

## **👨🏻‍💻 Tech Stack**

| **Component** | **Tech Used** |
| --- | --- |
| **Language** | Python 3.10 |
| **Data Sources** | `yfinance` (Yahoo Finance), `SmartAPI` (Angel One) |
| **Data Handling** | `pandas` |
| **Indicators** | Custom logic, `pandas_ta` |
| **Version Control** | Git + GitHub |
| **Scheduler** | `APScheduler`/`cron` (macOS) |
| **Logging** | `logging`  |
| **Storage** | CSV files (optionally SQLite later) |

---

## 🛠️ Key Components

- utilities/getData_YahooFinanace.py and update_data_and_calculate_indicators() – Fetches and appends intraday and daily market data
- run_signals_generator() – Entry and exit logic engine for signals
- utilities/telegram_alerts.py and send_alerts_to_telegram() – Pushes signal notifications to Telegram group
- run_trading_bot() and start_scheduler() – Orchestrates end-to-end automation with APScheduler

---

## 🔁 Bot Workflow

### 1. Environment Initialization

- Imports essential libraries and loads modular utility scripts.

### 2. Data Collection

- Downloads latest OHLCV data from Yahoo Finance.
- Supports 5m, 60m, and daily timeframes.
- Saves to `data/raw/` directory with timestamped integrity.

### 3. Indicator Computation

- Applies EMA(20), RSI(8), and RSI(14) using `pandas_ta`.
- Saves enriched outputs to `data/indicators/`.

### 4. Signal Generation Engine

- Entry Signal: RSI-50 crossover + price vs EMA alignment
- Exit Signal: RSI reversion or trade reversal detection
- Tracks:
    - Entry Signal (e.g., Go Long, Go Short)
    - Trade Status (e.g., Entered Long)
    - Exit Point & MTM (Mark-to-Market) for live trade

### 5. Signal Logging

- Appends new signal rows to `data/signals/{TICKER}_60m.csv`
- Maintains continuity with historical buffer (last 100 rows)

### 6. Telegram Alerting

- Sends formatted trade alerts to Telegram group:
    - Entry/Exit updates
    - Price info, RSI/EMA stats
    - Trade performance summary, etc.

<img src="https://github.com/user-attachments/assets/7a64f8c1-ed6b-48f7-8a6b-c8f5437c55d1" width="350">

### 7. Job Scheduling

- APScheduler runs:
    - `update_data_and_calculate_indicators(tickers)` every hour
    - `run_signals_generator(tickers)` after data update
    - `send_alerts_to_telegram(tickers)` shortly after signals
- Run time control ensures candle close before signal computation by running job every 16th minute of an hour.

---

## 📈  Performance Summary (Backtesting + Live Market)
**STRATEGY 3: Re-enter on trend change.**

The example below is the best case scenario when RELIANCE.NSE was either bullish or bearish (not sideways) over a period of 3-months.\
The performace of the bot varies if the market is choppy. The issue will be fixed in the next version of the trading bot.

> [!Tip]
> View the complete tradelog: [tradelogs/strategy_3_re-enter_reliance_60m.csv](/tradelogs/strategy_3_re-enter_reliance_60m.csv)

**Summary**
| Metric | Value |
| --- | --- |
| Total Trades | 20 |
| Winning Trades | 10 |
| Losing Trades | 10 |
| Win Rate (%) | 50.0 |
| Total Return | ₹126,300 |
| Average Win | ₹14,997.5 |
| Average Loss | ₹-2,367.5 |
| Profit Factor | 6.33 |

<aside>
💡

**✅ ROI for Reliance Futures: ~99.77%**

</aside>

$\text{ROI (\%)} = \left( \frac{\text{Total Return}}{\text{Capital Invested}} \right) \times 100$

Given:

- **Total Return** = ₹126,300
- **Capital Invested (Margin Required)** = ₹126,591

Calculation:

$\text{ROI} = \left( \frac{126300}{126591} \right) \times 100 \approx 99.77\%$

## 🔍 Explore Key Project Folders

- **`strategies/`**: [Private Folder] Contains entry and exit strategies based on the generated signals
- **`notebooks/`**: [Private Folder] Contains playground/testing jupyter notebooks
- **`tradelogs/`**: Captures detailed runtime logs and event triggers
- **`utilities/`**: Contains helper scripts for modular data and signal operations
- **`data/signals/`**: Final outputs of trade signals with trade status and MTM
- **`data/indicators/`**: Technical indicator-enriched OHLCV data
- **`data/raw/`**: Original raw downloaded files for transparency

---

## **🔐 Security Considerations**

1. API keys are stored in `config.py` (excluded via .gitignore)
2. No hardcoding sensitive credentials
3. Rate limits respected while fetching data

## 📌 Next Steps

1. Auto-trade execution with Angel Broker’s SmartAPI or Zerodha Broker’s Kite Connect API
2. Add RSI-EMA multiple timeframe analysis (5m-60m)
3. Support for more indicators and strategies

---

For queries, contributions, or **if you want to develop your own trading bot feel free to reach out!** [💼 LinkedIn](https://www.linkedin.com/in/datawizhimj/)
