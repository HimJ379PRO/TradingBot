import yfinance as yf
from datetime import datetime
import pandas as pd
import os

tickers = ["RELIANCE.NS","AAPL"]

def update_daily_data(tickers, data_folder="data/raw"):
    for ticker in tickers:
        file_path = f"{data_folder}/{ticker}_D.csv"

        if os.path.exists(file_path):
            df = pd.read_csv(file_path, parse_dates=['Date'])
            last_downloaded_date = df['Date'].max()
            new_start_date = last_downloaded_date + pd.Timedelta(days=1)

            # Avoid fetching if data is already up to date
            if new_start_date >= datetime.now():
                print(f"✅ {ticker} is already up to date. Skipping.")
                continue
        else:
            new_start_date = pd.to_datetime("2020-01-01")

        print(f"⬇️ Downloading {ticker} from {new_start_date.date()} to today...")

        data = yf.download(ticker, start=new_start_date, end=datetime.now(), interval="1d", rounding=True)

        if not data.empty:
            # Clean up the data
            data.columns = [col[0] for col in data.columns]

            # Append or write
            mode = 'a' if os.path.exists(file_path) else 'w'
            header = not os.path.exists(file_path)
            data.to_csv(file_path, mode=mode, header=header, index=True)
            print(f"📦 Data saved to {file_path}")
        else:
            print(f"⚠️ No new data found for {ticker}")


# === Get the DAILY ticker data from Yahoo Finance ===

# Get the latest ticker data if the prev. data exists, else get all the data since Jan 2020
for ticker in tickers:
    # Check if the ticker data already exists
    if os.path.exists(f"data/raw/{ticker}_D.csv"):
        # Extract the date from the last record and use it as a start date
        df = pd.read_csv(f"data/raw/{ticker}_D.csv", parse_dates=['Date'])
        last_downloaded_date = df['Date'].max()
        new_start_date = last_downloaded_date + pd.Timedelta(days=1)
        # Get only the latest ticker data from yahoo finance
        data = yf.download(ticker, start=new_start_date, end=datetime.now(), interval="1d", rounding=True)
        data.columns = [col[0] for col in data.columns]
        # Append it to CSV
        data.to_csv(f"data/raw/{ticker}_D.csv", mode='a', header=False, index=True)
    else:
        # Get ticker data - Daily - 2020 to NOW()
        data = yf.download(ticker, start="2020-01-01", end=datetime.now(), interval="1d", rounding=True)
        data.columns = [col[0] for col in data.columns]
        # Save to CSV
        data.to_csv(f"data/raw/{ticker}_D.csv", index=True)


# === Get the 60m ticker data from Yahoo Finance ===

# Get the latest ticker data if the prev. data exists, else get all the data since Jan 2020
for ticker in tickers:
    # Check if the ticker data already exists
    if os.path.exists(f"data/raw/{ticker}_60m.csv"):
        # Extract the date from the last record and use it as a start date
        df = pd.read_csv(f"data/raw/{ticker}_60m.csv", parse_dates=['Date'])
        last_downloaded_date = df['Date'].max()
        new_start_date = last_downloaded_date + pd.Timedelta(days=1)
        # Get only the latest ticker data from yahoo finance
        data = yf.download(ticker, start=new_start_date, end=datetime.now(), interval="60m", rounding=True, ignore_tz=True)
        data.columns = [col[0] for col in data.columns]
        # Append it to CSV
        data.to_csv(f"data/raw/{ticker}_60m.csv", mode='a', header=False, index=True)
    else:
        # Get ticker data - 60m - Jan 2024 to NOW()
        data = yf.download(ticker, start="2024-01-01", end=datetime.now(), interval="60m", rounding=True, ignore_tz=True)
        data.columns = [col[0] for col in data.columns]
        # Save to CSV
        data.to_csv(f"data/raw/{ticker}_60m.csv", index=True)