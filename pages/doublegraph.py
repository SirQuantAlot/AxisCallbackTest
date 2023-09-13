from os import environ

import pickle as pkl
import dash
import dash_mantine_components as dmc
from dash import html, dash_table,html, dcc, callback, Output, Input
import pandas as pd
import plotly.graph_objects as go
from dash_iconify import DashIconify
import callbacks
from datetime import datetime

dash.register_page(
    __name__,
    "/doublegraph",
    title="doublegraph",
)

def layout():
    return dmc.Container(
    [
        html.Br(),
        dmc.Grid(
            [
                dmc.Title("Portfolio PnL", color="blue", size="h4"),
                dmc.Col([dcc.Graph(id="constant_portfolio_pnl")]),
                html.Br(),
                dmc.Title("Daily Returns", color="blue", size="h4"),
                dmc.Col([dcc.Graph(id="positions_rtns_scatter")]),
            ]
        ),
    ]
)

