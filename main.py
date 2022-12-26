# Code by: glinsky
# Made in December, 2022

import math, telebot, requests, time, random, wikipedia, qrcode

from telebot import types
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup
from pymongo import MongoClient

from database import *
from config import *

bot = telebot.TeleBot(BOT_TOKEN, parse_mode = None)

url = "https://mainfin.ru/currency/omsk"
request_get = requests.get(url)
soup = BeautifulSoup(request_get.text, "html.parser")
price_usd = soup.find("span", id="buy_usd").text
price_euro = soup.find("span", id="buy_eur").text

# Command - /start
@bot.message_handler(commands=['start'])
def start(message):
    global id, username, name, lastActive

    id = message.from_user.id
    username = message.from_user.username
    name = message.from_user.first_name
    lastActive = datetime.now()

    updateUser()

    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton("🧾 Таблица лидеров")
    item2 = types.KeyboardButton("💎 Функции")
    item3 = types.KeyboardButton("🛠 Прочее")
    markup.row(item1)
    markup.row(item2)
    markup.row(item3)
    bot.send_message(id, "Привет " + name + " 👋" +", чем я могу тебе помочь?", reply_markup = markup)

# Type - Text
@bot.message_handler(content_types = ["text"])
def bot_message(message):
    global id, username, name, lastActive

    id = message.from_user.id
    username = message.from_user.username
    name = message.from_user.first_name
    lastActive = datetime.now()

    if message.chat.type == "private":
        match message.text:
            case "🛠 Прочее":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
                item1 = types.KeyboardButton("📄 Информация")
                item2 = types.KeyboardButton("📝 Предложения и улучшения")
                item3 = types.KeyboardButton("📍 Вернуться в Главное меню")
                markup.row(item1)
                markup.row(item2)
                markup.row(item3)
                bot.send_message(id, "🚩 Выберите действие", reply_markup = markup)

                updateUser()

            case "📝 Предложения и улучшения":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
                item1 = types.KeyboardButton("Да ✅")
                item2 = types.KeyboardButton("Нет ⛔")
                markup.row(item1)
                markup.row(item2)
                bot.send_message(id, "Желаете оставить предложение по улучшению?", reply_markup = markup)

                updateUser()

            case "Да ✅":
                bot.send_message(id, "Напишите ваши улучшения в чат! ⤵️")
                bot.register_next_step_handler(message, up_bot)

                updateUser()   

            case "Нет ⛔":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
                item1 = types.KeyboardButton("📄 Информация")
                item2 = types.KeyboardButton("📝 Предложения и улучшения")
                item3 = types.KeyboardButton("📍 Вернуться в Главное меню")
                markup.row(item1)
                markup.row(item2)
                markup.row(item3)
                bot.send_message(id, "🚩 Выберите действие", reply_markup = markup)

                updateUser()

            case "📄 Информация":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                item1 = types.KeyboardButton("🆔 Узнать ID")
                item2 = types.KeyboardButton("📑 Информация о боте")
                item3 = types.KeyboardButton("🔙 Вернуться в Прочее")
                markup.row(item1)
                markup.row(item2)
                markup.row(item3)
                bot.send_message(id, "🚩 Выберите действие", reply_markup = markup)

                updateUser()

            case "📑 Информация о боте":
                bot.send_message(id, "Данный бот создан для удобства и практики) 🙂.\nПо всем вопросам - @disanaverno")
                
                updateUser()

            case "🔙 Вернуться в Информация":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                item1 = types.KeyboardButton("🆔 Узнать ID")
                item2 = types.KeyboardButton("📑 Информация о боте")
                item3 = types.KeyboardButton("🔙 Вернуться в Прочее")
                markup.row(item1)
                markup.row(item2)
                markup.row(item3)
                bot.send_message(id, "🚩 Выберите действие", reply_markup = markup)

                updateUser()

            case "🔙 Вернуться в Прочее":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
                item1 = types.KeyboardButton("📄 Информация")
                item2 = types.KeyboardButton("📝 Предложения и улучшения")
                item3 = types.KeyboardButton("📍 Вернуться в Главное меню")
                markup.row(item1)
                markup.row(item2)
                markup.row(item3)
                bot.send_message(id, "🚩 Выберите действие", reply_markup = markup)

                updateUser()

            case "🆔 Узнать ID":
                bot.send_message(id, "Ваш ID - " + str(id))

                updateUser()

            case "🧾 Таблица лидеров":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                item1 = types.KeyboardButton("🧾 Показать таблица лидеров")
                item2 = types.KeyboardButton("🧾 Подробная статистика игр")
                item3 = types.KeyboardButton("📍 Вернуться в Главное меню")
                markup.row(item1)
                markup.row(item2)
                markup.row(item3)
                bot.send_message(id, "🚩 Выберите действие", reply_markup = markup)

                updateUser()

            case "🧾 Показать таблица лидеров":
                allUsers = users.find().sort("score", -1)

                bot.send_message(id, "Таблица лидеров среди людей которые больше всего выйграли бота")
                bot.send_message(id, "№ | Участник | Кол-во игр | Кол-во побед")

                for index, user in enumerate(allUsers, start=1):
                    bot.send_message(id, str(index) + " | " + str(user["name"]) + " (@" + str(user["username"]) + ") | " + str(user["games"]) + " | " + str(user["score"]))
   
                    if index == 5:
                        break

            case "🧾 Подробная статистика игр":      
                bot.send_message(id, "Подробная статистика игр")

                statsUser = date.find_one({"id": id})

                # General
                if statsUser["games"] == 0 and statsUser["score"] == 0:
                    win_general = 0
                else:
                    win_general = statsUser["score"] / statsUser["games"] * 100

                # Darts
                if statsUser["games_darts"] == 0 and statsUser["score_darts"] == 0:
                    win_darts = 0
                else:
                    win_darts = statsUser["score_darts"] / statsUser["games_darts"] * 100
  
                # Number
                if statsUser["games_number"] == 0 and statsUser["score_number"] == 0:
                    win_number = 0
                else:
                    win_number = statsUser["score_number"] / statsUser["games_number"] * 100

                # Kosti
                if statsUser["games_kosti"] == 0 and statsUser["score_kosti"] == 0:
                    win_kosti = 0
                else:
                    win_kosti = statsUser["score_kosti"] / statsUser["games_kosti"] * 100

                # Bowling
                if statsUser["games_bowling"] == 0 and statsUser["score_bowling"] == 0:
                    win_bowling = 0
                else:
                    win_bowling = statsUser["score_bowling"] / statsUser["games_bowling"] * 100

                # Football
                if statsUser["games_football"] == 0 and statsUser["score_football"] == 0:
                    win_football = 0
                else:
                    win_football = statsUser["score_football"] / statsUser["games_football"] * 100

                # Basket
                if statsUser["games_basket"] == 0 and statsUser["score_basket"] == 0:
                    win_basket = 0
                else:
                    win_basket = statsUser["score_basket"] / statsUser["games_basket"] * 100

                # Moneta
                if statsUser["games_moneta"] == 0 and statsUser["score_moneta"] == 0:
                    win_moneta = 0
                else:
                    win_moneta = statsUser["score_moneta"] / statsUser["games_moneta"] * 100

                bot.send_message(id, "Название  |  Игр  |  Побед  | Winrate")
                bot.send_message(id, "🎈 Общее - " + str(statsUser["games"]) + " - " + str(statsUser["score"]) + " - " + f'{win_general:.0f}' + "%")
                bot.send_message(id, "🎯 Дартс - " + str(statsUser["games_darts"]) + " - " + str(statsUser["score_darts"]) + " - " + f'{win_darts:.0f}' + "%")
                bot.send_message(id, "🎰 Угадай число - " + str(statsUser["games_number"]) + " - " + str(statsUser["score_number"]) + " - " + f'{win_number:.0f}' + "%")
                bot.send_message(id, "🎲 Игра *Кости* - " + str(statsUser["games_kosti"]) + " - " + str(statsUser["score_kosti"]) + " - " + f'{win_kosti:.0f}' + "%")
                bot.send_message(id, "🎳 Боулинг - " + str(statsUser["games_bowling"]) + " - " + str(statsUser["score_bowling"]) + " - " + f'{win_bowling:.0f}' + "%")
                bot.send_message(id, "⚽️ Футбол - " + str(statsUser["games_football"]) + " - " + str(statsUser["score_football"]) + " - " + f'{win_football:.0f}' + "%")
                bot.send_message(id, "🏀 Баскетбол - " + str(statsUser["games_basket"]) + " - " + str(statsUser["score_basket"]) + " - " + f'{win_basket:.0f}' + "%")
                bot.send_message(id, "🟡 Орел & Решка - " + str(statsUser["games_moneta"]) + " - " + str(statsUser["score_moneta"]) + " - " + f'{win_moneta:.0f}' + "%")

            # Horoscope
            case "🔮 Гороскоп":	
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
                bot.send_message(id, "🚩 Выберите свой знак зодиака", reply_markup = markup)

                updateUser()	            
            
            case "Лев ♌️":
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
                bot.send_message(id, "Выберите день.", reply_markup = markup)

                updateUser()  

            case "Лев - сегодня":
                url = "https://horo.mail.ru/prediction/leo/today"
                request = requests.get(url)
                soup = BeautifulSoup(request.text, "html.parser")
                today = soup.find("span", class_="link__text").text
                tomorrow = soup.find("span", class_="link__text").text
                lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text         
                bot.send_message(id, today + " - *Лев* ♌️" +"\n\n" + lev, parse_mode = "Markdown")

                updateUser()

            case "Лев - завтра":
                url = "https://horo.mail.ru/prediction/leo/tomorrow"
                request = requests.get(url)
                soup = BeautifulSoup(request.text, "html.parser")
                today = soup.find("span", class_="link__text").text
                tomorrow = soup.find("span", class_="link__text").text
                lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text         
                bot.send_message(id, tomorrow + " - *Лев* ♌️" + "\n\n" + lev, parse_mode = "Markdown")

                updateUser()           
            
            case "Телец ♉️":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                item1 = types.KeyboardButton("Телец - сегодня")
                item2 = types.KeyboardButton("Телец - завтра")
                item3 = types.KeyboardButton("🔙 Назад")
                markup.row(item1)
                markup.row(item2)
                markup.row(item3)
                bot.send_message(id, "Выберите день.", reply_markup = markup)

                updateUser()     
            
            case "Телец - сегодня":
                url = "https://horo.mail.ru/prediction/taurus/today"
                request = requests.get(url)
                soup = BeautifulSoup(request.text, "html.parser")
                today = soup.find("span", class_="link__text").text
                tomorrow = soup.find("span", class_="link__text").text
                lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text         
                bot.send_message(id, today + " - *Телец* ♉️" +"\n\n" + lev, parse_mode = "Markdown")

                updateUser()       
            
            case "Телец - завтра":
                url = "https://horo.mail.ru/prediction/taurus/tomorrow"
                request = requests.get(url)
                soup = BeautifulSoup(request.text, "html.parser")
                today = soup.find("span", class_="link__text").text
                tomorrow = soup.find("span", class_="link__text").text
                lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text         
                bot.send_message(id, tomorrow + " - *Телец* ♉️" + "\n\n" + lev, parse_mode = "Markdown")

                updateUser()        
            
            case "Овен ♈️":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                item1 = types.KeyboardButton("Овен - сегодня")
                item2 = types.KeyboardButton("Овен - завтра")
                item3 = types.KeyboardButton("🔙 Назад")
                markup.row(item1)
                markup.row(item2)
                markup.row(item3)
                bot.send_message(id, "Выберите день.", reply_markup = markup)

                updateUser()

            case "Овен - сегодня":
                url = "https://horo.mail.ru/prediction/aries/today"
                request = requests.get(url)
                soup = BeautifulSoup(request.text, "html.parser")
                today = soup.find("span", class_="link__text").text
                tomorrow = soup.find("span", class_="link__text").text
                lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
                bot.send_message(id, today + " - *Овен* ♈️" +"\n\n" + lev, parse_mode = "Markdown")

                updateUser()      

            case "Овен - завтра":
                url = "https://horo.mail.ru/prediction/aries/tomorrow"
                request = requests.get(url)
                soup = BeautifulSoup(request.text, "html.parser")
                today = soup.find("span", class_="link__text").text
                tomorrow = soup.find("span", class_="link__text").text
                lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
                bot.send_message(id, tomorrow + " - *Овен* ♈️" + "\n\n" + lev, parse_mode = "Markdown")

                updateUser()     

            case "Близнецы ♊️":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                item1 = types.KeyboardButton("Близнецы - сегодня")
                item2 = types.KeyboardButton("Близнецы - завтра")
                item3 = types.KeyboardButton("🔙 Назад")
                markup.row(item1)
                markup.row(item2)
                markup.row(item3)
                bot.send_message(id, "Выберите день.", reply_markup = markup)

                updateUser() 

            case "Близнецы - сегодня":
                url = "https://horo.mail.ru/prediction/gemini/today"
                request = requests.get(url)
                soup = BeautifulSoup(request.text, "html.parser")
                today = soup.find("span", class_="link__text").text
                tomorrow = soup.find("span", class_="link__text").text
                lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
                bot.send_message(id, today + " - *Близнецы* ♊️" +"\n\n" + lev, parse_mode = "Markdown")

                updateUser()     

            case "Близнецы - завтра":
                url = "https://horo.mail.ru/prediction/gemini/tomorrow"
                request = requests.get(url)
                soup = BeautifulSoup(request.text, "html.parser")
                today = soup.find("span", class_="link__text").text
                tomorrow = soup.find("span", class_="link__text").text
                lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
                bot.send_message(id, tomorrow + " - *Близнецы* ♊️" + "\n\n" + lev, parse_mode = "Markdown")

                updateUser()      

            case "Рак ♋️":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                item1 = types.KeyboardButton("Рак - сегодня")
                item2 = types.KeyboardButton("Рак - завтра")
                item3 = types.KeyboardButton("🔙 Назад")
                markup.row(item1)
                markup.row(item2)
                markup.row(item3)
                bot.send_message(id, "Выберите день.", reply_markup = markup)

                updateUser()

            case "Рак - сегодня":
                url = "https://horo.mail.ru/prediction/cancer/today"
                request = requests.get(url)
                soup = BeautifulSoup(request.text, "html.parser")
                today = soup.find("span", class_="link__text").text
                tomorrow = soup.find("span", class_="link__text").text
                lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
                bot.send_message(id, today + " - *Рак* ♋️" +"\n\n" + lev, parse_mode = "Markdown")

                updateUser()       

            case "Рак - завтра":
                url = "https://horo.mail.ru/prediction/cancer/tomorrow"
                request = requests.get(url)
                soup = BeautifulSoup(request.text, "html.parser")
                today = soup.find("span", class_="link__text").text
                tomorrow = soup.find("span", class_="link__text").text
                lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
                bot.send_message(id, tomorrow + " - *Рак* ♋️" + "\n\n" + lev, parse_mode = "Markdown")

                updateUser()        

            case "Дева ♍️":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                item1 = types.KeyboardButton("Дева - сегодня")
                item2 = types.KeyboardButton("Дева - завтра")
                item3 = types.KeyboardButton("🔙 Назад")
                markup.row(item1)
                markup.row(item2)
                markup.row(item3)
                bot.send_message(id, "Выберите день.", reply_markup = markup)

                updateUser()

            case "Дева - сегодня":
                url = "https://horo.mail.ru/prediction/virgo/today"
                request = requests.get(url)
                soup = BeautifulSoup(request.text, "html.parser")
                today = soup.find("span", class_="link__text").text
                tomorrow = soup.find("span", class_="link__text").text
                lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
                bot.send_message(id, today + " - *Дева* ♍️" +"\n\n" + lev, parse_mode = "Markdown")

                updateUser()    

            case "Дева - завтра":
                url = "https://horo.mail.ru/prediction/virgo/tomorrow"
                request = requests.get(url)
                soup = BeautifulSoup(request.text, "html.parser")
                today = soup.find("span", class_="link__text").text
                tomorrow = soup.find("span", class_="link__text").text
                lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
                bot.send_message(id, tomorrow + " - *Дева* ♍️" + "\n\n" + lev, parse_mode = "Markdown")

                updateUser()      

            case "Весы ♎️":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                item1 = types.KeyboardButton("Весы - сегодня")
                item2 = types.KeyboardButton("Весы - завтра")
                item3 = types.KeyboardButton("🔙 Назад")
                markup.row(item1)
                markup.row(item2)
                markup.row(item3)
                bot.send_message(id, "Выберите день.", reply_markup = markup)

                updateUser() 

            case "Весы - сегодня":
                url = "https://horo.mail.ru/prediction/libra/today"
                request = requests.get(url)
                soup = BeautifulSoup(request.text, "html.parser")
                today = soup.find("span", class_="link__text").text
                tomorrow = soup.find("span", class_="link__text").text
                lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
                bot.send_message(id, today + " - *Весы* ♎️" +"\n\n" + lev, parse_mode = "Markdown")

                updateUser()     

            case "Весы - завтра":
                url = "https://horo.mail.ru/prediction/libra/tomorrow"
                request = requests.get(url)
                soup = BeautifulSoup(request.text, "html.parser")
                today = soup.find("span", class_="link__text").text
                tomorrow = soup.find("span", class_="link__text").text
                lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
                bot.send_message(id, tomorrow + " - *Весы* ♎️" + "\n\n" + lev, parse_mode = "Markdown")

                updateUser()       

            case "Скорпион ♏️":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                item1 = types.KeyboardButton("Скорпион - сегодня")
                item2 = types.KeyboardButton("Скорпион - завтра")
                item3 = types.KeyboardButton("🔙 Назад")
                markup.row(item1)
                markup.row(item2)
                markup.row(item3)
                bot.send_message(id, "Выберите день.", reply_markup = markup)

                updateUser()

            case "Скорпион - сегодня":
                url = "https://horo.mail.ru/prediction/scorpio/today"
                request = requests.get(url)
                soup = BeautifulSoup(request.text, "html.parser")
                today = soup.find("span", class_="link__text").text
                tomorrow = soup.find("span", class_="link__text").text
                lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
                bot.send_message(id, today + " - *Скорпион* ♏️" +"\n\n" + lev, parse_mode = "Markdown")

                updateUser()      

            case "Скорпион - завтра":
                url = "https://horo.mail.ru/prediction/scorpio/tomorrow"
                request = requests.get(url)
                soup = BeautifulSoup(request.text, "html.parser")
                today = soup.find("span", class_="link__text").text
                tomorrow = soup.find("span", class_="link__text").text
                lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
                bot.send_message(id, tomorrow + " - *Скорпион* ♏️" + "\n\n" + lev, parse_mode = "Markdown")

                updateUser()      

            case "Стрелец ♐️":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                item1 = types.KeyboardButton("Стрелец - сегодня")
                item2 = types.KeyboardButton("Стрелец - завтра")
                item3 = types.KeyboardButton("🔙 Назад")
                markup.row(item1)
                markup.row(item2)
                markup.row(item3)
                bot.send_message(id, "Выберите день.", reply_markup = markup)

                updateUser() 

            case "Стрелец - сегодня":
                url = "https://horo.mail.ru/prediction/sagittarius/today"
                request = requests.get(url)
                soup = BeautifulSoup(request.text, "html.parser")
                today = soup.find("span", class_="link__text").text
                tomorrow = soup.find("span", class_="link__text").text
                lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
                bot.send_message(id, today + " - *Стрелец* ♐️" +"\n\n" + lev, parse_mode = "Markdown")

                updateUser()       

            case "Стрелец - завтра":
                url = "https://horo.mail.ru/prediction/sagittarius/tomorrow"
                request = requests.get(url)
                soup = BeautifulSoup(request.text, "html.parser")
                today = soup.find("span", class_="link__text").text
                tomorrow = soup.find("span", class_="link__text").text
                lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
                bot.send_message(id, tomorrow + " - *Стрелец* ♐️" + "\n\n" + lev, parse_mode = "Markdown")        

                updateUser()

            case "Козерог ♑️":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                item1 = types.KeyboardButton("Козерог - сегодня")
                item2 = types.KeyboardButton("Козерог - завтра")
                item3 = types.KeyboardButton("🔙 Назад")
                markup.row(item1)
                markup.row(item2)
                markup.row(item3)
                bot.send_message(id, "Выберите день.", reply_markup = markup)

                updateUser()   

            case "Козерог - сегодня":
                url = "https://horo.mail.ru/prediction/capricorn/today"
                request = requests.get(url)
                soup = BeautifulSoup(request.text, "html.parser")
                today = soup.find("span", class_="link__text").text
                tomorrow = soup.find("span", class_="link__text").text
                lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
                bot.send_message(id, today + " - *Козерог* ♑️" +"\n\n" + lev, parse_mode = "Markdown")

                updateUser()        

            case "Козерог - завтра":
                url = "https://horo.mail.ru/prediction/capricorn/tomorrow"
                request = requests.get(url)
                soup = BeautifulSoup(request.text, "html.parser")
                today = soup.find("span", class_="link__text").text
                tomorrow = soup.find("span", class_="link__text").text
                lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
                bot.send_message(id, tomorrow + " - *Козерог* ♑️" + "\n\n" + lev, parse_mode = "Markdown")

                updateUser()        

            case "Водолей ♒️":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                item1 = types.KeyboardButton("Водолей - сегодня")
                item2 = types.KeyboardButton("Водолей - завтра")
                item3 = types.KeyboardButton("🔙 Назад")
                markup.row(item1)
                markup.row(item2)
                markup.row(item3)
                bot.send_message(id, "Выберите день.", reply_markup = markup)

                updateUser()  

            case "Водолей - сегодня":
                url = "https://horo.mail.ru/prediction/aquarius/today"
                request = requests.get(url)
                soup = BeautifulSoup(request.text, "html.parser")
                today = soup.find("span", class_="link__text").text
                tomorrow = soup.find("span", class_="link__text").text
                lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
                bot.send_message(id, today + " - *Водолей* ♒️" +"\n\n" + lev, parse_mode = "Markdown")

                updateUser()       

            case "Водолей - завтра":
                url = "https://horo.mail.ru/prediction/aquarius/tomorrow"
                request = requests.get(url)
                soup = BeautifulSoup(request.text, "html.parser")
                today = soup.find("span", class_="link__text").text
                tomorrow = soup.find("span", class_="link__text").text
                lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
                bot.send_message(id, tomorrow + " - *Водолей* ♒️" + "\n\n" + lev, parse_mode = "Markdown")

                updateUser()        

            case "Рыбы ♓️":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                item1 = types.KeyboardButton("Рыбы - сегодня")
                item2 = types.KeyboardButton("Рыбы - завтра")
                item3 = types.KeyboardButton("🔙 Назад")
                markup.row(item1)
                markup.row(item2)
                markup.row(item3)
                bot.send_message(id, "Выберите день.", reply_markup = markup)

                updateUser()  

            case "Рыбы - сегодня":
                url = "https://horo.mail.ru/prediction/pisces/today"
                request = requests.get(url)
                soup = BeautifulSoup(request.text, "html.parser")
                today = soup.find("span", class_="link__text").text
                tomorrow = soup.find("span", class_="link__text").text
                lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
                bot.send_message(id, today + " - *Рыбы* ♓️" +"\n\n" + lev, parse_mode = "Markdown")

                updateUser()     

            case "Рыбы - завтра":
                url = "https://horo.mail.ru/prediction/pisces/tomorrow"
                request = requests.get(url)
                soup = BeautifulSoup(request.text, "html.parser")
                today = soup.find("span", class_="link__text").text
                tomorrow = soup.find("span", class_="link__text").text
                lev = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text     
                bot.send_message(id, tomorrow + " - *Рыбы* ♓️" + "\n\n" + lev, parse_mode = "Markdown")

                updateUser()																		                    
            
            case "🔙 Назад":
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
                bot.send_message(id, "🚩 Выберите свой знак зодиака", reply_markup = markup)

                updateUser()			        
        
        # ФУНКЦИИ       
            case "💎 Функции":
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
                bot.send_message(id, "🚩 Выберите действие", reply_markup = markup)

                updateUser()
          
            case "🔙 Вернуться в Функции":          
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
                bot.send_message(id, "🚩 Выберите действие", reply_markup = markup)

                updateUser()                
            
            case "📖 Вики":
                bot.send_message(id, "Введите ваш запрос: ")
                bot.register_next_step_handler(message, wiki)

                updateUser()
          
            case "📍 Вернуться в Главное меню":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                item1 = types.KeyboardButton("🧾 Таблица лидеров")
                item2 = types.KeyboardButton("💎 Функции")
                item3 = types.KeyboardButton("🛠 Прочее")
                markup.row(item1)
                markup.row(item2)
                markup.row(item3)
                bot.send_message(id,  str(name) + ", чем я могу тебе помочь?", reply_markup = markup)

                updateUser()   
          
            # КУРС ВАЛЮТ        
            case "💰 Курс валют":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                item1 = types.KeyboardButton("📈 Курс валют")
                item2 = types.KeyboardButton("🔁 Перевести")
                item3 = types.KeyboardButton("🔙 Вернуться в Функции")
                markup.row(item1, item2)
                markup.row(item3)
                bot.send_message(id, "🚩 Выберите действие", reply_markup = markup)

                updateUser()      
          
            case "📈 Курс валют":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                item1 = types.KeyboardButton("💵 Доллар")
                item2 = types.KeyboardButton("💶 Евро")
                item3 = types.KeyboardButton("🔙 Вернуться в Курс Валют")
                markup.row(item1, item2)
                markup.row(item3)
                bot.send_message(id, "Выберите валюту 💵 💶", reply_markup = markup)

                updateUser()    
          
            case "💵 Доллар":
                bot.send_message(id, "💵 Доллар на данный момент - " + price_usd + " ₽")

                updateUser()
          
            case "💶 Евро":
                bot.send_message(id, "💶 Евро на данный момент - " + price_euro + " ₽")

                updateUser()     
          
            case "🔁 Перевести":	
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                item1 = types.KeyboardButton("💴 Рубли в 💵 Доллар")
                item2 = types.KeyboardButton("💴 Рубли в 💶 Евро")
                item3 = types.KeyboardButton("💵 Доллар в 💴 Рубли")
                item4 = types.KeyboardButton("💶 Евро в 💴 Рубли")
                item5 = types.KeyboardButton("🔙 Вернуться в Курс Валют")
                markup.row(item1, item3)
                markup.row(item2, item4)
                markup.row(item5)
                bot.send_message(id, "🚩 Выберите действие", reply_markup = markup)

                updateUser()      
          
            case "🔙 Вернуться в Курс Валют":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                item1 = types.KeyboardButton("📈 Курс валют")
                item2 = types.KeyboardButton("🔁 Перевести")
                item3 = types.KeyboardButton("🔙 Вернуться в Функции")
                markup.row(item1, item2)
                markup.row(item3)
                bot.send_message(id, "🚩 Выберите действие", reply_markup = markup)

                updateUser()      
          
            case "💴 Рубли в 💵 Доллар":
                bot.send_message(id, "Введите кол-во которое хотите перевести\n" + price_usd + " ₽" + " = 1 USD")
                bot.register_next_step_handler(message, rubl_dollar)

                updateUser()      
          
            case "💴 Рубли в 💶 Евро":
                bot.send_message(id, "Введите кол-во которое хотите перевести\n" + price_euro + " ₽" + " = 1 EURO")
                bot.register_next_step_handler(message, rubl_euro)

                updateUser()
          
            case "💵 Доллар в 💴 Рубли":
                bot.send_message(id, "Введите кол-во которое хотите перевести\n1 USD = " + price_usd + " ₽")
                bot.register_next_step_handler(message, dollar_rubl)

                updateUser()
          
            case "💶 Евро в 💴 Рубли":
                bot.send_message(id, "Введите кол-во которое хотите перевести\n1 EURO = " + price_euro + " ₽")
                bot.register_next_step_handler(message, euro_rubl)

                updateUser()
          
            # ПОГОДА        
            case "🌍 Погода":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                item1 = types.KeyboardButton("🌍 Омск")
                item2 = types.KeyboardButton("🌍 Москва")
                item3 = types.KeyboardButton("🌍 Новосибирск")
                item4 = types.KeyboardButton("🔙 Вернуться в Функции")
                markup.row(item1)
                markup.row(item2)
                markup.row(item3)
                markup.row(item4)
                bot.send_message(id, "В каком городе хотите узнать погоду?", reply_markup = markup)        
          
                updateUser()

            # ОМСК      
            case "🌍 Омск":
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
                bot.send_message(id, "Погода в Омске\n" + time + "\n\nТемпература:  " + str(temp) + " - " + str(note) + "\n" + str(feelslike) + "\n" + str(precipitation) + "\n" + str(pressure) + "\n" + str(humidity) + "\nВосход - " + str(sunrise_time) + "\nЗакат - " + str(sunset_time))     
          
                updateUser()

            # МОСКВА        
            case "🌍 Москва":
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
                bot.send_message(id, "Погода в Москве\n" + time + "\n\nТемпература:  " + str(temp) + " - " + str(note) + "\n" + str(feelslike) + "\n" + str(precipitation) + "\n" + str(pressure) + "\n" + str(humidity) + "\nВосход - " + str(sunrise_time) + "\nЗакат - " + str(sunset_time))        
          
                updateUser()

            # НОВОСИБИРСК       
            case "🌍 Новосибирск":
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
                bot.send_message(id, "Погода в Новосибирске\n" + time + "\n\nТемпература:  " + str(temp) + " - " + str(note) + "\n" + str(feelslike) + "\n" + str(precipitation) + "\n" + str(pressure) + "\n" + str(humidity) + "\nВосход - " + str(sunrise_time) + "\nЗакат - " + str(sunset_time))      
          
                updateUser()

            # РАНДОМНОЕ ЧИСЛО       
            case "🎰 Рандомное число":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                item1 = types.KeyboardButton("🎲 От 0 до 10")
                item2 = types.KeyboardButton("🎲 От 0 до 100")
                item3 = types.KeyboardButton("🎲 От 0 до 1000")
                item5 = types.KeyboardButton("🔙 Вернуться в Функции")
                markup.row(item1)
                markup.row(item2)
                markup.row(item3)
                markup.row(item4)
                markup.row(item5)
                bot.send_message(id, "🚩 Выберите диапазон", reply_markup = markup)

                updateUser()      
          
            case "🎲 От 0 до 10":
                bot.send_message(id, "*Вам выпало число -* " + str(random.randint(0,10)), parse_mode = "Markdown")     

                updateUser()

            case "🎲 От 0 до 100":
                bot.send_message(id, "*Вам выпало число -* " + str(random.randint(0,100)), parse_mode = "Markdown")        
          
                updateUser()

            case "🎲 От 0 до 1000":
                bot.send_message(id, "*Вам выпало число -* " + str(random.randint(0,1000)), parse_mode = "Markdown")       
          
                updateUser()

            # СЫГРАТЬ С БОТОМ
            case "🎡 Сыграть с ботом":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                item1 = types.KeyboardButton("🎰 Угадай число")
                item2 = types.KeyboardButton("🎲 Игра *Кости*")
                item3 = types.KeyboardButton("🎳 Боулинг")
                item4 = types.KeyboardButton("⚽️ Футбол")
                item5 = types.KeyboardButton("🏀 Баскетбол")
                item6 = types.KeyboardButton("🟡 Орел & Решка")
                item7 = types.KeyboardButton("🎯 Дартс")
                item8 = types.KeyboardButton("🔙 Вернуться в Функции")
                markup.row(item1)
                markup.row(item2, item3, item4)
                markup.row(item5, item6, item7)
                markup.row(item8)
                bot.send_message(id, "🚩 Выберите игру", reply_markup = markup)

                updateUser()    
          
            case "🔙 Вернуться назад":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                item1 = types.KeyboardButton("🎰 Угадай число")
                item2 = types.KeyboardButton("🎲 Игра *Кости*")
                item3 = types.KeyboardButton("🎳 Боулинг")
                item4 = types.KeyboardButton("⚽️ Футбол")
                item5 = types.KeyboardButton("🏀 Баскетбол")
                item6 = types.KeyboardButton("🟡 Орел & Решка")
                item7 = types.KeyboardButton("🎯 Дартс")
                item8 = types.KeyboardButton("🔙 Вернуться в Функции")
                markup.row(item1) 
                markup.row(item2, item3, item4)
                markup.row(item5, item6, item7)
                markup.row(item8)
                bot.send_message(id, "🚩 Выберите игру", reply_markup = markup)

                updateUser()
          
            # ОРЕЛ & РЕШКА      
            case "🟡 Орел & Решка": 
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                item1 = types.KeyboardButton("Орел")
                item2 = types.KeyboardButton("Решка")
                markup.row(item1)
                markup.row(item2)
                bot.send_message(id, "Орел или Решка ?" , reply_markup = markup)			
                bot.register_next_step_handler(message, moneta)

                updateUser()
          
            # ДАРТС     
            case "🎯 Дартс":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
                item1 = types.KeyboardButton("Бросить дротик 🎯")
                item2 = types.KeyboardButton("🔙 Вернуться назад")
                markup.row(item1)
                markup.row(item2)
                bot.send_message(id, "🎯 Кидает дротик - " + str(name) , reply_markup = markup)

                updateUser()      
          
            case "Бросить дротик 🎯":
                users.update_one(
                    {"id": id},
                    {"$inc": {"games": 1}}
                )

                date.update_one(
                    {"id": id},
                    {"$inc": {"games": 1, "games_darts": 1}}
                )

                ball = bot.send_dice(id, '🎯')
                sleep(5)    

                match ball.dice.value:
                    case 1:
                        bot.send_message(id, "Игрок " + str(name) + " не попал")
                    case 2 | 3 | 4 | 5:
                        bot.send_message(id, "Игрок " + str(name) + " попал в " + str(ball.dice.value))
                    case 6:
                        bot.send_message(id, "Игрок " + str(name) + " попал в яблочко!")  

                sleep(0.5)
                bot.send_message(id, "🎯 Кидает дротик БОТ")
                sleep(1.5)
                ball_two = bot.send_dice(id, '🎯')
                sleep(5)         

                match ball_two.dice.value:
                    case 1:
                        bot.send_message(id, "БОТ не попал")
                    case 2 | 3 | 4 | 5:
                        bot.send_message(id, "БОТ попал в " + str(ball_two.dice.value))
                    case 6:
                        bot.send_message(id, "БОТ попал в яблочко!")   
       
                sleep(0.5)
                bot.send_message(id, "⏳ Идет подсчет результатов...")
                sleep(0.5)
                bot.send_message(id, "⌛️ Идет подсчет результатов...")
                sleep(0.5)

                if ball.dice.value > ball_two.dice.value:
                    users.update_one(
                        {"id": id},
                        {"$inc": {"score": 1}}
                    )

                    date.update_one(
                        {"id": id},
                        {"$inc": {"score": 1, "score_darts": 1}}
                    )

                    bot.send_message(id, "*Победил - *" + str(name), parse_mode = "Markdown")
                    bot.send_message(id, "🥳")
                elif ball.dice.value == ball_two.dice.value:
                    bot.send_message(id, "*Ничья!*", parse_mode = "Markdown")
                    bot.send_message(id, "🤷‍♂")
                else:
                    bot.send_message(id, "😑 *Победил БОТ*", parse_mode = "Markdown")
                    bot.send_message(id, "😞")

                sleep(2)

                markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
                item1 = types.KeyboardButton("Бросить дротик 🎯")
                item2 = types.KeyboardButton("🔙 Вернуться назад")
                markup.row(item1)
                markup.row(item2)
                bot.send_message(id, "Сыграете еще раз?" , reply_markup = markup)
                
                updateUser() 
          
            # БАСКЕТБОЛ     
            case "🏀 Баскетбол":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
                item1 = types.KeyboardButton("Кинуть мяч 🏀")
                item2 = types.KeyboardButton("🔙 Вернуться назад")
                markup.row(item1)
                markup.row(item2)
                bot.send_message(id, "🏀 Кидает мяч - " + str(name) , reply_markup = markup)

                updateUser()     
          
            case "Кинуть мяч 🏀":
                users.update_one(
                    {"id": id},
                    {"$inc": {"games": 1}}
                )

                date.update_one(
                    {"id": id},
                    {"$inc": {"games": 1, "games_basket": 1}}
                )

                ball = bot.send_dice(id, '🏀')
                sleep(5)  

                if ball.dice.value > 3:
                    name = message.from_user.first_name
                    bot.send_message(id, "Игрок " + str(name) + " попал в кольцо, и он получает оценку " + str(ball.dice.value))
                    sleep(1.5)
                else:
                    bot.send_message(id, "Игрок " + str(name) + " промахнулся")

                bot.send_message(id, "🏀 Кидает мяч БОТ")
                sleep(1.5)
                ball_two = bot.send_dice(id, '🏀')
                sleep(5)     

                if ball_two.dice.value > 3:
                    bot.send_message(id, "БОТ попал в кольцо, и он получает оценку " + str(ball_two.dice.value))
                    sleep(1.5)
                else:
                    bot.send_message(id, "БОТ промахнулся")

                bot.send_message(id, "⏳ Идет подсчет результатов...")
                sleep(1.5)
                bot.send_message(id, "⌛️ Идет подсчет результатов...")
          
                if ball.dice.value > 3:
                    if ball_two.dice.value > 3:
                        if ball.dice.value > ball_two.dice.value:
                            users.update_one(
                                {"id": id},
                                {"$inc": {"score": 1}}
                            )

                            date.update_one(
                                {"id": id},
                                {"$inc": {"score": 1, "score_basket": 1}}
                            )

                            bot.send_message(id, "*Победил - *" + str(name), parse_mode = "Markdown")
                            bot.send_message(id, "🥳")
                        elif ball.dice.value == ball_two.dice.value:
                            bot.send_message(id, "*Ничья!*", parse_mode = "Markdown")
                            bot.send_message(id, "🤷‍♂")
                        else:
                            bot.send_message(id, "😑 *Победил БОТ*", parse_mode = "Markdown")
                            bot.send_message(id, "😞")
                    else:
                        users.update_one(
                            {"id": id},
                            {"$inc": {"score": 1}}
                        )

                        date.update_one(
                            {"id": id},
                            {"$inc": {"score": 1, "score_basket": 1}}
                        )

                        bot.send_message(id, "*Победил - *" + str(name), parse_mode="Markdown")
                        bot.send_message(id, "🥳")
                elif ball.dice.value < 3:
                    if ball_two.dice.value > 3:
                        bot.send_message(id, "😑 *Победил БОТ*", parse_mode = "Markdown")
                        bot.send_message(id, "😞")
                    else:
                        bot.send_message(id, "Никто не попал. Ничья!")
                        bot.send_message(id, "🤷‍♂")
                else:
                    bot.send_message(id, "Никто не попал. Ничья!")
                    bot.send_message(id, "🤷‍♂")    

                sleep(1)
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
                item1 = types.KeyboardButton("Кинуть мяч 🏀")
                item2 = types.KeyboardButton("🔙 Вернуться назад")
                markup.row(item1)
                markup.row(item2)
                bot.send_message(id, "Сыграете еще раз?" , reply_markup = markup)

                updateUser()      
          
            # ФУТБОЛ        
            case "⚽️ Футбол":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
                item1 = types.KeyboardButton("Пнуть мяч ⚽️")
                item2 = types.KeyboardButton("🔙 Вернуться назад")
                markup.row(item1)
                markup.row(item2)
                bot.send_message(id, "⚽️ Пинает мяч - " + str(name) , reply_markup = markup)

                updateUser()      
          
            case "Пнуть мяч ⚽️":
                users.update_one(
                    {"id": id},
                    {"$inc": {"games": 1}}
                )

                date.update_one(
                    {"id": id},
                    {"$inc": {"games": 1, "games_football": 1}}
                )

                ball = bot.send_dice(id, '⚽️')
                sleep(5)         

                if ball.dice.value > 2:
                    bot.send_message(id, "Игрок " + str(name) + " попал в ворота, и он получает оценку " + str(ball.dice.value))
                    sleep(1.5)
                else:
                    bot.send_message(id, "Игрок " + str(name) + " промахнулся")
                    sleep(1.5)

                bot.send_message(id, "⚽️ Пинает мяч БОТ")
                sleep(1.5)
                ball_two = bot.send_dice(id, '⚽️')
                sleep(5)
          
                if ball_two.dice.value > 2:
                    bot.send_message(id, "БОТ попал в ворота, и он получает оценку " + str(ball_two.dice.value))
                    sleep(1.5)
                else:
                    bot.send_message(id, "БОТ промахнулся")

                sleep(0.5)
                bot.send_message(id, "⏳ Идет подсчет результатов...")
                sleep(0.5)
                bot.send_message(id, "⌛️ Идет подсчет результатов...")
                sleep(0.5)  

                if ball.dice.value > 2:
                    if ball_two.dice.value > 2:
                        if ball.dice.value > ball_two.dice.value:
                            users.update_one(
                                {"id": id},
                                {"$inc": {"score": 1}}
                            )

                            date.update_one(
                                {"id": id},
                                {"$inc": {"score": 1, "score_football": 1}}
                            )

                            bot.send_message(id, "*Победил - *" + str(name) , parse_mode = "Markdown")
                            bot.send_message(id, "🥳")
                        elif ball.dice.value == ball_two.dice.value:
                            bot.send_message(id, "*Ничья!*", parse_mode = "Markdown")
                            bot.send_message(id, "🤷‍♂")
                        else:
                            bot.send_message(id, "😑 *Победил БОТ*", parse_mode = "Markdown")
                            bot.send_message(id, "😞")
                    else:
                        users.update_one(
                            {"id": id},
                            {"$inc": {"score": 1}}
                        )

                        date.update_one(
                            {"id": id},
                            {"$inc": {"score": 1, "score_football": 1}}
                        )

                        bot.send_message(id, "*Победил - *" + str(name), parse_mode = "Markdown")
                        bot.send_message(id, "🥳")
                elif ball.dice.value < 2:
                    if ball_two.dice.value > 2:
                        bot.send_message(id, "😑 *Победил БОТ*", parse_mode = "Markdown")
                        bot.send_message(id, "😞")
                    else:
                        bot.send_message(id, "Никто не попал. Ничья!")
                        bot.send_message(id, "🤷‍♂")
                else:
                    bot.send_message(id, "Никто не попал. Ничья!")
                    bot.send_message(id, "🤷‍♂")

                sleep(1.5)

                markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
                item1 = types.KeyboardButton("Пнуть мяч ⚽️")
                item2 = types.KeyboardButton("🔙 Вернуться назад")
                markup.row(item1)
                markup.row(item2)
                bot.send_message(id, "Сыграете еще раз?" , reply_markup = markup)

                updateUser()   
          
            # ИГРА "БОУЛИНГ"        
            case "🎳 Боулинг":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
                item1 = types.KeyboardButton("Бросить шар 🎳")
                item2 = types.KeyboardButton("🔙 Вернуться назад")
                markup.row(item1)
                markup.row(item2)
                bot.send_message(id, "🎳 Бросает шар - " + str(name) , reply_markup = markup)     
          
                updateUser()

            case "Бросить шар 🎳":
                users.update_one(
                    {"id": id},
                    {"$inc": {"games": 1}}
                )

                date.update_one(
                    {"id": id},
                    {"$inc": {"games": 1, "games_bowling": 1}}
                )

                ball = bot.send_dice(id, '🎳')
                sleep(5)

                match ball.dice.value:
                    case 1:
                        bot.send_message(id, "Игрок " + str(name) + " промахнулся")
                    case 2:
                        bot.send_message(id, "Игрок " + str(name) + " сбил 1 кеглю")
                    case 3 | 4:
                        bot.send_message(id, "Игрок " + str(name) + " сбил " + str(ball.dice.value) + " кегли")
                    case 5:
                        bot.send_message(id, "Игрок " + str(name) + " сбил " + str(ball.dice.value) + " кеглей")
                    case 6:
                        bot.send_message(id, "Игрок " + str(name) + " выбил STRIKE!!") 
           
                sleep(1.5)
                bot.send_message(id, "🎳 Бросает шар БОТ")
                sleep(1.5)
                ball_two = bot.send_dice(id, '🎳')
                sleep(5)

                match ball_two.dice.value:
                    case 1:
                        bot.send_message(id, "БОТ промахнулся")
                    case 2:
                        bot.send_message(id, "БОТ сбил 1 кеглю")
                    case 3 | 4:
                        bot.send_message(id, "БОТ сбил " + str(ball_two.dice.value) + " кегли")
                    case 5:
                        bot.send_message(id, "БОТ сбил " + str(ball_two.dice.value) + " кеглей")
                    case 6:
                        bot.send_message(id, "БОТ выбил STRIKE!!")

                sleep(1)
                bot.send_message(id, "⏳ Идет подсчет результатов...")
                sleep(1)
                bot.send_message(id, "⌛️ Идет подсчет результатов...")
                sleep(0.5)

                if ball.dice.value > ball_two.dice.value:
                    users.update_one(
                        {"id": id},
                        {"$inc": {"score": 1}}
                    )

                    date.update_one(
                        {"id": id},
                        {"$inc": {"score": 1, "score_bowling": 1}}
                    )

                    bot.send_message(id, "*Победил - *" + str(name), parse_mode = "Markdown")
                    bot.send_message(id, "🥳")
                elif ball.dice.value == ball_two.dice.value:
                    bot.send_message(id, "*Ничья!*", parse_mode = "Markdown")
                    bot.send_message(id, "🤷‍♂")
                else:
                    bot.send_message(id, "😑 *Победил БОТ*", parse_mode = "Markdown")
                    bot.send_message(id, "😞")     
              
                sleep(2)

                markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
                item1 = types.KeyboardButton("Бросить шар 🎳")
                item2 = types.KeyboardButton("🔙 Вернуться назад")
                markup.row(item1)
                markup.row(item2)
                bot.send_message(id, "Сыграете еще раз?" , reply_markup = markup)

                updateUser()
          
            # ИГРА *КОСТИ*      
            case "🎲 Игра *Кости*":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
                item1 = types.KeyboardButton("Бросить кубик 🎲")
                item2 = types.KeyboardButton("🔙 Вернуться назад")
                markup.row(item1)
                markup.row(item2)
                bot.send_message(id, "🎲 Бросает кубик - " + str(name) , reply_markup = markup)

                updateUser()     
          
            case "Бросить кубик 🎲":
                users.update_one(
                    {"id": id},
                    {"$inc": {"games": 1}}
                )

                date.update_one(
                    {"id": id},
                    {"$inc": {"games": 1, "games_kosti": 1}}
                )

                cube = bot.send_dice(id)
                sleep(5)
                bot.send_message(id, "Игроку " + str(name) + " выпало число - " + str(cube.dice.value))
                sleep(1.5)
                bot.send_message(id, "🎲 Бросает кубик БОТ")
                sleep(1.5)

                cube_two = bot.send_dice(id)
                sleep(5)
                bot.send_message(id, "БОТ выбил число - " + str(cube_two.dice.value))
                sleep(1)
                bot.send_message(id, "⏳ Идет подсчет результатов...")
                sleep(1)
                bot.send_message(id, "⌛️ Идет подсчет результатов...")
                sleep(2)        
              
                if cube.dice.value > cube_two.dice.value:
                    users.update_one(
                        {"id": id},
                        {"$inc": {"score": 1}}
                    )

                    date.update_one(
                        {"id": id},
                        {"$inc": {"score": 1, "score_kosti": 1}}
                    )

                    bot.send_message(id, "*Победил - *" + str(name), parse_mode = "Markdown")
                    bot.send_message(id, "🥳")
                elif cube.dice.value == cube_two.dice.value:
                    bot.send_message(id, "*Ничья!*", parse_mode = "Markdown")
                    bot.send_message(id, "🤷‍♂")
                else:
                    bot.send_message(id, "*Победил БОТ*", parse_mode = "Markdown")
                    bot.send_message(id, "😞")     
              
                sleep(1)

                markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
                item1 = types.KeyboardButton("Бросить кубик 🎲")
                item2 = types.KeyboardButton("🔙 Вернуться назад")
                markup.row(item1)
                markup.row(item2)
                bot.send_message(id, "Сыграете еще раз?" , reply_markup = markup)

                updateUser()
          
            # УГАДАЙ ЧИСЛО      
            case "🎰 Угадай число":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
                item1 = types.KeyboardButton("Да")
                item2 = types.KeyboardButton("Нет")
                markup.row(item1)
                markup.row(item2)
                bot.send_message(id, "Хотите сыграть с ботом в Угадай число?\nПравила игры максимально просты.\nБот загадывает число от 1 до 10, а вам нужно угадать это число, у вас будет 5 попыток", reply_markup = markup )        
          
                updateUser()

            case "Да":
                global counter, random_number

                users.update_one(
                    {"id": id},
                    {"$inc": {"games": 1}}
                )

                date.update_one(
                    {"id": id},
                    {"$inc": {"games": 1, "games_number": 1}}
                )

                sleep(0.5)
                bot.send_message(id, "Отлично. Тогда начнем")
                sleep(0.5)
                bot.send_message(id, "Бот загадал число. У вас 5 попыток!")        
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
                bot.send_message(id, "Выберите число", reply_markup = markup)
                bot.register_next_step_handler(message, number)

                updateUser()

            case "Нет":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                item1 = types.KeyboardButton("🎰 Угадай число")
                item2 = types.KeyboardButton("🎲 Игра *Кости*")
                item3 = types.KeyboardButton("🎳 Боулинг")
                item4 = types.KeyboardButton("⚽️ Футбол")
                item5 = types.KeyboardButton("🏀 Баскетбол")
                item6 = types.KeyboardButton("🟡 Орел & Решка")
                item7 = types.KeyboardButton("🎯 Дартс")
                item8 = types.KeyboardButton("🔙 Вернуться в Функции")
                markup.row(item1) 
                markup.row(item2, item3, item4)
                markup.row(item5, item6, item7)
                markup.row(item8)
                bot.send_message(id, "🚩 Выберите игру", reply_markup = markup)

                updateUser()       
          
            # ОТЧЕТ О ДОСТАВКЕ СООБЩЕНИЯ "ПРЕДЛОЖЕНИЯ И УЛУЧШЕНИЯ"      
            case "Все верно ✅":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
                item1 = types.KeyboardButton("📍 Вернуться в Главное меню")
                markup.row(item1)
                bot.send_message(id, "Успешно! Ваше сообщение доставлено!  📦", reply_markup = markup)
                chat_id = "1277445345"
                bot.send_message(chat_id, "Предложение по улучшения от " + str(name) + " (@" + str(username) + " ) " + "\n\n" + up_text, reply_markup = markup)       
          
                updateUser()

            case "Хочу переписать 📄":
                bot.send_message(id, "Напишите ваши улучшения в чат! ⤵️")
                bot.register_next_step_handler(message, up_bot)

                updateUser()
          
            case "Отмена ⛔️":
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
                item1 = types.KeyboardButton("📄 Информация")
                item2 = types.KeyboardButton("📝 Предложения и улучшения")
                item3 = types.KeyboardButton("📍 Вернуться в Главное меню")
                markup.row(item1)
                markup.row(item2)
                markup.row(item3)
                bot.send_message(id, "🚩 Выберите действие", reply_markup = markup)

                updateUser()            

            case _:
                bot.send_message(id, "🗿 Я тебя не понимаю. Напиши /start")

                updateUser()

