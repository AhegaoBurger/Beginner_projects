import sqlite3

import telebot

API_KEY = "5582044861:AAEP-2xXeydEDLVJqhJ_cgU1BsGojjoKgcQ"
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
    # get all categories
    markup = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton("Category 1", callback_data="category_1")
    button2 = telebot.types.InlineKeyboardButton("Category 2", callback_data="category_2")
    button3 = telebot.types.InlineKeyboardButton("Category 3", callback_data="category_3")
    markup.add(button1, button2, button3)
    # Add button to return to main menu
    markup.add(telebot.types.InlineKeyboardButton(text="← Main menu", callback_data="main_menu"))
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
    message_text += f"Service: {service[3]}$\n"
    # Add button to return to the services
    services_button = telebot.types.InlineKeyboardButton(text="← Services", callback_data=f"category_{service[5]}")
    markup.add(services_button)
    return message_text, markup


# main menu command handler
@bot.message_handler(commands=["menu"])
def main_menu_handler(message):
    markup = main_menu()
    bot.send_message(message.chat.id, "Main menu:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.split("_")[0] in ["main", "category", "service"])
def callback_menu(call):
    text = False
    if call.data == "main_menu":
        text = "Main menu:"
        markup = main_menu()
    elif call.data == "category_menu":
        text = "Categories menu:"
        markup = category_menu()
    elif call.data.startswith("category_"):
        text, markup = service_menu(call.data.split("_")[1])
    elif call.data.startswith("service_"):
        text, markup = service_detail_menu(call.data.split("_")[1])
    if text:
        # Edit the current message
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=text, reply_markup=markup)


bot.polling(none_stop=True, interval=0)

# @bot.callback_query_handler(func=lambda call: call.data in ["category_1", "category_2", "category_3"])
# def category_callback(call):
#     if call.data == "category_1":
#         service_menu()
#     elif call.data == "category_2":
#         service_menu()
#     elif call.data == "category_3":
#         service_menu()


# @bot.callback_query_handler(func=lambda call: call.data in ["service1", "service2", "service3", "service4", "service5", "service6" ])
# def service_callback(call):
#     if call.data == "service1":
#         service_details()
#     elif call.data == "service2":
#         service_details()
#     elif call.data == "service3":
#         service_details()
#     elif call.data == "service4":
#         service_details()
#     elif call.data == "service5":
#         service_details()
#     elif call.data == "service6":
#         service_details()
#
# def service_details(details, service_id):
#     # Create an inline keyboard markup
#     markup = telebot.types.InlineKeyboardMarkup()
#     # Add a button to buy the service
#     buy_button = telebot.types.InlineKeyboardButton("💳 Buy", callback_data=f'buy_{service_id}')
#     markup.add(buy_button)
#
#     # Add button to return to the services
#     services_button = telebot.types.InlineKeyboardButton(text="← Services", callback_data="services")
#     markup.add(services_button)
#
#     # Build the message to be sent to the user
#     message_text = f"Service Name: {service[1]}\n"
#     message_text += f"Service Description: {service[3]}\n"
#     message_text += f"Service: {service[2]}$\n"
#
#     # Edit the current message to show the service details
#     bot.edit_message_text(chat_id=details.message.chat.id, message_id=details.message.message_id, text=message_text,
#                           reply_markup=markup)
#
#
# def service_menu(menu2):
#     # Create an inline keyboard markup
#     markup = telebot.types.InlineKeyboardMarkup()
#     button1 = telebot.types.InlineKeyboardButton("Service 1", callback_data="service1", category_id=1)
#     button2 = telebot.types.InlineKeyboardButton("Service 2", callback_data="service2", category_id=1)
#     button3 = telebot.types.InlineKeyboardButton("Service 3", callback_data="service3", category_id=2)
#     button4 = telebot.types.InlineKeyboardButton("Service 4", callback_data="service1", category_id=2)
#     button5 = telebot.types.InlineKeyboardButton("Service 5", callback_data="service2", category_id=3)
#     button6 = telebot.types.InlineKeyboardButton("Service 6", callback_data="service3", category_id=3)
#     markup.add(button1, button2, button3, button4, button5, button6)
#
#     # Add button to return to the services
#     services_button = telebot.types.InlineKeyboardButton(text="← Categories", callback_data="category_menu")
#     markup.add(services_button)
#
#     # Edit the current message with the inline keyboard markup
#     bot.edit_message_text(chat_id=menu2.message.chat.id, message_id=menu2.message.message_id, text="Select a service:",
#                           reply_markup=markup)
#
#
# def category_menu(menu1):
#     markup = telebot.types.InlineKeyboardMarkup()
#     button1 = telebot.types.InlineKeyboardButton("Category 1", callback_data="category1")
#     button2 = telebot.types.InlineKeyboardButton("Category 2", callback_data="category2")
#     button3 = telebot.types.InlineKeyboardButton("Category 3", callback_data="category3")
#     markup.add(button1, button2, button3)
#     # Add button to return to main menu
#     main_menu_button = telebot.types.InlineKeyboardButton(text="← Main menu", callback_data="return_main_menu")
#     markup.add(main_menu_button)
#
#     #     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Main menu:",
#     #                           reply_markup=main_menu_markup)
#
#     # Edit the current message with the inline keyboard markup
#     bot.edit_message_text(chat_id=menu1.message.chat.id, message_id=menu1.message.message_id, text="Select a category:",
#                           reply_markup=markup)
#
#
# @bot.callback_query_handler(func=lambda call: call.data == "return_main_menu")
# def return_main_menu(call):
#     # Create an inline keyboard markup
#     markup = telebot.types.InlineKeyboardMarkup()
#     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Main menu:",
#                           reply_markup=markup)


