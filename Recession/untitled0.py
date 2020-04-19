#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 19:08:09 2020

@author: theodorepender
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from fredapi import Fred
import yfinance as yf
import functools



"""
Functionaility

Variables:
---------
fred_series_ids = {'Non-farm_Payrolls': 'PAYEMS',
                    'Civilian_Unemployment_Rate': 'UNRATE',
                    'Effective_Fed_Funds': 'FEDFUNDS',
                    'CPI_All_Items': 'CPIAUCSL',
                    '10Y_Treasury_Rate': 'GS10',
                    '5Y_Treasury_Rate': 'GS5',
                    '3_Month_T-Bill_Rate': 'TB3MS',
                    'IPI': 'INDPRO'}
yahoo_series_ids = {'S&P_500_Index': '^GSPC'}
primary_dictionary_output = {}
primary_df_output = pd.DataFrame()
shortest_series_name = ''
shortest_series_length = 1000000
secondary_df_output = pd.DataFrame()
"""

def getFredData(fred_series_ids, primary_dictionary_output):
    
    fred = Fred(api_key='e0e39002ebdae285ab9269213a68ccda')

        
    now = datetime.datetime.now()
    month = now.strftime('%m')
    year = now.year        
    most_recent_date = '{}-{}-07'.format(year, month)
    print('\nGetting data from FRED\'s API as of {}...'.format(most_recent_date))
    
    for series_name in list(fred_series_ids.keys()):
        series_id = fred_series_ids[series_name]
        print('\t|--Getting data for {}({}).'.format(series_name, series_id))
          
        data = fred.get_series(series_id)
        primary_dictionary_output[series_name] = pd.DataFrame(data).rename({0 : series_name}, axis = 1)
        
    return primary_dictionary_output

def getYahooData(yahoo_series_ids, primary_dictionary_output):
         
    print('\nGetting data from Yahhoo\'s API ...')
    
    for series_name in list(yahoo_series_ids.keys()):
        series_id = yahoo_series_ids[series_name]
        print('\t|--Getting data for {}({}).'.format(series_name, series_id))
         
        data = yf.Ticker(series_id).history(period="max")[['Close']].rename({'Close' : 'SP500'}, axis = 1)
        data.index = list(data.reset_index().Date)
        primary_dictionary_output[series_name] = data
        
    return primary_dictionary_output
    


if __name__ == "__main__":
    
    fred_series_ids = {'Non-farm_Payrolls': 'PAYEMS',
                        'Civilian_Unemployment_Rate': 'UNRATE',
                        'Effective_Fed_Funds': 'FEDFUNDS',
                        'CPI_All_Items': 'CPIAUCSL',
                        '10Y_Treasury_Rate': 'GS10',
                        '5Y_Treasury_Rate': 'GS5',
                        '3_Month_T-Bill_Rate': 'TB3MS',
                        'IPI': 'INDPRO'}
    yahoo_series_ids = {'S&P_500_Index': '^GSPC'}
    primary_dictionary_output = {}
    primary_df_output = pd.DataFrame()
    shortest_series_name = ''
    shortest_series_length = 1000000
    secondary_df_output = pd.DataFrame()
    
    
    getFredData(fred_series_ids, primary_dictionary_output)
    getYahooData(yahoo_series_ids, primary_dictionary_output)
    
    df = pd.concat([primary_dictionary_output[series_name] for series_name in primary_dictionary_output.keys()], axis = 1).ffill()
    
