# Import necessary libraries
import pandas as pd

def calculate_rsi(series, period: int = 14, ema_length: int = 14):
    """
    Calculate the Relative Strength Index (RSI) using EMA smoothing.

    RSI stands for Relative Strength Index. 
    It's a momentum oscillator that measures how strong or weak a stock's recent price movement is, 
    to help identify if it's overbought or oversold. 
    It ranges from 0 to 100.

    Args:
        series (pd.Series): Price series (closing prices recommended).
        period (int): Lookback period for calculating gains and losses. Default is 14.
        ema_length (int): Smoothing length for EMA. Default is 14.

    Returns:
        pd.Series: RSI values ranging from 0 to 100.
    """
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    # Use EMA instead of SMA
    avg_gain = gain.ewm(span=ema_length, adjust=False).mean()
    avg_loss = loss.ewm(span=ema_length, adjust=False).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    # Set first `period` values as NaN to avoid misleading early values
    rsi[:period] = pd.NA

    return rsi