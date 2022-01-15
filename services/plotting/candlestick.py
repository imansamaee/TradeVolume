# import numpy as np
import pandas as pd
import plotly.graph_objects as go

from services.data.data_object import DataObject

# config = dict({'scrollZoom': True})


# noinspection PyTypeChecker
def draw_chart(data_object: DataObject):
    print("done!..")
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
    print("done!....")
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                         open=df['AAPL.Open'],
                                         high=df['AAPL.High'],
                                         low=df['AAPL.Low'],
                                         close=df['AAPL.Close'])])

    fig.show()
    print("done!.55.")