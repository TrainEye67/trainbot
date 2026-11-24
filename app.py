import os
import asyncio
from threading import Thread
from flask import Flask
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# --- ЗАГЛУШКА ДЛЯ RENDER + UPTIMEROBOT ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask, daemon=True)
    t.start()
# ----------------------------------------

api_id = 34525517
api_hash = os.environ.get('API_HASH')
session_str = os.environ.get('STRING_SESSION')
bot_token = os.environ.get('BOT_TOKEN')

source_channel = 'where_suburban_train'  # Откуда пересылаем (@where_suburban_train)
target_channel = 'GSUESPB'               # Куда пересылаем (@GSUESPB)

user_client = TelegramClient(StringSession(session_str), api_id, api_hash)
bot_client = TelegramClient('bot_session', api_id, api_hash)

@user_client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    try:
        preview = event.message.message[:30] if event.message.message else 'Медиа'
        print(f"Поймал пост [{event.message.id}]: {preview}...")
        
        await bot_client.forward_messages(
            entity=target_channel,
            messages=event.message.id,
            from_peer=source_channel
        )
        print(f"✅ Успешно переслано от имени бота в @{target_channel}!")
    except Exception as e:
        print(f"❌ Ошибка пересылки: {e}")

async def main():
    await bot_client.start(bot_token=bot_token)
    await user_client.start()
    await user_client.get_dialogs()
    
    print(f"🚀 Слушаем @{source_channel} -> пересылаем ботом в @{target_channel}")
    await asyncio.gather(
        user_client.run_until_disconnected(),
        bot_client.run_until_disconnected()
    )

if __name__ == '__main__':
    keep_alive()
    asyncio.run(main())
