import requests
from config import BOT_API_TOKEN, GROUP_CHAT_ID
from typing import Any

def send_message_to_telegram_group(message: str, parse_mode: str = 'Markdown') -> dict[str, Any]:
    """
    Sends a message to the Telegram group using the bot.

    Parameters:
        message (str): The message to send.
        parse_mode (str): The format of the message text (e.g., 'Markdown', 'HTML').

    Returns:
        dict: The JSON response from Telegram's API.
    """
    
    # Construct the Telegram Bot API URL with the bot token
    url = f"https://api.telegram.org/bot{BOT_API_TOKEN}/sendMessage"

    # Define the payload with chat ID, message, and formatting style
    payload = {
        'chat_id': GROUP_CHAT_ID,  # ID of the group or channel the bot should message
        'text': message,           # The message content
        'parse_mode': parse_mode   # Formatting style ('Markdown' or 'HTML')
    }

    try:
        # Send the POST request to Telegram with a timeout of 10 seconds
        response = requests.post(url, data=payload, timeout=10)

        # Raise an HTTPError if one occurred (e.g., 4xx or 5xx response)
        response.raise_for_status()

        # Return the parsed JSON response from Telegram API
        return response.json()
    
    except requests.RequestException as e:
        # Print a helpful error message if something goes wrong
        print(f"❌ Telegram message failed: {e}")
        
        # Return a fallback response indicating failure
        return {"ok": False, "error": str(e)}