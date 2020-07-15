# -*- coding: utf-8 -*-
from config import *


@bot.message_handler(func=lambda message: message.text == '🤩Каталог🤩')
def catalog(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    keyboard = types.InlineKeyboardMarkup()
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM article WHERE availability NOT IN (0)")
    article = cursor.fetchall()
    for element in article:
        index1 = element[0].find('«')
        index2 = element[0].find('»')
        but = types.InlineKeyboardButton(text=element[0], callback_data=f'element{element[0][index1+1:index2]}')
        keyboard.add(but)
    # Тут має бути інлайн кнопка Головне меню
    keyboard.add(main_menu_inline_button)
    conn.commit()
    cursor.close()
    conn.close()
    bot.send_message(message.from_user.id, "Стикеры в наличии:", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == '🛒Корзина🛒')
def basket(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM basket WHERE user_id = ?", (message.from_user.id,))
    article = cursor.fetchall()
    string = 'Корзина:'
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    if article:
        for el in article:
            string += f'\nТовар {el[1]}\n Cет: {el[2]} стикеров\n Количество стикерпаков: {el[3]}'
        button_order = types.InlineKeyboardButton('💌Оформить💌', callback_data='Оформить')
        button_edit = types.InlineKeyboardButton('✏️Редактировать✏️', callback_data='Редактировать')
        button_clean = types.InlineKeyboardButton('🗑Очистить корзину🗑', callback_data='Очистить корзину')
        keyboard.add(button_order, button_edit, button_clean)
    else:
        string += '\nПустая'
        keyboard.add(catalog_inline_button)
    keyboard.add(main_menu_inline_button)
    bot.send_message(message.from_user.id, string, reply_markup=keyboard)
    cursor.execute("SELECT * FROM orders WHERE user_id = ?", (message.from_user.id,))
    result = cursor.fetchone()
    if not result:
        cursor.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (message.from_user.id, None, None, None, None, None, None, None))
    conn.commit()
    cursor.close()
    conn.close()


# InlineButton Стикерпак "На на на"
@bot.callback_query_handler(func=lambda message: 'element' in message.data)
def show_article(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    try:
        query = str('SELECT * FROM article WHERE name LIKE \'%' + message.data[7:] + '%\'')
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(query)
        article = cursor.fetchone()
        index1 = article[0].find('«')
        index2 = article[0].find('»')
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        article_price = article[4]
        while article_price.find('грн') != -1:
            index = article_price.find('грн')
            price = article_price[:index + 3]
            price = price.replace('\n', '')
            article_price = article_price[index + 3:]
            button = types.InlineKeyboardButton(text=f'🎁Добавить в корзину {price}',
                                                callback_data=f'basket_{price}_{article[0][index1 + 1:index2]}')
            keyboard.add(button)
        back = types.InlineKeyboardButton(text='👈Назад👈', callback_data='Назад')
        sum = 0
        cursor.execute("SELECT price FROM basket WHERE user_id = ?", (message.from_user.id,))
        result = cursor.fetchall()
        for el in result:
            sum += int(el[0])
        order = types.InlineKeyboardButton(text=f'🛒В Корзину. Заказ на {sum} грн', callback_data='OpenBasket')
        keyboard.add(order, back)
        try:
            bot.delete_message(message.message.chat.id, message.message.message_id)
        except:
            MyLoger.error(f"Error delete message! message.from_user.id={message.from_user.id}")
        bot.send_photo(message.message.chat.id, photo=article[2], caption=f'{article[0]}\n{article[1]}',
                       reply_markup=keyboard)
        conn.commit()
        cursor.close()
        conn.close()
    except:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(catalog_inline_button)
        bot.delete_message(message.message.chat.id, message.message.message_id)
        bot.send_message(message.from_user.id, 'Упс. Произошла ошибка. Похоже вы пытались открыть стикерпак которого уже нет в наличии🤪', reply_markup=keyboard)


# - InlineButton 'Назад' в Каталог + InlineButton Каталог
@bot.callback_query_handler(func=lambda message: message.data == 'Назад' or message.data == 'Каталог')
def catalog_back(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    try:
        bot.delete_message(message.message.chat.id, message.message.message_id)
    except:
        MyLoger.error(f"Error delete message! message.from_user.id={message.from_user.id}")
    catalog(message)


# InlineButton add new item in basket (Добавить в корзину N шт - M грн)
@bot.callback_query_handler(func=lambda message: 'basket' in message.data)
def add_new_item_basket(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    index = message.data.rfind('_')
    article_name = message.data[index + 1:]
    index = message.data.find('_')
    index2 = message.data.rfind('_')
    price = message.data[index + 1:index2]
    index = price.find('шт')
    pack_size = price[:index - 1]
    index = price.find('-')
    index2 = price.find('грн')
    price = price[index + 2:index2 - 1]
    amount = 1
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    query = str('SELECT name FROM article WHERE name LIKE \'%' + article_name + '%\'')
    cursor.execute(query)
    full_article_name = cursor.fetchone()
    cursor.execute("SELECT amount FROM basket WHERE user_id=? and article_name=? and pack_size=?",
                   (message.from_user.id, article_name, pack_size))
    result = cursor.fetchone()
    if result:
        cursor.execute("UPDATE basket SET amount=? WHERE user_id=? and article_name=? and pack_size=?",
                       (int(result[0]) + 1, message.from_user.id, article_name, pack_size))
    else:
        cursor.execute("INSERT INTO basket VALUES (?, ?, ?, ?, ?)",
                       (message.from_user.id, article_name, pack_size, amount, price))
    try:
        bot.delete_message(message.message.chat.id, message.message.message_id)
    except:
        MyLoger.error(f"Error delete message! message.from_user.id={message.from_user.id}")
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    button1 = telebot.types.InlineKeyboardButton('✅Оформить заказ✅', callback_data='OpenBasket')
    button2 = telebot.types.InlineKeyboardButton('👈Вернутся в Каталог👈', callback_data='Назад')
    markup.add(button1, button2)
    bot.send_message(message.from_user.id,
                     f"Товар {full_article_name[0]} (сет из {pack_size} стикеров) добавлен в корзину!",
                     reply_markup=markup)
    conn.commit()
    cursor.close()
    conn.close()


# InlineButton В корзину. заказ на Х грн + InlineButton Оформить заказ
@bot.callback_query_handler(func=lambda message: message.data == 'OpenBasket')
def open_basket(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    try:
        bot.delete_message(message.message.chat.id, message.message.message_id)
    except:
        MyLoger.error(f"Error delete message! message.from_user.id={message.from_user.id}")
    basket(message)

