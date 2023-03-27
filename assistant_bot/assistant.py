import telebot
import psycopg2
from psycopg2 import sql
import requests
from bs4 import BeautifulSoup


# create a new bot with your API token
bot = telebot.TeleBot('6029161135:AAGImRP25u9cJe0_T7E5MLQJ4eE_aaVg0J0')


def main_menu():
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    button1 = telebot.types.InlineKeyboardButton("To-do List", callback_data="to_do_menu")
    button2 = telebot.types.InlineKeyboardButton("News", callback_data="news_page")
    markup.add(button1, button2)
    return markup


def news_page():
    markup = telebot.types.InlineKeyboardMarkup()

    url = "https://espanarusa.com/ru/news/index"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("div", class_="er-fresh-container")
    news_elements = results.find_all("div", class_="er-fresh")
    links = []
    for news_element in news_elements:
        title_elements = news_element.find("div", class_="er-item-title")
        links.append(title_elements.find('a'))
    message_text = f'<b>News</b> \n'
    for link in links:
        link_url = link["href"]
        message_text += f'<a>• </a><a href="https://espanarusa.com{link_url}">{link.text}</a>\n'

    markup.add(telebot.types.InlineKeyboardButton(text="← Main menu", callback_data="main_menu"))
    return message_text, markup


@bot.callback_query_handler(func=lambda call: call.data == 'to_do_menu')
def to_do_menu_callback_handler(call):
    text, markup = to_do_menu(call)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML'
                          , text=text, reply_markup=markup)


def to_do_menu(call):
    text = '<b>To do menu</b>'
    # create a connection to the PostgreSQL database
    conn = psycopg2.connect(
        host='ep-raspy-base-853661.eu-central-1.aws.neon.tech',
        port='5432',
        dbname='neondb',
        user='AhegaoBurger',
        password='1MV3HhWojRdq'
    )
    c = conn.cursor()
    c.execute('SELECT * FROM task WHERE user_id=%s' % (call.from_user.id,))
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    rows = c.fetchall()
    task_list = ''
    if len(rows) == 0:
        text += 'No tasks in the list'
    else:
        for i, row in enumerate(rows):
            task_list = telebot.types.InlineKeyboardButton(f'{i + 1}. {row[2]}', callback_data=f'task_{row[0]}')
            markup.add(task_list)
    conn.close()
    add_task_button = telebot.types.InlineKeyboardButton('Add a task', callback_data='add_task')
    markup.add(add_task_button)
    main_menu_button = telebot.types.InlineKeyboardButton('← Main menu', callback_data='main_menu')
    markup.add(main_menu_button)
    return text, markup


@bot.callback_query_handler(func=lambda call: call.data.split("_")[0] in ['task'])
def task_menu_callback_query_handler(call):
    text, markup = task_menu(call)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML'
                          , text=text, reply_markup=markup)


def task_menu(call):
    # create a connection to the PostgreSQL database
    conn = psycopg2.connect(
        host='ep-raspy-base-853661.eu-central-1.aws.neon.tech',
        port='5432',
        dbname='neondb',
        user='AhegaoBurger',
        password='1MV3HhWojRdq'
    )
    c = conn.cursor()
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    c.execute('SELECT * FROM task WHERE user_id=%s and id=%s' % (call.from_user.id, call.data.split("_")[1]))
    task = c.fetchall()
    if task == None:
        task = 'task does not exist'
        markup = None
    else:
        task = task
        edit_task_button = telebot.types.InlineKeyboardButton('Edit a task', callback_data=f'edit_task_{task[0]}')
        delete_task_button = telebot.types.InlineKeyboardButton('Delete a task', callback_data=f'delete_task_{0}')
        mark_done_button = telebot.types.InlineKeyboardButton('Mark task done', callback_data=f'mark_done_{0}')
        to_do_menu_button = telebot.types.InlineKeyboardButton('← To do list', callback_data='to_do_menu')
        markup.add(edit_task_button, delete_task_button, mark_done_button, to_do_menu_button)
    return task, markup


# function to handle the add task button
@bot.callback_query_handler(func=lambda call: call.data == 'add_task')
def add_task_callback(call):
    bot.answer_callback_query(callback_query_id=call.id)
    msg = bot.send_message(call.message.chat.id, 'Enter a new task:')
    bot.register_next_step_handler(msg, add_task)


# function to add a new task
def add_task(message):
    conn = psycopg2.connect(
        host='ep-raspy-base-853661.eu-central-1.aws.neon.tech',
        port='5432',
        dbname='neondb',
        user='AhegaoBurger',
        password='1MV3HhWojRdq'
    )
    c = conn.cursor()
    task = message.text
    user_id = message.from_user.id
    if task != '':
        c.execute('INSERT INTO task (user_id, task) VALUES (%s, %s)', (user_id, task))
        conn.commit()
        bot.reply_to(message, f'Added task {task} to the list')
    else:
        bot.reply_to(message, 'Please enter a task')


