import numpy as np
import plotly.graph_objects as go

config = dict({'scrollZoom': True})


# noinspection PyTypeChecker
def draw_chart(symbol):
    print(f"plotting {symbol}")
    from bot.bot import STATE
    data = STATE.data_objects[symbol]
    df = data.training_data_df[-200:]
    from plotly.subplots import make_subplots
    fig = make_subplots(rows=4, cols=1, shared_xaxes=True,
                        vertical_spacing=0.01, subplot_titles=(data.symbol, 'volume'),
                        row_width=[.5, .5, .5, 1.5])

    fig.add_trace(go.Candlestick(x=df.index, open=df["open"], high=df["high"],
                                 low=df["low"], close=df["close"], name=data.symbol),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['b_band_high'], marker_color='green', name="smma_21"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["b_band_low"], marker_color='red', name="smma_50"), row=1, col=1)
    # fig.add_trace(go.Scatter(x=df.index, y=df["smma_200"], marker_color='brown', name="smma_200"), row=1, col=1)

    ## Volume
    # ---------------------------------------

    fig.add_trace(
        go.Bar(x=df.index, y=df['volume_none'], marker_color=np.where(df['volume'] < 0, 'red', 'green'),
               showlegend=False), row=2, col=1)


    ## MACD
    # ---------------------------------------

    # fig.add_trace(
    #     go.Bar(x=df.index, y=macd['MACDh_12_26_9'], marker_color=np.where(macd['MACDh_12_26_9'] < 0, 'red', 'green'),
    #            showlegend=False), row=2, col=1)
    # fig.add_trace(go.Scatter(x=df.index, y=macd['MACDs_12_26_9'], marker_color='pink', name="macd_signal"), row=2,
    #               col=1)
    # fig.add_trace(go.Scatter(x=df.index, y=macd['MACD_12_26_9'], marker_color='blue', name="macd"), row=2, col=1)

    ## RSI
    # ---------------------------------------
    #
    fig.add_trace(go.Scatter(x=df.index, y=df['rsi_14'], marker_color='pink', name="rsi_14"), row=4,
                  col=1)

    # fig.add_trace(
    #     go.Bar(x=df.index, y=df['fractals_high'], marker_color='green', name="fractals_high"),
    #     row=3, col=1)
    fig.add_trace(
        go.Bar(x=df.index, y=df['result'], marker_color='red',
               name="result"),
        row=3, col=1)

    # fig.add_trace(go.Scatter(x=df.index, y=df['previous_data'], marker_color='pink', name="smma_200_difference"), row=2,
    #               col=1)
    # fig.add_trace(go.Scatter(x=df.index, y=df['atr'], marker_color='pink', name="atr"), row=2,
    #               col=1)

    cs = fig.data[0]

    # Set line and fill colors
    cs.increasing.fillcolor = '#3D9970'
    cs.increasing.line.color = '#3D9970'
    cs.decreasing.fillcolor = '#FF4136'
    cs.decreasing.line.color = '#FF4136'

    fig.update_layout(
        title=data.symbol + ' - ' + data.timeframe,
        xaxis_tickfont_size=12,
        yaxis=dict(
            title='Price ($/share)',
            titlefont_size=14,
            tickfont_size=12,

        ),
        autosize=False,
        width=2500,
        height=1100,
        margin=dict(l=50, r=50, b=100, t=100, pad=4),
        template="plotly_white"
    )

    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.show(config=config)
