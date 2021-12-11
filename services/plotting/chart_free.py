import numpy as np
import plotly.graph_objects as go

config = dict({'scrollZoom': True})


# noinspection PyTypeChecker
def draw_free_chart(df):
    from plotly.subplots import make_subplots
    fig = make_subplots(rows=4, cols=1, shared_xaxes=True,
                        vertical_spacing=0.01, subplot_titles=("Free Style", 'volume'),
                        row_width=[.5, .5, .5, 1.5])

    fig.add_trace(go.Candlestick(x=df.index, open=df["open"], high=df["high"],
                                 low=df["low"], close=df["close"], name="Free"),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['next_close'], marker_color='green', name="smma_21"), row=1, col=1)

    # ---------------------------------------
    # RSI
    # for i in [500, 200, 100, 50, 25, 14, 5, 2, 1]:
    #     fig.add_trace(
    #         go.Scatter(x=df.index, y=df[f'rsi_{i}'], marker_color=np.where(df['volume'] < 0, 'red', 'green'),
    #                showlegend=False), row=2, col=1)

    #
    # fig.add_trace(
    #     go.Bar(x=df.index, y=df['volume_none'], marker_color=np.where(df['volume'] < 0, 'red', 'green'),
    #            showlegend=False), row=2, col=1)
    #
    #
    # MACD
    # ---------------------------------------

    fig.add_trace(go.Bar(x=df.index, y=df['next_close']-df['close'], marker_color=np.where((df['next_close']-df['close']) < 0, 'red', 'green'), name="macd_signal"), row=2,
                  col=1)

    #


    cs = fig.data[0]

    # Set line and fill colors
    cs.increasing.fillcolor = '#3D9970'
    cs.increasing.line.color = '#3D9970'
    cs.decreasing.fillcolor = '#FF4136'
    cs.decreasing.line.color = '#FF4136'

    fig.update_layout(
        title="Free Style",
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
    return fig
def update_free_chart(df, fig):
    fig.data[1].y=df['next_close']
