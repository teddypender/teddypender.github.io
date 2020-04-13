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
from functools import reduce


"""
Trump w/ S&P 500

"""
#approval_url = "https://projects.fivethirtyeight.com/trump-approval-data/approval_polllist.csv"
# "https://projects.fivethirtyeight.com/polls-page/president_polls.csv"
#s = requests.get(approval_url).content
#c = pd.read_csv(io.StringIO(s.decode('utf-8')))
#c['DateTime'] = [pd.datetime(a[0], a[2], a[1]) for a in [[int(y) for  y in x.split('/')][::-1] for x in c['enddate']]]
#df_approval = c.groupby(['DateTime']).median()[['adjusted_approve', 'adjusted_disapprove']]
#df_approval = df_approval[df_approval.index >= pd.datetime(2020,1,15)].round(2)
#df_approval.rename({'adjusted_approve' : 'Approval (%)',
#                    'adjusted_disapprove' : 'Disapproval (%)'}, axis = 1, inplace = True)
#df_approval.reset_index(inplace = True)
#df_approval['Approval (%)'] = df_approval['Approval (%)'] / df_approval['Approval (%)'].iloc[0] * 100
#df_approval['Disapproval (%)'] = df_approval['Disapproval (%)'] / df_approval['Disapproval (%)'].iloc[0] * 100

trump_poll = "https://projects.fivethirtyeight.com/polls-page/president_polls.csv"
s = requests.get(trump_poll).content
c = pd.read_csv(io.StringIO(s.decode('utf-8')))
c = c[(c.stage == 'general') & (c.answer.isin(['Biden', 'Trump']))]
c['DateTime'] = [pd.datetime(int('20' + str(a[0])), a[2], a[1]) for a in [[int(y) for  y in x.split('/')][::-1] for x in c['end_date']]]
df_polling = c.groupby(['DateTime', 'answer']).median()[['pct']]
df_polling.reset_index(inplace = True)
df_polling = df_polling[df_polling.DateTime >= pd.datetime(2020,1,1)].round(2)
df_polling = df_polling.pivot(index='DateTime', columns = 'answer', values = 'pct')
idx = pd.date_range(min(df_polling.index), max(df_polling.index))
df_polling = df_polling.reindex(idx)
df_polling.ffill(inplace = True)
df_polling.bfill(inplace = True)
df_polling['Biden'] = df_polling['Biden'].rolling(window = 7).mean()
df_polling['Trump'] = df_polling['Trump'].rolling(window = 7).mean()
df_polling = df_polling[df_polling.index >= pd.datetime(2020,1,15)].round(2)
df_polling.rename({'Biden' : 'Biden Poll (%)',
                    'Trump' : 'Trump Poll (%)'}, axis = 1, inplace = True)
df_polling['Biden Poll (%)'] = df_polling['Biden Poll (%)'] / df_polling['Biden Poll (%)'].iloc[0] * 100
df_polling['Trump Poll (%)'] = df_polling['Trump Poll (%)'] / df_polling['Trump Poll (%)'].iloc[0] * 100


df_polling.reset_index(inplace = True)
df_polling.rename({'index' : 'DateTime'}, axis = 1, inplace = True)

sp500 = yf.Ticker("^GSPC")
# get historical market data
df_sp500 = sp500.history(period="max")
idx = pd.date_range(min(df_sp500.index), max(df_sp500.index))

df_sp500 = df_sp500.reindex(idx)
df_sp500.ffill(inplace = True)

df_sp500 = df_sp500[(df_sp500.index >= pd.datetime(2020,1,15)) & (df_sp500.index <= max(df_polling.DateTime))][['Close']] 
df_sp500['Close'] = df_sp500['Close'] / df_sp500['Close'].iloc[0] * 100
df_sp500 = df_sp500.round(2)
df_sp500.reset_index(inplace = True)
df_sp500.rename({'index' : 'DateTime',
                 'Close' : 'S&P 500 (re-based to 100 at 1/15/20)'}, axis = 1, inplace = True)

df_polls_sp500 = pd.merge(df_polling, df_sp500, on = 'DateTime')

"""
MSCI Indicators

"""

#MSCI USA IMI Energy Index (FENY)
#MSCI USA IMI Materials Index (FMAT)
#MSCI USA IMI Industrials Index (FIDU)
#MSCI USA IMI Consumer Staples Index (FSTA)
#MSCI USA IMI Health Care Index (FHLC)
#MSCI USA IMI Financials Index (FNCL)


MSCI_EI = yf.Ticker("FENY")
MSCI_EI = MSCI_EI.history(period="max")
idx = pd.date_range(min(MSCI_EI.index), max(MSCI_EI.index))
MSCI_EI = MSCI_EI.reindex(idx)
MSCI_EI.ffill(inplace = True)
MSCI_EI = MSCI_EI[MSCI_EI.index >= pd.datetime(2020,1,15)][['Close']]
MSCI_EI['Close'] = MSCI_EI['Close'] / MSCI_EI['Close'].iloc[0] * 100
MSCI_EI = MSCI_EI.round(2)
MSCI_EI.reset_index(inplace = True)
MSCI_EI.rename({'index' : 'DateTime',
                 'Close' : 'MSCI USA IMI Energy Index (FENY)'}, axis = 1, inplace = True)


