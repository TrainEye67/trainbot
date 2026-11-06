from telethon import TelegramClient, events
import asyncio

# Твои данные для чтения
api_id = 34525517
api_hash = 'ba7701494543e410242ee56ac3ae577a'
source_channel = 'where_suburban_train'
target_channel = 'GSUESPB'

# Твой токен (взял со скрина)
bot_token = '9027029313:AAG9bupAtrpaXvMaDKfJxNl-YckyGuCDdic'

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
bot_client.start(bot_token=bot_token) # Запускаем бота по токену
user_client.start() # Запускаем твой аккаунт
user_client.run_until_disconnected()
