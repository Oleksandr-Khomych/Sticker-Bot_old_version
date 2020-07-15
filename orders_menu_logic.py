# -*- coding: utf-8 -*-
from config import *


@bot.message_handler(func=lambda message: message.text == '🛍Заказы🛍')
def order_generated(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM order_generated WHERE user_id = ?", (message.from_user.id,))
    orders_list = cursor.fetchall()
    keyboard = types.InlineKeyboardMarkup()
    string = "Список заказов :"
    if orders_list:
        for order in orders_list:
            button = types.InlineKeyboardButton(f'📌Заказ #{order[1]}', callback_data=f'Order#{order[1]}')
            keyboard.add(button)
    else:
        string += '\nВы не сделали ни одного заказа'
    keyboard.add(main_menu_inline_button)
    bot.send_message(message.from_user.id, string, reply_markup=keyboard)
    conn.commit()
    cursor.close()
    conn.close()


@bot.callback_query_handler(func=lambda message: 'Order#' in message.data)
def show_order(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM order_generated WHERE user_id = ? AND order_id = ?", (message.from_user.id, message.data[6:]))
    order = cursor.fetchone()
    user_id, order_id, status, TTH, article, delivery, city, delivery_addres, full_name, phone = order
    delivery_type = 'Error #687'
    delivery_type = delivery_type_show[order[5]]
    text = f'Заказ №{order_id}\nСтатус заказа: {status}\nТТН: {TTH}\nСостав :\n{article}\n Тип доставки: {delivery}\nГород : {city}\n{delivery_type}{delivery_addres}\nПолное имя: {full_name}\nНомер телефона: {phone}\n'
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton('👈Назад👈', callback_data='Назад в Заказы')
    keyboard.add(button)
    try:
        bot.delete_message(message.message.chat.id, message.message.message_id)
    except:
        MyLoger.error(f"Error delete message! message.from_user.id={message.from_user.id}")
    bot.send_message(message.from_user.id, text, reply_markup=keyboard)
    conn.commit()
    cursor.close()
    conn.close()


# Назад в Заказы
@bot.callback_query_handler(func=lambda message: message.data == 'Назад в Заказы')
def back_in_orders(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    try:
        bot.delete_message(message.message.chat.id, message.message.message_id)
    except:
        MyLoger.error(f"Error delete message! message.from_user.id={message.from_user.id}")
    order_generated(message)
