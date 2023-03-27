API_KEY = "5582044861:AAEP-2xXeydEDLVJqhJ_cgU1BsGojjoKgcQ"
import sqlite3
import telebot
from telebot import types
import datetime
from datetime import datetime

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=["start"])
def start(m, res=False):
        # Добавляем три кнопки
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton('List')
        item2=types.KeyboardButton('1.2. Курсы языка в Испании: услуги по подбору и зачислению')
        item3=types.KeyboardButton('1.1. Получение образования в Испании: консультации специалиста')
        item4=types.KeyboardButton('1.8. Открытие разрешения на работу студентам в Испании')
        item5=types.KeyboardButton('Add to the list')
        item6=types.KeyboardButton('Remove from the list')

        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        markup.add(item5)
        markup.add(item6)

        bot.send_message(m.chat.id, 'What would you like to see',  reply_markup=markup)


try:
        @bot.message_handler(content_types=["text"])
        def handle_text(message):

                # Если юзер прислал item1, выдаем ему ссылки

                if message.text.strip() == 'List' :
                    # Connect to the database
                    conn = sqlite3.connect('C:\\sqlite\\test.db')
                    c = conn.cursor()

                    # Fetch all services from the database
                    c.execute("SELECT * FROM test")
                    test = c.fetchall()

                    # Build the message to be sent to the user
                    message_text = "Our services:\n"
                    for service in test:
                        message_text += f"- {service[0]}: {service[1]}$\n"

                    # Send the message to the user
                    bot.send_message(message.chat.id, message_text)

                    # Close the database connection
                    conn.close()


                elif message.text.strip() == '1.2. Курсы языка в Испании: услуги по подбору и зачислению' :
                    service_name = message.text.split() # get the service name from the message text
                    code = message.text[:4]

                    # Connect to the database
                    conn = sqlite3.connect('C:\\sqlite\\test.db')
                    c = conn.cursor()

                    # Fetch the service from the database
                    c.execute("SELECT * FROM test WHERE code = ?", (code,))
                    service = c.fetchone()

                    if service:
                        # Build the message to be sent to the user
                        message_text = f"Information for service {service[0]}: \n"
                        message_text += f"Price: {service[1]}$\n"
                        # Send the message to the user
                        bot.send_message(message.chat.id, message_text)
                    else:
                        bot.send_message(message.chat.id, f"Service {service_name} not found.")

                    # Close the database connection
                    conn.close()


                elif message.text.strip() == '1.1. Получение образования в Испании: консультации специалиста' :
                    service_name = message.text.split() # get the service name from the message text
                    code = message.text[:4]

                    # Connect to the database
                    conn = sqlite3.connect('C:\\sqlite\\test.db')
                    c = conn.cursor()

                    # Fetch the service from the database
                    c.execute("SELECT * FROM test WHERE code = ?", (code,))
                    service = c.fetchone()

                    if service:
                        # Build the message to be sent to the user
                        message_text = f"Information for service {service[0]}: \n"
                        message_text += f"Price: {service[1]}$\n"
                        # Send the message to the user
                        bot.send_message(message.chat.id, message_text)
                    else:
                        bot.send_message(message.chat.id, f"Service {service_name} not found.")

                    # Close the database connection
                    conn.close()
                       
                elif message.text.strip() == '1.8. Открытие разрешения на работу студентам в Испании':
                    service_name = message.text.split() # get the service name from the message text
                    code = message.text[:4]

                    # Connect to the database
                    conn = sqlite3.connect('C:\\sqlite\\test.db')
                    c = conn.cursor()

                    # Fetch the service from the database
                    c.execute("SELECT * FROM test WHERE code = ?", (code,))
                    service = c.fetchone()

                    if service:
                        # Build the message to be sent to the user
                        message_text = f"Information for service {service[0]}: \n"
                        message_text += f"Price: {service[1]}$\n"
                        # Send the message to the user
                        bot.send_message(message.chat.id, message_text)
                    else:
                        bot.send_message(message.chat.id, f"Service {service_name} not found.")

                    # Close the database connection
                    conn.close()
                
except:
    @bot.message_handler(content_types=["text"])
    def handle_text(message):
        answer = r"D:\Artur\Memes\Meme Templates\giphy.gif"
        bot.send_document(message.chat.id, answer)

bot.polling(none_stop=True, interval=0)