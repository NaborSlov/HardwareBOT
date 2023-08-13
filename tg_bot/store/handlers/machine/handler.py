from django.conf import settings
from telebot.types import CallbackQuery, Message
from telebot import TeleBot
from telebot.util import quick_markup
from tg_bot.store.utils.buttons import (
    create_fix_dates,
    create_inline_list_button,
    one_button,
)
from machinery.models import IndustrialUnit, MachineNode, Element, VixDate
from django.core.paginator import Paginator


def query_create_or_look(call: CallbackQuery, bot: TeleBot) -> None:
    command = call.data.split(":")[1]
    if command == "look":
        industrial_models = IndustrialUnit.objects.all()
        paginator = Paginator(industrial_models, per_page=settings.PER_PAGE)
        count_models = paginator.page(1)
        industrial_buttons = create_inline_list_button(
            list(count_models.object_list),
            page=count_models.number,
            total_page=paginator.num_pages,
            model_name=IndustrialUnit.__name__,
        )

        bot.edit_message_text(
            "Выберете одну из опций",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=industrial_buttons,
        )

        with bot.retrieve_data(  # type: ignore
            call.from_user.id, call.message.chat.id
        ) as data:
            data["back_model"] = IndustrialUnit.__name__
            data["back_item_id"] = None
            data["item_id"] = None


def choice_list_model(call: CallbackQuery, bot: TeleBot):
    data_call = call.data.split(":")
    item_id = int(data_call[2])
    model_name = ""

    match data_call[1], item_id:
        case IndustrialUnit.__name__, _:
            model_obj = MachineNode.objects.filter(industial_unit=item_id)
            model_name = MachineNode.__name__
            back_model = IndustrialUnit.__name__
        case MachineNode.__name__, _:
            model_obj = Element.objects.filter(hardware=item_id)
            model_name = Element.__name__
            back_model = MachineNode.__name__

        case _:
            return None

    paginator = Paginator(model_obj, per_page=settings.PER_PAGE)
    models_page = paginator.page(1)
    page_button = create_inline_list_button(
        list(models_page.object_list),
        models_page.number,
        paginator.num_pages,
        model_name=model_name,
    )

    bot.edit_message_text(
        "Выберете одну из опций",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=page_button,
    )

    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:  # type: ignore
        data["back_model"] = back_model
        data["back_item_id"] = data["item_id"]
        data["item_id"] = item_id


def look_page_model(call: CallbackQuery, bot: TeleBot):
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:  # type: ignore
        item_id = data["item_id"]
    data_call = call.data.split(":")
    model_name_call = data_call[1]
    page = int(data_call[2])
    command = data_call[3]

    match model_name_call, item_id:
        case IndustrialUnit.__name__, None:
            model_obj = IndustrialUnit.objects.all()
            model_name = IndustrialUnit.__name__
        case MachineNode.__name__, _:
            model_obj = MachineNode.objects.filter(industial_unit=item_id)
            model_name = MachineNode.__name__
        case Element.__name__, _:
            model_obj = Element.objects.filter(hardware=item_id)
            model_name = Element.__name__
        case _:
            return None

    paginator = Paginator(model_obj, per_page=settings.PER_PAGE)

    if command == "next" and page < paginator.num_pages:
        page += 1
    elif command == "back" and page > 1:
        page -= 1

    models_page = paginator.page(page)
    page_button = create_inline_list_button(
        list(models_page.object_list),
        models_page.number,
        paginator.num_pages,
        model_name=model_name,
    )

    bot.edit_message_text(
        "Выберете одну из опций",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=page_button,
    )


def back_model(call: CallbackQuery, bot: TeleBot) -> None:
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:  # type: ignore
        back_model = data["back_model"]
        back_item_id = data["back_item_id"]

    match back_model, back_item_id:
        case IndustrialUnit.__name__, _:
            model_obj = IndustrialUnit.objects.all()
            model_name = IndustrialUnit.__name__
            back_model = IndustrialUnit.__name__
        case MachineNode.__name__, _:
            model_obj = MachineNode.objects.filter(industial_unit=back_item_id)
            model_name = MachineNode.__name__
            back_model = IndustrialUnit.__name__
        case Element.__name__, _:
            model_obj = Element.objects.filter(hardware=back_item_id)
            model_name = Element.__name__
            back_model = MachineNode.__name__
        case _:
            return None

    paginator = Paginator(model_obj, per_page=settings.PER_PAGE)
    models_page = paginator.page(1)
    page_button = create_inline_list_button(
        list(models_page.object_list),
        models_page.number,
        paginator.num_pages,
        model_name=model_name,
    )

    bot.edit_message_text(
        "Выберете одну из опций",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=page_button,
    )

    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:  # type: ignore
        data["back_model"] = back_model


