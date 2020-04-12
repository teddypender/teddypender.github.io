#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 11:37:43 2020

@author: theodorepender
"""

import pandas as pd
import io
import requests
import yfinance as yf
import pygsheets


approval_url = "https://projects.fivethirtyeight.com/trump-approval-data/approval_polllist.csv"
s = requests.get(approval_url).content
c = pd.read_csv(io.StringIO(s.decode('utf-8')))
c['DateTime'] = [pd.datetime(a[0], a[2], a[1]) for a in [[int(y) for  y in x.split('/')][::-1] for x in c['enddate']]]
df_approval = c.groupby(['DateTime']).median()[['adjusted_approve', 'adjusted_disapprove']]
df_approval = df_approval[df_approval.index >= pd.datetime(2020,1,15)].round(2)
df_approval.rename({'adjusted_approve' : 'Approval (%)',
                    'adjusted_disapprove' : 'Disapproval (%)'}, axis = 1, inplace = True)
df_approval.reset_index(inplace = True)


sp500 = yf.Ticker("^GSPC")

# get historical market data
df_sp500 = sp500.history(period="max")
idx = pd.date_range(min(df_approval.DateTime), max(df_approval.DateTime))

df_sp500 = df_sp500.reindex(idx)
df_sp500.ffill(inplace = True)

df_sp500 = df_sp500[df_sp500.index >= pd.datetime(2020,1,15)][['Close']] /df_sp500['Close'].iloc[0] * 100
df_sp500 = df_sp500.round(2)
df_sp500.reset_index(inplace = True)
df_sp500.rename({'index' : 'DateTime',
                 'Close' : 'S&P 500 (re-based to 100 at 1/15/20)'}, axis = 1, inplace = True)

df_trump_sp500 = pd.merge(df_approval, df_sp500, on = 'DateTime')

#authorization
gc = pygsheets.authorize(service_file='/Users/theodorepender/Documents/Github/teddypender.github.io/covid_dashboard/covid19-dashboard-274000-97b3f9900832.json')

#open the google spreadsheet (where 'COVID Dashboard' is the name of my sheet)
sh = gc.open('COVID Dashboard')

#select the first sheet 
wks = sh[0]

#update the first sheet with df, starting at cell B2. 
wks.set_dataframe(df_trump_sp500,(1,1))
