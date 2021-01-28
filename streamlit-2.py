from numpy.core.fromnumeric import _all_dispatcher
import streamlit as st
import pandas as pd
import numpy as np
import datetime
from datetime import date

df = pd.read_csv('Copy of FK Data_Power BI_12_01_2020.csv')

df['Confirmation date'] = pd.to_datetime(df['Confirmation date'])
df['Creation Date'] = pd.to_datetime(df['Creation Date'])
df['Confirmation date'] = df['Confirmation date'].dt.date


df = df.drop(['Transfer Order Number', 'Transfer order item', 'Source storage unit','Filler', 'Storage Unit Type','Alternative Unit of Measure','Queue','Dest.Storage Bin','Filler.1'], axis=1)

conditions = [
    (df['Source Storage Type']=='P01') | (df['Source Storage Type']=='P04'),
    (df['Source Storage Type']=='S21') | (df['Source Storage Type']=='S22'),
    (df['Source Storage Type']=='P08') | (df['Source Storage Type']=='P07') | (df['Source Storage Type']=='P05')
    ]
choices = ['SMP1', 'B1P2', 'B1P1']
df['Size'] = np.select(conditions, choices)

df.groupby(['Confirmation date', 'Size'])['Dest.storage unit'].nunique()

st.dataframe(df)

# add_date_sidebar = st.sidebar.slider('Select Confirmation Date', 3/1/20, 12/31/21, (11/1/20, 3/1/21)) 
#########################################
min_date = datetime.datetime(2019, 6,6)
max_date = datetime.datetime(2021,12,31)

date1 = st.sidebar.date_input(
     "Select Confirmation Date Range",
    (min_date, max_date))

"The date range selected:", date1
"The type", type(date1)
"Singling out a date for dataframe filtering", date1[0]
"Singling out a date for dataframe filtering", date1[1]


date_range = df[(df['Confirmation date']>date1[0]) & (df['Confirmation date']<date1[1])]
st.dataframe(date_range)





###############################################
date2 = st.sidebar.date_input(
     "Select Confirmation Date",
    datetime.date(2019, 7, 6))

st.write(date2)
filtered = df[df['Confirmation date'] == date2]

st.dataframe(filtered)
###########

""" filtered2 =  df[(df['Confirmation date']==datetime.datetime(2020,12,1))]
st.write(filtered2) """