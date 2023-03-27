from chatgpt_wrapper import ChatGPT
import requests
from bs4 import BeautifulSoup
import telebot

# API_KEY = "5890376662:AAFaY9EYP-Mfg5_fV2bJizn--PS881teiD0"
# telegram_bot = telebot.TeleBot(API_KEY)



url = "https://finance.yahoo.com/news/big-oil-raked-in-record-profits-last-year-but-check-out-big-tech-161530609.html"
page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")
articles = []
results = soup.find("div", class_="caas-body")
# news_elements = results.find_all("div", class_="er-fresh")
articles.append(results.find_all('p'))


chat_bot = ChatGPT()
# return the full result
# response = chat_bot.ask(f'translate into Russian and summarise this article in less than 200 characters {articles[0][:22]}')
# response1 = chat_bot.ask_stream(f'Please summarise this article in less than 200 characters and translate the summary into Russian {articles[0][:22]}')
response2 = chat_bot.ask(f'Please summarise this article in less than 200 characters and translate the summary into Russian {articles[0][:22]}')

# print(response)
# print(response1)
print(response2)

# # return the result in streaming (chunks)
# for chunk in bot.ask_stream('tell me a story about cats and dogs'):
#     print(chunk)