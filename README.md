# OPEN AI - GPT3 CHAT INSIDE YOU TELEGRAM

## TELEGRAM BOT SETUP

1. Find BotFather on Telegram - type @BotFather in the search bar

2. Then, type /newbot and give your bot a name and username.

3. You will then receive a token to access the HTTP API.

4. Repeat step 1-3 for second bot (you will need 2 separate bots)


## OPEN API -GETTING ACCESS KEY
Next, go to https://beta.openai.com/account/api-keys and create a new secret key. 


## CHANGE A CODE USING THESE ACCESS keys
Finally, open the file telegram-bot-chatgpt.py in a text editor and insert your API keys in the designated places:
 - line 7 - open api key between " "
 - line 10 - telegram token between ' '
 - line 15 - your auth password " "
 
Theb, open the file telegram-bot-dalle.py in a text editor and insert your API keys in the designated places:
 - line 44 - open api key between " "
 - line 68 - telegram token between " "
 - line 15 - your auth password " "
 
## RUN server.py on your server
    python3 telegram-bot-chatgpt.py > outputfile_for_stdout &
    python3 telegram-bot-dalle.py > outputfile_for_stdout &

## TRY CHATTING WITH telegram-bot-chatgpt
    "/auth + password" - Login to Bot to get access to chating
    "/ask + prompt" - Ask any question to Bot
    "/start" - Allow Bot to be asked by you
    "/stop" - Forbid Bot to be asked by you
    "/clear" - History clearing (drop previous context) and starting new chat
    
## TRY CHATTING WITH telegram-bot-dalle
    "/auth + password" - Login to Bot to get access to chating
    "/img + prompt" - Describe to Bot what you want to draw
    
Remember that ChatBot works with all users individually. If you add it to group chat, all users who want to interract with it have to do same "auth + start" procedure before they can "ask" it anything.

Examples for telegram-bot-chatgpt:
/auth P@ssword
/start
/ask write a tweet about why is important to have work-life-balance
/clear
/stop

Examples for telegram-bot-dalle:
/auth P@ssword
/img beautiful red cat in garden
