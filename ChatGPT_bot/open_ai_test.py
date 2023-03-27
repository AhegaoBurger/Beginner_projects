import openai
import requests
import sqlite3
import telebot
from telebot.types import LabeledPrice
from bs4 import BeautifulSoup
import html2text

openai.api_key = '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'



url = "https://finance.yahoo.com/news/big-oil-raked-in-record-profits-last-year-but-check-out-big-tech-161530609.html"
page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")
articles = []
results = soup.find("div", class_="caas-body")
articles.append(results.find_all('p'))

# Convert articles from HTML to plain text
h = html2text.HTML2Text()
h.ignore_links = True
articles_text = [h.handle(str(article)) for article in articles]

# Use OpenAI API to summarize and translate the article
prompt = f"Summarize this article and translate the summary into Russian with less than 200 characters\n\n{articles_text}"
response = openai.Completion.create(
    engine="text-curie-001",
    prompt=prompt,
    temperature=0.1,
    max_tokens=800,
)

# Print the response
print(response)
print(response.choices[0].text)
