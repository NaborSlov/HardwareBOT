from typing import Any
from telebot.util import quick_markup
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from machinery.models import VixDate

one_button = quick_markup(
    {
        "Показать даты ремонта": {"callback_data": "date:look"},
        "Добавить дату ремонта": {"callback_data": "date:add"},
    },
    row_width=1,
)

quest_after_auth = quick_markup(
    {
        "Показать оборудование": {"callback_data": "ans:look"},
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
        markup.add(button, row_width=1)

    markup.add(
        InlineKeyboardButton(
            text="<---", callback_data=f"page:{model_name}:{page}:back"
        ),
        InlineKeyboardButton(text=f"{page}/{total_page}", callback_data=" "),
        InlineKeyboardButton(
            text="--->", callback_data=f"page:{model_name}:{page}:next"
        ),
        row_width=3,
    )
    markup.add(
        InlineKeyboardButton(text="Назад", callback_data="back_model"),
        InlineKeyboardButton(
            text="Создать", callback_data=f"create:{model_name}"
        ),
        row_width=2,
    )

    return markup


def create_fix_dates(dates: list[VixDate]) -> list[str]:
    dates_str = []

    for date in dates:
        date_format = date.data_fix.strftime("%M:%H %d.%m.%Y")
        dates_str.append(
            "*Дата ремонта:*\n"
            f"_{date_format}_\n"
            "*Описание ремонта:*\n"
            f"_{date.description}_"
        )

    return dates_str