# function to handle the edit task button
@bot.callback_query_handler(func=lambda call: call.data.startswith('edit_task_'))
def edit_task_callback(call):
    conn = psycopg2.connect(
        host='ep-raspy-base-853661.eu-central-1.aws.neon.tech',
        port='5432',
        dbname='neondb',
        user='AhegaoBurger',
        password='1MV3HhWojRdq'
    )
    c = conn.cursor()
    task_index = int(call.data.split('_')[2])
    user_id = call.message.chat.id
    c.execute('SELECT * FROM task WHERE user_id=%s', (user_id,))
    rows = c.fetchall()
    if task_index >= 0 and task_index < len(rows):
        msg = bot.send_message(user_id, f'Enter a new name for task {task_index+1}:')
        bot.register_next_step_handler(msg, lambda m: edit_task(m, task_index, user_id))
    else:
        bot.reply_to(call.message, 'Invalid task index')


# function to edit a task
def edit_task(message, task_index, user_id):
    conn = psycopg2.connect(
        host='ep-raspy-base-853661.eu-central-1.aws.neon.tech',
        port='5432',
        dbname='neondb',
        user='AhegaoBurger',
        password='1MV3HhWojRdq'
    )
    c = conn.cursor()
    new_task = message.text
    c.execute('SELECT * FROM task WHERE user_id=?', (user_id,))
    rows = c.fetchall()
    if task_index >= 0 and task_index < len(rows):
        task_id = rows[task_index][0]
        c.execute('UPDATE tasks SET task=? WHERE id=?', (new_task, task_id))
        conn.commit()
        bot.reply_to(message, f'Task {task_index+1} edited to {new_task}')
    else:
        bot.reply_to(message, 'Invalid task index')


# function to handle the Delete task button
@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_task_'))
def delete_task_callback(call):
    conn = psycopg2.connect(
        host='ep-raspy-base-853661.eu-central-1.aws.neon.tech',
        port='5432',
        dbname='neondb',
        user='AhegaoBurger',
        password='1MV3HhWojRdq'
    )
    c = conn.cursor()
    task_index = int(call.data.split('_')[2])
    user_id = call.message.chat.id
    c.execute('SELECT * FROM task WHERE user_id=?', (user_id,))
    rows = c.fetchall()
    if task_index >= 0 and task_index < len(rows):
        task_id = rows[task_index][0]
        c.execute('DELETE FROM tasks WHERE id=?', (task_id,))
        conn.commit()
        bot.reply_to(call.message, f'Task {task_index+1} deleted')
    else:
        bot.reply_to(call.message, 'Invalid task index')


# function to handle the mark task as done button
@bot.callback_query_handler(func=lambda call: call.data.startswith('mark_done_'))
def mark_done_callback(call):
    conn = psycopg2.connect(
        host='ep-raspy-base-853661.eu-central-1.aws.neon.tech',
        port='5432',
        dbname='neondb',
        user='AhegaoBurger',
        password='1MV3HhWojRdq'
    )
    c = conn.cursor()
    task_index = int(call.data.split('_')[2])
    user_id = call.message.chat.id
    c.execute('SELECT * FROM task WHERE user_id=?', (user_id,))
    rows = c.fetchall()
    # check to see the differences between the commented code and non-commented
    # if task_index >= 0 and task_index < len(rows):
    if 0 <= task_index < len(rows):
        task_id = rows[task_index][0]
        c.execute('DELETE FROM tasks WHERE id=?', (task_id,))
        conn.commit()
        bot.reply_to(call.message, f'Task {task_index+1} marked as done')
    else:
        bot.reply_to(call.message, 'Invalid task index')


def start():
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    text = '<b>WELCOME</b>'
    video = open('D:\\Artur\\Database\\Video\\new_intro.mp4', 'rb')
    return text, video, markup

# function to handle the start command
@bot.message_handler(commands=['start'])
def start_handler(message):
    if message.html_text == '/start':
        text = "<b>Main menu</b>"
        video = start()
        markup = main_menu()
        text1, markup1 = news_page()
    else:
        text = '<b>Main menu</b>'
        video = start()
        markup = main_menu()
        text1, markup1 = main_menu()
    bot.send_video(message.chat.id, video)
    bot.send_message(message.chat.id, text=text1, reply_markup=markup1, parse_mode='HTML')
    bot.send_message(message.chat.id, text=text, reply_markup=markup, parse_mode='HTML')


# function to handle unknown commands
@bot.message_handler(func=lambda message: True)
def unknown(message):
    bot.reply_to(message, 'Sorry, I didn\'t understand that command.')


# start the bot
bot.polling(none_stop=True, interval=0)
