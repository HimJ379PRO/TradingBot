import requests
from config import BOT_API_TOKEN, GROUP_CHAT_ID


def send_message_to_telegram_group(message: str):
    """
    Sends a message to the Telegram Group using the bot.
    """
    url = f"https://api.telegram.org/bot{BOT_API_TOKEN}/sendMessage"
    payload = {
        'chat_id': GROUP_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    response = requests.post(url, data=payload)
    
    if response.status_code != 200:
        print("Failed to send message:", response.text)
    
    return response.json()