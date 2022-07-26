from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import sqlite3
from database_functions import insert_user, insert_link, create_user_table, update_user


# Set the API key
secret_api_key="YOUR KEY HERE"

# Defining database
user_database='users.db'

# Initial connection to database, necessary for some reason
conn = sqlite3.connect(user_database, check_same_thread=False)

def start(update, context):
    # SEND A MESSAGE WHEN USER SENDS /START
    update.message.reply_text('Hi! Please set settings for me to work!')
    
    # CONVERT CHATID TO A SUITABLE STRING FOR TABLENAME IN SQLITE
    chatid = update.message.chat_id
    userid = "user" + str(chatid)

    # INSERT USER TO USERS TABLE
    insert_user(chatid, "", "")

    print("Inserted new user: {}".format(chatid))


     # CREATE USER<CHATID> TABLE
    create_user_table(userid)

    print("Created new table for user: {}".format(userid))
    
    

def set_settings(update,context):
    """Set the keywords to search for and the subreddits to search."""
    # REMOVE "/settings" FROM THE MESSAGE CONTENT
    parameters = update.message.text[10:]
    
    # A LOT OF FUCKERY TO GET THE KEYWORDS FROM MESSAGE CONTENT
    # There is probably a way better way to this but this works for now
    keywords = parameters.split("-")[0]
    keywords = keywords[1:-2]
    keywords = keywords.split('"')
    keywords = [keyword for keyword in keywords if len(keyword)>1]
    keywords = "|".join(keywords)

    # GET SUBREDDITS FROM MESSAGE CONTENT
    subreddits = str(parameters.split("-")[1])
    subreddits = subreddits.strip()
    
    id = update.message.chat_id
    update_user(id, keywords, subreddits)
    print("Updated preferences for user {}".format(id))


def echo(update, context):
    """Just a function to echo whatever the user sends for debugging purposes"""
    update.message.reply_text(update.message.text)


def send_message(chat_id, message):
    # SENDS UPDATES TO USER
    updater = Updater(secret_api_key, use_context=True)

    updater.bot.send_message(chat_id, message)
    print("Sent message: {} to chat {}".format(message,chat_id))

    

def main():
    """Starts the bot."""
    updater = Updater(secret_api_key, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands do different things
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("settings", set_settings))

    # if not a command, just echo the message
    dp.add_handler(MessageHandler(Filters.text, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you kill the process
    updater.idle()



