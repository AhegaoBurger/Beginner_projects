import requests
import os

# create a request header
headers = {'User-Agent': 'Mozilla/5.0'}

# Define the URL of the endpoint and set the parameters
endpoint = 'https://www.sec.gov/cgi-bin/browse-edgar'
params = {
    'action': 'getcompany',
    'CIK': '0000320193',  # Replace with the CIK of the company you want to retrieve filings for
    'type': '10-Q',  # Set the type of filing you want to retrieve, in this case quarterly filings
    'count': '10'  # Set the number of filings you want to retrieve
}

# Send a GET request to the endpoint and retrieve the response
response = requests.get(endpoint, params=params, headers=headers)

# Parse the response using BeautifulSoup
from bs4 import BeautifulSoup

soup = BeautifulSoup(response.content, 'html.parser')

# Find all the filing links in the response
filing_links = soup.find_all('a', {'id': 'documentsbutton'})

# Loop through the filing links and download the filing documents
for link in filing_links:
    filing_url = 'https://www.sec.gov' + link.get('href')
    filing_response = requests.get(filing_url)
    filing_soup = BeautifulSoup(filing_response.content, 'html.parser')
    filing_table = filing_soup.find('table', {'class': 'tableFile'})

    # Find the first filing document in the filing table
    filing_row = filing_table.find_all('tr')[1]
    filing_document = filing_row.find_all('td')[2].find('a')

    # Download the filing document
    document_url = 'https://www.sec.gov' + filing_document.get('href')
    document_response = requests.get(document_url, headers=headers)
    document_filename = filing_document.text.strip()
    with open(os.path.join('filings', document_filename), 'wb') as f:
        f.write(document_response.content)