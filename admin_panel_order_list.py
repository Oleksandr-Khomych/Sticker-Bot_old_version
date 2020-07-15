# -*- coding: utf-8 -*-
from config import *

# ===============================================================Список замовлень


@bot.message_handler(func=lambda message: message.text == 'Список Замовлень' and message.from_user.id in admins_id)
def order_list_admin(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Всі замовлення', callback_data='all')
    button2 = types.InlineKeyboardButton('Актуальні', callback_data='relevant')
    keyboard.add(button1, button2)
    keyboard.add(admin_main_inline_button)
    bot.send_message(message.from_user.id, 'Оберіть фільтр:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda message: message.data == 'all' and message.from_user.id in admins_id)
def all_orders(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM order_generated")
    orders_list = cursor.fetchall()
    keyboard = types.InlineKeyboardMarkup()
    string = "Список всіх замовлень:"
    if orders_list:
        for order in orders_list:
            button = types.InlineKeyboardButton(f'📌Заказ #{order[1]}. Статус:{order[2]}',
                                                callback_data=f'admin_order#{order[1]}')
            keyboard.add(button)
    else:
        string += '\nЗамовлень ще немає'
    button_main = types.InlineKeyboardButton('Адмін Меню', callback_data='Адмін Меню')
    keyboard.add(button_main)
    bot.delete_message(message.message.chat.id, message.message.message_id)
    bot.send_message(message.from_user.id, string, reply_markup=keyboard)
    conn.commit()
    cursor.close()
    conn.close()


@bot.callback_query_handler(func=lambda message: message.data == 'relevant' and message.from_user.id in admins_id)
def relevant_orders(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM order_generated WHERE status NOT IN ("Выполнено")')
    orders_list = cursor.fetchall()
    keyboard = types.InlineKeyboardMarkup()
    string = "Список всіх замовлень:"
    if orders_list:
        for order in orders_list:
            button = types.InlineKeyboardButton(f'📌Заказ #{order[1]}. Статус:{order[2]}',
                                                callback_data=f'admin_order#{order[1]}')
            keyboard.add(button)
    else:
        string += '\nЗамовлень ще немає'
    button_main = types.InlineKeyboardButton('Адмін Меню', callback_data='Адмін Меню')
    keyboard.add(button_main)
    bot.delete_message(message.message.chat.id, message.message.message_id)
    bot.send_message(message.from_user.id, string, reply_markup=keyboard)
    conn.commit()
    cursor.close()
    conn.close()


@bot.callback_query_handler(func=lambda message: message.data == 'Список Замовлень' and message.from_user.id in admins_id)
def order_list_admin_callback(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    try:
        bot.delete_message(message.message.chat.id, message.message.message_id)
    except:
        MyLoger.error(f"Error delete message! message.from_user.id={message.from_user.id}")
    order_list_admin(message)


@bot.callback_query_handler(func=lambda message: 'admin_order#' in message.data and message.from_user.id in admins_id)
def show_order_admin(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM order_generated WHERE order_id = ?", (message.data[12:],))
    order = cursor.fetchone()
    delivery_type = 'Error #687'
    if order[5] == 'Новая Почта':
        delivery_type = 'Отделение Новой почты: '
    elif order[5] == 'Укр Почта':
        delivery_type = 'Почтовый индекс:'
    text = f'📌Заказ №{order[1]}\nСтатус заказа: {order[2]}\nТТН: {order[3]}\n💡Состав заказа:\n{order[4]}\n 🚚Тип доставки: {order[5]}\n🏙Город : {order[6]}\n🏢{delivery_type}{order[7]}\n👤Полное имя: {order[8]}\n📱Номер телефона: {order[9]}'
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Оновити статус замовлення:', callback_data=f'update_status#{order[1]}')
    button2 = types.InlineKeyboardButton('Оновити ТТН', callback_data=f'update_TTH#{order[1]}')
    button3 = types.InlineKeyboardButton('Назад', callback_data='Список Замовлень')
    keyboard.add(button1, button2, button3)
    try:
        bot.delete_message(message.message.chat.id, message.message.message_id)
    except:
        MyLoger.error(f"Error delete message! message.from_user.id={message.from_user.id}")
    bot.send_message(message.from_user.id, text, reply_markup=keyboard)
    conn.commit()
    cursor.close()
    conn.close()


@bot.callback_query_handler(func=lambda message: 'update_status#' in message.data and message.from_user.id in admins_id)
def update_status_order(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    index = message.data.find("#")
    order_number = message.data[index+1:]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton('Заказ принят. Ожидайте ТТН', callback_data=f'setStatus_Заказ принят#{order_number}')
    button2 = types.InlineKeyboardButton('В процесе доставки', callback_data=f'setStatus_В процесе доставки#{order_number}')
    button3 = types.InlineKeyboardButton('Выполнено', callback_data=f'setStatus_Выполнено#{order_number}')
    button4 = types.InlineKeyboardButton('Заказ отклонено', callback_data=f'setStatus_Заказ отклонено#{order_number}')
    button5 = types.InlineKeyboardButton('Назад', callback_data='Список Замовлень')
    keyboard.add(button1, button2, button3, button4, button5)
    try:
        bot.delete_message(message.message.chat.id, message.message.message_id)
    except:
        MyLoger.error(f"Error delete message! message.from_user.id={message.from_user.id}")
    bot.send_message(message.from_user.id, f'📌Виберіть статус замовлення #{order_number}:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda message: 'setStatus_' in message.data and message.from_user.id in admins_id)
def set_status_order(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    print(f'message.data = {message.data}')
    index1 = message.data.find('_')
    index2 = message.data.find('#')
    status = message.data[index1+1:index2]
    order_id = message.data[index2+1:]
    print(f'status={status}')
    print(f'order_id={order_id}')
    global update_order_status
    update_order_status = [status, order_id]
    try:
        bot.delete_message(message.message.chat.id, message.message.message_id)
    except:
        MyLoger.error(f"Error delete message! message.from_user.id={message.from_user.id}")
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton('Добавити коментар', callback_data='comment_true')
    button2 = types.InlineKeyboardButton('Не добавляти коментар', callback_data='comment_false')
    button3 = types.InlineKeyboardButton('Відмінити редактування статусу', callback_data='comment_cancel')
    keyboard.add(button1, button2, button3)
    bot.send_message(message.from_user.id, 'Бажаєте добавити коментар з поясненням до статусу?',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda message: 'comment_' in message.data and message.from_user.id in admins_id)
def add_comment(message):
    MyLoger.debug(
        f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    index1 = message.data.find('_')
    action = message.data[index1+1:]
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        global update_order_status
        status, order_id = update_order_status
        if action == 'cancel':
            bot.send_message(message.from_user.id,
                             f'Ви відмінили оновлення статусу для замовлення #{order_id}. Вас буде перенаправлено в Список Замовлень')
            order_list_admin(message)
            update_order_status = False
        elif action == 'false':
            cursor.execute("UPDATE order_generated SET status = ? WHERE order_id = ?", (status, order_id))
            bot.send_message(message.from_user.id, f'Для замовлення #{order_id} встановлено новий статус: {status}')
            cursor.execute("SELECT user_id FROM order_generated WHERE order_id = ?", (order_id,))
            result = cursor.fetchone()
            user_id = result[0]
            bot.send_message(user_id, f'В заказе #{order_id} обновлено статус: {status}')
            update_order_status = False
        elif action == 'true':
            bot.send_message(message.from_user.id, f'Введіть коментар до оновлення статусу для замовлення #{order_id}:')
        bot.delete_message(message.message.chat.id, message.message.message_id)
    except:
        MyLoger.error(f"Error update order status! message.from_user.id={message.from_user.id}")
        update_order_status = False
        bot.send_message(message.from_user.id, 'Відбулася помилка. Вас буде перенаправлено в Список Замовлень')
        bot.delete_message(message.message.chat.id, message.message.message_id)
        order_list_admin(message)


    conn.commit()
    cursor.close()
    conn.close()


@bot.message_handler(func=lambda message: update_order_status and message.from_user.id in admins_id, content_types=['text'])
def comment(message):
    MyLoger.debug(
        f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    admin_comment = message.text
    global update_order_status
    status, order_id = update_order_status
    update_order_status = False
    #
    cursor.execute("UPDATE order_generated SET status = ? WHERE order_id = ?", (status, order_id))
    bot.send_message(message.from_user.id, f'Для замовлення #{order_id} встановлено новий статус: {status}. Також добавлено коментар: {admin_comment}')
    cursor.execute("SELECT user_id FROM order_generated WHERE order_id = ?", (order_id,))
    result = cursor.fetchone()
    user_id = result[0]
    bot.send_message(user_id, f'В заказе #{order_id} обновлено статус: {status}.\nКомментарий администратора: {admin_comment}')
    conn.commit()
    cursor.close()
    conn.close()



@bot.callback_query_handler(func=lambda message: 'update_TTH#' in message.data and message.from_user.id in admins_id)
def update_tth(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    index_status = message.data.find("#")
    order_number = message.data[index_status + 1:]
    global new_TTH
    new_TTH = order_number
    try:
        bot.delete_message(message.message.chat.id, message.message.message_id)
    except:
        MyLoger.error(f"Error delete message! message.from_user.id={message.from_user.id}")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Скасувати оновлення ТТН')
    keyboard.add(button)
    bot.send_message(message.from_user.id, f'Введіть новий ТТН для замовлення #{order_number}', reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Скасувати оновлення ТТН' and message.from_user.id in admins_id)
def cancel_update_tth(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    global new_TTH
    new_TTH = False
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(admin_edit_catalog_button, admin_order_list_button, admin_distribution_button)
    bot.send_message(message.from_user.id, 'Оновлення поля ТТН скасовано.', reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.from_user.id in admins_id and new_TTH)
def set_new_tth(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    TTH = message.text
    global new_TTH
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("UPDATE order_generated SET TTH = ? WHERE order_id = ?", (TTH, new_TTH))
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(admin_edit_catalog_button, admin_order_list_button, admin_distribution_button)
    cursor.execute("UPDATE order_generated SET status = ? WHERE order_id = ?", ('В процесе доставки', new_TTH))
    cursor.execute("SELECT user_id FROM order_generated WHERE order_id = ?", (new_TTH,))
    user_id = cursor.fetchone()
    bot.send_message(user_id[0], f'В заказе #{new_TTH} обновлен статус: В процесе доставки')
    bot.send_message(message.from_user.id, f'Новий статус "В Процесе доставки" і  новий ТТН для замовлення #{new_TTH} успішно встановлено.', reply_markup=keyboard)
    cursor.execute("SELECT user_id FROM order_generated WHERE order_id = ?", (new_TTH,))
    result = cursor.fetchone()
    bot.send_message(result[0], f'В заказе #{new_TTH} обновлен ТТН: {TTH}')
    new_TTH = False
    conn.commit()
    cursor.close()
    conn.close()
