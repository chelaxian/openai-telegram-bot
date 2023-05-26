import openai
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters

# Global variables
API_KEY = "sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
BOT_TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
AUTH_PASSWORD = "/auth XXXXXXXXXXXXXXXXX"
IMAGE_MODEL = "image-alpha-001"
TEXT_MODEL = "gpt-3.5-turbo"

openai.api_key = API_KEY
updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

def auth(update: Update, context: CallbackContext):
    if update.message.text == AUTH_PASSWORD:
        context.user_data['authorized'] = True
        update.message.reply_text("Авторизация успешно пройдена!")
    else:
        update.message.reply_text("Неверный пароль!")

def clear(update: Update, context: CallbackContext):
    if context.user_data.get('authorized', False):
        context.user_data['messages'] = []
        update.message.reply_text("История сообщений была сброшена. Контекст беседы забыт.")
    else: 
        update.message.reply_text("Сначала вам нужно пройти авторизацию!")

def start(update: Update, context: CallbackContext):
    if not context.user_data.get('authorized', False):
        update.message.reply_text("Сначала вам нужно пройти авторизацию!")
        return

    context.user_data['reply_all_msg'] = True
    update.message.reply_text("Теперь бот будет отвечать на всё даже без команды 'ask'.")

def stop(update: Update, context: CallbackContext):
    if not context.user_data.get('authorized', False):
        update.message.reply_text("Сначала вам нужно пройти авторизацию!")
        return

    context.user_data['reply_all_msg'] = False
    update.message.reply_text("Бот снова отвечает только по команде 'ask'.")

def ask(update: Update, context: CallbackContext):
    if not context.user_data.get('authorized', False):
        update.message.reply_text("Сначала вам нужно пройти авторизацию!")
        return

    messages = context.user_data.get('messages', [])
    user_message = update.message.text.replace('/ask ', '')
    if '/ask' in update.message.text:
        user_message = user_message.strip()
    messages.append({'role':'user', 'content': user_message})

    response = openai.ChatCompletion.create(
        model=TEXT_MODEL,
        messages=messages
    )

    generated_message_content = response['choices'][0]['message']['content']

    messages.append({'role': 'assistant', 'content': generated_message_content})
    context.user_data['messages'] = messages
    update.message.reply_text(generated_message_content)

def img(update: Update, context: CallbackContext):
    if not context.user_data.get('authorized', False):
        update.message.reply_text("Сначала вам нужно пройти авторизацию!")
        return

    prompt = update.message.text.replace("/img ", "")
    endpoint = "https://api.openai.com/v1/images/generations"
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + API_KEY}
    data = {"model": IMAGE_MODEL, "prompt": prompt}
    response = requests.post(endpoint, headers=headers, json=data)

    if response.status_code == 200:
        image_url = response.json()["data"][0]["url"]
        update.message.reply_photo(photo=image_url)
    else:
        update.message.reply_text("Этот запрос запрещен политикой OpenAI.")

def handle_message(update: Update, context: CallbackContext):
    if context.user_data.get('reply_all_msg', False):
        ask(update, context)

auth_handler = CommandHandler('auth', auth)
clear_handler = CommandHandler('clear', clear)
start_handler = CommandHandler('start', start)
stop_handler = CommandHandler('stop', stop)
ask_handler = CommandHandler('ask', ask)
img_handler = CommandHandler('img', img)
message_handler = MessageHandler(Filters.text & ~Filters.command, handle_message)

dispatcher.add_handler(auth_handler)
dispatcher.add_handler(clear_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(stop_handler)
dispatcher.add_handler(ask_handler)
dispatcher.add_handler(img_handler)
dispatcher.add_handler(message_handler)

updater.start_polling()
