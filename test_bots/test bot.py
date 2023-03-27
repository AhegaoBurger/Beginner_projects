import telebot
from telebot import types
import datetime
from datetime import datetime

bot = telebot.TeleBot("5890376662:AAFaY9EYP-Mfg5_fV2bJizn--PS881teiD0")

@bot.message_handler(commands=["start"])
def start(m, res=False):
        # Добавляем три кнопки
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton('Meme')
        item2=types.KeyboardButton('Sign in')
        item3=types.KeyboardButton('Sign out')
        item4=types.KeyboardButton('To do list')
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

                if message.text.strip() == 'Meme' :
                        answer = r"D:\Artur\Database\Rainbow-man.jpg"

                        bot.send_document(message.chat.id, document=open(answer, 'rb'), caption="RAINBOW")

                elif message.text.strip() == 'Sign in' :
                        now1 = datetime.now()
                        start = open('D:\\Artur\\Database\\logins.csv', 'a')
                        start.write('in,%s\n' % str(now1))
                        bot.send_message(message.chat.id, now1)
                        start.close()

                elif message.text.strip() == 'Sign out' :
                        now2 = datetime.now()
                        date_logout = open('D:\\Artur\\Database\\logins.csv', 'r')
                        lines = date_logout.readlines()
                        date_login = lines[-1].replace('\n', '').split(',')[1]
                        duration = now2 - datetime.strptime(date_login, '%Y-%m-%d %H:%M:%S.%f')
                        # print(duration)
                        end = open('D:\\Artur\\Database\\logins.csv', 'a')
                        end.write('out,%s\n' % str(now2))
                        bot.send_message(message.chat.id, duration)
                        end.close()
                        date_logout.close()
                
                elif message.text.strip() == 'To do list':
                        to_do_list = open('D:\\Artur\\Database\\text.txt', 'r')
                        points = to_do_list.readlines()
                        # send = points.replace('\n', '')
                        bot.send_document(message.chat.id, points)
                        to_do_list.close()

                elif message.text.strip() == 'Add to the list':
                        number = 0
                        add = input('What would you like to add: ')
                        to_do_list = open('D:\\Artur\\Database\\text.txt', 'a')
                        to_do_list.write(number + 1, add)
                        to_do_list.close()



                        
except:
        @bot.message_handler(content_types=["text"])
        def handle_text(message):
                answer = r"D:\Artur\Memes\Meme Templates\giphy.gif"
                bot.send_document(message.chat.id, answer)

bot.polling(none_stop=True, interval=0)