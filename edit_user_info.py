# -*- coding: utf-8 -*-
from config import *


@bot.message_handler(func=lambda message: message.text == '✏️Редактировать заказ✏️')
def edit_order_information(message):
    #Редактировать заказ
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Тип доставки')
    button2 = types.KeyboardButton('Город')
    button3 = types.KeyboardButton('Отделение/Почтовый индекс')
    button4 = types.KeyboardButton('Имя')
    button5 = types.KeyboardButton('Номер телефона')
    keyboard.add(button1, button2, button4, button3, button5)
    bot.send_message(message.from_user.id, 'Выберите информацию для редактирования:', reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Город')
def edit_city(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    keyboard = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.from_user.id, 'Введите название вашего города:', reply_markup=keyboard)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET city = ?, delivery_address = ? WHERE user_id = ?", (None, None, message.from_user.id))
    conn.commit()
    cursor.close()
    conn.close()


@bot.message_handler(func=lambda message: message.text == 'Имя')
def edit_name(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    keyboard = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.from_user.id, 'Введите ваше полное имя:', reply_markup=keyboard)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET full_name = ? WHERE user_id = ?", (None, message.from_user.id))
    conn.commit()
    cursor.close()
    conn.close()


@bot.message_handler(func=lambda message: message.text == 'Номер телефона')
def edit_phone(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Отправить номер телефона📲', request_contact=True)
    keyboard.add(button1)
    bot.send_message(message.from_user.id, 'Введите ваш номер телефона:', reply_markup=keyboard)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET phone = ? WHERE user_id = ?", (None, message.from_user.id))
    conn.commit()
    cursor.close()
    conn.close()


@bot.message_handler(func=lambda message: message.text == 'Тип доставки')
def edit_delivery(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🚚Новая Почта🚚')
    button2 = types.KeyboardButton('🚚Укр Почта🚚')
    keyboard.add(button1, button2)
    bot.send_message(message.from_user.id, 'Тип доставки:', reply_markup=keyboard)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET delivery = ?, delivery_address = ? WHERE user_id = ?", (None, None, message.from_user.id))
    conn.commit()
    cursor.close()
    conn.close()


@bot.message_handler(func=lambda message: message.text == 'Отделение/Почтовый индекс')
def edit_delivery_address(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    keyboard = types.ReplyKeyboardRemove(selective=False)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT delivery FROM orders WHERE user_id = ?", (message.from_user.id,))
    result = cursor.fetchone()
    delivery_string = 'Error 851'
    delivery_string = delivery_type_edit[result[0]]
    bot.send_message(message.from_user.id, delivery_string, reply_markup=keyboard)
    cursor.execute("UPDATE orders SET delivery_address = ? WHERE user_id = ?", (None, message.from_user.id))
    conn.commit()
    cursor.close()
    conn.close()

