import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('E:/Python practice/turnstile-usage-data-2018.csv')
    df.columns = df.columns.str.strip()
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df1 = load_data()

# Sidebar - Date filter
st.sidebar.title('Filter Options')
start_date = st.sidebar.date_input('Start date', df1['Date'].min())
end_date = st.sidebar.date_input('End date', df1['Date'].max())
filtered_data = df1[(df1['Date'] >= pd.to_datetime(start_date)) & (df1['Date'] <= pd.to_datetime(end_date))]

# Title
st.title('NYC Turnstile Usage Dashboard')

# Show dataframe
if st.sidebar.checkbox('Show raw data'):
    st.subheader('Raw Data')
    st.write(filtered_data)

# Group by 'Date' and 'Station' to sum entries
grouped_entries = filtered_data.groupby(['Date', 'Station'])['Entries'].sum().reset_index()

# Find the day with the maximum entries for each station
max_entries_per_station = grouped_entries.loc[grouped_entries.groupby('Station')['Entries'].idxmax()]

# Plot maximum entries per station
st.subheader('Maximum Entries per Station on Any Given Day')
plt.figure(figsize=(12, 6))
sns.barplot(x='Station', y='Entries', data=max_entries_per_station)
plt.xticks(rotation=90)
plt.xlabel('Station')
plt.ylabel('Entries')
st.pyplot(plt)

# Sum entries by station
station_entries = filtered_data.groupby('Station')['Entries'].sum().reset_index()

# Top 10 stations by entries
top_10_stations = station_entries.sort_values(by='Entries', ascending=False).head(10)

# Plot top 10 stations by entries
st.subheader('Top 10 Stations by Number of Entries')
plt.figure(figsize=(12, 6))
sns.barplot(x='Station', y='Entries', data=top_10_stations)
plt.xticks(rotation=90)
plt.xlabel('Station')
plt.ylabel('Entries')
st.pyplot(plt)

# Sum exits by station
station_exits = filtered_data.groupby('Station')['Exits'].sum().reset_index()

# Top 10 stations by exits
top_10_stations_exits = station_exits.sort_values(by='Exits', ascending=False).head(10)

# Plot top 10 stations by exits
st.subheader('Top 10 Stations by Number of Exits')
plt.figure(figsize=(12, 6))
sns.barplot(x='Station', y='Exits', data=top_10_stations_exits)
plt.xticks(rotation=90)
plt.xlabel('Station')
plt.ylabel('Exits')
st.pyplot(plt)
