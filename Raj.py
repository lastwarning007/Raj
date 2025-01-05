import os
import requests
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

API_TOKEN = '7700765492:AAH62P0CN-IaECNza3m0wxUzz7PWcx9L2Zw'
API_URL = "https://logo.pikaapis.workers.dev/?prompt={}&type=json"
bot = Bot(token=API_TOKEN)

app = Flask(__name__)

# Set up webhook handler
@app.route(f'/{API_TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    dispatcher.process_update(update)
    return 'OK'

# Command Handler for /start
def start(update, context):
    user = update.message.from_user
    chat_id = update.message.chat_id
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Channel", url="https://t.me/Misterbillu")
    button2 = types.InlineKeyboardButton("Developer", url="https://t.me/BihariDeveloper")
    markup.add(button1, button2)
    bot.send_photo(chat_id, "https://iili.io/2kWRM12.md.jpg", caption="Welcome to Last Warning Bot! Please enter your text.", reply_markup=markup)

# Message Handler for text messages
def handle_text(update, context):
    user_input = update.message.text
    update.message.reply_text(f"Processing your input: {user_input}")
    
    try:
        response = requests.get(API_URL.format(user_input))
        response.raise_for_status()
        data = response.json()

        if data['status'] == 'success' and 'url' in data:
            image_url = data['url']
            bot.send_photo(update.message.chat_id, image_url)
        else:
            update.message.reply_text("Sorry, there was an issue generating the image.")
            
    except requests.exceptions.RequestException as e:
        update.message.reply_text(f"Error: {e}")

# Set up Dispatcher
dispatcher = Dispatcher(bot, None, workers=0)
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

# Run Flask app
if __name__ == '__main__':
    app.run(port=os.environ.get('PORT', 5000))