import os
import threading
from flask import Flask
import telebot
import time

TOKEN = os.environ.get('TOKEN')
ALLOWED_USERS = [1585718150] 

bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

def normalize_text(text):
    if not text:
        return text
    
    replacements = {
        'a': 'а', 'b': 'б', 'c': 'ц', 'd': 'д', 'e': 'е', 'f': 'ф', 
        'g': 'г', 'h': 'х', 'i': 'и', 'j': 'й', 'k': 'к', 'l': 'л', 
        'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п', 'q': 'к', 'r': 'р', 
        's': 'с', 't': 'т', 'u': 'у', 'v': 'в', 'w': 'в', 'x': 'кс', 
        'y': 'ы', 'z': 'з'
    }
    
    text_lower = text.lower()
    normalized = ''
    for char in text_lower:
        if char in replacements:
            normalized += replacements[char]
        else:
            normalized += char
    
    return normalized

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.chat.type in ['group', 'supergroup']:
        message_text = message.text.lower().strip() if message.text else ''
        normalized_text = normalize_text(message_text)
        user_id = message.from_user.id
        
        if user_id in ALLOWED_USERS:
            if 'test' in message_text:
                bot.reply_to(message, "Сосал?")
        else:
            if 'сосал' in message_text or 'сосал' in normalized_text:
                bot.reply_to(message, "да")
            elif (message_text in ['да', 'lf', 'da', 'дa', 'дa', 'dа'] or
                  normalized_text in ['да'] or
                  message_text == 'да'):
                bot.reply_to(message, "Сосал?")

@app.route('/')
@app.route('/health')
@app.route('/healthcheck')
def health():
    return 'OK', 200

def run_bot():
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"Bot crashed: {e}, restarting in 5 seconds...")
            time.sleep(5)

if __name__ == '__main__':
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
