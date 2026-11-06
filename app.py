from telethon import TelegramClient, events
import asyncio
import os
from flask import Flask
from threading import Thread

# --- ЗАГЛУШКА ДЛЯ RENDER ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive"

def run_flask():
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
target_channel = '@GSUESPB'

# ВСТАВЬ СЮДА НОВЫЙ ТОКЕН
bot_token = '9027029313:AAG9bupAtrpaXvMaDKfJxNl-YckyGuCDdic'

try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# 1. Клиент для чтения (твой аккаунт)
user_client = TelegramClient('train_session', api_id, api_hash)

# 2. Клиент для отправки (бот)
bot_client = TelegramClient('bot_session', api_id, api_hash)

async def test_send():
    print("--- НАЧАЛО ТЕСТА ОТПРАВКИ ---")
    try:
        print(f"Пытаюсь отправить сообщение в {target_channel}...")
        await bot_client.send_message(target_channel, 'Тест отправки от бота! Если ты это видишь, значит права есть.')
        print("✅ ТЕСТ ПРОЙДЕН: Бот может писать в канал!")
    except Exception as e:
        print(f"❌ ОШИБКА ТЕСТА: {e}")

@user_client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    try:
        print(f"Поймал пост из донора: {event.message.message[:30]}...")
        await bot_client.forward_messages(target_channel, event.message)
        print(f"Переслано ботом: {event.message.message[:30] if event.message.message else 'Медиа'}...")
    except Exception as e:
        print(f"Ошибка пересылки: {e}")

print("Бот запущен. Читаем твоим аккаунтом, отправляем ботом...")

keep_alive()

# Запускаем бота
print("Запускаю bot_client...")
bot_client.start(bot_token=bot_token)
print("Запускаю user_client...")
user_client.start()

# Выполняем тестовую отправку при старте
print("Запускаю тестовую отправку...")
with bot_client:
    bot_client.loop.run_until_complete(test_send())

print("Тест завершен. Бот переходит в режим ожидания постов...")
user_client.run_until_disconnected()