def updateUser():
    users.update_one(
        {"id": id},
        {"$set": {"lastActive": str(lastActive)}}
    )

    checkID = users.find_one({"id": id})

    if not checkID:
        users.insert_one({
            "id" : id,
            "username" : username,
            "name" : name,
            "lastActive": str(lastActive),
            "games" : 0,
            "score": 0
        })

        date.insert_one({
            "id": id,
            "games": 0,
            "score": 0,

            "games_darts": 0,
            "score_darts": 0,

            "games_number": 0,
            "score_number": 0,

            "games_kosti": 0,
            "score_kosti": 0,

            "games_bowling": 0,
            "score_bowling": 0,

            "games_football": 0,
            "score_football": 0,

            "games_basket": 0,
            "score_basket": 0,

            "games_moneta": 0,
            "score_moneta": 0,
        })

def moneta(message):
    users.update_one(
        {"id": id},
        {"$inc": {"games": 1}}
    )

    date.update_one(
        {"id": id},
        {"$inc": {"games": 1, "games_moneta": 1}}
    )

    moneta = ["Орел", "Решка"]
    moneta_random = random.choice(moneta)
    moneta_user = message.text
    stick = open("image/AnimatedSticker.tgs", "rb")
    bot.send_sticker(id, stick)
    sleep(3)
    bot.send_message(id, str(moneta_random))
    sleep(1)
      
    if moneta_random == moneta_user:
        users.update_one(
            {"id": id},
            {"$inc": {"score": 1}}
        )

        date.update_one(
            {"id": id},
            {"$inc": {"score": 1, "score_moneta": 1}}
        )

        bot.send_message(id, "Вы победили!")
        sleep(2)

        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton("🎰 Угадай число")
        item2 = types.KeyboardButton("🎲 Игра *Кости*")
        item3 = types.KeyboardButton("🎳 Боулинг")
        item4 = types.KeyboardButton("⚽️ Футбол")
        item5 = types.KeyboardButton("🏀 Баскетбол")
        item6 = types.KeyboardButton("🟡 Орел & Решка")
        item7 = types.KeyboardButton("🎯 Дартс")
        item8 = types.KeyboardButton("🔙 Вернуться в Функции")
        markup.row(item1) 
        markup.row(item2, item3, item4)
        markup.row(item5, item6, item7)
        markup.row(item8)
        bot.send_message(id, "🚩 Выберите игру", reply_markup = markup)  
    else:
        bot.send_message(id, "Вы проиграли!")
        sleep(2)
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton("🎰 Угадай число")
        item2 = types.KeyboardButton("🎲 Игра *Кости*")
        item3 = types.KeyboardButton("🎳 Боулинг")
        item4 = types.KeyboardButton("⚽️ Футбол")
        item5 = types.KeyboardButton("🏀 Баскетбол")
        item6 = types.KeyboardButton("🟡 Орел & Решка")
        item7 = types.KeyboardButton("🎯 Дартс")
        item8 = types.KeyboardButton("🔙 Вернуться в Функции")
        markup.row(item1) 
        markup.row(item2, item3, item4)
        markup.row(item5, item6, item7)
        markup.row(item8)
        bot.send_message(id, "🚩 Выберите игру", reply_markup = markup) 

