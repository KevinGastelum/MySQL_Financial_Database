import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
from streamlit_extras.stoggle import stoggle

# Load Environment Variables
from dotenv import load_dotenv
import os

# Load and get db Environment Variables
load_dotenv()
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')

# Establish db Connection
conn = psycopg2.connect(
  dbname=db_name,
  user=db_user,
  password=db_password,
  host=db_host,
  port=db_port
)

# Page config
st.set_page_config(
    layout="wide",
    page_title="Finance Dashboard",
    page_icon="📈"
)

#@st.cache
def fetch_data(table_name, date):
  date_str = date.strftime('%Y-%m-%d')
  query = f"""
      SELECT ticker, price, change_amount, ROUND(change_percentage) AS change_percentage, volume, date
      FROM {table_name}
      WHERE date = '{date_str}'
      ORDER BY change_percentage DESC
      LIMIT 20;
  """
  data = pd.read_sql_query(query, conn)
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
def plot_data(df, title):
    fig = px.bar(df, x='ticker', y='change_percentage', title=title, labels={'ticker': 'Ticker', 'change_percentage': 'Change Percentage'})
    st.plotly_chart(fig)


def main():
    custom_css()
    st.title("Automized Daily Stock Tracker📈")

    stoggle(
        "Click me!",
        """ This Dashboard refreshes daily using Github Actions, running a Python script to automate fetching and storing data in an SQL Database, displaying the top 20 gainers, losers and most actively traded financial stocks of the day from the S&P 500, Nasdaq, and Crypto market.
        """
    )

    date = st.date_input('**Select a Date** (Data begins on date of project creation 2023/10/11)', value=pd.to_datetime('today'))  # Date Picker

    st.header(f"Top 20 Gainers on {date.strftime('%Y-%m-%d')}")
    top_gainers = fetch_data("top_gainers", date)
    cols = st.columns(2)  # Create two columns
    with cols[0]:
        st.write(top_gainers)  # Display table in the first column
    with cols[1]:
        fig = px.bar(top_gainers, x='ticker', y='change_percentage', title='Top 20 Gainers')
        st.plotly_chart(fig)  # Display chart in the second column

    st.header(f"Top 20 Losers on {date.strftime('%Y-%m-%d')}")
    top_losers = fetch_data("top_losers", date)
    cols = st.columns(2)
    with cols[0]:
        st.write(top_losers)
    with cols[1]:
        fig = px.bar(top_losers, x='ticker', y='change_percentage', title='Top 20 Losers')
        st.plotly_chart(fig)

    st.header(f"Top 20 Most Actively Traded {date.strftime('%Y-%m-%d')}")
    most_actively_traded = fetch_data("most_actively_traded", date)
    cols = st.columns(2)
    with cols[0]:
        st.write(most_actively_traded)
    with cols[1]:
        fig = px.bar(most_actively_traded, x='ticker', y='volume', title='Top 20 Most Actively Traded')
        st.plotly_chart(fig)

if __name__ == "__main__":
  main()

# Close db connection
conn.close()






