import sqlite3

import telebot

API_KEY = "5890376662:AAFaY9EYP-Mfg5_fV2bJizn--PS881teiD0"
database = 'C:\\sqlite\\test.db'
bot = telebot.TeleBot(API_KEY)


def main_menu():
    markup = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton("Service Shop", callback_data="category_menu")
    button2 = telebot.types.InlineKeyboardButton("News", callback_data="news_page")
    button3 = telebot.types.InlineKeyboardButton("Afisha", callback_data="afisha_page")
    button4 = telebot.types.InlineKeyboardButton("Spainopedia", callback_data="spainopedia_page")
    button5 = telebot.types.InlineKeyboardButton("About us", callback_data="help_page")
    markup.add(button1, button2, button3, button4, button5)
    return markup


def news_page():
    markup = telebot.types.InlineKeyboardMarkup()
    message_text = 'none'
    markup.add(telebot.types.InlineKeyboardButton(text="← Main menu", callback_data="main_menu"))
    return message_text, markup


def afisha_page():
    markup = telebot.types.InlineKeyboardMarkup()
    message_text = 'none'
    markup.add(telebot.types.InlineKeyboardButton(text="← Main menu", callback_data="main_menu"))
    return message_text, markup


def help_page():
    markup = telebot.types.InlineKeyboardMarkup()
    message_text = '<b>Documentation:</b> \n<a>1.</a> <a ' \
                   'href="https://www.example.com">General Manual:</a>\n' \
                   '<a>2.</a> <a href="https://www.example.com">Your mum</a>\n' \
                   '\n'
    message_text += '<b>Customer support:</b> @lifeisatestbot'
    # Add a button to go back to the main menu
    markup.add(telebot.types.InlineKeyboardButton(text="← Main menu", callback_data="main_menu"))
    return message_text, markup


def category_menu():
    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Fetch all services from the database
    c.execute("SELECT * FROM category")
    categories = c.fetchall()

    # Create an inline keyboard markup
    markup = telebot.types.InlineKeyboardMarkup()

    # Add buttons for each category
    for category in categories:
        button = telebot.types.InlineKeyboardButton(category[1], callback_data=f'category_{category[0]}')
        markup.add(button)

    markup.add(telebot.types.InlineKeyboardButton(text="← Main menu", callback_data="main_menu"))
    conn.close()
    return markup


def service_menu(category_id):
    # get all services of category_id
    conn = sqlite3.connect(database)
    c = conn.cursor()
    # Fetch all services from the database
    c.execute("SELECT c.name, s.id, s.name FROM service AS s "
              "INNER JOIN category AS c "
              "ON s.category_id = c.id "
              "WHERE s.category_id = ?", (category_id,))
    services = c.fetchall()
    category_name = services[0][0]
    markup = telebot.types.InlineKeyboardMarkup()
    # Add buttons for each service
    for service in services:
        button = telebot.types.InlineKeyboardButton(service[2], callback_data=f'service_{category_id}_{service[1]}')
        markup.add(button)
    # Add button to return to the services
    services_button = telebot.types.InlineKeyboardButton(text="← Categories", callback_data="category_menu")
    markup.add(services_button)
    conn.close()
    return category_name, markup


def service_detail_menu(service_id, cart_id):
    # get all services of category_id
    conn = sqlite3.connect(database)
    c = conn.cursor()
    # Fetch all services from the database
    c.execute("SELECT id, code, name, price, description, category_id FROM service WHERE id = ?", (service_id,))
    service = c.fetchall()[0]
    markup = telebot.types.InlineKeyboardMarkup()
    message_text = f"Service Name: {service[2]}\n"
    message_text += f"Service Description: {service[4]}\n"
    message_text += f"Price: {service[3]}$\n"

    # Add a button to add the service to the cart
    add_to_cart_button = telebot.types.InlineKeyboardButton("Add to cart", callback_data=f'add_{service_id}')
    markup.add(add_to_cart_button)

    # Add remove buttons
    remove_from_cart_button = telebot.types.InlineKeyboardButton('Remove from cart', callback_data=f'remove_'
                                                                                                   f'{service_id}')
    markup.add(remove_from_cart_button)

    # Add button to return to the services
    services_button = telebot.types.InlineKeyboardButton(text="← Services", callback_data=f'category_{service[5]}')
    markup.add(services_button)

    # Add button to view the cart
    c.execute('SELECT user_id FROM cart WHERE user_id  = ?', (cart_id,))
    view_cart_button = telebot.types.InlineKeyboardButton(text="View Cart", callback_data=f'cart_{cart_id}')
    markup.add(view_cart_button)
    conn.close()
    return message_text, markup


