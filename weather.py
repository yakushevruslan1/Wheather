import os
import requests
import telebot
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

if TOKEN is None or WEATHER_API_KEY is None:
    raise ValueError("Не удалось загрузить TELEGRAM_BOT_TOKEN или WEATHER_API_KEY из файла .env")

bot = telebot.TeleBot(TOKEN)

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    response = requests.get(url).json()

    if response.get("cod") != 200:
        return "Город не найден. Попробуйте ещё раз."

    weather = response["weather"][0]["description"].capitalize()
    temp = response["main"]["temp"]
    feels_like = response["main"]["feels_like"]
    city_name = response["name"]

    return f"Погода в {city_name}: {weather}\nТемпература: {temp}°C\nОщущается как: {feels_like}°C"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Напишите название города, и я скажу, какая там погода.")

@bot.message_handler(func=lambda message: True)
def weather(message):
    city = message.text.strip()
    weather_info = get_weather(city)
    bot.reply_to(message, weather_info)

if __name__ == "__main__":
    bot.polling(none_stop=True)