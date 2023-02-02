import openai
import telegram
from telegram import Update
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters

def start(update: Update, context):
    context.user_data['ignored'] = False
    update.message.reply_text("Started listening to messages")

def stop(update: Update, context):
    context.user_data['ignored'] = True
    update.message.reply_text("Stopped listening to messages")

def clear(update: Update, context):
    context.user_data.clear()
    update.message.reply_text("History cleared")

def respond(update: Update, context):
    if 'ignored' in context.user_data and context.user_data['ignored']:
        return

    openai.api_key = "YOUR_OPENAI_API_KEY"
    model_engine = "text-davinci-003"
    prompt = f"{' '.join(context.user_data.get('history', []))} {update.message.text}"

    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.5,
    ).choices[0].text

    context.user_data['history'] = context.user_data.get('history', []) + [update.message.text, response]
    update.message.reply_text(response)

def main():
    openai.api_key = "YOUR_OPENAI_API_KEY"
    updater = Updater("YOUR_TELEGRAM_BOTFATHER_TOKEN", use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(CommandHandler("clear", clear))
    dp.add_handler(MessageHandler(Filters.text, respond))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
