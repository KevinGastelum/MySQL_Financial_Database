import os
from dotenv import load_dotenv
import requests
#import psycopg2
#import psycopg2.extras
import supabase_py
from datetime import datetime

# Fetch Stock data from Alpha Vantage
load_dotenv()
api_key = os.getenv('ALPHA_VANTAGE_API_KEY')

# API endpoint URL
url = 'https://www.alphavantage.co/query'

# API parameters
params = {
    "function": "TOP_GAINERS_LOSERS",
    "apikey": api_key
}

# Make the API request
try:
    response = requests.get(url, params=params)
    response.raise_for_status()  # Check if the request was successful
except requests.RequestException as e:
    print(f"Request failed: {e}")
else:
    # Parse the data
    data = response.json() # Data response from AlphaVantage 

"""
# Store Data into PSQL Database
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=db_name,
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port
)
cur = conn.cursor()
"""

#Store data in my PSQL Databse using Supabase
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
supabase = supabase_py.create_client(supabase_url, supabase_key)

# Define a function to insert data into specified table
def insert_data(table_name, data):
    today = datetime.today().strftime('%Y-%m-%d')
    # print(data)
    # insert_query = f"""
    #     INSERT INTO {table_name} (ticker, price, change_amount, change_percentage, volume, date)
    #     VALUES %s
    #     ON CONFLICT (ticker) DO UPDATE 
    #     SET price = EXCLUDED.price,
    #         change_amount = EXCLUDED.change_amount,
    #         change_percentage = EXCLUDED.change_percentage,
    #         volume = EXCLUDED.volume;
    # """
    values = [{
        'ticker': item['ticker'],
        'price': float(item['price']),
        'change_amount': float(item['change_amount']),
        'change_percentage': float(item['change_percentage'].strip('%')),
        'volume': int(item['volume']),
        'date': today
    } for item in data]
    
    # Insert data into the Supabase table
    supabase.table(table_name).insert(values).execute()
    # print(response) # Print our response just name the variable above to response

# Insert data into tables
insert_data('top_gainers', data['top_gainers'])
insert_data('top_losers', data['top_losers'])
insert_data('most_actively_traded', data['most_actively_traded'])

# Commit changes and close connection
#conn.commit()
#cur.close()
#conn.close()