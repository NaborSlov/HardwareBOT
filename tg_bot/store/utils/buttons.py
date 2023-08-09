from typing import Any
from telebot.util import quick_markup
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

one_button = quick_markup(
    {"Показать даты ремонта": {"callback_data": "date:look"}}
)

quest_after_auth = quick_markup(
    {
        "Показать оборудование": {"callback_data": "ans:look"},
        "Создать оборудование": {"callback_data": "ans:create"},
    },
    row_width=1,
)


def create_inline_list_button(
    obj_list: list[Any], page: int, total_page: int, model_name: str
) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()

    list_button = [
        InlineKeyboardButton(
            text=item.__str__(), callback_data=f"one:{model_name}:{item.id}"
        )
        for item in obj_list
    ]
    for button in list_button:
        markup.add(button)

    markup.add(
        InlineKeyboardButton(
            text="<--- Назад", callback_data=f"page:{model_name}:{page}:back"
        ),
        InlineKeyboardButton(text=f"{page}/{total_page}", callback_data=" "),
        InlineKeyboardButton(
            text="Вперёд --->", callback_data=f"page:{model_name}:{page}:next"
        ),
    )

    return markup
