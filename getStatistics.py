import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://finance.yahoo.com/quote/MELI/key-statistics?p=MELI'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')

# Find the table or data elements using BeautifulSoup
# For example, if the data is in a table:
tables = soup.find_all('table')

# Parse the table into a pandas dataframe
# This will depend on the structure of the table
df = pd.read_html(str(tables[0]))[0]  # Example for the first table

#print(response)

#print(soup)

#print(tables)

print(df)
