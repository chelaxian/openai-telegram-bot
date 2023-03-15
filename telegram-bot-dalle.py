import requests
import logging
from telegram import Bot
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler

# setup logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# authentication token
AUTH_TOKEN = "XXXXXXXXXXXXXXX"

# flag to keep track of authentication status
authenticated = False

# function to handle /auth command
def auth(update: Update, context):
    global authenticated
    if update.message.text.split()[1] == AUTH_TOKEN:
        authenticated = True
        update.message.reply_text("Authorization successful!")
    else:
        update.message.reply_text("Incorrect password!")

# function to handle /img command
def imagine(update: Update, context):
    if not authenticated:
        update.message.reply_text("You must be logged in. Use command /auth <password>")
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

def main():
    # initialize bot
    bot = Bot(token="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    updater = Updater(bot=bot, use_context=True)
    
    # add handlers for commands
    updater.dispatcher.add_handler(CommandHandler("auth", auth))
    updater.dispatcher.add_handler(CommandHandler("img", imagine))
    
    # start bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()