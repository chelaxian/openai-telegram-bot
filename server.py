import openai
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
        update.message.reply_text("Authorization successful.")
    else:
        update.message.reply_text("Authorization failed.")

# Start handling messages
def start(update: Update, context: CallbackContext):
    context.user_data['ignore'] = False
    update.message.reply_text("Started handling messages.")

# Stop handling messages
def stop(update: Update, context: CallbackContext):
    context.user_data['ignore'] = True
    update.message.reply_text("Stopped handling messages.")

# Clear history of messages
def clear(update: Update, context: CallbackContext):
    context.user_data['history'] = []
    update.message.reply_text("History cleared.")

# Handle messages
def handle_message(update: Update, context: CallbackContext):
    if not context.user_data.get('authorized', False):
        update.message.reply_text("You are not authorized.")
        return

    if context.user_data.get('ignore', True):
        return

    context.user_data['history'] = context.user_data.get('history', []) + [update.message.text]
    prompt = ' '.join(context.user_data['history'])

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    ).choices[0].text

    context.user_data['history'] = context.user_data.get('history', []) + [response]
    update.message.reply_text(response)

auth_handler = CommandHandler('auth', auth)
start_handler = CommandHandler('start', start)
stop_handler = CommandHandler('stop', stop)
clear_handler = CommandHandler('clear', clear)
message_handler = MessageHandler(Filters.text & (~Filters.command), handle_message)

dispatcher.add_handler(auth_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(stop_handler)
dispatcher.add_handler(clear_handler)
dispatcher.add_handler(message_handler)

updater.start_polling()
