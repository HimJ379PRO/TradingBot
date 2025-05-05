import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import os

# === Get the DAILY ticker data from Yahoo Finance ===

def update_daily_data(tickers, data_folder="data/raw"):
    """
    Update daily data for the given tickers from Yahoo Finance.
    Saves data to CSVs with incremental updates.
    """ 
    now = datetime.now()
    # Include today only if the market is closed
    end_date = now - timedelta(days=1) if 9 <= now.hour < 16 else now

    # Ensure data folder exists
    os.makedirs(data_folder, exist_ok=True)
    
    try:
        for ticker in tickers:
            file_path = os.path.join(data_folder, f"{ticker}_D.csv")
            file_exists = os.path.exists(file_path)

            if file_exists:
                df = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')
                last_downloaded_date = df.index.max()
                if last_downloaded_date == now.date():
                    print(f"✅ {ticker} is already up to date.")
                    continue
                elif last_downloaded_date + pd.Timedelta(days=1) == now.date():
                    start_date = last_downloaded_date
                else:
                    start_date = last_downloaded_date + pd.Timedelta(days=1)
            else:
                # Handle new file cases
                start_date = pd.to_datetime("2020-01-01")
                df = None

            # Fetch data
            print(f"⬇️ Downloading {ticker} from {start_date.date()} to {end_date.date()}...")
            data = yf.download(ticker, start=start_date, end=end_date, ignore_tz=True, interval="1d", rounding=True)

            if not data.empty:
                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = [col[0] for col in data.columns]

                # Make sure index is named 'Date' for saving consistency
                data.index.name = 'Date'

                if df is not None:
                    new_data = data[~data.index.isin(df.index)]
                else:
                    new_data = data

                if not new_data.empty:
                    mode = 'a' if file_exists else 'w'
                    header = not file_exists
                    new_data.to_csv(file_path, mode=mode, header=header, index=True)
                    print(f"✅ {ticker} updated with {len(new_data)} new rows at {now.time().strftime('%H:%M:%S')}.")
                else:
                    print(f"✅ {ticker} is already up to date. No new rows to add.")
            else:
                print(f"⚠️ No new data downloaded for '{ticker}'.")

    except Exception as e:
        print(f"❌ Error while updating: {e}")


# === Get the 60m ticker data from Yahoo Finance ===

def update_60m_data(tickers, data_folder="data/raw"):
    """
    Update 60-minute intraday data for the given tickers from Yahoo Finance.
    Saves data to CSVs with incremental updates.
    Fetches only completed hourly candles and filters for NSE normal trading session (9:15 - 15:30).

    Note: Data is fetched from 2024-01-01 up to the current time.
    """
    now = datetime.now()

    # ✅ Determine last completed 60-minute candle that closes at HH:15
    if now.minute >= 15:
        end_datetime = now.replace(minute=15, second=0, microsecond=0)
    else:
        end_datetime = (now - timedelta(hours=1)).replace(minute=15, second=0, microsecond=0)

    # Ensure data folder exists
    os.makedirs(data_folder, exist_ok=True)

    try:
        for ticker in tickers:
            file_path = os.path.join(data_folder, f"{ticker}_60m.csv")
            file_exists = os.path.exists(file_path)

            if file_exists:
                df = pd.read_csv(file_path, parse_dates=['Datetime'], index_col='Datetime')
                last_downloaded_datetime = df.index.max()
                start_datetime = last_downloaded_datetime
            else:
                df = None  # Handle new file cases
                start_datetime = pd.to_datetime("2024-01-01")
                
            # Fetch data
            print(f"⬇️ Downloading {ticker} from {start_datetime} to {end_datetime}...")
            data = yf.download(ticker, start=start_datetime, end=end_datetime, ignore_tz=True, interval="60m", rounding=True)

            if not data.empty:
                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = [col[0] for col in data.columns]

                # Make sure index is named 'Datetime' for saving consistency
                if not data.index.name == 'Datetime':
                    data.index.name = 'Datetime'
                    print("Index name changed to 'Datetime'")

                if df is not None:
                    new_data = data[~data.index.isin(df.index)]
                else:
                    new_data = data

                if not new_data.empty:
                    mode = 'a' if file_exists else 'w'
                    header = not file_exists
                    new_data.to_csv(file_path, mode=mode, header=header, index=True)
                    print(f"✅ {ticker} updated with {len(new_data)} new rows at {now.time().strftime('%H:%M:%S')}.")
                else:
                    print(f"✅ {ticker} is already up to date. No new rows added.")
            else:
                print(f"⚠️ No new data downloaded for '{ticker}'.")

    except Exception as e:
        print(f"❌ Error while updating: {e}")


# === Get the 5m ticker data from Yahoo Finance ===

def update_5m_data(tickers, data_folder="data/raw"):
    """
    Update 5-minute intraday data for the given tickers from Yahoo Finance.
    Saves data to CSVs with incremental updates.
    Fetches only completed 5-minute candles during NSE trading hours (9:15 - 15:30).

    Note: Data is fetched from last 55 days up to the last completed 5-minute interval.
    """
    now = datetime.now()

    # ✅ Determine last completed 5-minute candle
    minute = (now.minute // 5) * 5
    end_datetime = now.replace(minute=minute, second=0, microsecond=0)
    if end_datetime == now:
        end_datetime -= timedelta(minutes=5)

    # Ensure data folder exists
    os.makedirs(data_folder, exist_ok=True)

    try:
        for ticker in tickers:
            file_path = os.path.join(data_folder, f"{ticker}_5m.csv")
            file_exists = os.path.exists(file_path)

            if file_exists:
                df = pd.read_csv(file_path, parse_dates=['Datetime'], index_col='Datetime')
                last_downloaded_datetime = df.index.max()
                start_datetime = last_downloaded_datetime
            else:
                df = None
                start_datetime = now - pd.Timedelta(days=55)

            # Fetch data
            print(f"⬇️ Downloading {ticker} 5m data from {start_datetime} to {end_datetime}...")
            data = yf.download(ticker, start=start_datetime, end=end_datetime, interval="5m", ignore_tz=True, rounding=True)

            if not data.empty:
                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = [col[0] for col in data.columns]

                if not data.index.name == 'Datetime':
                    data.index.name = 'Datetime'
                    print("Index name changed to 'Datetime'")

                if df is not None:
                    new_data = data[~data.index.isin(df.index)]
                else:
                    new_data = data

                if not new_data.empty:
                    mode = 'a' if file_exists else 'w'
                    header = not file_exists
                    new_data.to_csv(file_path, mode=mode, header=header, index=True)
                    print(f"✅ {ticker} 5m updated with {len(new_data)} new rows at {now.time().strftime('%H:%M:%S')}.")
                else:
                    print(f"✅ {ticker} 5m is already up to date. No new rows added.")
            else:
                print(f"⚠️ No new 5m data downloaded for '{ticker}'.")

    except Exception as e:
        print(f"❌ Error while updating 5m data: {e}")