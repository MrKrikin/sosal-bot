import os
import threading
from flask import Flask, request
import telebot


TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)


app = Flask(__name__)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.chat.type in ['group', 'supergroup']:
        message_text = message.text.lower() if message.text else ''
        if 'сосал' in message_text:
            bot.reply_to(message, "да")
        elif message_text in ['да', 'lf', 'da']:
            bot.reply_to(message, "Сосал?")


@app.route('/')
@app.route('/health')
@app.route('/healthcheck')
def health():
    return 'OK', 200

def run_bot():
    bot.infinity_polling()

if __name__ == '__main__':

    threading.Thread(target=run_bot, daemon=True).start()

    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
