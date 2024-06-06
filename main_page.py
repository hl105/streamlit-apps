import streamlit as st

st.markdown("Google Top Stories: 2020 Elections breakdown by Candidate")
st.sidebar.markdown("# main page: by candidate")

import streamlit as st
import pandas as pd
import numpy as np
import os
from collections import Counter



st.title('2020 Elections Google Top Stories')

option = st.selectbox(
   "Which candidate are you interested in? Choose to continue '◡'",
   ("Joe Biden", "Bernie Sanders", "Kamala Harris", "Beto O Rourke", "Elizabeth Warren","Amy Klobuchar", "Kristen Gillibrand","Pete Buttigieg",
"Cory Booker",
"Julian Castro",
"Tulsi Gabbard",
"Andrew Yang",
"John Hickenlooper",
"Jay Inslee",
"Seth Moulton",
"Michael Bloomberg",
"Tim Ryan",
"Eric Swalwell",
"Deval Patrick",
"Tom Steyer",
"Steve Bullock",
"Howard Schultz",
"Marianne Williamson",
"Mike Gravel",
"Wayne Messam",
"Bill Weld",
"John Delaney",
"Michael Bennet",
"Bill de Blasio","Donald Trump"),
   index=None,
   placeholder="Select a candidate",
)
st.write("You selected:", option)

if not option:
    st.write(':violet[you need to select a candidate to continue]')

if option:


    DATE_COLUMN = 'date'

    def load_data():
        json_file_name = os.path.join(os.getcwd(), 'data', 'candidates-stories', f'{option}.json')
        data = pd.read_json(json_file_name)
        data.style.hide(axis="index")
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis='columns', inplace=True)
        data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN]).dt.date
        return data

    data = load_data()

    if st.checkbox(f'Show raw data for {option}'):
        st.subheader('Raw data')
        st.write(data)


    date_to_filter = st.slider('select date', data[DATE_COLUMN].min(), data[DATE_COLUMN].max(), data[DATE_COLUMN].min())  # min: 0h, max: 23h, default: 17h
    filtered_data = data[data[DATE_COLUMN] == date_to_filter]
    st.subheader(f'Top Stories for query "{option}" on {date_to_filter}')

    st.write(':violet[By source name]')
    grouped_sources = filtered_data.groupby('story_position')['source'].apply(list).reset_index()
    st.dataframe(grouped_sources, hide_index=True)

    st.divider()

    st.write(':violet[By article title]')
    grouped_title = filtered_data.groupby('story_position')['title'].apply(list).reset_index()
    st.dataframe(grouped_title, hide_index=True)

    st.subheader(f'Top 20 Sources in the upper positions for {option}')
    st.write('upper position means the top 1,2,3, positions on the Top Stories panel')
    source_counter = Counter(data[data['story_position']>3]['source'])
    df_upper_sources = pd.DataFrame(source_counter.most_common(20),columns=['source','count'])
    st.bar_chart(df_upper_sources, x='source',y='count')