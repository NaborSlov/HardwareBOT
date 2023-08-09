import telebot

from tg_bot.store.handlers.auth.handler import register_handler_auth
from tg_bot.store.handlers.look_machine.handler import register_handler_look


def register_handler(bot: telebot.TeleBot) -> None:
    register_handler_auth(bot)
    register_handler_look(bot)
