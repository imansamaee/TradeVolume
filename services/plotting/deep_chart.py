from datetime import datetime

import pandas as pd
import plotly.graph_objects as go



def draw_predict_chart(df):
    from bot.deep_bot import DEEPSTATE
    fig = go.Figure(data=[go.Candlestick(x=pd.to_datetime(df['time'], unit='ms'),
                                         open=df['open'],
                                         high=df['high'],
                                         low=df['low'],
                                         close=df['close'])])

    fig.add_vrect(x0=pd.to_datetime(df['time'].iloc[0], unit='ms'), x1=pd.to_datetime(df['time'].iloc[-10], unit='ms'),
                  annotation_text="decline", annotation_position="top left",
                  fillcolor="grey", opacity=0.25, line_width=0)
    fig.update_layout(
        title="BTCUSDT 1m Chart",
        xaxis_tickfont_size=12,
        yaxis=dict(
            title='Price Prediction',
            titlefont_size=14,
            tickfont_size=12,

        ),
        autosize=False,
        width=2500,
        height=1100,
        margin=dict(l=50, r=50, b=100, t=100, pad=4),
        template="plotly_white"
    )

    fig.show()
    DEEPSTATE.fig = fig
    return fig


