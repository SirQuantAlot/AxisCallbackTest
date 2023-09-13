# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 16:10:41 2023

@author: asgre
"""

import pandas as pd
import pickle as pkl
import numpy as np
import plotly.graph_objects as go
from dash import callback, Input, Output, State, exceptions
import lib.riskfunctions as rf
import pickle as pkl
from dash.exceptions import PreventUpdate
import os

# Get Returns Data
home_dir = os.getcwd()
returns_pickle = open(home_dir + "/assets/returns_df_AlphaVantage.pkl", "rb")
returns_df = pkl.load(returns_pickle)

# insert into table
@callback(
    Output("adding-rows-table", "data"),
    Input("editing-rows-button", "n_clicks"),
    State("adding-rows-table", "data"),
    State("adding-rows-table", "columns"),
)
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.insert(0, {c["name"]: 0 for c in columns})
    return rows


#Create/ Update pnl chart
@callback(
    [
        Output("constant_portfolio_pnl", "figure"),
        Output("store_constant_portfolio_pnl_df", "data"),
    ],
    [
        Input("positions_store", "data"),
        Input("store_positions_rtns_scatter_df", "data"),
        Input("positions_rtns_scatter", "figure"),
    ],
)
def graph_constant_portfolio_pnl(data, df, fig):
    if sum([abs(pd.to_numeric(row["$ Amount"])) for row in data]) == 0:
        return go.Figure(), {}
    else:
        returns_df = rf.est_missing_returns()
        perf_df = pd.DataFrame(index=returns_df.index)
        for row in data:
            perf_df[row["Ticker"]] = float(row["$ Amount"]) * returns_df[row["Ticker"]]

        try:
            print("trying...")
            print(fig["layout"]["xaxis"]["range"])
            df = pd.DataFrame(index=df["index"], data=df["data"], columns=df["columns"])
            df.index = pd.to_datetime(df.index, format="%Y-%m-%d")
            print(fig)
            print(fig["layout"]["xaxis"]["range"][0])
            if fig["layout"]["xaxis"]["range"][0] in fig:
                print('fig["layout"]["xaxis"]["range"][0]:')
                print(fig["layout"]["xaxis"]["range"][0])
                xmin, xmax =  fig["layout"]["xaxis"]["range"][0], fig["layout"]["xaxis"]["range"][1]
                mask = (df == xmin).any(axis=1)
                dmin = df.index[mask].tolist()
                mask = (df == xmax).any(axis=1)
                dmax = df.index[mask].tolist()
                print(dmin)
                print(dmax)
            else:
                pass
                perf_df.index = pd.to_datetime(perf_df.index, format="%Y-%m-%d")
                perf_df = perf_df[dmin:dmax]
        except:
            pass

        fig = go.Figure()
        for stock in perf_df.columns.values:
            print("About to graph...")
            y = perf_df.loc[:, stock]
            x = perf_df.index.values
            fig.add_trace(
                go.Bar(
                    name=stock,
                    y=y,
                    x=x,
                )
            )
        fig.update_layout(barmode="stack")
        fig.layout.plot_bgcolor = "#fff"
        fig.layout.paper_bgcolor = "#fff"
    return fig, perf_df.to_dict("tight")

#Create/ Update scatter chart
@callback(
    [
        Output("positions_rtns_scatter", "figure"),
        Output("store_positions_rtns_scatter_df", "data"),
    ],
    Input("positions_store", "data"),
)
def positions_rtns_scatter(data):
    if sum([abs(pd.to_numeric(row["$ Amount"])) for row in data]) == 0:
        return go.Figure(), {}
    else:
        returns_df = rf.est_missing_returns()
        perf_df = pd.DataFrame(index=returns_df.index)
        print("positions_rtns_scatter:", perf_df)
        for row in data:
            perf_df[row["Ticker"]] = returns_df[row["Ticker"]]
        fig = go.Figure()
        for stock in perf_df.columns.values:
            y = perf_df.loc[:, stock]
            x = perf_df.index.values
            z = perf_df.loc[:, stock] - perf_df.mean(axis=1)
            fig.add_trace(
                go.Scatter(
                    name=stock,
                    y=z,
                    x=y,
                    mode="markers",
                    # z=z
                )
            )
        fig.update_layout(yaxis_tickformat="0.0%")
        fig.update_layout(xaxis_tickformat="0.0%")
        fig.update_layout(xaxis_title="Position Return", yaxis_title="Alpha Return")
        fig.layout.plot_bgcolor = "#fff"
        fig.layout.paper_bgcolor = "#fff"
    return fig, perf_df.to_dict("tight")


# Saving Data
@callback(
    Output("positions_store", "data"),
    [Input("editing-rows-button", "n_clicks"), Input("adding-rows-table", "data")],
)
def save_test_data(n, data):
    print("Saving data...")
    print(data)
    print(type(data))
    return data