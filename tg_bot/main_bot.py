from telebot.custom_filters import StateFilter
import telebot

from tg_bot.store.handlers.setting import register_handler


def setting_bot(bot: telebot.TeleBot) -> None:
    bot.add_custom_filter(StateFilter(bot))
    register_handler(bot)
