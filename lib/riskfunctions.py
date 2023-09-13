import math
from sklearn import linear_model
from sklearn.metrics import r2_score
import pickle as pkl
import pandas as pd
import os

# Get Returns Data
home_dir = os.getcwd()
returns_pickle = open(home_dir + "/assets/returns_df_AlphaVantage.pkl", "rb")
returns_df = pkl.load(returns_pickle)

def round_sig(x, sig=2):
    if x==0:
        return 0
    else:
        return round(x, sig - int(math.ceil(math.log10(abs(x)))) - 1)


def est_missing_returns(returns_df=returns_df):
    # Separate which stocks have missing data as the y variables, those without missing as x
    variables = pd.DataFrame(returns_df.isna().sum() == 0)
    x_indep = variables[variables[0].isin([True])]
    y_dep = variables[variables[0].isin([False])]

    # Get the timeseries of each of x and y
    returns_filtered_df = returns_df.dropna(how="any")
    x = returns_filtered_df[x_indep.index.values]
    y = returns_filtered_df[y_dep.index.values]

    # Get the predicted missing y data values based on x
    regr = linear_model.LinearRegression()
    regr.fit(x, y)
    y_predicted = regr.predict(x)
    r2_score(y, y_predicted)

    # Combine estimated and actual y values back together
    returns_exfiltered_df = returns_df[
        ~returns_df.index.isin(returns_filtered_df.index)
    ]
    x_exfiltered = returns_exfiltered_df[x_indep.index.values]
    y_predicted = pd.DataFrame(regr.predict(x_exfiltered), columns=y_dep.index.values)
    all_exfiltered = x_exfiltered
    all_exfiltered[y_dep.index.values] = y_predicted.values

    returns_filled_df = pd.concat([returns_filtered_df, all_exfiltered], axis=0)

    # data=[{'Ticker':'KVUE','$ Amount':100},{'Ticker':'JNJ','$ Amount':200}]
    # updated_df = pd.DataFrame(data)
    return returns_filled_df

if __name__ == "__main__":
    returns_filled_df = est_missing_returns()
    pass