def dollar_rubl(message):
    number = message.text
    try:
        number = int(message.text)
        result = int(number) / float(price_usd)
        bot.send_message(id, "*Результат -* " + str('{:.2f}'.format(result)) + " *USD*", parse_mode = "Markdown")

        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton("💴 Рубли в 💵 Доллар")
        item2 = types.KeyboardButton("💴 Рубли в 💶 Евро")
        item3 = types.KeyboardButton("💵 Доллар в 💴 Рубли")
        item4 = types.KeyboardButton("💶 Евро в 💴 Рубли")
        item5 = types.KeyboardButton("🔙 Вернуться в Курс Валют")
        markup.row(item1, item3)
        markup.row(item2, item4)
        markup.row(item5)
        bot.send_message(id, "🚩 Выберите действие", reply_markup = markup)
    except:
        bot.send_message(id, "Нужно вводить значения цифрами.")
        bot.register_next_step_handler(message, dollar_rubl)

def rubl_dollar(message):
    number = message.text
    try:
        number = int(message.text)
        result = int(number) / float(price_usd)
        bot.send_message(id, "*Результат -* " + str('{:.2f}'.format(result)) + " *USD*", parse_mode = "Markdown")

        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton("💴 Рубли в 💵 Доллар")
        item2 = types.KeyboardButton("💴 Рубли в 💶 Евро")
        item3 = types.KeyboardButton("💵 Доллар в 💴 Рубли")
        item4 = types.KeyboardButton("💶 Евро в 💴 Рубли")
        item5 = types.KeyboardButton("🔙 Вернуться в Курс Валют")
        markup.row(item1, item3)
        markup.row(item2, item4)
        markup.row(item5)
        bot.send_message(id, "🚩 Выберите действие", reply_markup = markup)
    except:
        bot.send_message(id, "Нужно вводить значения цифрами.")
        bot.register_next_step_handler(message, rubl_dollar)