MSCI_MI = yf.Ticker("FMAT")
MSCI_MI = MSCI_MI.history(period="max")
idx = pd.date_range(min(MSCI_MI.index), max(MSCI_MI.index))
MSCI_MI = MSCI_MI.reindex(idx)
MSCI_MI.ffill(inplace = True)
MSCI_MI = MSCI_MI[MSCI_MI.index >= pd.datetime(2020,1,15)][['Close']]
MSCI_MI['Close'] = MSCI_MI['Close'] / MSCI_MI['Close'].iloc[0] * 100
MSCI_MI = MSCI_MI.round(2)
MSCI_MI.reset_index(inplace = True)
MSCI_MI.rename({'index' : 'DateTime',
                 'Close' : 'MSCI USA IMI Materials Index (FMAT)'}, axis = 1, inplace = True)


MSCI_II = yf.Ticker("FIDU")
MSCI_II = MSCI_II.history(period="max")
idx = pd.date_range(min(MSCI_II.index), max(MSCI_II.index))
MSCI_II = MSCI_II.reindex(idx)
MSCI_II.ffill(inplace = True)
MSCI_II = MSCI_II[MSCI_II.index >= pd.datetime(2020,1,15)][['Close']]
MSCI_II['Close'] = MSCI_II['Close'] / MSCI_II['Close'].iloc[0] * 100
MSCI_II = MSCI_II.round(2)
MSCI_II.reset_index(inplace = True)
MSCI_II.rename({'index' : 'DateTime',
                 'Close' : 'MSCI USA IMI Industrials Index (FIDU)'}, axis = 1, inplace = True)


MSCI_CSI = yf.Ticker("FSTA")
MSCI_CSI = MSCI_CSI.history(period="max")
idx = pd.date_range(min(MSCI_CSI.index), max(MSCI_CSI.index))
MSCI_CSI = MSCI_CSI.reindex(idx)
MSCI_CSI.ffill(inplace = True)
MSCI_CSI = MSCI_CSI[MSCI_CSI.index >= pd.datetime(2020,1,15)][['Close']]
MSCI_CSI['Close'] = MSCI_CSI['Close'] / MSCI_CSI['Close'].iloc[0] * 100
MSCI_CSI = MSCI_CSI.round(2)
MSCI_CSI.reset_index(inplace = True)
MSCI_CSI.rename({'index' : 'DateTime',
                 'Close' : 'MSCI USA IMI Consumer Staples Index (FSTA)'}, axis = 1, inplace = True)


MSCI_HCI = yf.Ticker("FHLC")
MSCI_HCI = MSCI_HCI.history(period="max")
idx = pd.date_range(min(MSCI_HCI.index), max(MSCI_HCI.index))
MSCI_HCI = MSCI_HCI.reindex(idx)
MSCI_HCI.ffill(inplace = True)
MSCI_HCI = MSCI_HCI[MSCI_HCI.index >= pd.datetime(2020,1,15)][['Close']] 
MSCI_HCI['Close'] = MSCI_HCI['Close'] / MSCI_HCI['Close'].iloc[0] * 100
MSCI_HCI = MSCI_HCI.round(2)
MSCI_HCI.reset_index(inplace = True)
MSCI_HCI.rename({'index' : 'DateTime',
                 'Close' : 'MSCI USA IMI Health Care Index (FHLC)'}, axis = 1, inplace = True)


MSCI_FI = yf.Ticker("FNCL")
MSCI_FI = MSCI_FI.history(period="max")
idx = pd.date_range(min(MSCI_FI.index), max(MSCI_FI.index))
MSCI_FI = MSCI_FI.reindex(idx)
MSCI_FI.ffill(inplace = True)
MSCI_FI = MSCI_FI[MSCI_FI.index >= pd.datetime(2020,1,15)][['Close']] 
MSCI_FI['Close'] = MSCI_FI['Close'] / MSCI_FI['Close'].iloc[0] * 100
MSCI_FI = MSCI_FI.round(2)
MSCI_FI.reset_index(inplace = True)
MSCI_FI.rename({'index' : 'DateTime',
                 'Close' : 'MSCI USA IMI Financials Index (FNCL)'}, axis = 1, inplace = True)

dfIndexList = [MSCI_EI, MSCI_MI, MSCI_II, MSCI_CSI, MSCI_HCI, MSCI_FI]
MSCI_df = reduce(lambda x, y: pd.merge(x, y, on = 'DateTime'), dfIndexList)

"""
Coronavirus cases

"""
covid19_url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
covid_cases = requests.get(covid19_url).content
df_COVID = pd.read_csv(io.StringIO(covid_cases.decode('utf-8')))
df_COVID['DateTime'] = [pd.datetime(a[2], a[1], a[0]) for a in [[int(y) for  y in x.split('-')][::-1] for x in df_COVID['date']]]
df_COVID = df_COVID.groupby('DateTime').sum()[['cases', 'deaths']]
df_COVID['New Cases'] = df_COVID['cases'].diff().fillna(0)
df_COVID['Death Rate (%)'] = df_COVID['deaths'] / df_COVID['cases'] * 100

df_COVID.rename({'cases' : 'Total Cases'}, axis = 1, inplace = True)
df_COVID = df_COVID[['Total Cases', 'New Cases', 'Death Rate (%)']].reset_index().round(2)


#authorization
gc = pygsheets.authorize(service_file='/Users/theodorepender/Desktop/covid19-dashboard-274000-97b3f9900832.json')

#open the google spreadsheet (where 'COVID Dashboard' is the name of my sheet)
sh = gc.open('COVID Dashboard')

#add worksheets
#sh.add_worksheet('Sheet3')

#select the sheet 
wks_trump_sp500 = sh[0]
wks_msci_inx = sh[1]
wks_covid_cases = sh[2]

#update the sheets with the dataframes. 
wks_trump_sp500.set_dataframe(df_polls_sp500,(1,1))
wks_msci_inx.set_dataframe(MSCI_df,(1,1))
wks_covid_cases.set_dataframe(df_COVID,(1,1))



