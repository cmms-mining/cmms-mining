from asyncio import run

from aiogram import Bot

from django.conf import settings


async def send_telegram_message(message: str):
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    await bot.send_message(settings.TELEGRAM_USER_ID, message)
    await bot.session.close()


def notify_telegram(message: str):
    try:
        run(send_telegram_message(message))
    except Exception as e:
        print(f"Ошибка при вызове функции отправки сообщения: {e}")
