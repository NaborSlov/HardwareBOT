from telebot import TeleBot

from tg_bot.store.handlers.auth.handler import (
    auth_login,
    auth_password,
    exit_bot,
    start_auth_user,
    start_login,
)
from tg_bot.store.handlers.state import StateAuth


def register_handler_auth(bot: TeleBot) -> None:
    bot.register_message_handler(
        start_login, commands=["login"], pass_bot=True
    )
    bot.register_message_handler(exit_bot, commands=["exit"], pass_bot=True)
    bot.register_message_handler(
        start_auth_user,
        commands=["start"],
        pass_bot=True,
    )
    bot.register_message_handler(
        auth_login, state=StateAuth.login, pass_bot=True
    )
    bot.register_message_handler(
        auth_password, state=StateAuth.password, pass_bot=True
    )
