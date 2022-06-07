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
    context.bot.send_message(chat_id=update.effective_chat.id, text="🚀 Searching for your movie...")

    movies = getMovieInfoFor(search_text)
    if not movies:
        update.message.reply_text("⛔ No movies found for your search term!", reply_markup=keyboard.getDefaultKeyboard())
        return -1
    
    new_keyboard = []
    for ele in movies[:5]:
      new_keyboard.append([InlineKeyboardButton(ele["Title"] + " (" + str(ele['Year']) + ")", callback_data=ele["imdbID"])])
    new_keyboard.append([InlineKeyboardButton("Cancel", callback_data="cancel")])


    reply_markup = InlineKeyboardMarkup(new_keyboard)
    update.message.reply_text("Please choose the movie you searched for:", reply_markup=reply_markup)
    
    return -1


def done(update, context, message="That's it!"):    
    context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=keyboard.getDefaultKeyboard())
    return ConversationHandler.END
