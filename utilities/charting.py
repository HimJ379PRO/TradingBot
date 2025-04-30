import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_candlesticks_RSI_chart(df, rsi_period=14):
    """
    Plots a candlestick chart using Plotly with a range slider.
    Adds an RSI indicator below the candlestick chart.

    Parameters:
        df(pd.DataFrame): A DataFrame containing 'Date', 'Open', 'High', 'Low', 'Close' columns.
        rsi_period(int): The period for the RSI calculation. Default is 14.
    """
    # Step 1: Create a figure with 2 rows (1 for price, 1 for RSI)
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.7, 0.3],
        subplot_titles=("Candlesticks Chart", "RSI Indicator")
    )

    # Step 2: Candlestick chart (Row 1)
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='Candlestick'
    ), row=1, col=1)

    # Step 3: RSI line (Row 2)
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['RSI_14' if rsi_period == 14 else 'RSI_9'],
        mode='lines',
        name='RSI',
        line=dict(color='blue')
    ), row=2, col=1)

    # Step 4: Add RSI 30 and 70 lines
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1, annotation_text="Overbought (70)")
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1, annotation_text="Oversold (30)")

    # Step 5: Layout
    fig.update_layout(
        title='RELIANCE - Candlestick with RSI (14)',
        xaxis_rangeslider_visible=False,
        height=800,
        showlegend=False
    )

    fig.show()