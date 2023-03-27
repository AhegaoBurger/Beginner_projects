import sqlite3

import telebot

API_KEY = "5890376662:AAFaY9EYP-Mfg5_fV2bJizn--PS881teiD0"
database = 'C:\\sqlite\\test.db'
bot = telebot.TeleBot(API_KEY)


def main_menu():
    markup = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton("Categories", callback_data="category_menu")
    button2 = telebot.types.InlineKeyboardButton("Contacts", callback_data="contacts_menu")
    button3 = telebot.types.InlineKeyboardButton("Help", callback_data="help_menu")
    markup.add(button1, button2, button3)
    return markup


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


def service_detail_menu(service_id):
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
    # Add a button to buy the service
    add_to_cart_button = telebot.types.InlineKeyboardButton("Add to cart", callback_data=f'add_{service_id}')
    markup.add(add_to_cart_button)
    # Add button to return to the services
    services_button = telebot.types.InlineKeyboardButton(text="← Services", callback_data=f"category_{service[5]}")
    markup.add(services_button)
    conn.close()
    return message_text, markup


def add_to_cart(cart):
    # Connect to the database
    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Split the callback data to get the service ID
    service_id = cart.data.split("_")[1]

    # Add the service to the cart
    c.execute("INSERT INTO cart (user_id, service_id) VALUES (?,?)", (cart.from_user.id, service_id))
    conn.commit()
    conn.close()

    # Confirm the service was added to the cart
    bot.answer_callback_query(cart.id, text="Service added to cart!")


def cart_menu(cart_user_id):
    # code to view the cart
    # Connect to the database
    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Find the user's cart items
    # c.execute("SELECT service_id FROM cart WHERE user_id=%s" % user_id)
    # c.execute("select name, price from service where id in %s" % service_ids)
    c.execute("SELECT service.id, service.name, service.price FROM service "
              "INNER JOIN cart ON service.id = cart.service_id "
              "WHERE cart.user_id = ?", (cart_user_id, ))
    items = c.fetchall()

    # Create an inline keyboard markup
    markup = telebot.types.InlineKeyboardMarkup()

    # Build the message to display the items
    if items:
        for item in items:
            button = telebot.types.InlineKeyboardButton(item[1], callback_data=f'service_{item[0]}')
            # msg += f"- {item[0]}, {item[1]}€\n"
            markup.add(button)
    else:
        text = "Your cart is empy"
        bot.answer_callback_query(cart_user_id, text=text)

    # Close the cursor and connection
    conn.close()
    return markup


# Slash command handler
@bot.message_handler(commands=["menu", "cart"])
def main_menu_handler(message):
    if message.html_text == "/menu":
        text = "Main menu"
        markup = main_menu()
    elif message.html_text == "/cart":
        text = "Cart:"
        markup = cart_menu(message.from_user.id)
    else:
        markup = "tough titty"
        text = "none"
    bot.send_message(message.chat.id, text=text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.split("_")[0] in ["main", "category", "service"])
def callback_menu_handler(call):
    if call.data == "main_menu":
        text = "Main menu:"
        markup = main_menu()
    elif call.data == "category_menu":
        text = "Categories menu:"
        markup = category_menu()
    elif call.data.startswith("category_"):
        text, markup = service_menu(call.data.split("_")[1])
    elif call.data.startswith("service_"):
        text, markup = service_detail_menu(call.data.split("_")[2])
    else:
        text = "none"
        markup = "no one loves me"
        # Edit the current message
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.split("_")[0] in ["add"])
def callback_add_handler(callback):
    if callback.data.startswith("add_"):
        add_to_cart(callback)


bot.polling(none_stop=True, interval=0)
