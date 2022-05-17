#!/usr/bin/python
# -*- coding: utf-8 -*-

from telegram.ext.conversationhandler import ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from api.searchForMovie import getMovieInfoFor
from modules.telegram import keyboard

ID = ""

def search(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please let me know the movie title!" )
    return 1
    
    
def findMovies(update, context):
    search_text = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text="Searching for: " + search_text )
    
    
    # TODO get movies based on 'search_text'
    movies = [
        {"id":"tt0111161","name":"The Shawshank Redemption"},
        {"id":"tt0068646","name":"The Godfather"},
        {"id":"tt0167260","name":"The Lord of the Rings: The Return of the King"},
        {"id":"tt0468569","name":"The Dark Knight"},
    ];

    movies = getMovieInfoFor(search_text)
    if not movies:
        update.message.reply_text("No movie found for this search term!", reply_markup=reply_markup)
    
    keyboard = []
    
    # get top 3 movies
    for ele in movies[:5]:
      keyboard.append([InlineKeyboardButton(ele["Title"] + " (" + str(ele['Year']) + ")", callback_data=ele["imdbID"])])
    keyboard.append([InlineKeyboardButton("Cancel", callback_data="cancel")])


    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Please choose the movie you searched for:", reply_markup=reply_markup)
    
    return done(update, context)


def done(update, context, message="That's it!"):    
    context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=keyboard.getDefaultKeyboard())
    return ConversationHandler.END
