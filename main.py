# -*- coding: utf-8 -*-
from config import *
import create_db
import howitworks
import edit_user_info
import edit_basket_item
import catalog_logic
import orders_menu_logic
import admin_panel_edit_catalog
import admin_panel_order_list
import admin_distribution
import ordering_process

# Головне меню ---------------------------


@bot.message_handler(commands=['start'])
def start_message(message):
    MyLoger.debug(f'''message.from_user.id={message.from_user.id}
    |message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}''')
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
    item_catalog = telebot.types.KeyboardButton('🤩Каталог🤩')
    item_buy = telebot.types.KeyboardButton('🛒Корзина🛒')
    item_order = telebot.types.KeyboardButton('🛍Заказы🛍')
    item_language = telebot.types.KeyboardButton('🌐Выбрать язык🌐')
    item_howitworks = telebot.types.KeyboardButton('❓Как это работает❓')
    item_aboutus = telebot.types.KeyboardButton('📝О нас📝')
    markup.row(item_catalog, item_buy)
    markup.row(item_order, item_language)
    markup.row(item_howitworks, item_aboutus)
    bot.send_message(message.chat.id, 'Привет! Я Стикербот!', reply_markup=markup)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE user_id = ?", (message.from_user.id,))
    result = cursor.fetchone()
    if not result:
        cursor.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (message.from_user.id, None, None, None, None, None, None, None))
    conn.commit()
    cursor.close()
    conn.close()


@bot.message_handler(func=lambda message: message.text == '/main' or message.text == '👣Главное меню👣')
def main_message(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
    item_catalog = telebot.types.KeyboardButton('🤩Каталог🤩')
    item_buy = telebot.types.KeyboardButton('🛒Корзина🛒')
    item_order = telebot.types.KeyboardButton('🛍Заказы🛍')
    item_language = telebot.types.KeyboardButton('🌐Выбрать язык🌐')
    item_howitworks = telebot.types.KeyboardButton('❓Как это работает❓')
    item_aboutus = telebot.types.KeyboardButton('📝О нас📝')
    markup.row(item_catalog, item_buy)
    markup.row(item_order, item_language)
    markup.row(item_howitworks, item_aboutus)
    bot.send_message(message.from_user.id, "Чем могу помочь?", reply_markup=markup)


@bot.callback_query_handler(func=lambda message: message.data == 'Главное Меню')
def main_message_callback(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    try:
        bot.delete_message(message.message.chat.id, message.message.message_id)
    except:
        MyLoger.error(f"Error delete message! message.from_user.id={message.from_user.id}")
    main_message(message)


# Хендлер для кнопки в головному меню (неактивни функціонал)
@bot.message_handler(func=lambda message: message.text == '🌐Выбрать язык🌐' or message.text == 'Вибрати мову')
def chose_language(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    bot.send_message(message.chat.id, "Неактивний функціонал...", reply_markup=False)


if __name__ == '__main__':
    create_db.create_db(db_name)
    MyLoger.debug('Bot start working...')
    bot.infinity_polling(none_stop=True)
