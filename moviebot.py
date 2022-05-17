#!/usr/bin/python
# -*- coding: utf-8 -*-

import random, config, traceback
from logging import basicConfig, INFO, getLogger

from modules.telegram import keyboard, conversionhandler

from telegram.ext import CallbackQueryHandler, CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext.conversationhandler import ConversationHandler
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=INFO)
logger = getLogger(__name__)

config.init()
config.DEBUG = True
        
if config.DEBUG:
    print("####### STARTING IN DEBUG MODE #######")

TOKEN = '5363080082:AAHltCun16zDne1St_7dGuaJTMIoQPYu0_E' # @movie_syi_bot


"""##########################################################"""

def main():
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    
    # start_handler = CommandHandler('start', start, Filters.chat(ALLOWED_USERS))
    
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    start_handler = CommandHandler('test', testing)
    dispatcher.add_handler(start_handler)

    keyboard_handler = CommandHandler('keyboard', getkeyboard)
    dispatcher.add_handler(keyboard_handler)
    
    cancel_handler = CommandHandler('cancel', cancel)
    dispatcher.add_handler(cancel_handler)

    movieInfo_handler = MessageHandler(Filters.regex('^(Find Random Movie)$'), getMovieInformation)
    dispatcher.add_handler(movieInfo_handler)

    content_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^(Find Streaming Platform)$'), conversionhandler.search)],
        # entry_points=[CommandHandler('conversation', conversionhandler.search)],
        states={
            1: [MessageHandler(Filters.text & (~Filters.command), conversionhandler.findMovies)],
        },
        fallbacks=[CommandHandler('cancel', conversionhandler.done)]
    )
    dispatcher.add_handler(content_handler)
    
    
    dispatcher.add_handler(CallbackQueryHandler(button))
    
    
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)
    
    if not config.DEBUG:
        dispatcher.add_error_handler(error_callback)
        
    #updater.bot.send_message(chat_id=config.CHAT_ID, text="ContentEngine Online!", reply_markup=getDefaultKeyboard())
    updater.start_polling()
    updater.idle()


def button(update, context):
    # Parses the CallbackQuery and updates the message text.
    query = update.callback_query
    
    if "tt" in query.data:
        getMovieInformation(update, context, imbd_id=query.data)
    elif query.data == "cancel":
        pass
    else:
        print("Unknown Callback data")
        
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Selected option: {query.data}", reply_markup=keyboard.getDefaultKeyboard())
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=query.message.message_id)
    

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Movie Finder is online")
    #keyboard(update, context)
    
def testing(update, context):
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [InlineKeyboardButton("Option 3", callback_data="1")],
        [InlineKeyboardButton("Option 3", callback_data="2")],
        [InlineKeyboardButton("Option 3", callback_data="3")],
        [InlineKeyboardButton("Cancel", callback_data="STOP")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Please choose:", reply_markup=reply_markup)

    
def getkeyboard(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="What do you like to do?", reply_markup=keyboard.getDefaultKeyboard())
    
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I couldn't understand this...")
   
def cancel(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ok, let's reset ...", reply_markup=keyboard.getDefaultKeyboard())


def keyboardcommand(update, context):
    message = update.message.text
    
    if message == 'Find Streaming Platform':
        try:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Mache einen MarketOverview Post...")
            #filepath = generateMarketOverview()
            #context.bot.send_document(chat_id=update.effective_chat.id, document=open(filepath, 'rb'))
        except Exception as e:
            print(e)
            context.bot.send_message(chat_id=config.CHAT_ID, text="Fehler bei MarketOverview:\n\n" + str(traceback.format_tb(e.__traceback__)))

    elif message == "Find Random Movie":
        print("Find Random Movie")
        
        getMovieInformation(update, context, imbd_id="")
        
    return -1 # To end the conversation handler



def getMovieInformation(update, context, imbd_id=""):
    if imbd_id == "":
        # TODO: add more ids to improve the results
        
        # get random movie id
        movie_ids = ["tt0111161", "tt0068646", "tt0167260", "tt0468569"]
        imbd_id = random.choice(movie_ids)

    
    print("getMovieInformation")

    
    # TODO: get data from api via 'imbd_id'
    
    # Demo Data
    name = "Spider-Man"
    streaming_services = [
        {"name":"Netflix","link":"https://www.netflix.com/title/60004481"},
        {"name":"Amazon Prime","link":"https://www.amazon.de/gp/video/detail/amzn1.dv.gti.bea9f6bc-f205-6fb2-bfef-2a99f8a81a41"},
    ] 
        
    keyboard = []
    
    for service in streaming_services:
        keyboard.append([InlineKeyboardButton(service['name'], url=service['link'])])
    keyboard.append([InlineKeyboardButton("Cancel", callback_data="cancel")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Have fun streaming:", reply_markup=reply_markup)

    
    return 

def error_callback(update, context):
    message = 'Update ' + str(update) + ' caused error ' + str(context.error)
    logger.warning(message)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=keyboard.getDefaultKeyboard())


if __name__ == '__main__':
    main()