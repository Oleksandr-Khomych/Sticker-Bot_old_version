# -*- coding: utf-8 -*-
from config import *
from main import main_message

# Оформлення замовлення ------------------------


@bot.message_handler(func=lambda message: message.text == '❌Отменить заказ❌')
def cancel_order(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE orders SET order_in_process = ?, delivery = ?, delivery_address = ?, order_id = ? WHERE user_id = ?",
        ('False', None, None, None, message.from_user.id,))
    bot.send_message(message.from_user.id, 'Заказ отменен. Вы будете перенаправлены в главное меню.')
    main_message(message)
    conn.commit()
    cursor.close()
    conn.close()


@bot.message_handler(func=lambda message: message.text == '✅Продолжить✅')
def payment_type(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT order_in_process FROM orders WHERE user_id = ?", (message.from_user.id,))
    order_in_process = cursor.fetchone()
    if order_in_process[0] == 'True':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('✅Отправить заказ на обработку✅')
        button2 = types.KeyboardButton('❌Отменить заказ❌')
        keyboard.add(button1, button2)
        cursor.execute("SELECT order_id FROM orders WHERE user_id = ?", (message.from_user.id,))
        result = cursor.fetchone()
        bot.send_message(message.from_user.id, f'Отлично. Отправляйте заказ на обработку, после чего отправьте предоплату на счет **** **** **** ****(обязательно укажите ваш номер заказа({result[0]}📝) в комментарии к переводу средств) и ожидайте номер накладной службы доставки', reply_markup=keyboard)
    conn.commit()
    cursor.close()
    conn.close()


@bot.message_handler(func=lambda message: message.text == '✅Отправить заказ на обработку✅')
def complete(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT order_in_process FROM orders WHERE user_id = ?", (message.from_user.id,))
    order_in_process = cursor.fetchone()
    if order_in_process[0] == 'True':
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
        keyboard.add(main_menu_button)
        bot.send_message(message.from_user.id, 'Заказ отправлен администратору на обработку', reply_markup=keyboard)
        cursor.execute("SELECT * FROM orders WHERE user_id = ?", (message.from_user.id,))
        result = cursor.fetchone()
        # Додаємо нового користувача в БД. (щоб уникнути ситуативного бага)
        if not result:
            cursor.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           (message.from_user.id, None, None, None, None, None, None, None))
            cursor.execute("SELECT * FROM orders WHERE user_id = ?", (message.from_user.id,))
            result = cursor.fetchone()
            MyLoger.error(f"Error get user by id! message.from_user.id={message.from_user.id}")
        user_id, order_in_process, delivery, city, delivery_address, full_name, phone, order_id = result
        cursor.execute("SELECT * FROM basket WHERE user_id = ?", (message.from_user.id,))
        article = cursor.fetchall()
        string = 'Заказ:'
        if article:
            for el in article:
                string += f'\nТовар {el[1]}\n Cет: {el[2]} стикеров\n Количество стикерпаков: {el[3]}'
        delivery_string = 'Error #492'
        delivery_string = delivery_type_show[delivery]
        for adm_id in admins_id:
            bot.send_message(adm_id,
                             f'📌Новый заказ!\nuser_id = {message.from_user.id}\n💡{string}\n\n🚚Тип доставки: {delivery}\n🏙Город: {city}\n🏢{delivery_string}: {delivery_address}\n👤Полное имя: {full_name}\n📱Номер телефона : {phone}\n📌id_Заказа : {order_id}')
        cursor.execute("INSERT INTO order_generated VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (message.from_user.id, order_id, 'Ожидает обработки администратором', None, string[7:],
                        delivery,
                        city, delivery_address, full_name, phone))
        cursor.execute("DELETE FROM basket WHERE user_id = ? ", (message.from_user.id,))
        cursor.execute(
            "UPDATE orders SET order_in_process = ?, delivery = ?, delivery_address = ?, order_id = ? WHERE user_id = ?",
            ('False', None, None, None, message.from_user.id,))
    conn.commit()
    cursor.close()
    conn.close()


