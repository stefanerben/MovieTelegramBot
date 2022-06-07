from telegram.replykeyboardmarkup import ReplyKeyboardMarkup

def getDefaultKeyboard():
    keyboard = [['🔎 Search Movie'], ['🔀 Random Movie']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup
