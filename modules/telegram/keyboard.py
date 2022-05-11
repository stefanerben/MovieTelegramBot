from telegram.replykeyboardmarkup import ReplyKeyboardMarkup

def getDefaultKeyboard():
    keyboard = [['Find Streaming Platform'], ['Find Random Movie']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup
