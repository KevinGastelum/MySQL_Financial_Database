import os
from dotenv import load_dotenv
import requests
import json

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
    # Parse and print the JSON data
    data = response.json()
    print(json.dumps(data, indent=4))



