import openai
import requests
import telegram
from telegram import Update
from telegram.ext import Updater, MessageHandler, CommandHandler, CallbackContext, Filters

# Replace with the API key for your OpenAI account
openai.api_key = "YOUR_OPENAI_API_KEY"

# Replace with the bot token you received from BotFather
updater = Updater(token='BOT_TOKEN', use_context=True)
dispatcher = updater.dispatcher

# Authorize user
def auth(update: Update, context: CallbackContext):
    if update.message.text == "/auth YOUR_SECRET_PASSWORD":
        context.user_data['authorized'] = True
        update.message.reply_text("Authorization passed successfully!")
    else:
        update.message.reply_text("Incorrect password!")

# Start handling messages
def start(update: Update, context: CallbackContext):
    if context.user_data['authorized'] == True:
        context.user_data['ignore'] = False
        update.message.reply_text("I start listening to messages and replying to them.")
    else: 
        update.message.reply_text("\nFirst you need to pass authorization!")

# Stop handling messages
def stop(update: Update, context: CallbackContext):
    if context.user_data['authorized'] == True:
        context.user_data['ignore'] = True
        update.message.reply_text("I no longer listen to messages and do not answer them.")
    else: 
        update.message.reply_text("First you need to pass authorization!")

# Clear history of messages
def clear(update: Update, context: CallbackContext):
    if context.user_data['authorized'] == True:
        context.user_data['history'] = []
        update.message.reply_text("The message history has been reset. The context of the conversation is forgotten.")
    else: 
        update.message.reply_text("First you need to pass authorization!")

# Handle messages
def ask(update: Update, context: CallbackContext):
    if not context.user_data.get('authorized', False):
        update.message.reply_text("First you need to pass authorization!")
        return

    context.user_data['history'] = context.user_data.get('history', []) + [update.message.text.replace('/ask ', '')]
    prompt = ' '.join(context.user_data['history'])

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.5,
    ).choices[0].text

    context.user_data['history'] = context.user_data.get('history', []) + [response]
    update.message.reply_text(response)

# Handle image generation
def img(update: Update, context: CallbackContext):
    if not context.user_data.get('authorized', False):
        update.message.reply_text("First you need to pass authorization!")
        return

    # get text prompt from user message
    prompt = update.message.text.replace("/img ", "")

    # OpenAI API endpoint
    endpoint = "https://api.openai.com/v1/images/generations"

    # request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    }

    # request data
    data = {
        "model": "image-alpha-001",
        "prompt": prompt
    }

    # send API request
    response = requests.post(endpoint, headers=headers, json=data)

    # check if request was successful
    if response.status_code == 200:
        # extract generated image from response
        image_url = response.json()["data"][0]["url"]

        # send generated image to user
        update.message.reply_photo(photo=image_url)
    else:
        update.message.reply_text("This request is prohibited by OpenAi policy.")

auth_handler = CommandHandler('auth', auth)
start_handler = CommandHandler('start', start)
stop_handler = CommandHandler('stop', stop)
clear_handler = CommandHandler('clear', clear)
ask_handler = CommandHandler('ask', ask)
img_handler = CommandHandler('img', img)

dispatcher.add_handler(auth_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(stop_handler)
dispatcher.add_handler(clear_handler)
dispatcher.add_handler(ask_handler)
dispatcher.add_handler(img_handler)

updater.start_polling()
