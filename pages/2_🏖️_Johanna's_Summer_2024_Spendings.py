import streamlit as st
import pandas as pd

st.set_page_config(page_title="Johanna's Summer 2024 Spendings", page_icon="🏖️")


won_to_dollar_currency = 0.00072
dollar_to_won_currency = 1381

def fix_prices(column: pd.Series) -> pd.Series:
    """
    Cleans price column and returns the corrected float column.

    Parameters:
        column (pd.Series): Pandas dataframe with prices as strings.

    Returns:
        pd.Series: returns corrected column with evalued float values
    """
    def evaluate_price(price):
         cleanPrice = price.replace(',', '')
         allowedChars = "0123456789+-*/.()"
         if all(char in allowedChars for char in cleanPrice):
                return eval(cleanPrice)
         else:
              raise ValueError(f"Invalid characters in price: {cleanPrice}")
    return column.apply(evaluate_price)

def price_to_dollars(row):
     if row['currency'] == 'w':
          dollar_price = won_to_dollar_currency*row['price']
          return dollar_price
     else:
          return row['price']
     
def calculate_date_diff(dataframe, colName):
      df_delivery = dataframe[dataframe['category']==colName].sort_values(by='date')
      df_delivery['date_diff'] = df_delivery['date'].diff().dt.days
      return df_delivery['date_diff'].mean()

df_original = pd.read_csv('./data/summer_2024.csv')
df = df_original.copy() # for data manipulation

df['price'] = fix_prices(df['price'])
df['date'] = pd.to_datetime(df['date'], format = "%m/%d/%y")
df_currency_grouped = df.groupby(['currency'])['price'].sum().reset_index()
won_net = int(df_currency_grouped[df_currency_grouped['currency'] == 'w']['price'].iloc[0])
dollar_net = int(df_currency_grouped[df_currency_grouped['currency'] == 'd']['price'].iloc[0])

df['dollarPrice'] = df.apply(price_to_dollars, axis=1)


# SPENDINGS
df_spendings = df[df['dollarPrice'] < 0] 
df_spendings['spendings'] = df_spendings['dollarPrice'] * -1 # make spendings positive for barplot 
spendings = df_spendings['spendings'].sum()
df_category_spendings = df_spendings.groupby(['category'])['spendings'].sum().sort_values(ascending=False).reset_index()
top_3_categories = "".join(" "+v for v in df_category_spendings['category'][:3].values)

avg_date_diff_delivery = calculate_date_diff(df_spendings, 'delivery')
avg_date_diff_grocery = calculate_date_diff(df_spendings, 'groceries')
avg_date_diff_dineout = calculate_date_diff(df_spendings, 'dineout')
avg_spending_per_day = df_spendings[df_spendings['category']!='vacation'].groupby('date')['spendings'].sum().reset_index()['spendings'].mean()

# INCOME
df_income = df[df['dollarPrice'] >= 0] 
total_income = df_income['dollarPrice'].sum()
avg_income_per_week = df_income.set_index('date')['dollarPrice'].resample('W').sum().mean()

st.title("Johanna's Summer 2024 Spendings")

if st.checkbox('Show summer 2024 raw data'):
        st.subheader('Raw data')
        st.write(df_original)

st.header("Spendings")
st.subheader("by category")
col1, col2 = st.columns(spec=[0.7,0.3])
col1.bar_chart(data=df_spendings, x="category", y="spendings", color="#DD66E0")

col2.write(f"""***top 3 categories:***\n
{top_3_categories}""")
if col2.checkbox(f'show full dataset'):
        col2.write('spending by category')
        col2.dataframe(df_category_spendings, hide_index=True)

col2.write(f"""spent {int(spendings)} dollars in total""")

st.subheader("over time")
st.bar_chart(df_spendings, x="date", y="spendings", color="category")
st.write(f"""
- Data is from `{min(df['date']).date()}` to `{max(df['date']).date()}`
- I ordered delivery every `{round(avg_date_diff_delivery,2)}` days on average 
- I went grocery shopping every `{round(avg_date_diff_grocery,2)}` days on average
- I dined out every `{round(avg_date_diff_dineout,2)}` days on average
- Excluding the `vacation` category, on average, I spend `{round(avg_spending_per_day,2)}` per day.
This includes the `fun` category with future events (concert tickets)
"""
)
if st.checkbox("my reflections..."):
      st.subheader("I HAD NO IDEA I WAS ORDERING SO MUCH")
      st.write("will really try to cut down on uber eats 😢") 
      st.write("travel expenses are for NY trip in August")   

st.header("Income")
col1, col2 = st.columns([0.5,0.5])
col1.bar_chart(data= df_income, x="date", y="dollarPrice")
col2.write(f"""
Total income is `{total_income}` dollars.\n
Average income per week is `{round(avg_income_per_week,2)}` dollars.
""")
st.subheader("Net")
st.write(f"""
- In total, my net income is `{won_net}` won and `{dollar_net}` dollars from
`{min(df['date']).date()}` to `{max(df['date']).date()}`
- in dollars, this adds up to `${won_net*won_to_dollar_currency+dollar_net}`
- in won, this adds up to `₩{won_net+dollar_net*dollar_to_won_currency}`
""")
