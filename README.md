# Automized Daily Stock Tracker App
## Project Description

This project aims to create a dynamic data dashboard to visualize the top 20 gainers, losers, and most actively traded tickers in the US market, utilizing data from the AlphaVantage API. This dashboard updates daily, providing a clear and concise view of market movers.

## Data Source

The data is retrieved from the AlphaVantage API, specifically using the TOP_GAINERS_LOSERS function to fetch the top gainers, losers, and the most actively traded tickers in the US market.

## Project Structure

- data/: Directory for storing data files.
- src/:
  - data_retrieval.py: Script to fetch data from AlphaVantage API and store it in a PostgreSQL database.
  - data_processing.py: Script to process the data for visualization.
- dashboard/:
  - app.py: Streamlit application to create the interactive dashboard.
- db_setup.sql: Script documenting the database schema creation.

## Setup and Installation

1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies using the following command:
   `pip install -r requirements.txt`
4. Set up the environment variables for database connection and API access in a .env file as follows:
   `ALPHA_VANTAGE_API_KEY=your_api_key_here <br>
    DB_NAME=your_db_name <br>
    DB_USER=your_db_username
    DB_PASSWORD=your_db_password
    DB_HOST=your_db_host
    DB_PORT=your_db_port`
5. Run the data_retrieval.py script to fetch and store the data.
6. Run the Streamlit app using the following command:
   `streamlit run dashboard/app.py`

## Usage

Upon launching the Streamlit app, you can select a date using the date picker widget to view the top gainers, losers, and most actively traded tickers for that specific day. The data displayed includes the ticker symbol, price, change amount, change percentage, and trading volume.
