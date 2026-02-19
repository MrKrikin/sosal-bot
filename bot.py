import os
import telebot

TOKEN = os.environ.get('TOKEN')

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.chat.type in ['group', 'supergroup']:
        message_text = message.text.lower() if message.text else ''
        
        if 'сосал' in message_text:
            bot.reply_to(message, "да")
        elif message_text in ['да', 'lf', 'da']:
            bot.reply_to(message, "Сосал?")

print("Бот запущен...")
bot.infinity_polling()