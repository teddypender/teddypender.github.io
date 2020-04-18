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
import requests
import json
from fredapi import Fred


"""
Trump & Biden w/ S&P 500

"""

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

region_dict = {
    'Alabama': 'South',
    'Alaska': 'West',
    'American Samoa' : 'West',
    'Arizona':'West',
    'Arkansas':'South',
    'California': 'West',
    'Colorado':'West',
    'Connecticut':'Northeast',
    'Delaware':'South',
    'District of Columbia' : 'South',
    'Florida': 'South',
    'Georgia': 'South',
    'Guam' : 'West',
    'Hawaii': 'West',
    'Idaho': 'West',
    'Illinois': 'Midwest',
    'Indiana': 'Midwest',
    'Iowa': 'Midwest',
    'Kansas': 'Midwest',
    'Kentucky': 'South',
    'Louisiana': 'South',
    'Maine': 'Northeast',
    'Maryland': 'South',
    'Massachusetts': 'Northeast',
    'Michigan': 'Midwest',
    'Minnesota': 'Midwest',
    'Mississippi': 'South',
    'Missouri': 'Midwest',
    'Montana': 'West',
    'Nebraska': 'Midwest',
    'Nevada': 'West',
    'New Hampshire': 'Northeast',
    'New Jersey': 'Northeast',
    'New Mexico': 'West',
    'New York': 'Northeast',
    'North Carolina': 'South',
    'North Dakota': 'Midwest',
    'Northern Mariana Islands' : 'West',
    'Ohio': 'Midwest',
    'Oklahoma': 'South',
    'Oregon': 'West',
    'Pennsylvania': 'Northeast',
    'Puerto Rico' : 'South',
    'Rhode Island': 'Northeast',
    'South Carolina': 'South',
    'South Dakota': 'Midwest',
    'Tennessee': 'South',
    'Texas': 'South',
    'Utah': 'West',
    'Vermont': 'Northeast',
    'Virgin Islands' : 'South',
    'Virginia': 'South',
    'Washington': 'West',
    'West Virginia': 'South',
    'Wisconsin': 'Midwest',
    'Wyoming': 'West'  
}

covid19_url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
covid_cases = requests.get(covid19_url).content
df_COVID = pd.read_csv(io.StringIO(covid_cases.decode('utf-8')))
df_COVID['DateTime'] = [pd.datetime(a[2], a[1], a[0]) for a in [[int(y) for  y in x.split('-')][::-1] for x in df_COVID['date']]]

df_COVID['Region'] = [region_dict[x] for x in df_COVID.state]
df_COVID_Region = df_COVID.groupby(['DateTime', 'Region']).sum()
df_COVID_Region = df_COVID_Region[df_COVID_Region.index.get_level_values('DateTime') >= pd.datetime(2020,3,1)]
df_COVID_Region_PCT = df_COVID_Region[['cases']].groupby(level=0).apply(lambda x: 100 * x / x.sum()).fillna(0).round(2).reset_index()
df_COVID_Region_PCT.rename({'cases' : 'Cases'}, axis = 1, inplace = True)
df_COVID_Region_PCT = df_COVID_Region_PCT.pivot(index='DateTime', columns = 'Region', values = 'Cases').fillna(0).reset_index()
df_COVID = df_COVID.groupby('DateTime').sum()[['cases', 'deaths']]
df_COVID['New Cases'] = df_COVID['cases'].diff().fillna(0)
df_COVID['Death Rate (%)'] = df_COVID['deaths'] / df_COVID['cases'] * 100

df_COVID.rename({'cases' : 'Total Cases'}, axis = 1, inplace = True)
df_COVID = df_COVID[['Total Cases', 'New Cases', 'Death Rate (%)']].reset_index().round(2)
df_COVID = df_COVID[df_COVID.DateTime >= pd.datetime(2020,3,1)]


"""
VIX Percentage Change
"""

VIX = yf.Ticker("^VIX")
VIX = VIX.history(period="max")
idx = pd.date_range(min(VIX.index), max(VIX.index))
VIX = VIX.reindex(idx)
VIX.ffill(inplace = True)
VIX['Close'] = VIX['Close'].pct_change() * 100
VIX = VIX[VIX.index >= pd.datetime(2020,1,15)][['Close']] 
VIX = VIX.round(2)
VIX.reset_index(inplace = True)
VIX.rename({'index' : 'DateTime',
                 'Close' : 'CBOE Volatility Index (VIX)'}, axis = 1, inplace = True)

