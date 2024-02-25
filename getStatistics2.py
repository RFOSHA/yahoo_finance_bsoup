import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

# List of stock tickers
#tickers = ['MELI', 'AAPL', 'MSFT', 'GOOG']  # Add more tickers as needed
with open('sp500_lists.json', 'r') as file:
    sp500_lists = json.load(file)
    tickers = sp500_lists.get('SnP500', [])
    print(tickers)

# Initialize an empty DataFrame to store results
all_data = pd.DataFrame()

for ticker in tickers:
    print(ticker)
    url = f'https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}'

    headers = {'User-Agent': 'Mozilla/5.0'}  # Set a user-agent
    response = requests.get(url, headers=headers)

    # Continue only if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find_all('table')

        if table:
            df = pd.read_html(str(table[0]))[0]

            # Extract and process data as needed
            # ...

            # Add a column for the ticker and append to the main DataFrame
            df['Ticker'] = ticker
            all_data = all_data.append(df, ignore_index=True)
        else:
            print(f"Table not found for ticker {ticker}")
    else:
        print(f"Failed to retrieve data for ticker {ticker}")

all_data.to_csv('stock_data.csv', index=False)

print(all_data)
