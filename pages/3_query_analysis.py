import streamlit as st
import pandas as pd
import os
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter


st.set_page_config(page_title="Query Analysis", page_icon="🚨")
st.markdown("Query Analysis")
st.title('Query Analysis')

directory = './data/'

def get_file_names(collectedFolder):
    fileNames = []
    for root, dirs, files in os.walk(os.path.join(directory,collectedFolder)):
        for file in files:
            fileNames.append(file)
    return fileNames

def get_queries(fileNames):
    queries = set()
    for fileName in fileNames:
        st.write(fileName)
        queries.add(fileName.split('_')[0])
    return queries

def get_dates(fileNames):
    """
    Returns:
        {query:[trending date]} dictionary
    """
    dct = {}
    for f in fileNames:
        query = f.split('_')[0]
        date = f.split('_')[2].split('@')[-1]
        if query not in dct:
            dct[query] = [date]
        else:
            dct[query].append(date)
    for query in dct:
        dct[query] = sorted(dct[query])
    return dct

collectedDate = 'collected@07-02-16'
fileNames = get_file_names(collectedDate)
data = get_dates(fileNames)
#st.write(get_queries(fileNames))
if st.checkbox(f'Show raw data for {collectedDate}'):
    st.subheader('Raw data')
    st.write(data)

all_dates = []
for query, dates in data.items():
    for date in dates:
        all_dates.append({"query": query, "date": pd.to_datetime(date, format='%m-%d-%H')})

df = pd.DataFrame(all_dates)

fig, ax = plt.subplots(figsize=(12, 8))

colors = plt.cm.tab20(range(len(data)))
color_map = {query: colors[i] for i, query in enumerate(data)}

for query, dates in df.groupby("query"):
    ax.plot_date(dates['date'], [query] * len(dates), 'o', color=color_map[query], label=query)

ax.xaxis.set_major_formatter(DateFormatter('%m-%d-%H'))
plt.xticks(rotation=45)
plt.xlabel('Date')
plt.yticks(range(len(data)), list(data.keys()))
plt.title(f'Timeline of Top 10 Queries Occurrence for {collectedDate}')
plt.grid(True)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

st.pyplot(fig)

st.write("From 6/29 2am to 7/1 9am, query collection stopped due to a technical issue")