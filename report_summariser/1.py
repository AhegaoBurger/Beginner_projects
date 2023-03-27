import requests
from bs4 import BeautifulSoup
import sqlite3
import pandas as pd

# create a request header
headers = {'User-Agent': 'Mozilla/5.0'}

# get all companies data
company_tickers = requests.get('https://www.sec.gov/files/company_tickers.json', headers=headers)

# dictionary to dataframe
company_data = pd.DataFrame.from_dict(company_tickers.json(), orient='index')

# add leading zeros to CIK
company_data['cik_str'] = company_data['cik_str'].astype(str).str.zfill(10)

# the stuff we need
cik = company_data.cik_str[:500]
ticker = company_data.ticker[:500]
title = company_data.title[:500]

# database stuff
db_filename = 'fortune500.db'
table_name = 'cik'
conn = sqlite3.connect(db_filename)

create_table_sql = f'''CREATE TABLE IF NOT EXISTS {table_name}
                     (cik TEXT,
                     ticker TEXT,
                     title TEXT)'''
conn.execute(create_table_sql)

# stuff I am not sure about
tickers = company_tickers.text.strip().split('\n')

# loop through the list of company tickers and retrieve the company data from the SEC API
for i in range(500):
    # extract the relevant data from the company data
    ticker_val = ticker.iloc[i]
    cik_val = cik.iloc[i]
    title_val = title.iloc[i]

    # insert the company data into the database
    # conn.execute(f'INSERT INTO {table_name} cik=%s, ticker=%s, title=%s' % (cik, ticker, title))
    conn.execute(f'INSERT INTO {table_name} (cik, ticker, title) VALUES (?, ?, ?)', (cik_val, ticker_val, title_val))

# commit the changes to the database
conn.commit()
conn.close()

