import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN, WEATHER_API_KEY
from googletrans import Translator

translator = Translator()

bot = Bot(token=TOKEN)
dp = Dispatcher()


# Функция для получения прогноза погоды
async def get_weather(city: str) -> str:
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            if response.status == 200:
                weather = data['weather'][0]['description']
                temp = data['main']['temp']
                return f'Погода в городе {city}: {weather}, температура: {temp}°C'
            else:
                return 'Не удалось получить прогноз погоды. Проверьте название города.'


@dp.message(Command('translation'))
async def translation(message: Message):
    text_to_translate = message.text  # Extract the text from user's message
    translated_text = translate_text_to_english(text_to_translate)  # Translate the text to English
    await message.answer(translated_text)
    await message.answer(
        'Этот бот перводит с русского на английский Используйте команду /translation <текст> для получения перевода.')

# Function to translate text to English
def translate_text_to_english(text):
    translation = translator.translate(text, src='auto', dest='en')  # Translate from auto-detected language to English
    return translation.text



@dp.message(F.photo)
async def react_photo(message: Message):
    await bot.download(message.photo[-1], destination=f'photo/{message.photo[-1].file_id}.jpg')

@dp.message(Command('audio'))
async def audio(message: Message):
    audio = FSInputFile('Their Emotions (Remix) (722d7726d8d8403883430b005188bf49).mp3')
    await bot.send_audio(message.chat.id, audio)

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот передаёт прогноз погоды. Используйте команду /weather <город> для получения прогноза.')


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет! Я бот! Используйте команду /weather<город> для получения прогноза погоды.')



@dp.message(Command('weather'))
async def weather(message: Message):
    await message.answer('Пожалуйста, укажите город после команды /weather. Например: /weather Москва')
    # Извлекаем название города из сообщения
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:

        return

    city = parts[1]





    try:
        weather_report = await get_weather(city)
        await message.answer(weather_report)
    except Exception as e:
        await message.answer("Произошла ошибка при получении данных о погоде.")



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

    import asyncio
    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling())
    loop.run_forever()
