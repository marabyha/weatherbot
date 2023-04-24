import telebot
import requests
import json
bot = telebot.TeleBot('5823054453:AAG1uqYUD50_yd9B-8fZY2USIKUYjZELNPk')
bot.set_webhook()

WEATHER_TOKEN = '8d761b50d04c864baf1b95dedf0a42b2'

WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={token}'


@bot.message_handler(commands=['start'])
def start_messaging(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Привет, это бот с погодой")
        bot.send_message(message.from_user.id, "для ознакомления с возможностями выбери /help")


@bot.message_handler(commands=['help'])
def help_for_user(message):
    if message.text == "/help":
        bot.send_message(message.from_user.id, "Для того, что бы узнать температуру в интресующем тебя городе напиши его назвавние на английском например: London")


def parse_weather_data(data):
    for elem in data['weather']:
        weather_state = elem['main']
    temp = round(data['main']['temp'] - 273.15, 2)
    city = data['name']
    msg = f'Погода в {city}: температура {temp}, состояние {weather_state}'
    return msg


@bot.message_handler(content_types=['text'])
def get_location(message):
    url = WEATHER_URL.format(city=message.text, token=WEATHER_TOKEN)
    response = requests.get(url)
    if response.status_code != 200:
        answer = 'Город не найден'
    else:
        data = json.loads(response.content)
        answer = parse_weather_data(data)
    bot.send_message(message.from_user.id, answer)


bot.polling(none_stop=True, interval=0)