# Хендлер для оформлення замовлення
@bot.message_handler(content_types=['contact', 'text'])
def get_order(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE user_id = ?", (message.from_user.id,))
    result = cursor.fetchone()
    if not result:
        cursor.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (message.from_user.id, None, None, None, None, None, None, None))
        cursor.execute("SELECT * FROM orders WHERE user_id = ?", (message.from_user.id,))
        result = cursor.fetchone()
        MyLoger.error(f"Error get user by id! message.from_user.id={message.from_user.id}")
    user_id, order_in_process, delivery, city, delivery_address, full_name, phone, order_id = result
    if order_in_process == 'True':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # Якщо правда, значить оформлюємо заказ
        if not delivery:
            if message.text == '🚚Новая Почта🚚' or message.text == '🚚Укр Почта🚚':
                cursor.execute("UPDATE orders SET delivery = ? WHERE user_id = ? ",
                               (message.text[1:-1], message.from_user.id))
                ordering_stage(message, cursor)
            else:
                button1 = types.KeyboardButton('🚚Новая Почта🚚')
                button2 = types.KeyboardButton('🚚Укр Почта🚚')
                button3 = types.KeyboardButton('❌Отменить заказ❌')
                keyboard.row(button1, button2)
                keyboard.row(button3)
                bot.send_message(message.from_user.id, 'Пожалуйста выберите тип доставки (см. кнопки внизу)', reply_markup=keyboard)
        elif not city:
            cursor.execute("UPDATE orders SET city = ? WHERE user_id = ?", (message.text, message.from_user.id))
            ordering_stage(message, cursor)
        elif not delivery_address:
            cursor.execute("UPDATE orders SET delivery_address = ? WHERE user_id = ?", (message.text, message.from_user.id))
            ordering_stage(message, cursor)
        elif not full_name:
            cursor.execute("UPDATE orders SET full_name = ? WHERE user_id = ?", (message.text, message.from_user.id))
            ordering_stage(message, cursor)
        elif not phone:
            if message.text is None:
                cursor.execute("UPDATE orders SET phone = ? WHERE user_id = ?", (message.contact.phone_number, message.from_user.id))
            else:
                cursor.execute("UPDATE orders SET phone = ? WHERE user_id = ?", (message.text, message.from_user.id))
            ordering_stage(message, cursor)
    conn.commit()
    cursor.close()
    conn.close()


# функція для оформлення замовлень(викликаєть з get_order())
def ordering_stage(message, cursor):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    cursor.execute("SELECT * FROM orders WHERE user_id = ?", (message.from_user.id,))
    result = cursor.fetchone()
    if not result:
        cursor.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (message.from_user.id, None, None, None, None, None, None, None))
        cursor.execute("SELECT * FROM orders WHERE user_id = ?", (message.from_user.id,))
        result = cursor.fetchone()
        MyLoger.error(f"Error get user by id! message.from_user.id={message.from_user.id}")
    user_id, order_in_process, delivery, city, delivery_address, full_name, phone, order_id = result
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if not city:
        button = types.KeyboardButton('❌Отменить заказ❌')
        keyboard.add(button)
        bot.send_message(message.from_user.id, 'Введите название вашего города:', reply_markup=keyboard)
    elif not delivery_address:
        button = types.KeyboardButton('❌Отменить заказ❌')
        keyboard.add(button)
        string = 'Error #924'
        string = delivery_type_edit[delivery]
        bot.send_message(message.from_user.id, string, reply_markup=keyboard)
    elif not full_name:
        button = types.KeyboardButton('❌Отменить заказ❌')
        keyboard.add(button)
        bot.send_message(message.from_user.id, 'Введите ваше полное имя:', reply_markup=keyboard)
    elif not phone:
        button = types.KeyboardButton('Отправить номер телефона📲', request_contact=True)
        button2 = types.KeyboardButton('❌Отменить заказ❌')
        keyboard.add(button)
        keyboard.add(button2)
        bot.send_message(message.from_user.id, 'Введите ваш номер телефона:', reply_markup=keyboard)
    elif phone:
        button = types.KeyboardButton('✅Продолжить✅')
        button1 = types.KeyboardButton('✏️Редактировать заказ✏️')
        button2 = types.KeyboardButton('❌Отменить заказ❌')
        keyboard.row(button)
        keyboard.row(button1, button2)
        cursor.execute("SELECT * FROM basket WHERE user_id = ?", (message.from_user.id,))
        article = cursor.fetchall()
        string = 'Состав заказа:'
        if article:
            for el in article:
                string += f'\n💡Товар {el[1]}\n 💡Cет: {el[2]} стикеров\n 💡Количество стикерпаков: {el[3]}'
        order_string = f'📌Заказ №{order_id}\n📍Проверьте введенную информацию:\n{string}'
        delivery_string = 'Error # 489'
        delivery_string = delivery_type_show[delivery]
        bot.send_message(message.from_user.id,
                         f'{order_string}\n🚚Тип доставки: {delivery}\n🏙Город: {city}\n🏢{delivery_string}: {delivery_address}\n👤Полное имя: {full_name}\n📱Номер телефона : {phone}',
                         reply_markup=keyboard)
