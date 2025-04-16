def calculate_rsi(series, period=14):
    """
    RSI stands for Relative Strength Index. 
    It's a momentum oscillator that measures how strong or weak a stock's recent price movement is, to help identify if it's overbought or oversold.
    It ranges from 0 to 100 and is typically used to identify overbought or oversold conditions in a market.
    """
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi