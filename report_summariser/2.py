import requests
from bs4 import BeautifulSoup
import re

# create a request header
headers = {'User-Agent': 'Mozilla/5.0'}

# define the company and quarter of interest
company = "0000320193"
quarter = "Q1 2022"

# search for the 10-Q form for the company and quarter of interest
search_url = f'https://www.sec.gov/cgi-bin/browse-edgar'
params = {
    'action': 'getcompany',
    'output': 'atom',
    'CIK': '0000320193',  # Replace with the CIK of your desired company
    'type': '10-Q',       # Specify the filing type as 10-Q for quarterly reports
    'count': '1'          # Retrieve only the latest filing
}

# define our response
response = requests.get(url=search_url, params=params, headers=headers)

# print status code
print(response.status_code)
print(response.url)
soup = BeautifulSoup(response.content, parser='lxml')

# find all the entry tags
entries = soup.find_all('entry')

# initialise our list for storage
master_list = []

# loop through each entry
for entry in entries:

    # grab the accession number so that we can create a key value
    accession_num = entry.find('accession-number').text
    print(accession_num)

    # create a new dictionary
    entry_dict = {}
    entry_dict[accession_num] = {}

    # store the category info
    category_info = entry.find('category')
    entry_dict[accession_num]['category'] = {}
    entry_dict[accession_num]['category']['label'] = category_info['label']
    entry_dict[accession_num]['category']['scheme'] = category_info['scheme']
    entry_dict[accession_num]['category']['term'] = category_info['term']

    # print(entry_dict)

    # store the file info
    entry_dict[accession_num]['file_info'] = {}
    entry_dict[accession_num]['file_info']['act'] = entry.find('act').text
    entry_dict[accession_num]['file_info']['file_number'] = entry.find('file-number').text
    entry_dict[accession_num]['file_info']['file_number_href'] = entry.find('file-number-href').text
    entry_dict[accession_num]['file_info']['filing_date'] = entry.find('filing-date').text
    entry_dict[accession_num]['file_info']['filing_href'] = entry.find('filing-href').text
    entry_dict[accession_num]['file_info']['filing_type'] = entry.find('filing-type').text
    entry_dict[accession_num]['file_info']['form_number'] = entry.find('film-number').text
    entry_dict[accession_num]['file_info']['form_name'] = entry.find('form-name').text
    entry_dict[accession_num]['file_info']['file_size'] = entry.find('size').text
    entry_dict[accession_num]['file_info']['xbrl_href'] = entry.find('xbrl_href').text

    # print(entry_dict)

    # store extra info
    entry_dict[accession_num]['request_info'] = {}
    entry_dict[accession_num]['request_info']['link'] = entry.find('link')['href']
    entry_dict[accession_num]['request_info']['title'] = entry.find('title').text
    entry_dict[accession_num]['request_info']['last_update'] = entry.find('updated').text

    # store in the master list
    master_list.append(entry_dict)

print(master_list[0])

