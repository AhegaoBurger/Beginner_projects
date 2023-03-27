API_KEY = "5582044861:AAEP-2xXeydEDLVJqhJ_cgU1BsGojjoKgcQ"
import sqlite3
import telebot
from telebot import types

bot = telebot.TeleBot(API_KEY)


@bot.message_handler(func=lambda message: message.text == "Menu")
def get_main_menu_markup():
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Shop", callback_data="shop")
        button2 = types.InlineKeyboardButton("Contacts", callback_data="contacts")
        button3 = types.InlineKeyboardButton("Help", callback_data="help")
        markup.add(button1, button2, button3)
        return markup


# main menu command handler
@bot.message_handler(commands=["menu"])
def main_menu(message):
    bot.send_message(message.chat.id, "Main menu:", reply_markup=get_main_menu_markup())


main_menu_markup = get_main_menu_markup()


def category_list(call):
    conn = sqlite3.connect('C:\\sqlite\\test.db')
    c = conn.cursor()

    # Fetch all services from the database
    c.execute("SELECT * FROM categories")
    categories = c.fetchall()

    # Create an inline keyboard markup
    markup = types.InlineKeyboardMarkup()

    # Add buttons for each category
    for category in categories:
        button = types.InlineKeyboardButton(category[1], callback_data=f'category_{category[0]}')
        markup.add(button)

    # Add button to return to main menu
    main_menu_button = types.InlineKeyboardButton("← Main menu", callback_data="main_menu")
    markup.add(main_menu_button)

    # Edit the current message with the inline keyboard markup
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Select a service:",
                          reply_markup=markup)

    # Close the database connection
    conn.close()


def service_list(call, category_id):
    conn = sqlite3.connect('C:\\sqlite\\test.db')
    c = conn.cursor()

    # Fetch all services from the database
    c.execute("SELECT * FROM services WHERE category_id = ?", (category_id,))
    services = c.fetchall()

    # Create an inline keyboard markup
    markup = types.InlineKeyboardMarkup()

    # Add buttons for each service
    for service in services:
        button = types.InlineKeyboardButton(service[1], callback_data=f'service_{service[0]}')
        markup.add(button)

    # Add button to return to the services
    services_button = types.InlineKeyboardButton("← Categories", callback_data="shop")
    markup.add(services_button)

    # Edit the current message with the inline keyboard markup
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Select a service:",
                          reply_markup=markup)
    
    # Close the database connection
    conn.close()


@bot.callback_query_handler(func=lambda call: call.data.startswith("service_"))
def show_service_details(call):
    # Get the service ID from the callback data
    service_id = call.data.split('_')[1]

    # Connect to the database
    conn = sqlite3.connect('C:\\sqlite\\test.db')
    c = conn.cursor()

    # Fetch the service details
    c.execute("SELECT * FROM services WHERE id = ?", (service_id,))
    service = c.fetchone()

    # Create an inline keyboard markup
    markup = types.InlineKeyboardMarkup()
    # Add a button to buy the service
    buy_button = types.InlineKeyboardButton("Buy", callback_data=f'buy_{service_id}')
    markup.add(buy_button)

    # Add button to return to the services
    services_button = types.InlineKeyboardButton("← Back", callback_data="back")
    markup.add(services_button)

    # Build the message to be sent to the user
    message_text = f"Service Name: {service[1]}\n"
    message_text += f"Service Description: {service[3]}\n"
    message_text += f"Service: {service[2]}$\n"

    # Edit the current message to show the service details
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message_text,
                          reply_markup=markup)

    # Close the database connection
    conn.close()


@bot.callback_query_handler(func=lambda call: call.data in ["main menu", "categories", "services"])
def callback(call):
    if call.data == "main menu":
        main_menu_callback(call)
    elif call.data == "categories":
        category_list(call)
    elif call.data == "services":
        service_list(call)


@bot.callback_query_handler(func=lambda call: call.data in ["shop", "contacts", "help"])
def main_menu_callback(call):
    if call.data == "shop":
        category_list(call)
    elif call.data == "contacts":
        bot.send_message(call.message.chat.id, "You selected option 2.")
    elif call.data == "help":
        bot.send_message(call.message.chat.id, "You selected option 3.")


@bot.callback_query_handler(func=lambda call: call.data == "main_menu")
def return_main_menu(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Main menu:",
                          reply_markup=main_menu_markup)

# @bot.message_handler(func=lambda message: message.text == "View cart")
# def view_cart(cart):
#     # code to view the cart
#     # Connect to the database
#     conn = sqlite3.connect('C:\\sqlite\\test.db')
#     c = conn.cursor()

#     # Find the user's cart items
#     c.execute("SELECT services.name, services.price FROM services INNER JOIN cart ON services.id = cart.service_id WHERE cart.user_id = ?", (cart.from_user.id,))
#     items = c.fetchall()

#     # Build the message to display the items
#     if items:
#         msg = "Your cart contains:\n"
#         for item in items:
#             msg += f"- {item[0]}, {item[1]}€\n"
#         bot.send_message(cart.chat.id, msg)
#     else:
#         bot.send_message(cart.chat.id, "Your cart is empty.")

#     # Close the cursor and connection
#     c.close()
#     conn.close()




#                 make buttons
#                         button_buy = types.InlineKeyboardButton('Buy', callback_data = '💳 Buy')
#                         button_back = types.InlineKeyboardButton('Back', callback_data = '← Back')

#                         keyboard = types.InlineKeyboardMarkup()
#                         keyboard.add(button_buy)
#                         keyboard.add(button_back)
#                         # Build the message to be sent to the user
#                         message_text = f"Information for service {service[1]}: \n"
#                         message_text += f"Price: {service[2]}$\n"
#                         # Send the message to the user
#                         bot.send_message(message.chat.id, message_text, reply_markup = keyboard)
#                     else:
#                         bot.send_message(message.chat.id, f"Service {service_name} not found.")

#                     # Close the database connection
#                     conn.close()
                
# except:
#     @bot.message_handler(content_types=["text"])
#     def handle_text(message):
#         answer = r"D:\Artur\Memes\Meme Templates\giphy.gif"
#         bot.send_document(message.chat.id, answer)

bot.polling(none_stop=True, interval=0)
