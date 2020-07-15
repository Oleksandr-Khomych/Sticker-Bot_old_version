# -*- coding: utf-8 -*-
from config import *


@bot.message_handler(func=lambda message: message.text == '❓Как это работает❓')
def howitworks(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item_buy = telebot.types.KeyboardButton('📌Как купить?')
    item_delivery = telebot.types.KeyboardButton('📌Все о доставке')
    item_security = telebot.types.KeyboardButton('📌Безопасно ли здесь оплачивать?')
    item_botinfo = telebot.types.KeyboardButton('📌Для чего этот бот?')
    item_tracking = telebot.types.KeyboardButton('📌Как узнать отправлен ли товар?')
    item_stikerinfo = telebot.types.KeyboardButton('📌Информация о стикерах')
    item_main = telebot.types.KeyboardButton('👣Главное меню👣')
    markup.row(item_buy, item_delivery)
    markup.row(item_security, item_botinfo)
    markup.row(item_tracking, item_stikerinfo)
    markup.row(item_main)
    bot.send_message(message.chat.id, "Что вас интересует?", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '📝О нас📝')
def info(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('👣Главное меню👣'))
    bot.send_message(message.chat.id, '''🚚Работаем по Украине.
✉️Связаться с нами:
📩Email: stickerspackua@gmail.com
📸Instagram: @stickers_pack_ua
📲Телефон: 
+38 0 (63) 278 80 19
+38 0 (99) 019 45 13''', reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == '📌Как купить?')
def buy(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    bot.send_message(message.chat.id, "✅Чтобы заказать стикеры, зайдите в главное меню и нажмите кнопку «Купить»➡️после чего выберите понравившийся стикер пак➡️Выберите удобный вам способ оплаты➡️запомните форму для оформления заказа.✅", reply_markup=False)


@bot.message_handler(func=lambda message: message.text == '📌Все о доставке')
def delivery(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    bot.send_message(message.chat.id, '''✅Доставка осуществляется Новой Почтой по всей Украине.🚚
✅Срок доставки от 1 до 3 дней. 🚚
✅После того как вы сделали заказ мы в тот же день обработаем и отправим эго вам. 🚚
✅Отправляем стикеры  в любой день недели за исключением воскресенья.🚚
✅Стоимость доставки Новой Почтой - 40 грн. 🚚
✅При заказе наложенным платежом почта снимает дополнительную плату за перевод средств в размере 20 грн 🚚''',
                     reply_markup=False)


@bot.message_handler(func=lambda message: message.text == '📌Безопасно ли здесь оплачивать?')
def security(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    bot.send_message(message.chat.id, '''Да, все ваши данные защищены. 🔒
Оплата осуществляется через Р24. 🔒
За перевод средств отвечает Приват Банк.🔒
Данные которые вы вводите при заказе, обрабатывает только администратор. 📝🔒''', reply_markup=False)


@bot.message_handler(func=lambda message: message.text == '📌Для чего этот бот?')
def botinfo(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    bot.send_message(message.chat.id, '''✅Этот бот создан для оптимизации процесса заказа. 🧠
✅Бот поможет вам купить стикеры не общаясь при этом с продавцом. 🧠
✅После совершения сделки бот отправит ваши данные  нам и мы их обработаем.🧠
✅Бот ответит на часто задаваемые вопросы простым и понятным языком.🧠
✅Бот сэкономит ваше время.🧠''', reply_markup=False)


@bot.message_handler(func=lambda message: message.text == '📌Как узнать отправлен ли товар?')
def tracking(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    bot.send_message(message.chat.id, '''✅Отслеживать свои посылки можно в приложении Новой Почты на телефоне или ПК. 📮
✅После того как мы отправим вам стикеры, у вас в личном кабинете на сайте Новой Почты появится ваша посылка, которой вы сможете управлять. 📮
✅Если в течении 2-х дней мы не отправили вам стикеры, свяжитесь с нами.📩''', reply_markup=False)


@bot.message_handler(func=lambda message: message.text == '📌Информация о стикерах')
def stikerinfo(message):
    MyLoger.debug(f'message.from_user.id={message.from_user.id}|message.from_user.first_name={message.from_user.first_name}|message.from_user.username={message.from_user.username}')
    bot.send_message(message.chat.id, '''✅Средний размер всех стикеров 5х5 см.
✅Покрытие матовое или глянцевое (зависит от стикер пака)
✅Стикеры защищены от влаги,пыли и грязи.
✅Хорошо клеятся, после того как вы решите их отклеить следов НЕ останется. ''', reply_markup=False)