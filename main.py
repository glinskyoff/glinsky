import math, telebot, requests, time, random, wikipedia, qrcode
import os
import logging
import psycopg2
from time import sleep
from telebot import types
from bs4 import BeautifulSoup
from config import *
from flask import Flask, request

bot = telebot.TeleBot(BOT_TOKEN)
server = Flask(__name__)
logger = telebot.logger
logger.setLevel(logging.DEBUG)

db = psycopg2.connect(DB_URI, sslmode="require")
cursor = db.cursor()

url = "https://mainfin.ru/currency/omsk"
request_get = requests.get(url)
soup = BeautifulSoup(request_get.text, "html.parser")
price_usd = soup.find("span", id="buy_usd").text
price_euro = soup.find("span", id="buy_eur").text

@bot.message_handler(commands=["start"])
def start(message):
    id = message.from_user.id
    username = message.from_user.username
    name = message.from_user.first_name
    cursor.execute(f"SELECT id FROM users WHERE id = {id}")
    result_id = cursor.fetchone()

    if not result_id:
        cursor.execute("INSERT INTO users(id, username, name, games, score) VALUES (%s, %s, %s, %s, %s)", (id, username, name, 0, 0))
        cursor.execute("INSERT INTO date (id, games, score, games_darts, score_darts, games_number, score_number, games_kosti, score_kosti, games_bowling, score_bowling, games_football, score_football, games_basket, score_basket, games_moneta, score_moneta) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        db.commit()

    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton("🧾 Таблица лидеров")
    item2 = types.KeyboardButton("💎 Функции")
    item3 = types.KeyboardButton("🛠 Прочее")
    markup.row(item1)
    markup.row(item2)
    markup.row(item3)
    bot.send_message(message.from_user.id, "Привет " + message.from_user.first_name + " 👋" +", чем я могу тебе помочь?", reply_markup = markup)
   
@bot.message_handler(commands = ["help"])
def help(message):
	bot.send_message(message.from_user.id, "Напиши /start")

@bot.message_handler(content_types = ["text"])
def bot_message(message):
    if message.chat.type == "private":
        
        # ПРОЧЕЕ
        if message.text == "🛠 Прочее":
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
            item1 = types.KeyboardButton("📄 Информация")
            item2 = types.KeyboardButton("📝 Предложения и улучшения")
            item3 = types.KeyboardButton("📍 Вернуться в Главное меню")
            markup.row(item1)
            markup.row(item2)
            markup.row(item3)
            bot.send_message(message.from_user.id, "🚩 Выберите действие", reply_markup = markup)

		# ПРЕДЛОЖЕНИЯ И УЛУЧШЕНИЯ
        elif message.text == "📝 Предложения и улучшения":
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
            item1 = types.KeyboardButton("Да ✅")
            item2 = types.KeyboardButton("Нет ⛔")
            markup.row(item1)
            markup.row(item2)
            bot.send_message(message.from_user.id, "Желаете оставить предложение по улучшению?", reply_markup = markup)

        elif message.text == "Да ✅":
            bot.send_message(message.chat.id, "Напишите ваши улучшения в чат! ⤵️")
            bot.register_next_step_handler(message, up_bot)

        elif message.text == "Нет ⛔":
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
            item1 = types.KeyboardButton("📄 Информация")
            item2 = types.KeyboardButton("📝 Предложения и улучшения")
            item3 = types.KeyboardButton("📍 Вернуться в Главное меню")
            markup.row(item1)
            markup.row(item2)
            markup.row(item3)
            bot.send_message(message.from_user.id, "🚩 Выберите действие", reply_markup = markup)

		# ИНФОРМАЦИЯ

        elif message.text == "📄 Информация":
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton("🆔 Узнать ID")
            item2 = types.KeyboardButton("📑 Информация о боте")
            item3 = types.KeyboardButton("🔙 Вернуться в Прочее")
            markup.row(item1)
            markup.row(item2)
            markup.row(item3)
            bot.send_message(message.from_user.id, "🚩 Выберите действие", reply_markup = markup)

        elif message.text == "📑 Информация о боте":
            bot.send_message(message.from_user.id, "Данный бот создан для удобства и практики) 🙂.\nПо всем вопросам - @glinskyoffical")

        elif message.text == "🔙 Вернуться в Информация":
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton("🆔 Узнать ID")
            item2 = types.KeyboardButton("📑 Информация о боте")
            item3 = types.KeyboardButton("🔙 Вернуться в Прочее")
            markup.row(item1)
            markup.row(item2)
            markup.row(item3)
            bot.send_message(message.from_user.id, "🚩 Выберите действие", reply_markup = markup)

        elif message.text == "🔙 Вернуться в Прочее":
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
            item1 = types.KeyboardButton("📄 Информация")
            item2 = types.KeyboardButton("📝 Предложения и улучшения")
            item3 = types.KeyboardButton("📍 Вернуться в Главное меню")
            markup.row(item1)
            markup.row(item2)
            markup.row(item3)
            bot.send_message(message.from_user.id, "🚩 Выберите действие", reply_markup = markup)					

        elif message.text == "🆔 Узнать ID":
            bot.send_message(message.from_user.id, "Ваш ID - " + str(message.from_user.id))

		# ТАБЛИЦА ЛИДЕРОВ

        elif message.text == "🧾 Таблица лидеров":

            id = message.from_user.id
            username = message.from_user.username
            name = message.from_user.first_name
            cursor.execute(f"SELECT id FROM users WHERE id = {id}")
            result_id = cursor.fetchone()

            if not result_id:
                cursor.execute("INSERT INTO users(id, username, name, games, score) VALUES (%s, %s, %s, %s, %s)", (id, username, name, 0, 0))
                cursor.execute("INSERT INTO date (id, games, score, games_darts, score_darts, games_number, score_number, games_kosti, score_kosti, games_bowling, score_bowling, games_football, score_football, games_basket, score_basket, games_moneta, score_moneta) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
                db.commit()

            bot.send_message(message.from_user.id, "Таблица лидеров среди людей которые больше всего выйграли данного бота)")
            bot.send_message(message.from_user.id, "Игр | Побед | Участник")

            sortirovka = (f"SELECT * FROM users ORDER BY score DESC")
            cursor.execute(sortirovka)
            sort = cursor.fetchall()

            for index, row in enumerate(sort, start = 1):
                bot.send_message(message.from_user.id, f"{index})     {row[4]}  |  {row[3]}  | {row[2]} - (@{row[1]})")
                
                limit = 8
                if index == limit:
                    break

		# ГОРОСКОП

        elif message.text == "🔮 Гороскоп":	
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton("Лев ♌️")
            item2 = types.KeyboardButton("Телец ♉️ ")
            item3 = types.KeyboardButton("Овен ♈️")
            item4 = types.KeyboardButton("Близнецы ♊️")
            item5 = types.KeyboardButton("Рак ♋️")
            item6 = types.KeyboardButton("Дева ♍️")
            item7 = types.KeyboardButton("Весы ♎️")
            item8 = types.KeyboardButton("Скорпион ♏️")
            item9 = types.KeyboardButton("Стрелец ♐️")
            item10 = types.KeyboardButton("Козерог ♑️")
            item11 = types.KeyboardButton("Водолей ♒️")
            item12 = types.KeyboardButton("Рыбы ♓️")
            item13 = types.KeyboardButton("🔙 Вернуться в Функции")
            markup.row(item1, item2, item3)
            markup.row(item4, item5, item6)
            markup.row(item7, item8, item9)
            markup.row(item10, item11, item12)
            markup.row(item13)
            bot.send_message(message.from_user.id, "🚩 Выберите свой знак зодиака", reply_markup = markup)	


        elif message.text == "Лев ♌️":
            url = "https://horo.mail.ru/prediction/leo/today"
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")
            today = soup.find("span", class_="link__text").text
            tomorrow = soup.find("span", class_="link__text").text

            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton("Лев - сегодня")
            item2 = types.KeyboardButton("Лев - завтра")
            item3 = types.KeyboardButton("🔙 Назад")
            markup.row(item1)
            markup.row(item2)
            markup.row(item3)
            bot.send_message(message.from_user.id, "Выберите день.", reply_markup = markup)

        elif message.text == "Лев - сегодня":
            url = "https://horo.mail.ru/prediction/leo/today"
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")
            today = soup.find("span", class_="link__text").text
            tomorrow = soup.find("span", class_="link__text").text
            lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text

            bot.send_message(message.from_user.id, today + " - *Лев* ♌️" +"\n\n" + lev, parse_mode = "Markdown")

        elif message.text == "Лев - завтра":
            url = "https://horo.mail.ru/prediction/leo/tomorrow"
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")
            today = soup.find("span", class_="link__text").text
            tomorrow = soup.find("span", class_="link__text").text
            lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text

            bot.send_message(message.from_user.id, tomorrow + " - *Лев* ♌️" + "\n\n" + lev, parse_mode = "Markdown")

        elif message.text == "Телец ♉️":
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton("Телец - сегодня")
            item2 = types.KeyboardButton("Телец - завтра")
            item3 = types.KeyboardButton("🔙 Назад")
            markup.row(item1)
            markup.row(item2)
            markup.row(item3)
            bot.send_message(message.from_user.id, "Выберите день.", reply_markup = markup)

        elif message.text == "Телец - сегодня":
            url = "https://horo.mail.ru/prediction/taurus/today"
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")
            today = soup.find("span", class_="link__text").text
            tomorrow = soup.find("span", class_="link__text").text
            lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text

            bot.send_message(message.from_user.id, today + " - *Телец* ♉️" +"\n\n" + lev, parse_mode = "Markdown")

        elif message.text == "Телец - завтра":
            url = "https://horo.mail.ru/prediction/taurus/tomorrow"
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")
            today = soup.find("span", class_="link__text").text
            tomorrow = soup.find("span", class_="link__text").text
            lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text

            bot.send_message(message.from_user.id, tomorrow + " - *Телец* ♉️" + "\n\n" + lev, parse_mode = "Markdown")

        elif message.text == "Овен ♈️":
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton("Овен - сегодня")
            item2 = types.KeyboardButton("Овен - завтра")
            item3 = types.KeyboardButton("🔙 Назад")
            markup.row(item1)
            markup.row(item2)
            markup.row(item3)
            bot.send_message(message.from_user.id, "Выберите день.", reply_markup = markup)     
        
        elif message.text == "Овен - сегодня":
            url = "https://horo.mail.ru/prediction/aries/today"
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")
            today = soup.find("span", class_="link__text").text
            tomorrow = soup.find("span", class_="link__text").text
            lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
            bot.send_message(message.from_user.id, today + " - *Овен* ♈️" +"\n\n" + lev, parse_mode = "Markdown")       
        
        elif message.text == "Овен - завтра":
            url = "https://horo.mail.ru/prediction/aries/tomorrow"
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")
            today = soup.find("span", class_="link__text").text
            tomorrow = soup.find("span", class_="link__text").text
            lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
            bot.send_message(message.from_user.id, tomorrow + " - *Овен* ♈️" + "\n\n" + lev, parse_mode = "Markdown")       
        
        elif message.text == "Близнецы ♊️":
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton("Близнецы - сегодня")
            item2 = types.KeyboardButton("Близнецы - завтра")
            item3 = types.KeyboardButton("🔙 Назад")
            markup.row(item1)
            markup.row(item2)
            markup.row(item3)
            bot.send_message(message.from_user.id, "Выберите день.", reply_markup = markup)     
        
        elif message.text == "Близнецы - сегодня":
            url = "https://horo.mail.ru/prediction/gemini/today"
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")
            today = soup.find("span", class_="link__text").text
            tomorrow = soup.find("span", class_="link__text").text
            lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
            bot.send_message(message.from_user.id, today + " - *Близнецы* ♊️" +"\n\n" + lev, parse_mode = "Markdown")       
        
        elif message.text == "Близнецы - завтра":
            url = "https://horo.mail.ru/prediction/gemini/tomorrow"
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")
            today = soup.find("span", class_="link__text").text
            tomorrow = soup.find("span", class_="link__text").text
            lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
            bot.send_message(message.from_user.id, tomorrow + " - *Близнецы* ♊️" + "\n\n" + lev, parse_mode = "Markdown")       
        
        elif message.text == "Рак ♋️":
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton("Рак - сегодня")
            item2 = types.KeyboardButton("Рак - завтра")
            item3 = types.KeyboardButton("🔙 Назад")
            markup.row(item1)
            markup.row(item2)
            markup.row(item3)
            bot.send_message(message.from_user.id, "Выберите день.", reply_markup = markup)     
        
        elif message.text == "Рак - сегодня":
            url = "https://horo.mail.ru/prediction/cancer/today"
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")
            today = soup.find("span", class_="link__text").text
            tomorrow = soup.find("span", class_="link__text").text
            lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
            bot.send_message(message.from_user.id, today + " - *Рак* ♋️" +"\n\n" + lev, parse_mode = "Markdown")        
        
        elif message.text == "Рак - завтра":
            url = "https://horo.mail.ru/prediction/cancer/tomorrow"
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")
            today = soup.find("span", class_="link__text").text
            tomorrow = soup.find("span", class_="link__text").text
            lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
            bot.send_message(message.from_user.id, tomorrow + " - *Рак* ♋️" + "\n\n" + lev, parse_mode = "Markdown")	        
        
        elif message.text == "Дева ♍️":
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton("Дева - сегодня")
            item2 = types.KeyboardButton("Дева - завтра")
            item3 = types.KeyboardButton("🔙 Назад")
            markup.row(item1)
            markup.row(item2)
            markup.row(item3)
            bot.send_message(message.from_user.id, "Выберите день.", reply_markup = markup)     
        
        elif message.text == "Дева - сегодня":
            url = "https://horo.mail.ru/prediction/virgo/today"
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")
            today = soup.find("span", class_="link__text").text
            tomorrow = soup.find("span", class_="link__text").text
            lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
            bot.send_message(message.from_user.id, today + " - *Дева* ♍️" +"\n\n" + lev, parse_mode = "Markdown")       
        
        elif message.text == "Дева - завтра":
            url = "https://horo.mail.ru/prediction/virgo/tomorrow"
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")
            today = soup.find("span", class_="link__text").text
            tomorrow = soup.find("span", class_="link__text").text
            lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
            bot.send_message(message.from_user.id, tomorrow + " - *Дева* ♍️" + "\n\n" + lev, parse_mode = "Markdown")       
        
        elif message.text == "Весы ♎️":
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton("Весы - сегодня")
            item2 = types.KeyboardButton("Весы - завтра")
            item3 = types.KeyboardButton("🔙 Назад")
            markup.row(item1)
            markup.row(item2)
            markup.row(item3)
            bot.send_message(message.from_user.id, "Выберите день.", reply_markup = markup)     
        
        elif message.text == "Весы - сегодня":
            url = "https://horo.mail.ru/prediction/libra/today"
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")
            today = soup.find("span", class_="link__text").text
            tomorrow = soup.find("span", class_="link__text").text
            lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
            bot.send_message(message.from_user.id, today + " - *Весы* ♎️" +"\n\n" + lev, parse_mode = "Markdown")       
        
        elif message.text == "Весы - завтра":
            url = "https://horo.mail.ru/prediction/libra/tomorrow"
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")
            today = soup.find("span", class_="link__text").text
            tomorrow = soup.find("span", class_="link__text").text
            lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
            bot.send_message(message.from_user.id, tomorrow + " - *Весы* ♎️" + "\n\n" + lev, parse_mode = "Markdown")	        
        
        elif message.text == "Скорпион ♏️":
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton("Скорпион - сегодня")
            item2 = types.KeyboardButton("Скорпион - завтра")
            item3 = types.KeyboardButton("🔙 Назад")
            markup.row(item1)
            markup.row(item2)
            markup.row(item3)
            bot.send_message(message.from_user.id, "Выберите день.", reply_markup = markup)     
        
        elif message.text == "Скорпион - сегодня":
            url = "https://horo.mail.ru/prediction/scorpio/today"
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")
            today = soup.find("span", class_="link__text").text
            tomorrow = soup.find("span", class_="link__text").text
            lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
            bot.send_message(message.from_user.id, today + " - *Скорпион* ♏️" +"\n\n" + lev, parse_mode = "Markdown")       
        
        elif message.text == "Скорпион - завтра":
            url = "https://horo.mail.ru/prediction/scorpio/tomorrow"
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")
            today = soup.find("span", class_="link__text").text
            tomorrow = soup.find("span", class_="link__text").text
            lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
            bot.send_message(message.from_user.id, tomorrow + " - *Скорпион* ♏️" + "\n\n" + lev, parse_mode = "Markdown")       
        
        elif message.text == "Стрелец ♐️":
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton("Стрелец - сегодня")
            item2 = types.KeyboardButton("Стрелец - завтра")
            item3 = types.KeyboardButton("🔙 Назад")
            markup.row(item1)
            markup.row(item2)
            markup.row(item3)
            bot.send_message(message.from_user.id, "Выберите день.", reply_markup = markup)     
        
        elif message.text == "Стрелец - сегодня":
            url = "https://horo.mail.ru/prediction/sagittarius/today"
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")
            today = soup.find("span", class_="link__text").text
            tomorrow = soup.find("span", class_="link__text").text
            lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
            bot.send_message(message.from_user.id, today + " - *Стрелец* ♐️" +"\n\n" + lev, parse_mode = "Markdown")        
        
        elif message.text == "Стрелец - завтра":
            url = "https://horo.mail.ru/prediction/sagittarius/tomorrow"
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")
            today = soup.find("span", class_="link__text").text
            tomorrow = soup.find("span", class_="link__text").text
            lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
            bot.send_message(message.from_user.id, tomorrow + " - *Стрелец* ♐️" + "\n\n" + lev, parse_mode = "Markdown")        
        
        elif message.text == "Козерог ♑️":
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton("Козерог - сегодня")
            item2 = types.KeyboardButton("Козерог - завтра")
            item3 = types.KeyboardButton("🔙 Назад")
            markup.row(item1)
            markup.row(item2)
            markup.row(item3)
            bot.send_message(message.from_user.id, "Выберите день.", reply_markup = markup)     
        
        elif message.text == "Козерог - сегодня":
            url = "https://horo.mail.ru/prediction/capricorn/today"
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")
            today = soup.find("span", class_="link__text").text
            tomorrow = soup.find("span", class_="link__text").text
            lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
            bot.send_message(message.from_user.id, today + " - *Козерог* ♑️" +"\n\n" + lev, parse_mode = "Markdown")        
        
        elif message.text == "Козерог - завтра":
            url = "https://horo.mail.ru/prediction/capricorn/tomorrow"
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")
            today = soup.find("span", class_="link__text").text
            tomorrow = soup.find("span", class_="link__text").text
            lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
            bot.send_message(message.from_user.id, tomorrow + " - *Козерог* ♑️" + "\n\n" + lev, parse_mode = "Markdown")        
        
        elif message.text == "Водолей ♒️":
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton("Водолей - сегодня")
            item2 = types.KeyboardButton("Водолей - завтра")
            item3 = types.KeyboardButton("🔙 Назад")
            markup.row(item1)
            markup.row(item2)
            markup.row(item3)
            bot.send_message(message.from_user.id, "Выберите день.", reply_markup = markup)     
        
        elif message.text == "Водолей - сегодня":
            url = "https://horo.mail.ru/prediction/aquarius/today"
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")
            today = soup.find("span", class_="link__text").text
            tomorrow = soup.find("span", class_="link__text").text
            lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
            bot.send_message(message.from_user.id, today + " - *Водолей* ♒️" +"\n\n" + lev, parse_mode = "Markdown")        
        
        elif message.text == "Водолей - завтра":
            url = "https://horo.mail.ru/prediction/aquarius/tomorrow"
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")
            today = soup.find("span", class_="link__text").text
            tomorrow = soup.find("span", class_="link__text").text
            lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
            bot.send_message(message.from_user.id, tomorrow + " - *Водолей* ♒️" + "\n\n" + lev, parse_mode = "Markdown")	        
        
        elif message.text == "Рыбы ♓️":
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton("Рыбы - сегодня")
            item2 = types.KeyboardButton("Рыбы - завтра")
            item3 = types.KeyboardButton("🔙 Назад")
            markup.row(item1)
            markup.row(item2)
            markup.row(item3)
            bot.send_message(message.from_user.id, "Выберите день.", reply_markup = markup)     
        
        elif message.text == "Рыбы - сегодня":
            url = "https://horo.mail.ru/prediction/pisces/today"
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")
            today = soup.find("span", class_="link__text").text
            tomorrow = soup.find("span", class_="link__text").text
            lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
            bot.send_message(message.from_user.id, today + " - *Рыбы* ♓️" +"\n\n" + lev, parse_mode = "Markdown")       
        
        elif message.text == "Рыбы - завтра":
            url = "https://horo.mail.ru/prediction/pisces/tomorrow"
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")
            today = soup.find("span", class_="link__text").text
            tomorrow = soup.find("span", class_="link__text").text
            lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
            bot.send_message(message.from_user.id, tomorrow + " - *Рыбы* ♓️" + "\n\n" + lev, parse_mode = "Markdown")																			        

        elif message.text == "🔙 Назад":
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton("Лев ♌️")
            item2 = types.KeyboardButton("Телец ♉️")
            item3 = types.KeyboardButton("Овен ♈️")
            item4 = types.KeyboardButton("Близнецы ♊️")
            item5 = types.KeyboardButton("Рак ♋️")
            item6 = types.KeyboardButton("Дева ♍️")
            item7 = types.KeyboardButton("Весы ♎️")
            item8 = types.KeyboardButton("Скорпион ♏️")
            item9 = types.KeyboardButton("Стрелец ♐️")
            item10 = types.KeyboardButton("Козерог ♑️")
            item11 = types.KeyboardButton("Водолей ♒️")
            item12 = types.KeyboardButton("Рыбы ♓️")
            item13 = types.KeyboardButton("🔙 Вернуться в Функции")
            markup.row(item1, item2, item3)
            markup.row(item4, item5, item6)
            markup.row(item7, item8, item9)
            markup.row(item10, item11, item12)
            markup.row(item13)
            bot.send_message(message.from_user.id, "🚩 Выберите свой знак зодиака", reply_markup = markup)				        
        
        # ФУНКЦИИ       
        elif message.text == "💎 Функции":             
            id = message.from_user.id
            username = message.from_user.username
            name = message.from_user.first_name
            cursor.execute(f"SELECT id FROM users WHERE id = {id}")
            result_id = cursor.fetchone()

            if not result_id:
                cursor.execute("INSERT INTO users(id, username, name, games, score) VALUES (%s, %s, %s, %s, %s)", (id, username, name, 0, 0))
                cursor.execute("INSERT INTO date (id, games, score, games_darts, score_darts, games_number, score_number, games_kosti, score_kosti, games_bowling, score_bowling, games_football, score_football, games_basket, score_basket, games_moneta, score_moneta) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
                db.commit()
                   
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
            item1 = types.KeyboardButton("💰 Курс валют")
            item2 = types.KeyboardButton("🌍 Погода")
            item3 = types.KeyboardButton("🎰 Рандомное число")
            item4 = types.KeyboardButton("🎡 Сыграть с ботом")
            item5 = types.KeyboardButton("📖 Вики")
            item6 = types.KeyboardButton("🔮 Гороскоп")
            item7 = types.KeyboardButton("📍 Вернуться в Главное меню")
            markup.row(item1, item2)
            markup.row(item3, item4)
            markup.row(item5, item6)
            markup.row(item7)
            bot.send_message(message.from_user.id, "🚩 Выберите действие", reply_markup = markup)    
        
        elif message.text == "🔙 Вернуться в Функции":
            id = message.from_user.id
            username = message.from_user.username
            name = message.from_user.first_name
            cursor.execute(f"SELECT id FROM users WHERE id = {id}")
            result_id = cursor.fetchone()

            if not result_id:
                cursor.execute("INSERT INTO users(id, username, name, games, score) VALUES (%s, %s, %s, %s, %s)", (id, username, name, 0, 0))
                cursor.execute("INSERT INTO date (id, games, score, games_darts, score_darts, games_number, score_number, games_kosti, score_kosti, games_bowling, score_bowling, games_football, score_football, games_basket, score_basket, games_moneta, score_moneta) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
                db.commit()

            markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
            item1 = types.KeyboardButton("💰 Курс валют")
            item2 = types.KeyboardButton("🌍 Погода")
            item3 = types.KeyboardButton("🎰 Рандомное число")
            item4 = types.KeyboardButton("🎡 Сыграть с ботом")
            item5 = types.KeyboardButton("📖 Вики")
            item6 = types.KeyboardButton("🔮 Гороскоп")
            item7 = types.KeyboardButton("📍 Вернуться в Главное меню")
            markup.row(item1, item2)
            markup.row(item3, item4)
            markup.row(item5, item6)
            markup.row(item7)
            bot.send_message(message.from_user.id, "🚩 Выберите действие", reply_markup = markup)       

        elif message.text == "📖 Вики":
            bot.send_message(message.chat.id, "Введите ваш запрос: ")
            bot.register_next_step_handler(message, wiki)       
        
        elif message.text == "📍 Вернуться в Главное меню":
            name = message.from_user.first_name     
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton("🧾 Таблица лидеров")
            item2 = types.KeyboardButton("💎 Функции")
            item3 = types.KeyboardButton("🛠 Прочее")
            markup.row(item1)
            markup.row(item2)
            markup.row(item3)
            bot.send_message(message.from_user.id,  str(name) + ", чем я могу тебе помочь?", reply_markup = markup)     
        
        # КУРС ВАЛЮТ        
        elif message.text == "💰 Курс валют":
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton("📈 Курс валют")
            item2 = types.KeyboardButton("🔁 Перевести")
            item3 = types.KeyboardButton("🔙 Вернуться в Функции")
            markup.row(item1, item2)
            markup.row(item3)
            bot.send_message(message.from_user.id, "🚩 Выберите действие", reply_markup = markup)       
        
        elif message.text == "📈 Курс валют":
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton("💵 Доллар")
            item2 = types.KeyboardButton("💶 Евро")
            item3 = types.KeyboardButton("🔙 Вернуться в Курс Валют")
            markup.row(item1, item2)
            markup.row(item3)
            bot.send_message(message.from_user.id, "Выберите валюту 💵 💶", reply_markup = markup)      
        
        elif message.text == "💵 Доллар":
            bot.send_message(message.chat.id, "💵 Доллар на данный момент - "+ price_usd +" ₽")     
        
        elif message.text == "💶 Евро":
            bot.send_message(message.chat.id, "💶 Евро на данный момент - "+ price_euro +" ₽")      
        
        elif message.text == "🔁 Перевести":	
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton("💴 Рубли в 💵 Доллар")
            item2 = types.KeyboardButton("💴 Рубли в 💶 Евро")
            item3 = types.KeyboardButton("💵 Доллар в 💴 Рубли")
            item4 = types.KeyboardButton("💶 Евро в 💴 Рубли")
            item5 = types.KeyboardButton("🔙 Вернуться в Курс Валют")
            markup.row(item1, item3)
            markup.row(item2, item4)
            markup.row(item5)
            bot.send_message(message.from_user.id, "🚩 Выберите действие", reply_markup = markup)       
        
        elif message.text == "🔙 Вернуться в Курс Валют":
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton("📈 Курс валют")
            item2 = types.KeyboardButton("🔁 Перевести")
            item3 = types.KeyboardButton("🔙 Вернуться в Функции")
            markup.row(item1, item2)
            markup.row(item3)
            bot.send_message(message.from_user.id, "🚩 Выберите действие", reply_markup = markup)       
        
        elif message.text == "💴 Рубли в 💵 Доллар":
            bot.send_message(message.chat.id, "Введите кол-во которое хотите перевести\n" + price_usd + " ₽" + " = 1 USD")
            bot.register_next_step_handler(message, rubl_dollar)        
        
        elif message.text == "💴 Рубли в 💶 Евро":
            bot.send_message(message.chat.id, "Введите кол-во которое хотите перевести\n" + price_euro + " ₽" + " = 1 EURO")
            bot.register_next_step_handler(message, rubl_euro)      
        
        elif message.text == "💵 Доллар в 💴 Рубли":
            bot.send_message(message.chat.id, "Введите кол-во которое хотите перевести\n1 USD = " + price_usd + " ₽")
            bot.register_next_step_handler(message, dollar_rubl)        
        
        elif message.text == "💶 Евро в 💴 Рубли":
            bot.send_message(message.chat.id, "Введите кол-во которое хотите перевести\n1 EURO = " + price_euro + " ₽")
            bot.register_next_step_handler(message, euro_rubl)      
        
        # ПОГОДА        
        elif message.text == "🌍 Погода":
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton("🌍 Омск")
            item2 = types.KeyboardButton("🌍 Москва")
            item3 = types.KeyboardButton("🌍 Новосибирск")
            item4 = types.KeyboardButton("🔙 Вернуться в Функции")
            markup.row(item1)
            markup.row(item2)
            markup.row(item3)
            markup.row(item4)
            bot.send_message(message.from_user.id, "В каком городе хотите узнать погоду на данный момент?\nЕсли здесь нету вашего города, напишите в предложку, и я с радостью добавлю)", reply_markup = markup)        
        
        # ОМСК      
        elif message.text == "🌍 Омск":
        
            url = "https://prognoz3.ru/россия/омская-область/погода-в-омске"
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")

            time = soup.find("div", class_="b-weather_current_date").text

            sunrise_time = soup.find("span", class_="sunrise_time").text
            sunset_time = soup.find("span", class_="sunset_time").text      
            temp = soup.find("span", class_="temperature").text
            note = soup.find("span", class_="note").text
            feelslike = soup.find("span", class_="feelslike").text
            precipitation = soup.find("span", class_="precipitation").text
            pressure = soup.find("span", class_="pressure").text
            humidity = soup.find("span", class_="humidity").text        

            bot.send_message(message.chat.id, "Погода в Омске\n" + time + "\n\nТемпература:  " + str(temp) + " - " + str(note) + "\n" + str(feelslike) + "\n" + str(precipitation) + "\n" + str(pressure) + "\n" + str(humidity) + "\nВосход - " + str(sunrise_time) + "\nЗакат - " + str(sunset_time))     
        
        # МОСКВА        
        elif message.text == "🌍 Москва":
        
            url = "https://prognoz3.ru/россия/московская-область/погода-в-москве"
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")

            time = soup.find("div", class_="b-weather_current_date").text       
            sunrise_time = soup.find("span", class_="sunrise_time").text
            sunset_time = soup.find("span", class_="sunset_time").text

            temp = soup.find("span", class_="temperature").text
            note = soup.find("span", class_="note").text
            feelslike = soup.find("span", class_="feelslike").text
            precipitation = soup.find("span", class_="precipitation").text
            pressure = soup.find("span", class_="pressure").text
            humidity = soup.find("span", class_="humidity").text        

            bot.send_message(message.chat.id, "Погода в Москве\n" + time + "\n\nТемпература:  " + str(temp) + " - " + str(note) + "\n" + str(feelslike) + "\n" + str(precipitation) + "\n" + str(pressure) + "\n" + str(humidity) + "\nВосход - " + str(sunrise_time) + "\nЗакат - " + str(sunset_time))        
        
        # НОВОСИБИРСК       
        elif message.text == "🌍 Новосибирск":
        
            url = "https://prognoz3.ru/россия/новосибирская-область/погода-в-новосибирске"
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")

            time = soup.find("div", class_="b-weather_current_date").text       
            sunrise_time = soup.find("span", class_="sunrise_time").text
            sunset_time = soup.find("span", class_="sunset_time").text

            temp = soup.find("span", class_="temperature").text
            note = soup.find("span", class_="note").text
            feelslike = soup.find("span", class_="feelslike").text
            precipitation = soup.find("span", class_="precipitation").text
            pressure = soup.find("span", class_="pressure").text
            humidity = soup.find("span", class_="humidity").text        

            bot.send_message(message.chat.id, "Погода в Новосибирске\n" + time + "\n\nТемпература:  " + str(temp) + " - " + str(note) + "\n" + str(feelslike) + "\n" + str(precipitation) + "\n" + str(pressure) + "\n" + str(humidity) + "\nВосход - " + str(sunrise_time) + "\nЗакат - " + str(sunset_time))      
        
        # РАНДОМНОЕ ЧИСЛО       
        elif message.text == "🎰 Рандомное число":
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton("🎲 От 0 до 10")
            item2 = types.KeyboardButton("🎲 От 0 до 100")
            item3 = types.KeyboardButton("🎲 От 0 до 1000")
            item4 = types.KeyboardButton("🔙 Вернуться в Функции")
            markup.row(item1)
            markup.row(item2)
            markup.row(item3)
            markup.row(item4)
            bot.send_message(message.from_user.id, "🚩 Выберите диапазон", reply_markup = markup)       
        
        elif message.text == "🎲 От 0 до 10":
            bot.send_message(message.chat.id, "*Вам выпало число -* " + str(random.randint(0,10)), parse_mode = "Markdown")     
        
        elif message.text == "🎲 От 0 до 100":
            bot.send_message(message.chat.id, "*Вам выпало число -* " + str(random.randint(0,100)), parse_mode = "Markdown")        
        
        elif message.text == "🎲 От 0 до 1000":
            bot.send_message(message.chat.id, "*Вам выпало число -* " + str(random.randint(0,1000)), parse_mode = "Markdown")       
        
        # СЫГРАТЬ С БОТОМ       
        elif message.text == "🎡 Сыграть с ботом":
            id = message.from_user.id
            username = message.from_user.username
            name = message.from_user.first_name
            cursor.execute(f"SELECT id FROM users WHERE id = {id}")
            result_id = cursor.fetchone()

            if not result_id:
                cursor.execute("INSERT INTO users(id, username, name, games, score) VALUES (%s, %s, %s, %s, %s)", (id, username, name, 0, 0))
                cursor.execute("INSERT INTO date (id, games, score, games_darts, score_darts, games_number, score_number, games_kosti, score_kosti, games_bowling, score_bowling, games_football, score_football, games_basket, score_basket, games_moneta, score_moneta) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
                db.commit()

            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton("🧾 Таблица лидеров")
            item2 = types.KeyboardButton("🎰 Угадай число")
            item3 = types.KeyboardButton("🎲 Игра *Кости*")
            item4 = types.KeyboardButton("🎳 Боулинг")
            item5 = types.KeyboardButton("⚽️ Футбол")
            item6 = types.KeyboardButton("🏀 Баскетбол")
            item7 = types.KeyboardButton("🟡 Орел & Решка")
            item8 = types.KeyboardButton("🎯 Дартс")
            item9 = types.KeyboardButton("🔙 Вернуться в Функции")
            markup.row(item1)
            markup.row(item2)
            markup.row(item3, item4, item5)
            markup.row(item6, item7, item8)
            markup.row(item9)
            bot.send_message(message.from_user.id, "🚩 Выберите игру", reply_markup = markup)       
        
        elif message.text == "🔙 Вернуться назад":
            id = message.from_user.id
            username = message.from_user.username
            name = message.from_user.first_name
            cursor.execute(f"SELECT id FROM users WHERE id = {id}")
            result_id = cursor.fetchone()

            if not result_id:
                cursor.execute("INSERT INTO users(id, username, name, games, score) VALUES (%s, %s, %s, %s, %s)", (id, username, name, 0, 0))
                cursor.execute("INSERT INTO date (id, games, score, games_darts, score_darts, games_number, score_number, games_kosti, score_kosti, games_bowling, score_bowling, games_football, score_football, games_basket, score_basket, games_moneta, score_moneta) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
                db.commit()

            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton("🧾 Таблица лидеров")
            item2 = types.KeyboardButton("🎰 Угадай число")
            item3 = types.KeyboardButton("🎲 Игра *Кости*")
            item4 = types.KeyboardButton("🎳 Боулинг")
            item5 = types.KeyboardButton("⚽️ Футбол")
            item6 = types.KeyboardButton("🏀 Баскетбол")
            item7 = types.KeyboardButton("🟡 Орел & Решка")
            item8 = types.KeyboardButton("🎯 Дартс")
            item9 = types.KeyboardButton("🔙 Вернуться в Функции")
            markup.row(item1)
            markup.row(item2) 
            markup.row(item3, item4, item5)
            markup.row(item6, item7, item8)
            markup.row(item9)
            bot.send_message(message.from_user.id, "🚩 Выберите игру", reply_markup = markup)       
        
        # ОРЕЛ & РЕШКА      
        elif message.text == "🟡 Орел & Решка":
            id = message.from_user.id
            name = message.from_user.first_name
            cursor.execute(f"UPDATE users SET games = games + 1 WHERE id = {id}")
            cursor.execute(f"UPDATE date SET games = games + 1 WHERE id = {id}")
            cursor.execute(f"UPDATE date SET games_moneta = games_moneta + 1 WHERE id = {id}")
            db.commit()

            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton("Орел")
            item2 = types.KeyboardButton("Решка")
            markup.row(item1)
            markup.row(item2)
            bot.send_message(message.chat.id, "Орел или Решка ?" , reply_markup = markup)			
            bot.register_next_step_handler(message, moneta)      
        
        # ДАРТС     
        elif message.text == "🎯 Дартс":
            name = message.from_user.first_name     
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
            item1 = types.KeyboardButton("Бросить дротик 🎯")
            item2 = types.KeyboardButton("🔙 Вернуться назад")
            markup.row(item1)
            markup.row(item2)
            bot.send_message(message.chat.id, "🎯 Кидает дротик - " + str(name) , reply_markup = markup)        
        
        elif message.text == "Бросить дротик 🎯":
            id = message.from_user.id
            name = message.from_user.first_name
            cursor.execute(f"UPDATE users SET games = games + 1 WHERE id = {id}")
            db.commit()

            cursor.execute(f"UPDATE date SET games = games + 1 WHERE id = {id}")
            db.commit()

            cursor.execute(f"UPDATE date SET games_darts = games_darts + 1 WHERE id = {id}")
            db.commit()

            ball = bot.send_dice(message.chat.id, '🎯')
            sleep(5)

            if ball.dice.value == 1:
                bot.send_message(message.chat.id, "Игрок " + str(name) + " не попал")
            elif ball.dice.value == 2:
                bot.send_message(message.chat.id, "Игрок " + str(name) + " попал в " + str(ball.dice.value))
            elif ball.dice.value == 3:
                bot.send_message(message.chat.id, "Игрок " + str(name) + " попал в " + str(ball.dice.value))
            elif ball.dice.value == 4:
                bot.send_message(message.chat.id, "Игрок " + str(name) + " попал в " + str(ball.dice.value))
            elif ball.dice.value == 5:
                bot.send_message(message.chat.id, "Игрок " + str(name) + " попал в " + str(ball.dice.value))
            elif ball.dice.value == 6:
                bot.send_message(message.chat.id, "Игрок " + str(name) + " попал в яблочко!")

            sleep(0.5)	
            bot.send_message(message.chat.id, "🎯 Кидает дротик БОТ")
            sleep(1.5)
            ball_two = bot.send_dice(message.chat.id, '🎯')
            sleep(5)

            if ball_two.dice.value == 1:
                bot.send_message(message.chat.id, "БОТ не попал")
            elif ball_two.dice.value == 2:
                bot.send_message(message.chat.id, "БОТ попал в " + str(ball_two.dice.value))
            elif ball_two.dice.value == 3:
                bot.send_message(message.chat.id, "БОТ попал в " + str(ball_two.dice.value))
            elif ball_two.dice.value == 4:
                bot.send_message(message.chat.id, "БОТ попал в " + str(ball_two.dice.value))
            elif ball_two.dice.value == 5:
                bot.send_message(message.chat.id, "БОТ попал в " + str(ball_two.dice.value))
            elif ball_two.dice.value == 6:
                bot.send_message(message.chat.id, "БОТ попал в яблочко!")

            sleep(0.5)
            bot.send_message(message.chat.id, "⏳ Идет подсчет результатов...")
            sleep(0.5)
            bot.send_message(message.chat.id, "⌛️ Идет подсчет результатов...")
            sleep(0.5)

            if ball.dice.value > ball_two.dice.value:
                id = message.from_user.id
                cursor.execute(f"UPDATE users SET score = score + 1 WHERE id = {id}")
                cursor.execute(f"UPDATE date SET score = score + 1 WHERE id = {id}")
                cursor.execute(f"UPDATE date SET score_darts = score_darts + 1 WHERE id = {id}")
                db.commit()

                bot.send_message(message.chat.id, "*Победил - *" + str(name), parse_mode = "Markdown")
                bot.send_message(message.chat.id, "🥳")
            elif ball.dice.value == ball_two.dice.value:
                bot.send_message(message.chat.id, "*Ничья!*", parse_mode = "Markdown")
                bot.send_message(message.chat.id, "🤷‍♂")
            else:
                bot.send_message(message.chat.id, "😑 *Победил БОТ*", parse_mode = "Markdown")
                bot.send_message(message.chat.id, "😞")

            sleep(2)        
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
            item1 = types.KeyboardButton("Бросить дротик 🎯")
            item2 = types.KeyboardButton("🔙 Вернуться назад")
            markup.row(item1)
            markup.row(item2)
            bot.send_message(message.chat.id, "Сыграете еще раз?" , reply_markup = markup)      
        
        # БАСКЕТБОЛ     
        elif message.text == "🏀 Баскетбол":
            name = message.from_user.first_name
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
            item1 = types.KeyboardButton("Кинуть мяч 🏀")
            item2 = types.KeyboardButton("🔙 Вернуться назад")
            markup.row(item1)
            markup.row(item2)
            bot.send_message(message.chat.id, "🏀 Кидает мяч - " + str(name) , reply_markup = markup)       
        
        elif message.text == "Кинуть мяч 🏀":
            id = message.from_user.id
            name = message.from_user.first_name
            cursor.execute(f"UPDATE users SET games = games + 1 WHERE id = {id}")
            db.commit()

            cursor.execute(f"UPDATE date SET games = games + 1 WHERE id = {id}")
            db.commit()

            cursor.execute(f"UPDATE date SET games_basket = games_basket + 1 WHERE id = {id}")
            db.commit()


            ball = bot.send_dice(message.from_user.id, '🏀')
            sleep(5)

            if ball.dice.value > 3:
                name = message.from_user.first_name
                bot.send_message(message.from_user.id, "Игрок " + str(name) + " попал в кольцо, и он получает оценку " + str(ball.dice.value))
                sleep(1.5)
            else:
                bot.send_message(message.from_user.id, "Игрок " + str(name) + " промахнулся")   

            bot.send_message(message.from_user.id, "🏀 Кидает мяч БОТ")
            sleep(1.5)
            ball_two = bot.send_dice(message.chat.id, '🏀')
            sleep(5)

            if ball_two.dice.value > 3:
                bot.send_message(message.from_user.id, "БОТ попал в кольцо, и он получает оценку " + str(ball_two.dice.value))
                sleep(1.5)
            else:
                bot.send_message(message.from_user.id, "БОТ промахнулся")

            bot.send_message(message.from_user.id, "⏳ Идет подсчет результатов...")
            sleep(1.5)
            bot.send_message(message.chat.id, "⌛️ Идет подсчет результатов...")
           
            if ball.dice.value > 3:
                if ball_two.dice.value > 3:
                    if ball.dice.value > ball_two.dice.value:
                        id = message.from_user.id
                        cursor.execute(f"UPDATE users SET score = score + 1 WHERE id = {id}")
                        cursor.execute(f"UPDATE date SET score = score + 1 WHERE id = {id}")
                        cursor.execute(f"UPDATE date SET score_basket = score_basket + 1 WHERE id = {id}")
                        db.commit()

                        bot.send_message(message.from_user.id, "*Победил - *" + str(name), parse_mode = "Markdown")
                        bot.send_message(message.from_user.id, "🥳")
                    elif ball.dice.value == ball_two.dice.value:
                        bot.send_message(message.from_user.id, "*Ничья!*", parse_mode = "Markdown")
                        bot.send_message(message.chat.id, "🤷‍♂")
                    else:
                        bot.send_message(message.from_user.id, "😑 *Победил БОТ*", parse_mode = "Markdown")
                        bot.send_message(message.from_user.id, "😞")
                else:
                    id = message.from_user.id
                    cursor.execute(f"UPDATE users SET score = score + 1 WHERE id = {id}")
                    cursor.execute(f"UPDATE date SET score = score + 1 WHERE id = {id}")
                    cursor.execute(f"UPDATE date SET score_basket = score_basket + 1 WHERE id = {id}")
                    db.commit()

                    bot.send_message(message.from_user.id, "*Победил - *" + str(name), parse_mode="Markdown")
                    bot.send_message(message.chat.id, "🥳")
            elif ball.dice.value < 3:
                if ball_two.dice.value < 3:
                    bot.send_message(message.from_user.id, "Никто не попал. Ничья!")
                    bot.send_message(message.chat.id, "🤷‍♂")
                else:
                    bot.send_message(message.from_user.id, "😑 *Победил БОТ*", parse_mode = "Markdown")
                    bot.send_message(message.from_user.id, "😞")
            else:
                bot.send_message(message.from_user.id, "Никто не попал. Ничья!")
                bot.send_message(message.from_user.id, "🤷‍♂")

            sleep(1)        
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
            item1 = types.KeyboardButton("Кинуть мяч 🏀")
            item2 = types.KeyboardButton("🔙 Вернуться назад")
            markup.row(item1)
            markup.row(item2)
            bot.send_message(message.from_user.id, "Сыграете еще раз?" , reply_markup = markup)      
        
        # ФУТБОЛ        
        elif message.text == "⚽️ Футбол":
            name = message.from_user.first_name     
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
            item1 = types.KeyboardButton("Пнуть мяч ⚽️")
            item2 = types.KeyboardButton("🔙 Вернуться назад")
            markup.row(item1)
            markup.row(item2)
            bot.send_message(message.chat.id, "⚽️ Пинает мяч - " + str(name) , reply_markup = markup)       
        
        elif message.text == "Пнуть мяч ⚽️":
            id = message.from_user.id
            name = message.from_user.first_name
            cursor.execute(f"UPDATE users SET games = games + 1 WHERE id = {id}")
            db.commit()

            cursor.execute(f"UPDATE date SET games = games + 1 WHERE id = {id}")
            db.commit()

            cursor.execute(f"UPDATE date SET games_football = games_football + 1 WHERE id = {id}")
            db.commit()

            ball = bot.send_dice(message.chat.id, '⚽️')
            sleep(5)

            if ball.dice.value > 2:
                bot.send_message(message.chat.id, "Игрок " + str(name) + " попал в ворота, и он получает оценку " + str(ball.dice.value))
                sleep(1.5)
            else:
                bot.send_message(message.chat.id, "Игрок " + str(name) + " промахнулся")
                sleep(1.5)

            bot.send_message(message.chat.id, "⚽️ Пинает мяч БОТ")
            sleep(1.5)
            ball_two = bot.send_dice(message.chat.id, '⚽️')
            sleep(5)
   
            if ball_two.dice.value > 2:
                bot.send_message(message.chat.id, "БОТ попал в ворота, и он получает оценку " + str(ball_two.dice.value))
                sleep(1.5)
            else:
                bot.send_message(message.chat.id, "БОТ промахнулся")

            sleep(0.5)
            bot.send_message(message.chat.id, "⏳ Идет подсчет результатов...")
            sleep(0.5)
            bot.send_message(message.chat.id, "⌛️ Идет подсчет результатов...")
            sleep(0.5)

            if ball.dice.value > 2:
                if ball_two.dice.value > 2:
                    if ball.dice.value > ball_two.dice.value:
                        id = message.from_user.id
                        name = message.from_user.first_name
                        cursor.execute(f"UPDATE users SET score = score + 1 WHERE id = {id}")
                        cursor.execute(f"UPDATE date SET score = score + 1 WHERE id = {id}")
                        cursor.execute(f"UPDATE date SET score_football = score_football + 1 WHERE id = {id}")
                        db.commit()

                        bot.send_message(message.chat.id, "*Победил - *" + str(name) , parse_mode = "Markdown")
                        bot.send_message(message.chat.id, "🥳")
                    elif ball.dice.value == ball_two.dice.value:
                        bot.send_message(message.chat.id, "*Ничья!*", parse_mode = "Markdown")
                        bot.send_message(message.chat.id, "🤷‍♂")
                    else:
                        bot.send_message(message.chat.id, "😑 *Победил БОТ*", parse_mode = "Markdown")
                        bot.send_message(message.chat.id, "😞")
                else:
                    id = message.from_user.id
                    name = message.from_user.first_name
                    cursor.execute(f"UPDATE users SET score = score + 1 WHERE id = {id}")
                    cursor.execute(f"UPDATE date SET score = score + 1 WHERE id = {id}")
                    cursor.execute(f"UPDATE date SET score_football = score_football + 1 WHERE id = {id}")
                    db.commit()

                    bot.send_message(message.chat.id, "*Победил - *" + str(name), parse_mode = "Markdown")
                    bot.send_message(message.chat.id, "🥳")
            elif ball.dice.value < 2:
                if ball_two.dice.value < 2:
                    bot.send_message(message.chat.id, "Никто не попал. Ничья!")
                    bot.send_message(message.chat.id, "🤷‍♂")
                else:
                    bot.send_message(message.chat.id, "😑 *Победил БОТ*", parse_mode = "Markdown")
                    bot.send_message(message.chat.id, "😞")
            else:
                bot.send_message(message.chat.id, "Никто не попал. Ничья!")
                bot.send_message(message.chat.id, "🤷‍♂")

            sleep(1.5)
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
            item1 = types.KeyboardButton("Пнуть мяч ⚽️")
            item2 = types.KeyboardButton("🔙 Вернуться назад")
            markup.row(item1)
            markup.row(item2)
            bot.send_message(message.chat.id, "Сыграете еще раз?" , reply_markup = markup)      
        
        # ИГРА "БОУЛИНГ"        
        elif message.text == "🎳 Боулинг":
            name = message.from_user.first_name     
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
            item1 = types.KeyboardButton("Бросить шар 🎳")
            item2 = types.KeyboardButton("🔙 Вернуться назад")
            markup.row(item1)
            markup.row(item2)
            bot.send_message(message.from_user.id, "🎳 Бросает шар - " + str(name) , reply_markup = markup)     
        
        elif message.text == "Бросить шар 🎳":
            id = message.from_user.id
            name = message.from_user.first_name
            cursor.execute(f"UPDATE users SET games = games + 1 WHERE id = {id}")
            db.commit()

            cursor.execute(f"UPDATE date SET games = games + 1 WHERE id = {id}")
            db.commit()

            cursor.execute(f"UPDATE date SET games_bowling = games_bowling + 1 WHERE id = {id}")
            db.commit()

            ball = bot.send_dice(message.chat.id, '🎳')
            sleep(5)

            if ball.dice.value == 1:
                bot.send_message(message.chat.id, "Игрок " + str(name) + " промахнулся")
            elif ball.dice.value == 2:
                bot.send_message(message.chat.id, "Игрок " + str(name) + " сбил 1 кеглю")
            elif ball.dice.value == 3:
                bot.send_message(message.chat.id, "Игрок " + str(name) + " сбил " + str(ball.dice.value) + " кегли")
            elif ball.dice.value == 4:
                bot.send_message(message.chat.id, "Игрок " + str(name) + " сбил " + str(ball.dice.value) + " кегли")
            elif ball.dice.value == 5:
                bot.send_message(message.chat.id, "Игрок " + str(name) + " сбил " + str(ball.dice.value) + " кеглей")
            elif ball.dice.value == 6:
                bot.send_message(message.chat.id, "Игрок " + str(name) + " выбил STRIKE!!")  

            sleep(1.5)
            bot.send_message(message.chat.id, "🎳 Бросает шар БОТ")
            sleep(1.5)
            ball_two = bot.send_dice(message.chat.id, '🎳')
            sleep(5)

            if ball_two.dice.value == 1:
                bot.send_message(message.chat.id, "БОТ промахнулся")
            elif ball_two.dice.value == 2:
                bot.send_message(message.chat.id, "БОТ сбил 1 кеглю")
            elif ball_two.dice.value == 3:
                bot.send_message(message.chat.id, "БОТ сбил " + str(ball_two.dice.value) + " кегли")
            elif ball_two.dice.value == 4:
                bot.send_message(message.chat.id, "БОТ сбил " + str(ball_two.dice.value) + " кегли")
            elif ball_two.dice.value == 5:
                bot.send_message(message.chat.id, "БОТ сбил " + str(ball_two.dice.value) + " кеглей")
            elif ball_two.dice.value == 6:
                bot.send_message(message.chat.id, "БОТ выбил STRIKE!!")

            sleep(1)
            bot.send_message(message.chat.id, "⏳ Идет подсчет результатов...")
            sleep(1)
            bot.send_message(message.chat.id, "⌛️ Идет подсчет результатов...")
            sleep(0.5)

            if ball.dice.value > ball_two.dice.value:
                id = message.from_user.id
                name = message.from_user.first_name
                cursor.execute(f"UPDATE users SET score = score + 1 WHERE id = {id}")
                cursor.execute(f"UPDATE date SET score = score + 1 WHERE id = {id}")
                cursor.execute(f"UPDATE date SET score_bowling = score_bowling + 1 WHERE id = {id}")
                db.commit()

                bot.send_message(message.chat.id, "*Победил - *" + str(name), parse_mode = "Markdown")
                bot.send_message(message.chat.id, "🥳")
            elif ball.dice.value == ball_two.dice.value:
                bot.send_message(message.chat.id, "*Ничья!*", parse_mode = "Markdown")
                bot.send_message(message.chat.id, "🤷‍♂")
            else:
                bot.send_message(message.chat.id, "😑 *Победил БОТ*", parse_mode = "Markdown")
                bot.send_message(message.chat.id, "😞")     
            
            sleep(2)        
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
            item1 = types.KeyboardButton("Бросить шар 🎳")
            item2 = types.KeyboardButton("🔙 Вернуться назад")
            markup.row(item1)
            markup.row(item2)
            bot.send_message(message.chat.id, "Сыграете еще раз?" , reply_markup = markup)      
        
        # ИГРА *КОСТИ*      
        elif message.text == "🎲 Игра *Кости*":
            name = message.from_user.first_name     
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
            item1 = types.KeyboardButton("Бросить кубик 🎲")
            item2 = types.KeyboardButton("🔙 Вернуться назад")
            markup.row(item1)
            markup.row(item2)
            bot.send_message(message.chat.id, "🎲 Бросает кубик - " + str(name) , reply_markup = markup)        
        
        elif message.text == "Бросить кубик 🎲":
            id = message.from_user.id
            name = message.from_user.first_name
            cursor.execute(f"UPDATE users SET games = games + 1 WHERE id = {id}")
            db.commit()

            cursor.execute(f"UPDATE date SET games = games + 1 WHERE id = {id}")
            db.commit()

            cursor.execute(f"UPDATE date SET games_kosti = games_kosti + 1 WHERE id = {id}")
            db.commit()

            cube = bot.send_dice(message.chat.id)
            sleep(5)
            bot.send_message(message.chat.id, "Игроку " + str(name) + " выпало число - " + str(cube.dice.value))
            sleep(1.5)
            bot.send_message(message.chat.id, "🎲 Бросает кубик БОТ")
            sleep(1.5)
            cube_two = bot.send_dice(message.chat.id)
            sleep(5)
            bot.send_message(message.chat.id, "БОТ выбил число - " + str(cube_two.dice.value))
            sleep(1)
            bot.send_message(message.chat.id, "⏳ Идет подсчет результатов...")
            sleep(1)
            bot.send_message(message.chat.id, "⌛️ Идет подсчет результатов...")
            sleep(2)        
            
            if cube.dice.value > cube_two.dice.value:
                id = message.from_user.id
                name = message.from_user.first_name
                cursor.execute(f"UPDATE users SET score = score + 1 WHERE id = {id}")
                cursor.execute(f"UPDATE date SET score = score + 1 WHERE id = {id}")
                cursor.execute(f"UPDATE date SET score_kosti = score_kosti + 1 WHERE id = {id}")
                db.commit()

                bot.send_message(message.chat.id, "*Победил - *" + str(name), parse_mode = "Markdown")
                bot.send_message(message.chat.id, "🥳")
            elif cube.dice.value == cube_two.dice.value:
                bot.send_message(message.chat.id, "*Ничья!*", parse_mode = "Markdown")
                bot.send_message(message.chat.id, "🤷‍♂")
            else:
                bot.send_message(message.chat.id, "*Победил БОТ*", parse_mode = "Markdown")
                bot.send_message(message.chat.id, "😞")     
            
            sleep(1)        
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
            item1 = types.KeyboardButton("Бросить кубик 🎲")
            item2 = types.KeyboardButton("🔙 Вернуться назад")
            markup.row(item1)
            markup.row(item2)
            bot.send_message(message.chat.id, "Сыграете еще раз?" , reply_markup = markup)
        
        # УГАДАЙ ЧИСЛО      
        elif message.text == "🎰 Угадай число":
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
            item1 = types.KeyboardButton("Да)")
            item2 = types.KeyboardButton("Нет)")
            markup.row(item1)
            markup.row(item2)
            bot.send_message(message.chat.id, "Хотите сыграть с ботом в Угадай число?\nПравила игры максимально просты.\nБот загадывает число от 1 до 10, а вам нужно угадать это число, даётся 5 попыток!", reply_markup = markup )        
        
        elif message.text == "Да)":
            id = message.from_user.id
            cursor.execute(f"UPDATE users SET games = games + 1 WHERE id = {id}")
            db.commit()

            cursor.execute(f"UPDATE date SET games = games + 1 WHERE id = {id}")
            db.commit()

            cursor.execute(f"UPDATE date SET games_number = games_number + 1 WHERE id = {id}")
            db.commit()

            global counter
            global random_number        
            sleep(0.5)
            bot.send_message(message.chat.id, "Отлично. Тогда начнем")
            sleep(0.5)
            bot.send_message(message.chat.id, "Бот загадал число. У вас 5 попыток!")        
            random_number = random.randint(1, 10)
            counter = 5     
            sleep(0.5)      
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton("1")
            item2 = types.KeyboardButton("2")
            item3 = types.KeyboardButton("3")
            item4 = types.KeyboardButton("4")
            item5 = types.KeyboardButton("5")
            item6 = types.KeyboardButton("6")
            item7 = types.KeyboardButton("7")
            item8 = types.KeyboardButton("8")
            item9 = types.KeyboardButton("9")
            item10 = types.KeyboardButton("10")     
            markup.row(item1, item2, item3)
            markup.row(item4, item5, item6)
            markup.row(item7, item8, item9)
            markup.row(item10)      
            bot.send_message(message.chat.id, "Выберите число", reply_markup = markup)
            bot.register_next_step_handler(message, number)

        elif message.text == "Нет)":
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton("🧾 Таблица лидеров")
            item2 = types.KeyboardButton("🎰 Угадай число")
            item3 = types.KeyboardButton("🎲 Игра *Кости*")
            item4 = types.KeyboardButton("🎳 Боулинг")
            item5 = types.KeyboardButton("⚽️ Футбол")
            item6 = types.KeyboardButton("🏀 Баскетбол")
            item7 = types.KeyboardButton("🟡 Орел & Решка")
            item8 = types.KeyboardButton("🎯 Дартс")
            item9 = types.KeyboardButton("🔙 Вернуться в Функции")
            markup.row(item1)
            markup.row(item2) 
            markup.row(item3, item4, item5)
            markup.row(item6, item7, item8)
            markup.row(item9)
            bot.send_message(message.from_user.id, "🚩 Выберите игру", reply_markup = markup)       
        
        # ОТЧЕТ О ДОСТАВКЕ СООБЩЕНИЯ "ПРЕДЛОЖЕНИЯ И УЛУЧШЕНИЯ"      
        elif message.text == "Все верно ✅":
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
            item1 = types.KeyboardButton("📍 Вернуться в Главное меню")
            markup.row(item1)
            bot.send_message(message.chat.id, "Успешно! Ваше сообщение доставлено!  📦", reply_markup = markup)
            chat_id = "1277445345"
            bot.send_message(chat_id, "Предложение по улучшения от " + str(message.from_user.first_name) + " (@" + str(message.from_user.username) + " ) " + "\n\n" + up_text, reply_markup = markup)       
        
        elif message.text == "Хочу переписать 📄":
            bot.send_message(message.chat.id, "Напишите ваши улучшения в чат! ⤵️")
            bot.register_next_step_handler(message, up_bot)
        
        elif message.text == "Отмена ⛔️":
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
            item1 = types.KeyboardButton("📄 Информация")
            item2 = types.KeyboardButton("📝 Предложения и улучшения")
            item3 = types.KeyboardButton("📍 Вернуться в Главное меню")
            markup.row(item1)
            markup.row(item2)
            markup.row(item3)
            bot.send_message(message.from_user.id, "🚩 Выберите действие", reply_markup = markup)	

		# ИНАЧЕ
        else:
            bot.send_message(message.chat.id, "🗿 Я тебя не понимаю. Напиши /start или /help")	


# ОРЕЛ & РЕШКА

def moneta(message):
    id = message.from_user.id
    name = message.from_user.first_name
    cursor.execute(f"UPDATE users SET games = games + 1 WHERE id = {id}")
    db.commit()

    cursor.execute(f"UPDATE date SET games = games + 1 WHERE id = {id}")
    db.commit()

    cursor.execute(f"UPDATE date SET games_moneta = games_moneta + 1 WHERE id = {id}")
    db.commit()


    moneta = ["Орел", "Решка"]
    moneta_random = random.choice(moneta)

    moneta_user = message.text

    stick = open("image/AnimatedSticker.tgs", "rb")
    bot.send_sticker(message.chat.id, stick)
    sleep(3)
    bot.send_message(message.chat.id, str(moneta_random))
    sleep(1)
        
    if moneta_random == moneta_user:
        id = message.from_user.id
        name = message.from_user.first_name
        cursor.execute(f"UPDATE date SET score_moneta = score_moneta + 1 WHERE id = {id}")
        cursor.execute(f"UPDATE date SET score = score + 1 WHERE id = {id}")
        db.commit()
        
        bot.send_message(message.chat.id, "Вы победили!")
        sleep(2)
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton("🧾 Таблица лидеров")
        item2 = types.KeyboardButton("🎰 Угадай число")
        item3 = types.KeyboardButton("🎲 Игра *Кости*")
        item4 = types.KeyboardButton("🎳 Боулинг")
        item5 = types.KeyboardButton("⚽️ Футбол")
        item6 = types.KeyboardButton("🏀 Баскетбол")
        item7 = types.KeyboardButton("🟡 Орел & Решка")
        item8 = types.KeyboardButton("🎯 Дартс")
        item9 = types.KeyboardButton("🔙 Вернуться в Функции")
        markup.row(item1)
        markup.row(item2) 
        markup.row(item3, item4, item5)
        markup.row(item6, item7, item8)
        markup.row(item9)
        bot.send_message(message.from_user.id, "🚩 Выберите игру", reply_markup = markup)
    else:
        bot.send_message(message.chat.id, "Вы проиграли!")
        sleep(2)
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton("🧾 Таблица лидеров")
        item2 = types.KeyboardButton("🎰 Угадай число")
        item3 = types.KeyboardButton("🎲 Игра *Кости*")
        item4 = types.KeyboardButton("🎳 Боулинг")
        item5 = types.KeyboardButton("⚽️ Футбол")
        item6 = types.KeyboardButton("🏀 Баскетбол")
        item7 = types.KeyboardButton("🟡 Орел & Решка")
        item8 = types.KeyboardButton("🎯 Дартс")
        item9 = types.KeyboardButton("🔙 Вернуться в Функции")
        markup.row(item1)
        markup.row(item2) 
        markup.row(item3, item4, item5)
        markup.row(item6, item7, item8)
        markup.row(item9)
        bot.send_message(message.from_user.id, "🚩 Выберите игру", reply_markup = markup) 



def dollar_rubl(message):
    dollar = 685468974538976564
    while dollar == 685468974538976564:
        try:
            dollar = int(message.text)
            result = int(dollar) * float(price_usd)
            bot.send_message(message.chat.id, "*Результат -* " + str('{:.2f}'.format(result)) + " *₽*", parse_mode = "Markdown")
        except Exception:
            bot.send_message(message.chat.id, "Нужно вводить цифрами.")
            break
    if dollar == 685468974538976564:
        bot.register_next_step_handler(message, dollar_rubl)

def rubl_dollar(message):
	rubl = 685468974538976564
	while rubl == 685468974538976564:
		try:
			rubl = int(message.text)
			result = int(rubl) / float(price_usd)
			bot.send_message(message.chat.id, "*Результат -* " + str('{:.2f}'.format(result)) + " *USD*", parse_mode = "Markdown")
		except Exception:
			bot.send_message(message.chat.id, "Нужно вводить цифрами.")
			break
	if rubl == 685468974538976564:
		bot.register_next_step_handler(message, rubl_dollar)
		

def euro_rubl(message):
	euro = 685468974538976564
	while euro == 685468974538976564:
		try:
			euro = int(message.text)
			result = int(euro) * float(price_euro)
			bot.send_message(message.chat.id, "*Результат -* " + str('{:.2f}'.format(result)) + " *₽*", parse_mode = "Markdown")
		except Exception:
			bot.send_message(message.chat.id, "Нужно вводить цифрами.")
			break
	if euro == 685468974538976564:
		bot.register_next_step_handler(message, euro_rubl)


def rubl_euro(message):
	rubl_two = 685468974538976564
	while rubl_two == 685468974538976564:
		try:
			rubl_two = int(message.text)
			result = int(rubl_two) / float(price_euro)
			bot.send_message(message.chat.id, "*Результат -* " + str('{:.2f}'.format(result)) + " *EURO*", parse_mode = "Markdown")
		except Exception:
			bot.send_message(message.chat.id, "Нужно вводить цифрами.")
			break
	if rubl_two == 685468974538976564:
		bot.register_next_step_handler(message, rubl_euro)


# ПРЕДЛОЖЕНИЯ И УЛУЧШЕНИЯ

def up_bot(message):
	global up_text
	up_text = message.text


	markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
	item1 = types.KeyboardButton("Все верно ✅")
	item2 = types.KeyboardButton("Хочу переписать 📄")
	item3 = types.KeyboardButton("Отмена ⛔️")
	markup.row(item1)
	markup.row(item2)
	markup.row(item3)

	bot.send_message(message.chat.id, "⏳ Формирование...")
	sleep(1)
	bot.send_message(message.chat.id, "⌛️ Формирование...")
	sleep(1)
	bot.send_message(message.chat.id, "Ваше сообщение сформировано. \n\n" + str(up_text), reply_markup = markup)


# УГАДАЙ ЧИСЛО

def number(message):
    global counter
    global random_number
    print("Загадано число - " + str(random_number))
    number_user = message.text

    if number_user.isdigit():
        if int(number_user) > 10:
            bot.send_message(message.from_user.id, "Введите число в диапазоне от 1 до 10")
            bot.register_next_step_handler(message, number)
        elif int(number_user) < 1:
            bot.send_message(message.from_user.id, "Введите число в диапазоне от 1 до 10")
            bot.register_next_step_handler(message, number)
        else:
            if int(number_user) == int(random_number): 
                id = message.from_user.id
                name = message.from_user.first_name
                cursor.execute(f"UPDATE users SET score = score + 1 WHERE id = {id}")
                cursor.execute(f"UPDATE date SET score = score + 1 WHERE id = {id}")
                cursor.execute(f"UPDATE date SET score_number = score_number + 1 WHERE id = {id}")
                db.commit()
            
            
                sleep(0.5)
                bot.send_message(message.chat.id, "Поздравляю, вы угадали число!")
                sleep(0.5)
                bot.send_message(message.chat.id, "Было загадано число - " + str(random_number))
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                item1 = types.KeyboardButton("Да)")
                item2 = types.KeyboardButton("Нет)")
                markup.row(item1)
                markup.row(item2)
                bot.send_message(message.chat.id, "Хотите сыграть еще?)", reply_markup = markup)
            
            elif counter > 1:
                counter -= 1
                sleep(0.5)
                bot.send_message(message.chat.id, "Неверно. Осталось попыток: " + str(counter))
                bot.register_next_step_handler(message, number)
                return
            else:
                sleep(0.5)
                bot.send_message(message.chat.id, "Увы, но вы не угадали число( ☹️")
                sleep(0.5)
                bot.send_message(message.chat.id, "Было загадано число - " + str(random_number))
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                item1 = types.KeyboardButton("Да)")
                item2 = types.KeyboardButton("Нет)")
                markup.row(item1)
                markup.row(item2)
                bot.send_message(message.chat.id, "Хотите сыграть еще?)", reply_markup = markup)
    else:
        bot.send_message(message.from_user.id, "Введите пожалуйста цифру!")
        bot.register_next_step_handler(message, number)


# ВИКИПЕДИЯ

def wiki(message):
	global search

	wikipedia.set_lang("RU")
	text = message.text

	search = wikipedia.search(text, results = 6)

	if len(search) == 0:
		bot.send_message(message.from_user.id, f"По запросу  *'{text}'*  ничего не найдено! ", parse_mode = "Markdown")

		markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
		item1 = types.KeyboardButton("📖 Вики")
		item2 = types.KeyboardButton("🔙 Вернуться в Функции")
		markup.row(item1)
		markup.row(item2)
		bot.send_message(message.from_user.id, "Хотите попробовать найти ваш запрос еще раз?", reply_markup= markup)

	else:
		for index, result in enumerate(search, start = 0):
			bot.send_message(message.from_user.id, f"{index}) {result}")

		markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
		item1 = types.KeyboardButton("0")
		item2 = types.KeyboardButton("1")
		item3 = types.KeyboardButton("2")
		item4 = types.KeyboardButton("3")
		item5 = types.KeyboardButton("4")
		item6 = types.KeyboardButton("5")
		markup.row(item1, item2)
		markup.row(item3, item4)
		markup.row(item5, item6)

		bot.send_message(message.from_user.id, "Выберите цифру запроса которого хотите узнать: ", reply_markup = markup)
		bot.register_next_step_handler(message, wiki_result)


def wiki_result(message):
	number = message.text

	try:
		number = int(message.text)
		if number < 0:
			bot.send_message(message.from_user.id, "Вы ввели неверный диапазон. \nВведите пожалуйста от 0 до 5")
			bot.register_next_step_handler(message, wiki_result)
		elif number > 5:
			bot.send_message(message.from_user.id, "Вы ввели неверный диапазон. \nВведите пожалуйста от 0 до 5")
			bot.register_next_step_handler(message, wiki_result)
		else:
			try:
				wikipedia.set_lang("RU")
				text = wikipedia.summary(search[int(number)])
				bot.send_message(message.from_user.id, str(text))
			except:
				bot.send_message(message.from_user.id, "Произошла ошибка, не удалось найти данный запрос!")

			sleep(2)

			markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
			item1 = types.KeyboardButton("📖 Вики")
			item2 = types.KeyboardButton("🔙 Вернуться в Функции")
			markup.row(item1)
			markup.row(item2)
			bot.send_message(message.from_user.id, "Хотите еще найти что-нибудь?", reply_markup= markup)


	except:
		bot.send_message(message.from_user.id, "Введите цифру пожалуйста!")
		bot.register_next_step_handler(message, wiki_result)








@server.route(f"/{BOT_TOKEN}", methods=["POST"])
def redirect_message():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))