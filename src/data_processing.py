#import psycopg2
import pandas as pd
import supabase_py
from dotenv import load_dotenv
import os

# Load and get db Environment Variables
load_dotenv()
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
supabase = supabase_py.create_client(supabase_url, supabase_key)

"""
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')

# Establish database connection
conn = psycopg2.connect(
    dbname=db_name,
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port
)
"""

# Fetch data from my PSQL github_database
def fetch_data(table_name):
    result = supabase.table(table_name).select().execute()
    data = pd.Dataframe(result['data'])
    return data

def process_data():
    top_gainers = fetch_data('top_gainers')
    top_losers = fetch_data('top_losers')
    most_actively_traded = fetch_data('most_actively_traded')
    return top_gainers, top_losers, most_actively_traded

if __name__ == "__main__":
    top_gainers, top_losers, most_actively_traded = process_data()
    # Print the top 5 rows of each dataframe to check the data
    print(top_gainers)
    print(top_losers.head())
    print(most_actively_traded.head())

# Close the database connection
#conn.close()
