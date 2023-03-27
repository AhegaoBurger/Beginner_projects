import re
import requests
import unicodedata
from bs4 import BeautifulSoup

# create a request header
headers = {'User-Agent': 'Mozilla/5.0'}


def restore_windows_1252_characters(restore_string):
    """
        Replace C1 control characters in the Unicode string s by the
        characters at the corresponding code points in Windows-1252,
        where possible.
    """

    def to_windows_1252(match):
        try:
            return bytes([ord(match.group(0))]).decode('windows-1252')
        except UnicodeDecodeError:
            # No character at the corresponding code point: remove it.
            return ''

    return re.sub(r'[\u0080-\u0099]', to_windows_1252, restore_string)


# define the url to specific html_text file
url = 'https://www.sec.gov/Archives/edgar/data/320193/000032019323000006/0000320193-23-000006.txt'

# grab the response
response = requests.get(url, headers=headers)

# parse the response
soup = BeautifulSoup(response.content, features='lxml')

# define a new dictionary that will house all of our filings
master_filings_dict = {}

# define the unique key for each filing which is the accession number
accession_number = '0000320193-23-000006'

# add the key to the dictionary and add a new level
master_filings_dict[accession_number] = {}

master_filings_dict[accession_number]['sec_header_content'] = {}
master_filings_dict[accession_number]['filing_documents'] = None

# grab the sec-header document
sec_header_tag = soup.find('sec-header')
# print(sec_header_tag.get_text())

# store the sec header content inside the dictionary
master_filings_dict[accession_number]['sec_header_content']['sec_header_code'] = sec_header_tag

# print(sec_header_tag)

# initialise our master document dictionary
master_document_dict = {}

# loop through each document in the filing
for filing_document in soup.find_all('document'):

    # define the document id
    document_id = filing_document.filename.find(text=True, recursive=False).strip()

    # here are the other parts if you want them.
    document_sequence = filing_document.sequence.find(text=True, recursive=False).strip()
    document_type = filing_document.type.find(text=True, recursive=False).strip()
    # document_description = filing_document.description.find(text=True, recursive=False).strip()

    # insert the key
    master_document_dict[document_id] = {}

    # add the different parts of the document
    master_document_dict[document_id]['document_sequence'] = document_sequence
    master_document_dict[document_id]['document_type'] = document_type
    # master_document_dict[document_id]['document_description'] = document_description

    # add the document content itself
    master_document_dict[document_id]['document_code'] = filing_document.extract()

    # # get all the text in the document
    # filing_doc_text = filing_document.find('text').extract()

    # get the text element
    filing_doc_text_elem = filing_document.find('text')

    # extract the text element from the document
    filing_doc_text_elem.extract()

    # get all the text in the document
    filing_doc_text = filing_doc_text_elem.get_text()

    # get all the thematic breaks
    # all_thematic_breaks = filing_doc_text.find_all('div',{'width':'100%'})
    all_thematic_breaks = filing_doc_text_elem.find_all('hr',{'style':'page-break-after:always'})

    # convert all the breaks into a string
    all_thematic_breaks = [str(thematic_break) for thematic_break in all_thematic_breaks]

    # prep the document for being split
    filing_doc_string = str(filing_doc_text)

    if len(all_thematic_breaks) > 0:
        # print('we have thematic breaks')
        # creates our pattern
        regex_delimited_pattern = '|'.join(map(re.escape, all_thematic_breaks))

        # split the document along the thematic breaks
        split_filing_string = re.split(regex_delimited_pattern, filing_doc_string)

        # store the document in the dictionary
        master_document_dict[document_id]['pages_code'] = split_filing_string

    elif len(all_thematic_breaks) == 0:
        # print('we dont have thematic breaks')
        # store the document in the dictionary
        master_document_dict[document_id]['pages_code'] = [split_filing_string]

    # display some information to the user.
    print('-' * 80)
    print('The document {} was parsed.'.format(document_id))
    print('There was {} thematic breaks(s) found.'.format(len(all_thematic_breaks)))

# store the documents in the master_filing_dictionary.
master_filings_dict[accession_number]['filing_documents'] = master_document_dict

print('-'*80)
print('All the documents for filing {} were parsed and stored.'.format(accession_number))

# grab all the documents
filing_documents = master_filings_dict[accession_number]['filing_documents']

# loop through each document
for document_id in filing_documents:

    # grab all the pages for each document
    document_pages = filing_documents[document_id]['pages_code']

    # page length
    pages_length = len(document_pages)

    # initialise some dictionaries
    repaired_pages = {}
    normalised_text = {}

    for index, page in enumerate(document_pages):

        # if isinstance(page, list):
        #     page = ''.join(page)
        # page_soup = BeautifulSoup(page, features='html5')

        # pass it through the parses to repair it
        page_soup = BeautifulSoup(page, features='html5')

        # grab the text from each page
        page_text = page_soup.html.body.get_text(' ', strip=True)

        # normalise the text
        page_text_norm = restore_windows_1252_characters(unicodedata.normalize('NFKD', page_text))

        # additional cleaning
        page_text_norm = page_text_norm.replace('  ',' ').replace('\n', ' ')

        print('-'*80)
        print(page_text_norm, file=open(f'D:\\Python\\reports\\{document_id}.txt', 'w', encoding='utf-8'))