def look_one_element(call: CallbackQuery, bot: TeleBot):
    data_call = call.data.split(":")
    item_id = int(data_call[2])

    obj_model = Element.objects.get(id=item_id)

    bot.edit_message_text(
        (
            "*Название элемента:*\n"
            f"_{obj_model.name}_\n"
            "*Описание элемента:*\n"
            f"_{obj_model.description}_\n"
            "*Приоритет:*\n"
            f"_{obj_model.get_priority_display()}_\n"  # type: ignore
            "*Количество:*\n"
            f"_{obj_model.count_fact}_\n"
            "*Необходимый запас:*\n"
            f"_{obj_model.count_need}_"
        ),
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=one_button,
        parse_mode="Markdown",
    )

    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:  # type: ignore
        data["id_element"] = item_id


def look_date_fix_element(call: CallbackQuery, bot: TeleBot):
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:  # type: ignore
        item_id = data["id_element"]

    obj_models = VixDate.objects.filter(element=item_id)

    if not obj_models:
        bot.edit_message_text(
            "Дат ремонта нет",
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            reply_markup=quick_markup(
                {"Добавить дату ремонта": {"callback_data": "date:add"}},
                row_width=1,
            ),
        )

    for date in create_fix_dates(obj_models):
        bot.send_message(
            call.message.chat.id,
            text=date,
            parse_mode="Markdown",
        )


def add_date_fix(call: CallbackQuery, bot: TeleBot):
    bot.send_message(
        call.message.chat.id,
        "Напишите описание ремонта",
    )
    bot.set_state(call.from_user.id, "date_add", call.message.chat.id)


def create_date_fix(msg: Message, bot: TeleBot):
    with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:  # type: ignore
        item_id = data["id_element"]

    vix_date = VixDate.objects.create(description=msg.text, element_id=item_id)
    obj_model = vix_date.element

    bot.send_message(msg.chat.id, "Дата добавлена")
    bot.send_message(
        msg.chat.id,
        "*Название элемента:*\n"
        f"_{obj_model.name}_\n"
        "*Описание элемента:*\n"
        f"_{obj_model.description}_\n"
        "*Приоритет:*\n"
        f"_{obj_model.get_priority_display()}_\n"  # type: ignore
        "*Количество:*\n"
        f"_{obj_model.count_fact}_\n"
        "*Необходимый запас:*\n"
        f"_{obj_model.count_need}_",
        parse_mode="Markdown",
        reply_markup=one_button,
    )


def add_model(call: CallbackQuery, bot: TeleBot):
    bot.send_message(
        call.message.chat.id,
        "Напишите название элемента",
    )

    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:  # type: ignore
        data["create_model"] = call.data.split(":")[1]

    bot.set_state(call.from_user.id, "model_add", call.message.chat.id)


def create_model(msg: Message, bot: TeleBot):
    with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:  # type: ignore
        back_item_id = data["item_id"]
        create_model = data["create_model"]

    match create_model, back_item_id:
        case IndustrialUnit.__name__, None:
            IndustrialUnit.objects.create(name=msg.text)
            model_name = IndustrialUnit.__name__
            back_models = IndustrialUnit.objects.all()
        case MachineNode.__name__, _:
            MachineNode.objects.create(
                name=msg.text, industial_unit_id=back_item_id
            )
            model_name = MachineNode.__name__
            back_models = MachineNode.objects.filter(
                industial_unit_id=back_item_id
            )
        case Element.__name__, _:
            Element.objects.create(
                name=msg.text, hardware_id=back_item_id
            )
            model_name = Element.__name__
            back_models = Element.objects.filter(hardware=back_item_id)
        case _:
            return None

    paginator = Paginator(back_models, per_page=settings.PER_PAGE)
    models_page = paginator.page(1)
    page_button = create_inline_list_button(
        list(models_page.object_list),
        models_page.number,
        paginator.num_pages,
        model_name=model_name,
    )

    bot.send_message(msg.chat.id, "Объект создан")
    bot.send_message(
        msg.chat.id,
        "Выберете одну из опций",
        reply_markup=page_button,
    )

    with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:  # type: ignore
        data["back_model"] = back_model
