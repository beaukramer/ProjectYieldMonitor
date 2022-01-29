import pandas as pd
import pandas_datareader as pdr
import numpy as np
import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta
from create_plots import create_yield_monitor_plots


def yield_monitor(tickers, api_key):
    start_date = date.today() - relativedelta(years=7, days=1)
    equity_tickers = list(tickers['EQ'].keys())
    fi_tickers = list(tickers['FI'].keys())
    div = pd.DataFrame()
    close = pd.DataFrame()
    for ticker in equity_tickers + fi_tickers:
        data = pdr.DataReader(ticker, 'tiingo', start='2000-01-01', end=date.today(), api_key=api_key).loc[:,
               ['divCash', 'adjClose']].reset_index(level=0, drop=True)
        div[ticker] = data['divCash'].copy()
        close[ticker] = data['adjClose'].copy()
    div.set_index(div.index.tz_convert(None), inplace=True)
    close.set_index(close.index.tz_convert(None), inplace=True)
    # change to getting ttm values. logic should be something like, sum the last 4 nonzero values
    div[equity_tickers] = div[equity_tickers].apply(lambda x: x[x != 0.].rolling(4).sum()).fillna(method='ffill')
    div[fi_tickers] = div[fi_tickers].apply(lambda x: x[x != 0.].rolling(12).sum()).fillna(method='ffill')
    div.fillna(method='ffill', inplace=True)
    div.dropna(inplace=True)
    close.dropna(inplace=True)
    div = div.loc[start_date:].copy()
    close = close.loc[start_date-relativedelta(days=60):].copy()
    yld = div/close
    yld.dropna(inplace=True)
    yld.rename(columns=tickers['EQ'],inplace=True)
    yld.rename(columns=tickers['FI'], inplace=True)
    return yld




if __name__ == "__main__":
    # initialize ArgumentParser class of argparse
    st.title('Yield Monitor')
    st.markdown("Yield monitor is a simple script that shows current asset class yields in context of the last 7 "
                "years. It is a quick way of seeing of where an asset's yield is relative to its own history and "
                "other assets.")
    # api_key = os.environ['API_KEY']
    api_key = st.secrets['TIINGO_API_KEY']

    # run the fold specified by command line arguments
    # tickers = list(args.tickers.split(','))
    tickers = {'EQ': {'VYM': 'US High Dividend', 'AMLP': 'MLP', 'VNQ': 'US REIT'},
               'FI': {'HYG': 'US High Yield', 'LQD': 'US Corporate', 'BKLN': 'Leverage Loans', 'VWOB': 'EM Sovereign',
                      'CEMB': 'EM Corporate'}}
    df = yield_monitor(tickers, api_key)
    fig = create_yield_monitor_plots(df)
    st.plotly_chart(fig)

