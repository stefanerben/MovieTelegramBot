#!/usr/bin/python
# -*- coding: utf-8 -*-

import random, os
from time import sleep
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



TOKEN = '5363080082:AAHltCun16zDne1St_7dGuaJTMIoQPYu0_E' # @movie_syi_bot


def main():
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    keyboard_handler = CommandHandler('keyboard', getkeyboard)
    dispatcher.add_handler(keyboard_handler)
    
    cancel_handler = CommandHandler('cancel', cancel)
    dispatcher.add_handler(cancel_handler)

    movieInfo_handler = MessageHandler(Filters.regex('^(🔀 Random Movie)$'), getMovieInformation)
    dispatcher.add_handler(movieInfo_handler)

    content_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^(🔎 Search Movie)$'), conversionhandler.search)],
        states={
            1: [MessageHandler(Filters.text & (~Filters.command), conversionhandler.findMovies)],
        },
        fallbacks=[CommandHandler('cancel', conversionhandler.done)]
    )
    dispatcher.add_handler(content_handler)
    
    dispatcher.add_handler(CallbackQueryHandler(button))
    
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    dispatcher.add_error_handler(error_callback)
        
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
        
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=query.message.message_id)
    

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Movie Finder is online")
    
def getkeyboard(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="What do you like to do?", reply_markup=keyboard.getDefaultKeyboard())
    
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I couldn't understand this...")
   
def cancel(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ok, let's reset ...", reply_markup=keyboard.getDefaultKeyboard())



def getMovieInformation(update, context, imbd_id=""):
    if imbd_id == "":
        context.bot.send_message(chat_id=update.effective_chat.id, text="Finding a random movie...")
        data = getRandomMovie()
    else:
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

    streaming_services = getStreamingServices(data['streamingInfo'])
    
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

    getPosterImage(posterData)

    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Have fun streaming:", reply_markup=reply_markup)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('image.png', 'rb'))
    return 

def getStreamingServices(streaming_info):
    streaming_services = []
    for service in streaming_info:
        if service == 'hbo':
            continue
        for country in streaming_info[service]:
            streaming_services.append({
                "name" : service,
                "link" : streaming_info[service][country]['link']
            })

    return streaming_services


def getRandomMovie():
    files = os.listdir('cache/')
    imdbs = []
    for ele in files:
        if "availabilityOf_" in ele:
            imdb = ele.replace('availabilityOf_', '').replace('.json', '')
            imdbs.append(imdb)

    imbd_id = random.choice(imdbs)
    data = getStreamingAvailabilityFor(imbd_id)

    streaming_services = []
    while not data or len(streaming_services) == 0:
        imbd_id = random.choice(imdbs)
        data = getStreamingAvailabilityFor(imbd_id)
        streaming_services = getStreamingServices(data['streamingInfo'])
        sleep(3)

    return data


def error_callback(update, context):
    message = 'Update ' + str(update) + ' caused error ' + str(context.error)
    logger.warning(message)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=keyboard.getDefaultKeyboard())


if __name__ == '__main__':
    main()