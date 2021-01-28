from numpy.core.fromnumeric import _all_dispatcher
import streamlit as st
import pandas as pd
import numpy as np
import datetime
from datetime import date
import matplotlib.pyplot as plt
import plotly.express as px

st.title("DHL/BMW Packing Data Analysis")

##########################
# Data manipulation - Start
##########################
df = pd.read_csv('Copy of FK Data_Power BI_12_01_2020.csv')

df['Confirmation date'] = pd.to_datetime(df['Confirmation date'])
df['Creation Date'] = pd.to_datetime(df['Creation Date'])
df['Confirmation date'] = df['Confirmation date'].dt.date
df['Dest.storage unit'] = df['Dest.storage unit'].astype(object)

df = df.drop(['Transfer Order Number', 'Transfer order item', 'Source storage unit','Filler', 'Storage Unit Type','Alternative Unit of Measure','Queue','Dest.Storage Bin','Filler.1'], axis=1)

conditions = [
    (df['Source Storage Type']=='P01') | (df['Source Storage Type']=='P04'),
    (df['Source Storage Type']=='S21') | (df['Source Storage Type']=='S22'),
    (df['Source Storage Type']=='P08') | (df['Source Storage Type']=='P07') | (df['Source Storage Type']=='P05')
    ]
choices = ['SMP1 (Small and Med)', 'B1P2 (Glass/Lines)', 'B1P1 (Med/Large)']
df['Size'] = np.select(conditions, choices)

group = df.groupby(['Confirmation date', 'Size'])['Dest.storage unit'].nunique()

st.header('Source Storage Summary by Date')
st.dataframe(group)

####### Date Range Picker - Start ##########
min_date = datetime.datetime(2019, 6,6)
max_date = datetime.datetime(2021,12,31)

date1 = st.sidebar.date_input(
     "Select Confirmation Date Range",
    (min_date, max_date))

########## Filtering dataframe by date range ####
date_range = df[(df['Confirmation date']>date1[0]) & (df['Confirmation date']<date1[1])]
st.header('Date Filtered Dataset')
st.dataframe(date_range)

######### Pivot ###############
st.header('Pivot by Size and Date')
pivot = pd.pivot_table(df, values=['Dest.storage unit'], index=['Confirmation date'], columns=['Size'], aggfunc=pd.Series.nunique, fill_value=0)
st.dataframe(pivot)

######## Groupby Table ############
st.header('Bar Chart by Size')
group4 = df.groupby(['Size'])['Dest.storage unit'].nunique().reset_index()
st.dataframe(group4)

####### Groupby Chart #################
st.header('Bar Chart by Size')
fig3 = px.bar(group4,
                y='Dest.storage unit',
                x='Size',
                color = 'Size'            
             )
st.write(fig3)

########### 2nd Version of Groupby Chart ##########
st.header('Groupby Chart 3')
dfg = df.groupby('Size')['Dest.storage unit'].count()
fig12 = px.bar(x = dfg.index, y = dfg)
st.write(fig12)

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
# To read file as bytes:
#    bytes_data = uploaded_file.read()
#    st.write(bytes_data)
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)