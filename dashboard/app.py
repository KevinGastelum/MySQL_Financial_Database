import streamlit as st
#import psycopg2
import pandas as pd
import plotly.express as px
from streamlit_extras.stoggle import stoggle
import supabase_py 
from dotenv import load_dotenv
import os

# Load and get db Environment Variables
load_dotenv()
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
supabase = supabase_py.create_client(supabase_url, supabase_key)

# Page config
st.set_page_config(
    layout="wide",
    page_title="Finance Dashboard",
    page_icon="📈"
)

#@st.cache
def fetch_data(table_name, date):
  date_str = date.strftime('%Y-%m-%d')
  result = supabase.table(table_name).select().eq('date', date_str).execute()
  #print(result) # print results
  data = pd.DataFrame(result['data'])
  return data

# Custom text fonts
def custom_css():
    st.markdown("""
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
            }
            .stTable {
                font-size: 14px;
            }
        </style>
    """, unsafe_allow_html=True)

# Plot our data
def plot_data(df, title, y_column):
    fig = px.bar(df, x='ticker', y=y_column, title=title, labels={'ticker': 'Ticker', y_column: y_column.capitalize()}, color=y_column, color_continuous_scale=px.colors.sequential.Plasma)
    st.plotly_chart(fig)


def main():
    custom_css()
    st.title("Kevin's Automized Daily Stock Tracker📈")

    stoggle(
        "Click me!",
        """ This Dashboard refreshes daily using Github Actions, by running a Python script to automate fetching and storing data in an SQL Database, displaying the top 20 gainers, losers and most actively traded financial stocks of the day from the S&P 500, Nasdaq, and Crypto market.
        """
    )

    date = st.date_input('**Select a Date** (Data begins on date of project creation 2023/10/16)', value=pd.to_datetime('today'))  # Date Picker

    st.header(f"Top 20 Gainers on {date.strftime('%Y-%m-%d')}")
    top_gainers = fetch_data("top_gainers", date)
    cols = st.columns(2)  # Create two columns
    with cols[0]:
        st.write(top_gainers)  # Display table in the first column
    with cols[1]:
        #fig = px.bar(top_gainers, x='ticker', y='change_percentage', title='Top 20 Gainers')
        plot_data(top_gainers, 'Top 20 Gainers', 'change_percentage')  # Display chart in the second column

    st.header(f"Top 20 Losers on {date.strftime('%Y-%m-%d')}")
    top_losers = fetch_data("top_losers", date)
    cols = st.columns(2)
    with cols[0]:
        st.write(top_losers)
    with cols[1]:
        #fig = px.bar(top_losers, x='ticker', y='change_percentage', title='Top 20 Losers')
        plot_data(top_losers, 'Top 20 Losers', 'change_percentage')

    st.header(f"Top 20 Most Actively Traded {date.strftime('%Y-%m-%d')}")
    most_actively_traded = fetch_data("most_actively_traded", date)
    cols = st.columns(2)
    with cols[0]:
        st.write(most_actively_traded)
    with cols[1]:
        #fig = px.bar(most_actively_traded, x='ticker', y='volume', title='Top 20 Most Actively Traded')
        plot_data(most_actively_traded, 'Top 20 Most Actively Traded', 'volume')

if __name__ == "__main__":
  main()

