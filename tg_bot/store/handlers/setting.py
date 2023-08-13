import telebot

from tg_bot.store.handlers.auth.setting import register_handler_auth
from tg_bot.store.handlers.machine.setting import register_handler_look


def register_handler(bot: telebot.TeleBot) -> None:
    register_handler_auth(bot)
    register_handler_look(bot)