def euro_rubl(message):
    number = message.text
    try:
        number = int(message.text)
        result = int(number) * float(price_euro)
        bot.send_message(id, "*Результат -* " + str('{:.2f}'.format(result)) + " *₽*", parse_mode = "Markdown")

        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton("💴 Рубли в 💵 Доллар")
        item2 = types.KeyboardButton("💴 Рубли в 💶 Евро")
        item3 = types.KeyboardButton("💵 Доллар в 💴 Рубли")
        item4 = types.KeyboardButton("💶 Евро в 💴 Рубли")
        item5 = types.KeyboardButton("🔙 Вернуться в Курс Валют")
        markup.row(item1, item3)
        markup.row(item2, item4)
        markup.row(item5)
        bot.send_message(id, "🚩 Выберите действие", reply_markup = markup)
    except:
        bot.send_message(id, "Нужно вводить значения цифрами.")
        bot.register_next_step_handler(message, rubl_dollar)


def rubl_euro(message):
    number = message.text
    try:
        number = int(number)
        result = int(number) / float(price_euro)
        bot.send_message(id, "*Результат -* " + str('{:.2f}'.format(result)) + " *EURO*", parse_mode = "Markdown")

        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton("💴 Рубли в 💵 Доллар")
        item2 = types.KeyboardButton("💴 Рубли в 💶 Евро")
        item3 = types.KeyboardButton("💵 Доллар в 💴 Рубли")
        item4 = types.KeyboardButton("💶 Евро в 💴 Рубли")
        item5 = types.KeyboardButton("🔙 Вернуться в Курс Валют")
        markup.row(item1, item3)
        markup.row(item2, item4)
        markup.row(item5)
        bot.send_message(id, "🚩 Выберите действие", reply_markup = markup)
    except:
        bot.send_message(id, "Нужно вводить значения цифрами.")
        bot.register_next_step_handler(message, rubl_dollar)

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
	bot.send_message(id, "⏳ Формирование...")
	sleep(1)
	bot.send_message(id, "⌛️ Формирование...")
	sleep(1)
	bot.send_message(id, "Ваше сообщение сформировано. \n\n" + str(up_text), reply_markup = markup)

