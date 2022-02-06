import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

# making bot sociable 
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Hello! Write me a city and I'll tell you a weather in it)")


@dp.message_handler()
async def get_weather(message: types.Message):

     # weather conditions
    weather_conditions = {
        "Clear": "Clear \U00002600",
        "Clouds": "Clouds \U00002601",
        "Rain": "Rain \U00002614",
        "Drizzle": "Little rain \U00002614",
        "Thunderstorm": "Thunderstorm \U000026A1",
        "Snow": "Snow \U0001F328",
        "Mist": "Mist \U0001F32B"
        
    }

    #using "requests" to import data from weather site
    try:
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        # weather description
        weather_description = data["weather"][0]["main"]
        if weather_description in weather_conditions:
            weather_description_answer = weather_conditions[weather_description]
        else:
            weather_description_answer = "Look at the weather by yourself)"

        # weather data
        city = data["name"]
        current_weather = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind_speed = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        # outout weather data
        await message.reply(f"""
            Today is {datetime.datetime.now().strftime("%Y-%m-%d")}
            Weather in city {city}:
            Temperature: {current_weather} C°, {weather_description_answer}
            Humidity: {humidity} %
            Pressure: {pressure} mmHg
            Wind speed: {wind_speed} m/s
            Sunrise at: {sunrise_timestamp}
            Sunset at: {sunset_timestamp}
            Day length: {length_of_the_day}
            Have a nice day!
            """)

# if city doesn't exist/city typed uncorrectly
    except Exception as ex:
        await message.reply("Сheck: is the name of the city spelled correctly?")


if __name__ == '__main__':
    executor.start_polling(dp)