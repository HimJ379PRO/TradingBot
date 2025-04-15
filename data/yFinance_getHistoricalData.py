import yfinance as yf
from datetime import datetime
import pandas as pd
import os

# Set up logging

# Set up global variables
start_date_daily = "2020-01-01"

# Get Reliance - D - 2020 to NOW()
data = yf.download("RELIANCE.NS", start=start_date_daily, end=datetime.now(), interval="1d", rounding=True)
data.columns = [col[0] for col in data.columns]

# Save to CSV
data.to_csv("data/processed/RELIANCE.NSE_D.csv", index=True)


