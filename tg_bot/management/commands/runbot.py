import logging
from typing import Any
from django.conf import settings
from django.core.management.base import BaseCommand
import telebot

from tg_bot.main_bot import setting_bot


class Command(BaseCommand):
    help = "Run telegram bot"

    def handle(self, *args: Any, **options: Any) -> str | None:
        logging.basicConfig(level=logging.INFO)
        bot = telebot.TeleBot(token=settings.API_TOKEN)

        setting_bot(bot)
        bot.infinity_polling()
