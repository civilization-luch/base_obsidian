import json
import os

articles = [
    {"title": "Вводная часть курса", "message_id": 5},
    {"title": "Как решать свои проблемы самим?", "message_id": 10},
    {"title": "Синергетические социальные структуры", "message_id": 28},
    {"title": "Синергетическая кооперация", "message_id": 30},
    {"title": "Эволюционный скачок развития цивилизации", "message_id": 32},
    {"title": "Что делать?", "message_id": 38},
    {"title": "Концепт социальной синергии", "message_id": 51},
    {"title": "Как работает среда взаимодействия", "message_id": 58},
    {"title": "Алгоритм поручительства", "message_id": 61},
    {"title": "Чем Социальные Синергетические Структуры (ССС) отличаются от простой кооперации", "message_id": 70},
    {"title": "Новые принципы кооперации на основе логики дарения", "message_id": 78},
    {"title": "Деньги, налоги, законы в социальной синергии", "message_id": 80},
    {"title": "Нужны ли сегодня деньги вообще? И какова их роль в будущем?", "message_id": 82},
    {"title": "Блокчейн обмен. Система экономического поручительства", "message_id": 85},
    {"title": "Способ оценки долевого вклада", "message_id": 95},
    {"title": "Токеномика - Народовластие", "message_id": 100}
]

exported_dir = os.path.join(os.getcwd(), "_exported")
# Load messages from JSON file
with open(f'{exported_dir}/messages.json', 'r', encoding='utf-8') as f:
    messages = json.load(f)

# Generate markdown documents for each article
for i, article in enumerate(articles):
    message_id = article['message_id']
    title = article['title']
    
    # Find the message with the corresponding message_id
    message = next((msg for msg in messages if msg['message_id'] == message_id), None)
    
    if message:
        # Create markdown content
        markdown_content = f"# {title}\n\n"
        markdown_content += f"![[{message['media_downloaded_url']}]]\n" if message.get('media_downloaded_url') else ""
        markdown_content += f"{message['media_content']}\n" if message.get('media_content') else ""

        
        # Find the next article's message_id
        next_message_id = articles[i + 1]['message_id']  if i + 1 < len(articles) else None
        
        # Append all messages between current and next message_id
        if next_message_id is not None:
            for msg in messages:
                if msg.get('message_id') and message_id < msg['message_id'] < (next_message_id or float('inf')):
                    markdown_content += f"![[{msg['media_downloaded_url']}]]\n" if msg.get('media_downloaded_url') else ""
                    markdown_content += f"{msg['media_content']}\n" if msg.get('media_content') else ""
        
        
        # Define the filename
        filename = f"{title}.md".replace(" ", "_").replace(":", "").replace("?", "").replace("!", "")  # Clean filename
        # Create documents directory if it doesn't exist
        documents_dir = os.path.join(exported_dir,  'documents')
        os.makedirs(documents_dir, exist_ok=True)
        filepath = os.path.join(documents_dir, filename)
        
        # Write to markdown file
        with open(filepath, 'w', encoding='utf-8') as md_file:
            md_file.write(markdown_content)
            print(f"Generated: {filepath}")
    else:
        print(f"No message found for article: {title}")
