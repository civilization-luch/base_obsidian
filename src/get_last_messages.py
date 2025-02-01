from telethon import TelegramClient
from dotenv import load_dotenv
import os
import json

# Загружаем переменные окружения из файла .env
load_dotenv()

# Replace 'your_api_id' and 'your_api_hash' with your actual API credentials
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')



# Create a new Telegram client
client = TelegramClient('session_name', api_id, api_hash)


async def download_and_cache(message_media_photo):
    file_path = f'images/{message_media_photo.id}.jpg'
    if not os.path.exists(file_path):
        return await client.download_media(message_media_photo, file=file_path )
    else:
        return None

async def get_last_messages():
    # Подключаемся к Telegram
    await client.start()

    # Получаем объект чата по имени группы или ссылке
    #group = await client.get_entity('https://t.me/+ZTzmreYWp5kwYTBi')

    '''
    Chat Name: ВКРИЗИС.ЧАТ, Chat ID: -1002230799086
Chat Name: ВКРИЗИС, Chat ID: -1001704993383
Chat Name: ВКРИЗИС.БОТ, Chat ID: 7376175904
Chat Name: ВКРИЗИС.БАЗА, Chat ID: -1002233618871
    '''
    group = await client.get_entity(-1002233618871)

    # Получаем последние 10 сообщений из группы
    
    messages = await client.get_messages(group, limit=None)

    messages_data = []  # Список для хранения данных сообщений

    for message in reversed(messages):
        if message.media and hasattr(message.media, 'photo'):
            
            #image_url = f"https://api.telegram.org/file/bot{api_hash}/{message.media.photo.id}"  # Пример URL, может потребоваться изменить
            await download_and_cache(message.media.photo)
            
            message_info = {
                "sender_id": message.sender_id,
                "message_id": message.id,
                "media_type": "photo",
                "media_content": message.text,
                "media_content_url": None,
                "media_downloaded_url": f"images/{message.media.photo.id}.jpg"
            }
            messages_data.append(message_info)

         
            
            
        elif message.media and hasattr(message.media, 'document') and message.media.document.mime_type.startswith('image/'):
            message_info = {
                "sender_id": message.sender_id,
                "message_id": message.id,
                "media_type": "document",
                "media_content_url": None,
                "media_content": message.media.document.url,
                
                "media_downloaded_url": None  # Здесь будет None, если не загружается
            }
            messages_data.append(message_info)
        else:
            message_info = {
                "sender_id": message.sender_id,
                "message_id": message.id,
                "media_type": None,
                "media_content": message.text,
                "media_content_url": None,
                "media_downloaded_url": None
            }
            messages_data.append(message_info)

    # Записываем данные в JSON файл
    with open('messages.json', 'w') as json_file:
        json.dump(messages_data, json_file, ensure_ascii=False, indent=4)

    await client.disconnect()

if __name__ == "__main__":
    # Run the script
    with client:
        client.loop.run_until_complete(get_last_messages())
