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
    end_date = now - timedelta(days=1) if now.hour < 16 else now

    # Ensure data folder exists
    os.makedirs(data_folder, exist_ok=True)
    
    try:
        for ticker in tickers:
            file_path = os.path.join(data_folder, f"{ticker}_D.csv")
            file_exists = os.path.exists(file_path)

            if file_exists:
                df = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')
                last_downloaded_date = df.index.max()
                start_date = last_downloaded_date + pd.Timedelta(days=1)
            else:
                start_date = pd.to_datetime("2020-01-01")
                df = None  # Handle new file cases

            # Fetch data
            print(f"⬇️ Downloading {ticker} from {start_date.date()} to {end_date.date()}...")
            data = yf.download(ticker, start=start_date, end=end_date, interval="1d", rounding=True)

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
                    print(f"✅ {ticker} updated with {len(new_data)} new rows.")
                else:
                    print(f"✅ {ticker} is already up to date. No new rows to add.")
            else:
                print(f"⚠️ No new data downloaded for '{ticker}'.")

    except Exception as e:
        print(f"❌ Error while updating: {e}")


# === Get the 60m ticker data from Yahoo Finance ===

