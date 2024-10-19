from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import requests

bot = Bot(token='7945893753:AAH6oYEKPh8Z-TnxD_dw5Ifb5_QMRole0pE')
dp = Dispatcher(bot)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    telegram_id = message.from_user.id
    username = message.from_user.username or "anonymous"  # Убедитесь, что username не пустой

    # Отправляем данные на сервер Django
    try:
        response = requests.post('https://eb7b-185-250-30-189.ngrok-free.app/register/',
                                 data={'telegram_id': telegram_id, 'username': username})

        # Проверяем успешность регистрации
        if response.status_code == 200 and response.json().get('status') == 'success':
            # Передаем telegram_id через URL для мини-приложения
            web_app_url = f"https://eb7b-185-250-30-189.ngrok-free.app/?telegram_id={telegram_id}"  # URL мини-приложения с параметром
            markup = InlineKeyboardMarkup()
            button = InlineKeyboardButton(text="Open Mini App", web_app=WebAppInfo(url=web_app_url))
            markup.add(button)

            await message.answer("You have been registered successfully!", reply_markup=markup)
        else:
            await message.answer(f"Something went wrong. Error: {response.json().get('message', 'Unknown error')}")

    except Exception as e:
        await message.answer(f"An error occurred: {e}")



if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
