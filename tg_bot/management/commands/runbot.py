import logging
from typing import Any
from django.core.management.base import BaseCommand
from tg_bot.main_bot import bot


class Command(BaseCommand):
    help = "Run telegram bot"

    def handle(self, *args: Any, **options: Any) -> str | None:
        logging.basicConfig(level=logging.INFO)
        bot.infinity_polling()