def number(message):
    global counter, random_number
    number_user = message.text
    try:
        number_user = int(number_user)

        if number_user < 1 or number_user > 10:
            bot.send_message(id, "Введите число в диапазоне от 1 до 10")
            bot.register_next_step_handler(message, number)
        else:
            if number_user == random_number:
                users.update_one(
                    {"id": id},
                    {"$inc": {"score": 1}}
                )

                date.update_one(
                    {"id": id},
                    {"$inc": {"score": 1, "score_number": 1}}
                )

                sleep(0.5)
                bot.send_message(id, "Поздравляю, вы угадали число!")
                sleep(0.5)
                bot.send_message(id, "Было загадано число - " + str(random_number))

                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                item1 = types.KeyboardButton("Да")
                item2 = types.KeyboardButton("Нет")
                markup.row(item1)
                markup.row(item2)
                bot.send_message(id, "Хотите сыграть еще? 😊", reply_markup = markup)
            elif counter > 1:
                counter -= 1
                sleep(0.5)
                bot.send_message(id, "Неверно. Осталось попыток: " + str(counter))
                bot.register_next_step_handler(message, number)
                return
            else:
                sleep(0.5)
                bot.send_message(id, "Увы, но вы не угадали число( ☹️")
                sleep(0.5)
                bot.send_message(id, "Было загадано число - " + str(random_number))

                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                item1 = types.KeyboardButton("Да")
                item2 = types.KeyboardButton("Нет")
                markup.row(item1)
                markup.row(item2)
                bot.send_message(id, "Хотите сыграть еще? 😊", reply_markup = markup)
    except:
        bot.send_message(id, "Введите пожалуйста цифру!")
        bot.register_next_step_handler(message, number)