"""
Brent Crude WTI Weekly Change
"""

BZ = yf.Ticker("BZ=F")
BZ = BZ.history(period="max")
idx = pd.date_range(min(BZ.index), max(BZ.index))
BZ = BZ.reindex(idx)
BZ.ffill(inplace = True)
BZ['Close'] = BZ['Close'].pct_change() * 100
BZ = BZ[BZ.index >= pd.datetime(2020,1,15)][['Close']] 
BZ = BZ.round(2)
BZ.reset_index(inplace = True)
BZ.rename({'index' : 'DateTime',
                 'Close' : 'Brent Crude Oil Last Day Financ (BZ=F)'}, axis = 1, inplace = True)

"""
Unemployment
Unemployment Rate (Seasonally Adjusted) - LNS14000000
"""

headers = {'Content-type': 'application/json'}
data = json.dumps({"seriesid": ['LNS14000000'],"startyear":"2019", "endyear":"2020"})
p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)

json_data = json.loads(p.text)
data = []
for series in json_data['Results']['series']:
    for item in series['data']:
        year = item['year']
        period = item['period']
        value = item['value']
        data.append([year, period, value])
        
Unemployment_df = pd.DataFrame(data = data, columns = ['Year', 'M', 'Unemployment Rate'])
Unemployment_df['Unemployment Rate'] = Unemployment_df['Unemployment Rate'].astype(float)
month = {'M01': '1','M02': '2','M03': '3','M04': '4','M05': '5','M06': '6','M07': '7','M08': '8','M09': '9','M10': '10','M11': '11','M12': '12'}
day = {'M01': '15','M02': '15','M03': '15','M04': '15','M05': '15','M06': '15','M07': '15','M08': '15','M09': '15','M10': '15','M11': '15','M12': '15'}
Unemployment_df['Year'] = Unemployment_df['Year'].astype(int)
Unemployment_df['month'] = [int(month[x]) for x in Unemployment_df.M]
Unemployment_df['day'] = [int(day[x]) for x in Unemployment_df.M]
Unemployment_df['DateTime'] = [pd.datetime(x,y,z) for x,y,z in zip(list(Unemployment_df.Year), list(Unemployment_df.month), list(Unemployment_df.day))]
Unemployment_df_change = Unemployment_df[::-1].copy()
Unemployment_df = Unemployment_df[['DateTime', 'Unemployment Rate']][:-7][::-1]
Unemployment_df_change['Unemployment Rate Change'] = Unemployment_df_change['Unemployment Rate'].pct_change().fillna(0).round(4) * 100
Unemployment_df_change = Unemployment_df_change[['DateTime', 'Unemployment Rate Change']][-7:]
Unemployment_df.rename({'Unemployment Rate' : 'Unemployment Rate (%)'}, axis = 1, inplace = True)
Unemployment_df_change.rename({'Unemployment Rate Change' : 'Unemployment Rate Change (%)'}, axis = 1, inplace = True)


"""
Zillow
ZRI methodology
Rental Statistics
http://files.zillowstatic.com/research/public/Metro/Metro_Zri_MultiFamilyResidenceRental.csv

Top Tier Homes
http://files.zillowstatic.com/research/public/Metro/Metro_Zhvi_TopTier.csv

Bottom Tier Homes
http://files.zillowstatic.com/research/public/Metro/Metro_Zhvi_BottomTier.csv

"""

rent_url = "http://files.zillowstatic.com/research/public/Metro/Metro_Zri_MultiFamilyResidenceRental.csv"
r = requests.get(rent_url).content
Rent_df = pd.read_csv(io.StringIO(r.decode('utf-8'))).T[[0]].drop(['RegionID', 'RegionName', 'SizeRank']).reset_index().rename({0 : 'U.S. Metro Rent - Multi-Family ($)', 'index' : 'DateTime'}, axis = 1,)
Rent_df['DateTime'] = [pd.datetime(a[1], a[0], 1) for a in [[int(y) for  y in x.split('-')][::-1] for x in Rent_df['DateTime']]]
Rent_df = Rent_df[-13:]


