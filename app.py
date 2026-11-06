from telethon import TelegramClient, events
import asyncio
import os
from flask import Flask
from threading import Thread

# --- ЗАГЛУШКА ДЛЯ RENDER (чтобы он видел порт) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive"

def run_flask():
    # Render передает порт через переменную PORT
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()
# -------------------------------------------------

# ТВОИ ДАННЫЕ
api_id = 34525517
api_hash = 'ba7701494543e410242ee56ac3ae577a'
source_channel = 'where_suburban_train'
target_channel = 'GSUESPB'

# ВСТАВЬ СЮДА НОВЫЙ ТОКЕН ОТ BOTFATHER
bot_token = '9027029313:AAG9bupAtrpaXvMaDKfJxNl-YckyGuCDdic'

# Костыль для Python 3.14 (чтобы не было ошибки с event loop)
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# 1. Клиент для чтения (твой аккаунт)
user_client = TelegramClient('train_session', api_id, api_hash)

# 2. Клиент для отправки (бот)
bot_client = TelegramClient('bot_session', api_id, api_hash)

@user_client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    try:
        # Пересылаем от лица бота
        await bot_client.forward_messages(target_channel, event.message)
        print(f"Переслано ботом: {event.message.message[:30] if event.message.message else 'Медиа'}...")
    except Exception as e:
        print(f"Ошибка: {e}")

print("Бот запущен. Читаем твоим аккаунтом, отправляем ботом...")

# Запускаем заглушку, чтобы Render не ругался на порт
keep_alive()

# Запускаем бота
bot_client.start(bot_token=bot_token)
user_client.start()
user_client.run_until_disconnected()
