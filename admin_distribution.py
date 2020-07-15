# -*- coding: utf-8 -*-
from config import *


@bot.message_handler(func=lambda message: message.text == 'Розсилка' and message.from_user.id in admins_id)
def distribution(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    global new_distribution
    new_distribution = True
    keyboard = types.InlineKeyboardMarkup()
    button_cancel = types.InlineKeyboardButton('Відмінити', callback_data='cancel')
    keyboard.add(button_cancel)
    bot.send_message(message.from_user.id,
                     'Чудово, надішліть повідомлення, яке потрібно розіслати.\nФормат повідомлення: фото з коментарем/текст', reply_markup=keyboard)


@bot.message_handler(func=lambda message: new_distribution and message.from_user.id in admins_id, content_types=['text', 'photo'])
def distribution_message(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    global new_distribution
    new_distribution = False
    keyboard = types.InlineKeyboardMarkup()
    button_send = types.InlineKeyboardButton('Зробити розсилку', callback_data='send')
    button_cancel = types.InlineKeyboardButton('Відмінити', callback_data='cancel')
    keyboard.add(button_send, button_cancel)
    if message.content_type == 'text':
        bot.send_message(message.from_user.id, message.text, reply_markup=keyboard)
    elif message.content_type == 'photo':
        photo_id = message.json['photo'][0]['file_id']
        caption = message.caption
        bot.send_photo(message.from_user.id, photo=photo_id, caption=caption, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda message: message.data in 'sendcancel' and message.from_user.id in admins_id)
def distribution_send(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(admin_main_inline_button)
    bot.delete_message(message.message.chat.id, message.message.message_id)
    count_user = 0
    count_block_user = 0
    if message.data == 'send':
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM orders")
        result = cursor.fetchall()
        if message.message.content_type == 'text':
            for user_id in result:
                try:
                    bot.send_message(user_id[0], message.message.text, reply_markup=False)
                    count_user += 1
                except:
                    count_block_user += 1
        elif message.message.content_type == 'photo':
            for user_id in result:
                try:
                    bot.send_photo(user_id[0], photo=message.message.json['photo'][0]['file_id'],
                                   caption=message.message.caption, reply_markup=False)
                    count_user += 1
                except:
                    count_block_user += 1
        conn.commit()
        cursor.close()
        conn.close()
        bot.send_message(message.from_user.id, f'Розсилка успішно завершена!\nКількість користувачів які отримали повідомлення:{count_user}\nКількість користувачів які заблокували бота:{count_block_user}', reply_markup=keyboard)
    elif message.data == 'cancel':
        global new_distribution
        new_distribution = False
        bot.send_message(message.from_user.id, 'Гаразд, обійдемось без розсилки цього разу😉', reply_markup=keyboard)

