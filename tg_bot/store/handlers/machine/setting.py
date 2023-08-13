from telebot import TeleBot
from machinery.models import Element
from tg_bot.store.handlers.machine.handler import (
    add_date_fix,
    add_model,
    back_model,
    choice_list_model,
    create_date_fix,
    create_model,
    look_one_element,
    look_page_model,
    query_create_or_look,
    look_date_fix_element,
)
from tg_bot.store.handlers.state import StateAuth


def register_handler_look(bot: TeleBot) -> None:
    bot.register_callback_query_handler(
        query_create_or_look,
        state=StateAuth.is_auth,
        func=lambda call: call.data.split(":")[0] == "ans",
        pass_bot=True,
    )

    bot.register_callback_query_handler(
        look_one_element,
        func=lambda call: call.data.split(":")[0] == "one"
        and call.data.split(":")[1] == Element.__name__,
        pass_bot=True,
    )

    bot.register_callback_query_handler(
        choice_list_model,
        func=lambda call: call.data.split(":")[0] == "one",
        pass_bot=True,
    )

    bot.register_callback_query_handler(
        look_page_model,
        func=lambda call: call.data.split(":")[0] == "page",
        pass_bot=True,
    )

    bot.register_callback_query_handler(
        back_model,
        func=lambda call: call.data.split(":")[0] == "back_model",
        pass_bot=True,
    )

    bot.register_callback_query_handler(
        look_date_fix_element,
        func=lambda call: call.data == "date:look",
        pass_bot=True,
    )

    bot.register_callback_query_handler(
        add_date_fix,
        func=lambda call: call.data == "date:add",
        pass_bot=True,
    )
    bot.register_message_handler(
        create_date_fix,
        state="date_add",
        pass_bot=True,
    )

    bot.register_callback_query_handler(
        add_model,
        func=lambda call: call.data.split(":")[0] == "create",
        pass_bot=True,
    )
    
    bot.register_message_handler(
        create_model,
        state="model_add",
        pass_bot=True,
    )
