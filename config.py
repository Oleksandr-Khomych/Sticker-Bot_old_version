# -*- coding: utf-8 -*-
import telebot
from telebot import types
import sqlite3
import logging


# - рівень логів
logging.getLogger('urllib3').setLevel('WARNING')
MyLoger = logging.getLogger('MyLoger')
MyLoger.setLevel('DEBUG')
logging.basicConfig(format='%(asctime)s %(funcName)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', filename='test.log', level=logging.DEBUG)
FORMATTER = logging.Formatter("%(time)s — %(name)s — %(level)s — %(message)s")
admins_id = [488339545, 613719744]
order_in_process_user_id = []
db_name = 'article.db'
name = ''
description = ''
file_id = ''
availability = ''
price = ''
new_item = False
new_TTH = False
edit_field = False
update_order_status = False
new_distribution = False
token = '1014150298:AAGZg9ana2UWzAu-P1YXGNFYquEATtHgjqQ' #- Stiker_Bot token
bot = telebot.TeleBot(token)


#token = '1057572412:AAGLPY2ZViqNoyO3KMbarL4QVEDIku8u3NU' # DickerBot token
#logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', filename='test.log', level=logging.DEBUG)

# - кнопки будуть тимчасово тут
main_menu_button = telebot.types.KeyboardButton('👣Главное меню👣')
main_menu_inline_button = types.InlineKeyboardButton('👣Главное меню👣', callback_data='Главное Меню')
catalog_inline_button = types.InlineKeyboardButton('🤩Каталог🤩', callback_data='Каталог')
cancel_add_new_article_inline_button = types.InlineKeyboardButton('Скасувати додавання нового товару')
admin_main_inline_button = types.InlineKeyboardButton('Адмін Меню', callback_data='Адмін Меню')
admin_edit_catalog_button = types.KeyboardButton('Редактировать каталог товаров')
admin_order_list_button = types.KeyboardButton('Список Замовлень')
admin_distribution_button = types.KeyboardButton('Розсилка')
delivery_type_edit = {'Новая Почта': 'Введите номер и/или адрес отделения Новой Почты: ',
                      'Укр Почта': 'Введите почтовый индекс: '}
delivery_type_show = {'Новая Почта': 'Отделение Новой почты: ',
                      'Укр Почта': 'Почтовый индекс: '}