def add_to_cart(user_id, service_id, quantity):
    # Connect to the database
    conn = sqlite3.connect(database)
    c = conn.cursor()

    query = "SELECT quantity FROM cart WHERE user_id=%s AND service_id=%s" % (user_id, service_id)
    c.execute(query)
    result = c.fetchone()

    if result:
        current_quantity = result[0]
        new_quantity = current_quantity + quantity
        update_query = "UPDATE cart SET quantity=%s WHERE user_id=%s AND service_id=%s" % (new_quantity, user_id,
                                                                                           service_id)
        c.execute(update_query)

    else:
        insert_query = "INSERT INTO cart (user_id, service_id, quantity) VALUES (%s, %s, %s)" % (user_id, service_id,
                                                                                                 quantity)
        c.execute(insert_query)

    conn.commit()
    conn.close()


def remove_from_cart(user_id, service_id, quantity):
    # Connect to the database
    conn = sqlite3.connect(database)
    c = conn.cursor()

    query = "SELECT quantity FROM cart WHERE user_id=%s AND service_id=%s" % (user_id, service_id)
    c.execute(query)
    result = c.fetchone()
    if result:
        current_quantity = result[0]
        new_quantity = current_quantity - quantity
        if new_quantity > 0:
            update_query = "UPDATE cart SET quantity=%s WHERE user_id=%s AND service_id=%s" % (new_quantity, user_id,
                                                                                               service_id)
            c.execute(update_query)
        else:
            delete_query = "DELETE FROM cart WHERE user_id=%s AND service_id=%s" % (user_id, service_id)
            c.execute(delete_query)
    conn.commit()
    conn.close()


def cart_menu(cart_user_id):
    # code to view the cart
    # Connect to the database
    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Find the user's cart items
    c.execute("SELECT service.id, service.name, service.price, service.category_id FROM service "
              "INNER JOIN cart ON service.id = cart.service_id "
              "WHERE cart.user_id = ?", (cart_user_id, ))
    items = c.fetchall()

    # Create an inline keyboard markup
    markup = telebot.types.InlineKeyboardMarkup()

    # Build the message to display the items
    if items:
        for item in items:
            button = telebot.types.InlineKeyboardButton(item[1], callback_data=f'service_{item[3]}_{item[0]}')
            markup.add(button)
    else:
        text = "Your cart is empy"
        bot.answer_callback_query(cart_user_id, text=text, cache_time=100)

    services_button = telebot.types.InlineKeyboardButton(text="← Categories", callback_data="category_menu")
    markup.add(services_button)
    # Close the cursor and connection
    conn.close()
    return markup


# Slash command handler
@bot.message_handler(commands=["menu", "shop", "cart", "help"])
def main_menu_handler(message):
    if message.html_text == "/menu":
        text = "Main menu"
        markup = main_menu()
    elif message.html_text == "/shop":
        text = "Service Shop"
        markup = category_menu()
    elif message.html_text == "/cart":
        text = "Cart:"
        markup = cart_menu(message.from_user.id)
    elif message.html_text == "/help":
        text, markup = help_page()
    else:
        markup = "tough titty"
        text = "none"
    bot.send_message(message.chat.id, text=text, reply_markup=markup, parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: call.data.split("_")[0] in ["main", "category", "service", "cart"])
def callback_menu_handler(call):
    if call.data == "main_menu":
        text = "Main menu:"
        markup = main_menu()
    elif call.data == "category_menu":
        text = "Service Shop:"
        markup = category_menu()
    elif call.data.startswith("category_"):
        text, markup = service_menu(call.data.split("_")[1])
    elif call.data.startswith("service_"):
        text, markup = service_detail_menu(call.data.split("_")[2], cart_id=call.from_user.id)
    elif call.data.startswith('cart_'):
        text = 'Cart'
        markup = cart_menu(call.from_user.id)
    else:
        text = "none"
        markup = "no one loves me"
        # Edit the current message
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.split("_")[0] in ["add", "remove"])
def execute_function_callback_handler(callback):
    if callback.data.startswith("add_"):
        text = "Service added to cart!"
        add_to_cart(callback.from_user.id, service_id=callback.data.split("_")[1], quantity=1)

    elif callback.data.startswith("remove_"):
        text = "Service removed from cart"
        remove_from_cart(callback.from_user.id, service_id=callback.data.split("_")[1], quantity=1)
    else:
        text = "none"

    # Confirm the service was added to the cart
    bot.answer_callback_query(callback_query_id=callback.id, text=text)


bot.polling(none_stop=True, interval=0)
