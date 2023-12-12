import requests

from icecream import *

from secured_data import api_key_yt
from secured_data import api_key_tg

import telebot
from telebot import types

bot = telebot.TeleBot(api_key_tg)

# Словарь для хранения выбранных пользователем ссылок
chosen_links = {}

cur_links = {
	1: [
		{'link': 'youtube.com',
		 'title': 'title'}
	]
}


def get_links(query, uid):
	url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=3&q={query}&key={api_key_yt}'

	response = requests.get(url)

	data = response.json()

	if uid in cur_links:
		i = 0
		for item in data['items']:
			print(f"https://www.youtube.com/watch?v={item['id']['videoId']}")
			cur_links[uid][i] = ({'link': f"https://www.youtube.com/watch?v={item['id']['videoId']}", 'title': f"{item['snippet']['title']}"})
			i += 1
	else:
		cur_links[uid]= [[], [], []]
		i = 0
		for item in data['items']:
			cur_links[uid][i] = {'link': f"https://www.youtube.com/watch?v={item['id']['videoId']}", 'title': f"{item['snippet']['title']}"}
			i += 1
	print(query)
	ic(cur_links)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id, "Привет! Введите запрос:")


# Обработчик текстовых сообщений от пользователя
@bot.message_handler(content_types=["text"])
def handle_text(message):
	get_links(message.text, message.from_user.id)

	num_links = len(cur_links[message.from_user.id])

	bot.send_message(message.chat.id, "Выберите одно из видео:")
	for i in range(num_links):
		bot.send_message(message.chat.id, f"{cur_links[message.from_user.id][i]['link']}")

	# Создаем клавиатуру для выбора
	keyboard = types.InlineKeyboardMarkup(row_width=1)
	for i in range(num_links):
		keyboard.add(types.InlineKeyboardButton(f"Видео {i + 1}", callback_data=f'vid{i + 1}'))

	bot.send_message(message.chat.id, "Выберите вариант", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "vid1")
def vid1(call: types.CallbackQuery):
	# bot.edit_message_reply_markup(message.chat.id, message_id=call.message_id - 1, reply_markup='')
	bot.send_message(chat_id=call.message.chat.id, text="Вы выбрали 1 видео")
	if call.from_user.id in chosen_links:
		pass
	else:
		chosen_links[call.from_user.id] = []
	chosen = cur_links[call.from_user.id][1]
	chosen_links[call.from_user.id].update(chosen)


# Запускаем бота
bot.polling()
