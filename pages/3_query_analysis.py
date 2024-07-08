import streamlit as st
import pandas as pd
import os
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from wordcloud import WordCloud

st.set_page_config(page_title="Query Analysis", page_icon="🚨")
st.markdown("Query Analysis")
st.title('Query Analysis')

###### FUNCTIONS ######

### POLITCIAL QUERIES FUNCTIONS ###
def get_df_list(directory):
    """
    Returns:
        a tuple of (name, dataframe) in the directory
    """
    df_list = []
    for root , dirs, files in os.walk(directory):
        for file in sorted(files):
            file_path = os.path.join(root, file)
            df_list.append((file, pd.read_csv(file_path)))
    return df_list 

@st.cache_data
def plot_dataframe(df_index):
    df = df_list[df_index][1]
    df.drop(columns=[df.columns[0]], inplace=True)
    df.sort_values(by=["count"])
    df = df.head(20)
    df.rename(columns={"raw-group":"Google Real-Time Trends Cluster", "summarized-query":"paraphrased query"}, inplace=True)

    df['date'] = df['csvFilePath'].apply(lambda x: [pd.to_datetime(filepath.split('/')[-1].split('_')[2].split('@')[-1], format='%m-%d-%H') for filepath in list(x.split(','))])
    df.drop(columns=['csvFilePath', 'platformDirPath'], inplace=True)

    df_query_date = df[['paraphrased query', 'date']]
    fig, ax = plt.subplots(figsize=(12, 8))

    colors = plt.cm.tab20(range(df_query_date.shape[0]))
    color_map = {query: colors[i] for i, query in enumerate(df_query_date['paraphrased query'])}

    for _, row in df_query_date.iterrows():
        ax.scatter(row['date'], [row['paraphrased query']] * len(row['date']), s=10, color=color_map[row['paraphrased query']], label=row['paraphrased query'])

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d-%H'))
    ax.invert_yaxis()
    plt.xticks(rotation=45)
    plt.xlabel('Date')
    plt.yticks(range(df_query_date.shape[0]), df_query_date['paraphrased query'])

    for i, label in enumerate(ax.get_yticklabels()):
        if i < 10:
            label.set_fontweight('bold')
    plt.title(f"Timeline of Top 10 Queries Occurrence for {df_list[df_index][0].split('.csv')[0].split('@')[-1]}")
    plt.grid(True)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

    st.pyplot(fig)
    return df

def createWordCloud(df_list):
    # Concatenate all queries into a single string
    text = ' '
    for name, df in df_list:
        print(df)
        current_text = ' '.join(df['summarized-query'])
        text += current_text

    # Create word cloud
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)

    # Display the word cloud using matplotlib
    fig = plt.figure(figsize=(10, 6))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    #plt.show()

    return fig

### ALL QUERIES FUNCTIONS ###


###### CALL STREAMLIT FUNCTIONS ######

### SECTION 1 ###
st.subheader("Section 1: Real Time Query Collection Pipleline Explained")

raw_queries_directory = './data/queries-raw'

st.write("""
How are these Google Real-Time Trends Cluster collected?
- Using the [pytrends](https://pypi.org/project/pytrends/) library, we set the location to ***United States*** and category to ***Top Stories*** and collected the trending query clusters
- There is a 300 query limit (e.g. [Trump, Biden, Debate] considered 3 queries), which is why we presort by Top Stories (rest of the categories are: Business, Entertainment, Health, Sci/Tech, Sports)
- Then we first ask GPT to identify if a query group is related to US politics or not. 
""")
st.write("This is the prompt we used to finetune GPT 3.5")
st.caption("""
You are a helpful assistant trained to classify queries based on their relevance to current United States politics.
Your role is to evaluate the overall relevance of the given list of queries to current United States politics. 
Your task is to analyze the queries comprehensively and assign a single relevance score from 0 to 5 based on the strength of their collective connection to the political climate, events, figures, or policies in the United States today. 
A score of 0 indicates no relation, while a score of 5 signifies a very strong connection.
""")

if st.checkbox("show training/validation data used for finetuning"):
    st.caption('Since GPT 3.5 labeling results were already satifactory, our finetuning purpose was soley to specify the output format. Thus the training dataset size was not large.')
    df_train = pd.read_csv(os.path.join(raw_queries_directory,'train.csv'))
    df_train.rename(columns={"relevance_jo":"manual_labels"})
    st.dataframe(df_train)

st.divider()
st.write("Then, we needed a second finetuned model to summarized the Google Real-Time Trends clusters into a short query that mimics typical user search behavior.")
st.write("#TO DO TMR TUES")

### SECTION 2 ###
st.subheader("Section 2: Top Political Queries Every 12 hours")

political_queries_directory = './data/topQueries'

df_list = get_df_list(political_queries_directory)

for i in range(len(df_list)):
    df = plot_dataframe(i)
    if st.checkbox(f"show raw data {i}"):
        st.dataframe(df)

st.write("""
I wasn't so sure about Texas Patrick Abbott Cyclone and Rieckhoff IAVA Independencd Day, so I looked it up
The original Google trends query cluster is: 
- Dan Patrick, Acting governor, Greg Abbott, Lieutenant Governor of Texas, Tropical cyclone
- Iraq and Afghanistan Veterans of America, ex-serviceman, Paul Rieckhoff, Independence Day (United States)

They had reasons to be classified as political queries. 
- https://www.ltgov.texas.gov/2024/07/06/acting-governor-dan-patrick-adds-81-texas-counties-to-hurricane-beryl-disaster-declaration/
- https://www.abc27.com/business/press-releases/cision/20240702PH53051/independent-veterans-of-america-launches-ahead-of-july-4th/

While observing the data visualizaitons, I realized that there was an error in the code as "SCOTUS biden social media" became "SCOTUS social media biden". This is because I
failed to address the problem taht the sliding window constantly changes the first occurance of the query... modified the query so that it is robust against the sliding window. 
""")

word_cloud = createWordCloud(df_list)
word_cloud
st.write("word cloud idea from Belle")

