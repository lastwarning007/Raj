import os
import telebot
import requests
from telebot import types
from flask import Flask, request

# List of required packages
required_packages = ['telebot', 'requests', 'Flask']

# Install missing packages
for package in required_packages:
    os.system(f'pip install {package}')

API_TOKEN = '7700765492:AAH62P0CN-IaECNza3m0wxUzz7PWcx9L2Zw'
bot = telebot.TeleBot(API_TOKEN)

API_URL = "https://logo.pikaapis.workers.dev/?prompt={}&type=json"

app = Flask(__name__)

# Webhook route for receiving updates from Telegram
@app.route(f'/{API_TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

# Command handler for /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Channel", url="https://t.me/Misterbillu")
    button2 = types.InlineKeyboardButton("Developer", url="https://t.me/BihariDeveloper")
    markup.add(button1, button2)
    bot.send_photo(message.chat.id, "https://iili.io/2kWRM12.md.jpg", caption="Welcome to Last Warning Bot! Please enter your text.", reply_markup=markup)

# Handler for processing the user's text input
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_input = message.text
    bot.reply_to(message, f"Processing your input: {user_input}")
    
    try:
        response = requests.get(API_URL.format(user_input))
        response.raise_for_status()
        data = response.json()

        if data['status'] == 'success' and 'url' in data:
            image_url = data['url']
            bot.send_photo(message.chat.id, image_url)
        else:
            bot.reply_to(message, "Sorry, there was an issue generating the image.")
            
    except requests.exceptions.RequestException as e:
        bot.reply_to(message, f"Error: {e}")

# Start the Flask server
if __name__ == "__main__":
    bot.remove_webhook()  # In case it's already set, remove it
    bot.set_webhook(url='https://raj-1-80o3.onrender.com' + API_TOKEN)  # Replace with your live domain
    app.run(host='0.0.0.0', port=5000)
