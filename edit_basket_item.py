# -*- coding: utf-8 -*-
from config import *
from catalog_logic import basket
import myUUID


# InlineButton Оформить в Корзине
@bot.callback_query_handler(func=lambda message: message.data == 'Оформить')
def make_out(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🚚Новая Почта🚚')
    button2 = types.KeyboardButton('🚚Укр Почта🚚')
    button3 = types.KeyboardButton('❌Отменить заказ❌')
    keyboard.row(button1, button2)
    keyboard.row(button3)
    try:
        bot.delete_message(message.message.chat.id, message.message.message_id)
    except:
        MyLoger.error(f"Error delete message! message.from_user.id={message.from_user.id}")
    bot.send_message(message.from_user.id, 'Выберите тип доставки:', reply_markup=keyboard)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET order_in_process = ? WHERE user_id = ?", ('True', message.from_user.id,))
    while True:
        order_id = myUUID.get_id()
        cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
        result = cursor.fetchall()
        if not result:
            cursor.execute("UPDATE orders SET order_id = ? WHERE user_id = ?", (order_id, message.from_user.id))
            break
    conn.commit()
    cursor.close()
    conn.close()


@bot.callback_query_handler(func=lambda message: message.data == 'Редактировать')
def edit_basket(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM basket WHERE user_id= ?", (message.from_user.id,))
    result = cursor.fetchall()

    keyboard = types.InlineKeyboardMarkup()
    for el in result:
        button = types.InlineKeyboardButton(f'Стикерпак {el[1]} сет {el[2]} количество {el[3]}',
                                            callback_data=f'edit_{el[1]}_{el[2]}')
        keyboard.add(button)
    button = types.InlineKeyboardButton('✅Готово✅', callback_data='Готово')
    keyboard.add(button)
    try:
        bot.delete_message(message.message.chat.id, message.message.message_id)
    except:
        MyLoger.error(f"Error delete message! message.from_user.id={message.from_user.id}")
    bot.send_message(message.from_user.id, 'Выберите товар для редактирования:\n', reply_markup=keyboard)
    conn.commit()
    cursor.close()
    conn.close()


# InlineButton Коли натиснув на Редактировать і обрав стікерпак для редактування?
@bot.callback_query_handler(func=lambda message: 'edit_' in message.data or 'plus' in message.data or 'minus' in message.data)
def edit_article(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    index1 = message.data.find('_')
    index2 = message.data.rfind('_')
    article_name = message.data[index1 + 1:index2]
    pack_size = message.data[index2 + 1:]
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT amount FROM basket WHERE user_id= ? AND article_name = ? AND pack_size = ?",
                   (message.from_user.id, article_name, pack_size))
    result = cursor.fetchone()
    amount = int(result[0])
    if 'plus' in message.data:
        amount += 1
        cursor.execute("UPDATE basket SET amount = ?  WHERE user_id = ? AND article_name = ? AND pack_size = ?",
                       (amount, message.from_user.id, article_name, pack_size))
    elif 'minus' in message.data:
        if amount > 1:
            amount -= 1
            cursor.execute("UPDATE basket SET amount = ?  WHERE user_id = ? AND article_name = ? AND pack_size = ?",
                           (amount, message.from_user.id, article_name, pack_size))
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    button1 = types.InlineKeyboardButton('➕', callback_data=f'plus{message.data[4:]}')
    button2 = types.InlineKeyboardButton('➖', callback_data=f'minus{message.data[4:]}')
    button3 = types.InlineKeyboardButton('❌', callback_data=f'delete{message.data[4:]}')
    button4 = types.InlineKeyboardButton('✅Готово✅', callback_data='Відредаговано')
    keyboard.row(button1, button2, button3)
    keyboard.row(button4)
    try:
        bot.delete_message(message.message.chat.id, message.message.message_id)
    except:
        MyLoger.error(f"Error delete message! message.from_user.id={message.from_user.id}")
    bot.send_message(message.from_user.id, f'Стикерпак {article_name}\nРазмер пака {pack_size}\nКоличество {amount}',
                     reply_markup=keyboard)
    conn.commit()
    cursor.close()
    conn.close()


# InlineButton X - видалення стікерпаку з корзини
@bot.callback_query_handler(func=lambda message: 'delete' in message.data)
def delete_article(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    index1 = message.data.find('_')
    index2 = message.data.rfind('_')
    article_name = message.data[index1 + 1:index2]
    pack_size = message.data[index2 + 1:]
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM basket WHERE user_id = ? AND article_name = ? AND pack_size = ?",
                   (message.from_user.id, article_name, pack_size))
    bot.send_message(message.from_user.id,
                     f'Стикерпак {article_name} (сет {pack_size}) удален из корзины.')
    conn.commit()
    cursor.close()
    conn.close()
    edit_basket(message)


# InlineButton Очистить корзину
@bot.callback_query_handler(func=lambda message: message.data == 'Очистить корзину')
def clean_basket(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM basket WHERE user_id = ?", (message.from_user.id,))
    conn.commit()
    cursor.close()
    conn.close()
    try:
        bot.delete_message(message.message.chat.id, message.message.message_id)
    except:
        MyLoger.error(f"Error delete message! message.from_user.id={message.from_user.id}")
    basket(message)


# InlineButton Готово(коли закінчуєш редагування всередині стікерпака) з callback_data = 'Відредаговано'
@bot.callback_query_handler(func=lambda message: message.data == 'Відредаговано')
def complete(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    try:
        bot.delete_message(message.message.chat.id, message.message.message_id)
    except:
        MyLoger.error(f"Error delete message! message.from_user.id={message.from_user.id}")
    basket(message)


# InlineButton Готово(коли закінчуєш редагування корзини) з callback_data = 'Готово'
@bot.callback_query_handler(func=lambda message: message.data == 'Готово')
def complete2(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    try:
        bot.delete_message(message.message.chat.id, message.message.message_id)
    except:
        MyLoger.error(f"Error delete message! message.from_user.id={message.from_user.id}")
    basket(message)
