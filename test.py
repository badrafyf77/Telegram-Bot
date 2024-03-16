import telebot
from decouple import config

BOT_TOKEN = config('BOT_TOKEN')
CHANNEL_ID = config('CHANNEL_ID')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message): 
    bot.send_message(message.chat.id,'Salam')

bot.polling()