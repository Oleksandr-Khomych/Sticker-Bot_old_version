# -*- coding: utf-8 -*-
from config import *

# Адмін менюха ----------


@bot.message_handler(func=lambda message: message.from_user.id in admins_id, commands=['admin'])
def admin_main(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(admin_edit_catalog_button, admin_order_list_button, admin_distribution_button)
    bot.send_message(message.from_user.id, "Що вас цікавить?", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda message: message.data == 'Адмін Меню' and message.from_user.id in admins_id)
def admin_main_callback(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    try:
        bot.delete_message(message.message.chat.id, message.message.message_id)
    except:
        MyLoger.error(f"Error delete message! message.from_user.id={message.from_user.id}")
    admin_main(message)


@bot.message_handler(
    func=lambda message: message.text == 'Редактировать каталог товаров' and message.from_user.id in admins_id)
def chose_type_edit_catalog(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Добавить товар', callback_data='Добавить товар')
    button2 = types.InlineKeyboardButton('Редактировать товар', callback_data='Редактировать товар')
    button3 = types.InlineKeyboardButton('Удалить товар', callback_data='Удалить товар')
    button4 = types.InlineKeyboardButton('Адмін Меню', callback_data='Адмін Меню')
    keyboard.add(button1, button2, button3, button4)
    bot.send_message(message.from_user.id, "Виберіть тип змін:", reply_markup=keyboard)


# Добавить товар ----------------------------------------------------


@bot.callback_query_handler(func=lambda message: message.data == 'Добавить товар' and message.from_user.id in admins_id)
def add_new_item_callback(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    global new_item
    new_item = True
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(cancel_add_new_article_inline_button)
    try:
        bot.delete_message(message.message.chat.id, message.message.message_id)
    except:
        MyLoger.error(f"Error delete message! message.from_user.id={message.from_user.id}")
    bot.send_message(message.from_user.id, 'Введіть назву товару:', reply_markup=keyboard)


@bot.message_handler(
    func=lambda message: message.text == 'Скасувати додавання нового товару' and message.from_user.id in admins_id)
def cancel_adding_new_product(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    global name, description, file_id, availability, price, new_item
    name = ''
    description = ''
    file_id = ''
    availability = ''
    price = ''
    new_item = False
    bot.send_message(message.from_user.id,
                     'Додавання нового товару скасоване. Всі поля очищено. Вас поверне в головне меню',
                     reply_markup=False)
    admin_main(message)


@bot.message_handler(
    func=lambda message: message.text == 'Підтвердити додавання нового товару' and message.from_user.id in admins_id and new_item)
def complete_add_new_item(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    global name, description, file_id, availability, price, new_item
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO article VALUES (?, ?, ?, ?, ?)", (name, description, file_id, availability, price))
    new_item = False
    bot.send_message(message.from_user.id, 'Новий товар додано у каталог', reply_markup=False)
    admin_main(message)
    conn.commit()
    cursor.close()
    conn.close()


@bot.message_handler(func=lambda message: message.from_user.id in admins_id and new_item,
                     content_types=['text', 'photo'])
def add_new_item(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    global name, description, file_id, availability, price, new_item
    try:
        if not name:
            name = message.text
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            keyboard.add(cancel_add_new_article_inline_button)
            bot.send_message(message.from_user.id, 'Введіть опис товару:', reply_markup=keyboard)
        elif not description:
            description = message.text
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            keyboard.add(cancel_add_new_article_inline_button)
            bot.send_message(message.from_user.id, 'Надішліть фотографію товару:', reply_markup=keyboard)
        elif not file_id:
            file_id = message.json['photo'][0]['file_id']
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            keyboard.add(cancel_add_new_article_inline_button)
            bot.send_message(message.from_user.id, 'Введіть наявність товару:', reply_markup=keyboard)
        elif not availability:
            availability = message.text
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            keyboard.add(cancel_add_new_article_inline_button)
            bot.send_message(message.from_user.id, 'Введіть ціну товару:', reply_markup=keyboard)
        elif not price:
            price = message.text
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            button1 = types.InlineKeyboardButton('Підтвердити додавання нового товару')
            keyboard.add(button1, cancel_add_new_article_inline_button)
            bot.send_photo(message.from_user.id, photo=file_id,
                           caption=f'{name}\n{description}\n{price}\navailability(приховане поле) = {availability}',
                           reply_markup=keyboard)
    except:
        bot.send_message(message.from_user.id, 'Під час додавання нового товару відбулась помилка...')
        cancel_adding_new_product(message)




# Редактування полів товару:-----------------------------------


@bot.callback_query_handler(
    func=lambda message: message.data == 'Редактировать товар' and message.from_user.id in admins_id)
def edit_article(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    keyboard = types.InlineKeyboardMarkup()
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM article")
    article = cursor.fetchall()
    for element in article:
        index1 = element[0].find('«')
        index2 = element[0].find('»')
        but = types.InlineKeyboardButton(text=element[0],
                                         callback_data=f'admin_edit{element[0][index1 + 1:index2]}')
        keyboard.add(but)
    conn.commit()
    cursor.close()
    conn.close()
    keyboard.add(admin_main_inline_button)
    try:
        bot.delete_message(message.message.chat.id, message.message.message_id)
    except:
        MyLoger.error(f"Error delete message! message.from_user.id={message.from_user.id}")
    bot.send_message(message.from_user.id, "Каталог стікерів:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda message: 'admin_edit' in message.data and message.from_user.id in admins_id)
def choose_field_to_edit(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    query = str('SELECT * FROM article WHERE name LIKE \'%' + message.data[10:] + '%\'')
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(query)
    article = cursor.fetchone()
    index1 = article[0].find('«')
    index2 = article[0].find('»')
    stiker_name = article[0][index1+1:index2]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button_name = types.InlineKeyboardButton(text='Редагувати назву', callback_data=f'set_name_{stiker_name}')
    button_description = types.InlineKeyboardButton(text='Редагувати опис', callback_data=f'set_description_{stiker_name}')
    button_file_id = types.InlineKeyboardButton(text='Надіслати нову фотографію', callback_data=f'set_file_id_{stiker_name}')
    button_avaliable = types.InlineKeyboardButton(text='Редагувати доступність', callback_data=f'set_availability_{stiker_name}')
    button_price = types.InlineKeyboardButton(text='Редактувати ціну', callback_data=f'set_price_{stiker_name}')
    back = types.InlineKeyboardButton(text='Назад', callback_data='Редактировать товар')
    keyboard.add(button_name, button_description, button_file_id, button_avaliable, button_price, back)
    try:
        bot.delete_message(message.message.chat.id, message.message.message_id)
    except:
        MyLoger.error(f"Error delete message! message.from_user.id={message.from_user.id}")
    bot.send_photo(message.message.chat.id, photo=article[2],
                   caption=f'{article[0]}\n{article[1]}\navaliable(not show)={article[3]}\nprice(not show):\n{article[4]}',
                   reply_markup=keyboard)
    conn.commit()
    cursor.close()
    conn.close()


@bot.callback_query_handler(func=lambda message: 'set_' in message.data and message.from_user.id in admins_id)
def choise_field(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    index1 = message.data.find('_')
    index2 = message.data.rfind('_')
    field = message.data[index1+1:index2]
    index3 = message.data.rfind('_')
    stiker_name = message.data[index3+1:]
    global edit_field
    edit_field = [stiker_name, field]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Скасувати редагування товару')
    keyboard.add(button)
    try:
        bot.delete_message(message.message.chat.id, message.message.message_id)
    except:
        MyLoger.error(f"Error delete message! message.from_user.id={message.from_user.id}")
    bot.send_message(message.from_user.id, f'Введіть нові данні для поля {field}', reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Скасувати редагування товару' and message.from_user.id in admins_id and admins_id)
def update_art_cancel(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    global edit_field
    edit_field = False
    bot.send_message(message.from_user.id, 'Редагування товару скасовано')
    admin_main(message)


@bot.message_handler(func=lambda message: message.from_user.id in admins_id and edit_field, content_types=['text', 'photo'])
def set_field(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    global edit_field
    stiker_name = edit_field[0]
    field = edit_field[1]
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        if field == 'file_id':
            photo_id = message.json['photo'][0]['file_id']
            query = f'UPDATE article SET {field} = "{photo_id}" WHERE name LIKE \'%{stiker_name}%\''
        else:
            text = message.text
            query = f'UPDATE article SET {field} = "{text}" WHERE name LIKE \'%{stiker_name}%\''
        cursor.execute(query)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button1 = types.KeyboardButton('Редактировать каталог товаров')
        button2 = types.KeyboardButton('Список Замовлень')
        keyboard.add(button1, button2)
        bot.send_message(message.from_user.id, f'Поле {field} товару {stiker_name} успішно оновлено',
                         reply_markup=keyboard)
        edit_field = False
        conn.commit()
        cursor.close()
        conn.close()
    except:
        bot.send_message(message.from_user.id, 'Під час редагування поля товару виникла помилка...Ви будете перенаправлені в Адмін Меню')
        admin_main(message)


# Видалення товару: ++++++++++++++++++++++++++++++++++++++++++


@bot.callback_query_handler(func=lambda message: message.data == 'Удалить товар' and message.from_user.id in admins_id)
def delete_article(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    keyboard = types.InlineKeyboardMarkup()
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM article")
    article = cursor.fetchall()
    for element in article:
        index1 = element[0].find('«')
        index2 = element[0].find('»')
        but = types.InlineKeyboardButton(text=element[0],
                                         callback_data=f'admin_del_{element[0][index1 + 1:index2]}')
        keyboard.add(but)
    conn.commit()
    cursor.close()
    conn.close()
    keyboard.add(admin_main_inline_button)
    try:
        bot.delete_message(message.message.chat.id, message.message.message_id)
    except:
        MyLoger.error(f"Error delete message! message.from_user.id={message.from_user.id}")
    bot.send_message(message.from_user.id, "Каталог стікерів:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda message: 'admin_del_' in message.data and message.from_user.id in admins_id)
def choose_delete_article(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    query = str('SELECT * FROM article WHERE name LIKE \'%' + message.data[10:] + '%\'')
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(query)
    article = cursor.fetchone()
    index1 = article[0].find('«')
    index2 = article[0].find('»')
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    article_price = article[4]
    button = types.InlineKeyboardButton(text=f'Видалити товар {price}',
                                        callback_data=f'del_article_{article[0][index1 + 1:index2]}')
    back = types.InlineKeyboardButton(text='Назад', callback_data='Удалить товар')
    keyboard.add(button, back)
    try:
        bot.delete_message(message.message.chat.id, message.message.message_id)
    except:
        MyLoger.error(f"Error delete message! message.from_user.id={message.from_user.id}")
    bot.send_photo(message.message.chat.id, photo=article[2], caption=f'{article[0]}\n{article[1]}',
                   reply_markup=keyboard)
    conn.commit()
    cursor.close()
    conn.close()


@bot.callback_query_handler(func=lambda message: 'del_article_' in message.data and message.from_user.id in admins_id)
def delete_complete(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    query = str('DELETE FROM article WHERE name LIKE \'%' + message.data[12:] + '%\'')
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(query)
    try:
        bot.delete_message(message.message.chat.id, message.message.message_id)
    except:
        MyLoger.error(f"Error delete message! message.from_user.id={message.from_user.id}")
    bot.send_message(message.from_user.id, f'Товар "{message.data[12:]}" успішно видалений з корзини.')
    admin_main(message)
    conn.commit()
    cursor.close()
    conn.close()


@bot.message_handler(commands=['user_id'])
def get_user_id(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    bot.send_message(message.chat.id, message.from_user.id)
