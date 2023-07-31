from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


read_db = InlineKeyboardButton("Посмотреть оборудование", callback_data="/read_hard")
create_db = InlineKeyboardButton("Создать оборудование", callback_data="/create_hard")

quest_db = InlineKeyboardMarkup(keyboard=[[read_db], [create_db]])