#
#
# @bot.callback_query_handler(func=lambda call: call.data.startswith("category_"))
# def service_list_callback(call):
#     category_id = call.data.split("_")[1]
#     service_list(call, category_id)
#
#
#
#
# @bot.callback_query_handler(func=lambda call: call.data.startswith("service_"))
# def show_service_details_callback(call):
#     # Get the service ID from the callback data
#     service_id = call.data.split('_')[1]
#     show_service_details(call, service_id)
#
#
# # @bot.callback_query_handler(func=lambda call: call.data == "services")
# # def return_to_services(call):
# #     markup = types.InlineKeyboardMarkup()
# #     category_id = call.data.split("_")[1]
# #     service_list(call, category_id)
# #     # Edit the current message with the inline keyboard markup
# #     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
# text="Select a service:",
# #                           reply_markup=markup)
#
#
# def back_button():
#     # Get the current function name
#     current_function = inspect.currentframe().f_back.f_code.co_name
#     print("Returning to", current_function)
#
#
# @bot.callback_query_handler(func=lambda call: call.data == "return_main_menu")
# def return_main_menu(call):
#     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Main menu:",
#                           reply_markup=main_menu_markup)
#
#
#
#
# # @bot.message_handler(func=lambda message: message.text == "View cart")
# # def view_cart(cart):
# #     # code to view the cart
# #     # Connect to the database
# #     conn = sqlite3.connect('C:\\sqlite\\test.db')
# #     c = conn.cursor()
#
# # # Find the user's cart items c.execute("SELECT services.name, services.price FROM services INNER JOIN cart ON
# # services.id = cart.service_id WHERE cart.user_id = ?", (cart.from_user.id,)) items = c.fetchall()
#
# #     # Build the message to display the items
# #     if items:
# #         msg = "Your cart contains:\n"
# #         for item in items:
# #             msg += f"- {item[0]}, {item[1]}€\n"
# #         bot.send_message(cart.chat.id, msg)
# #     else:
# #         bot.send_message(cart.chat.id, "Your cart is empty.")
#
# #     # Close the cursor and connection
# #     c.close()
# #     conn.close()
#
#