top_url = "http://files.zillowstatic.com/research/public/Metro/Metro_Zhvi_TopTier.csv"
p_top = requests.get(top_url).content
Top_Tier_ZHVI = pd.read_csv(io.StringIO(p_top.decode('utf-8'))).T[[0]].drop(['RegionID', 'RegionName', 'SizeRank', 'RegionType', 'StateName']).reset_index().rename({0 : 'Zillow Home Value Index - Top Tier ($)', 'index' : 'DateTime'}, axis = 1,)
Top_Tier_ZHVI['DateTime'] = [pd.datetime(a[2], a[1], a[0]) for a in [[int(y) for  y in x.split('-')][::-1] for x in Top_Tier_ZHVI['DateTime']]]
Top_Tier_ZHVI_Delta =  Top_Tier_ZHVI.copy()  
Top_Tier_ZHVI_Delta['Zillow Home Value Index - Top Tier Change (%)'] = Top_Tier_ZHVI['Zillow Home Value Index - Top Tier ($)'].pct_change() * 100

Top_Tier_ZHVI_Delta = Top_Tier_ZHVI_Delta[['DateTime','Zillow Home Value Index - Top Tier Change (%)']][-13:]
Top_Tier_ZHVI = Top_Tier_ZHVI[-13:]


bottom_url = "http://files.zillowstatic.com/research/public/Metro/Metro_Zhvi_BottomTier.csv"
p_Bottom = requests.get(bottom_url).content
Bottom_Tier_ZHVI = pd.read_csv(io.StringIO(p_Bottom.decode('utf-8'))).T[[0]].drop(['RegionID', 'RegionName', 'SizeRank', 'RegionType', 'StateName']).reset_index().rename({0 : 'Zillow Home Value Index - Bottom Tier ($)', 'index' : 'DateTime'}, axis = 1,)
Bottom_Tier_ZHVI['DateTime'] = [pd.datetime(a[2], a[1], a[0]) for a in [[int(y) for  y in x.split('-')][::-1] for x in Bottom_Tier_ZHVI['DateTime']]]
Bottom_Tier_ZHVI_Delta =  Bottom_Tier_ZHVI.copy()  
Bottom_Tier_ZHVI_Delta['Zillow Home Value Index - Bottom Tier Change (%)'] = Bottom_Tier_ZHVI_Delta['Zillow Home Value Index - Bottom Tier ($)'].pct_change() * 100

Bottom_Tier_ZHVI_Delta = Bottom_Tier_ZHVI_Delta[['DateTime','Zillow Home Value Index - Bottom Tier Change (%)']][-13:]
Bottom_Tier_ZHVI = Bottom_Tier_ZHVI[-13:]


#authorization
gc = pygsheets.authorize(service_file='/Users/theodorepender/Desktop/covid19-dashboard-274000-97b3f9900832.json')

#open the google spreadsheet (where 'COVID Dashboard' is the name of my sheet)
sh = gc.open('COVID Dashboard')

#add worksheets
#sh.add_worksheet('Sheet15')

#get last update time
last_update = gc.drive.get_update_time('1Bs0xB_pUrA3nyloh7mj-NOAe51nKodrEFPff4ijB_OU')[0:10].split('-')
last_update = pd.datetime(int(last_update[0]),int(last_update[1]), int(last_update[2]))

date_time = last_update.strftime("%A, %B %dth")
print("date: ", date_time)

#select the sheet 
wks_trump_sp500 = sh[0]
wks_msci_inx = sh[1]
wks_covid_cases = sh[2]
wks_vix = sh[3]
wks_region = sh[4]
wks_unemployment = sh[5]
wk_unemployment_change = sh[6]
wk_rent = sh[7]
wk_top_tier_index = sh[8]
wk_bottom_tier_index = sh[9]
wk_top_tier_index_change = sh[10]
wk_bottom_tier_index = sh[11]

#update the sheets with the dataframes. 
wks_trump_sp500.set_dataframe(df_polls_sp500,(1,1))
wks_msci_inx.set_dataframe(MSCI_df,(1,1))
wks_covid_cases.set_dataframe(df_COVID,(1,1))
wks_vix.set_dataframe(VIX,(1,1))
wks_region.set_dataframe(df_COVID_Region_PCT,(1,1))
wks_unemployment.set_dataframe(Unemployment_df,(1,1))
wk_unemployment_change.set_dataframe(Unemployment_df_change,(1,1))
wk_rent.set_dataframe(Rent_df,(1,1))
wk_top_tier_index.set_dataframe(Top_Tier_ZHVI,(1,1))
wk_bottom_tier_index.set_dataframe(Bottom_Tier_ZHVI,(1,1))
wk_top_tier_index_change.set_dataframe(Top_Tier_ZHVI_Delta,(1,1))
wk_bottom_tier_index.set_dataframe(Bottom_Tier_ZHVI_Delta,(1,1))