def wiki(message):
	global search
	wikipedia.set_lang("RU")
	text = message.text
	search = wikipedia.search(text, results = 6)
	if len(search) == 0:
		bot.send_message(id, f"По запросу  *'{text}'*  ничего не найдено! ", parse_mode = "Markdown")
		markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
		item1 = types.KeyboardButton("📖 Вики")
		item2 = types.KeyboardButton("🔙 Вернуться в Функции")
		markup.row(item1)
		markup.row(item2)
		bot.send_message(id, "Хотите попробовать найти ваш запрос еще раз?", reply_markup= markup)
	else:
		for index, result in enumerate(search, start = 0):
			bot.send_message(id, f"{index}) {result}")

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
		bot.send_message(id, "Выберите цифру запроса которого хотите узнать: ", reply_markup = markup)
		bot.register_next_step_handler(message, wiki_result)

def wiki_result(message):
	number = message.text
	try:
		number = int(message.text)
		if number < 0 or number > 5:
			bot.send_message(id, "Вы ввели неверный диапазон. \nВведите пожалуйста цифру от 0 до 5")
			bot.register_next_step_handler(message, wiki_result)
		else:
			try:
				wikipedia.set_lang("RU")
				text = wikipedia.summary(search[int(number)])
				bot.send_message(id, str(text))
			except:
				bot.send_message(id, "Произошла ошибка, не удалось найти данный запрос!")
			sleep(2)
			markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
			item1 = types.KeyboardButton("📖 Вики")
			item2 = types.KeyboardButton("🔙 Вернуться в Функции")
			markup.row(item1)
			markup.row(item2)
			bot.send_message(id, "Хотите еще найти что-нибудь?", reply_markup= markup)
	except:
		bot.send_message(id, "Введите цифру пожалуйста!")
		bot.register_next_step_handler(message, wiki_result)

bot.infinity_polling()