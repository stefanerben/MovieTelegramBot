#!/usr/bin/python
# -*- coding: utf-8 -*-

import random, config, traceback
from api.posterImage import getPosterImage
from api.streamingAvailability import getStreamingAvailabilityFor
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
    print(query)
    
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
        
        # get random movie id (top 50 movies of Germany)
        movie_ids = ["tt0111161","tt0468569","tt0108052","tt0099685","tt0114369","tt0102926","tt0245429","tt0120689","tt0816692","tt010306","tt005421","tt017249","tt040788","tt167543","tt007874","tt020914","tt008297","tt185372","tt040509","tt011969","tt134583","tt009060","tt531151","tt011257","tt098626","tt036174","tt507435","tt007185","tt037278","tt696669","tt034714","tt026897","tt099384","tt009628","tt113088","tt012038","tt472943","tt810819","tt226799","tt211953","tt011871","tt026446","tt139221","tt089276","tt331534","tt007947","tt008754","tt040550","tt443021","tt485726"]
        imbd_id = random.choice(movie_ids)

    
    print("getMovieInformation")

    
    # TODO: get data from api via 'imbd_id'
    data = getStreamingAvailabilityFor(imbd_id)
    
    name = data['originalTitle'] # The Lord of the Rings: The Fellowship of the Ring
    imdb_rating = data['imdbRating'] # 88 (int)
    # backdrop_url = data['backdropURLs']['original'] # https://image.tmdb.org/t/p/original/vRQnzOn4HjIMX4LBq9nHhFXbsSu.jpg
    countries = data['countries'] # ["NZ", "US"]
    year = data['year'] # 2001 (int)
    # runtime = data['runtime'] # 179 (int)
    cast = data['cast'] # ["Elijah Wood", "Ian McKellen", "Liv Tyler", "Viggo Mortensen", "Sean Bean", "Sean Astin", "Cate Blanchett"]
    overview = data['overview'] # "Young hobbit Frodo Baggins, after inheriting a mysterious ring from his uncle Bilbo, must leave his home in order to keep it from falling into the hands of its evil creator. Along the way, a fellowship is formed to protect the ringbearer and make sure that the ring arrives at its final destination: Mt. Doom, the only place where it can be destroyed."
    tagline = data['tagline'] # "One ring to rule them all"
    poster_url = data['posterURLs']['original'] # "https://image.tmdb.org/t/p/original/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg"
    streaming_info = data['streamingInfo'] # "hbo":{ "us":{ "link":"https://play.hbomax.com/page/urn:hbo:page:GXdu2ZAglVJuAuwEAADbA:type:feature", "added":1606841026, "leaving":0 }}

    streaming_services = []
    for service in streaming_info:
        if service == 'hbo':
            continue
        for country in streaming_info[service]:
            streaming_services.append({
                "name" : service,
                "link" : streaming_info[service][country]['link']
            })

    if len(streaming_services) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, this movie is not available for streaming in your country!")
        return
        
    keyboard = []
    
    for service in streaming_services:
        keyboard.append([InlineKeyboardButton(service['name'], url=service['link'])])
    keyboard.append([InlineKeyboardButton("Cancel", callback_data="cancel")])

    posterData = {
        "posterUrl" : poster_url,
        "name" : name,
        "availableAt" : [
            [x['name'] for x in streaming_services],
        ]
    }

    print(posterData)


    getPosterImage(posterData)

    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Have fun streaming:", reply_markup=reply_markup)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('image.png', 'rb'))

    
    return 

def error_callback(update, context):
    message = 'Update ' + str(update) + ' caused error ' + str(context.error)
    logger.warning(message)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=keyboard.getDefaultKeyboard())


if __name__ == '__main__':
    main()