# OPEN AI - GPT3 CHAT INSIDE YOU TELEGRAM

## TELEGRAM BOT SETUP

1. Find BotFather on Telegram - type @BotFather in the search bar

2. Then, type /newbot and give your bot a name and username.

3. You will then receive a token to access the HTTP API.



## OPEN API -GETTING ACCESS KEY
Next, go to https://beta.openai.com/account/api-keys and create a new secret key. 


## CHANGE A CODE USING THESE ACCESS keys
Finally, open the file server.py in a text editor and insert your API keys in the designated places:
 - line 7 - open api key between " "
 - line 10 - telegram token between ' '
 - line 15 - your auth password " "

## RUN server.py on your server
    python3 server.py

## TRY CHATTING WITH GPT3
    "/auth + password" - Login to Bot to get access to chating
    "/ask + prompt" - Ask any question to Bot
    "/start" - Allow Bot to be asked by you
    "/stop" - Forbid Bot to be asked by you
    "/clear" - History clearing (drop previous context) and starting new chat
    
Remember that ChatBot works with all users individually. If you add it to group chat, all users who want to interract with it have to do same "auth + start" procedure before they can "ask" it anything.

Examples:
/auth P@ssword
/start
/ask write a tweet about why is important to have work-life-balance
/clear
/stop
