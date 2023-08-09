from django.conf import settings
from telebot.types import CallbackQuery, Message
from telebot import TeleBot
from tg_bot.store.handlers.state import StateAuth
from tg_bot.store.utils.buttons import create_inline_list_button, one_button
from machinery.models import IndustrialUnit, MachineNode, Hardware, Element
from django.core.paginator import Paginator


def main_menu(msg: Message, bot: TeleBot):
    pass


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
            data["item_id"] = None

    else:
        pass


def choice_list_model(call: CallbackQuery, bot: TeleBot):
    data_call = call.data.split(":")
    item_id = int(data_call[2])
    model_name = ""

    match data_call[1], item_id:
        case IndustrialUnit.__name__, _:
            model_obj = MachineNode.objects.filter(industial_unit=item_id)
            model_name = MachineNode.__name__
        case MachineNode.__name__, _:
            model_obj = Hardware.objects.filter(machine_node=item_id)
            model_name = Hardware.__name__
        case Hardware.__name__, _:
            model_obj = Element.objects.filter(hardware=item_id)
            model_name = Element.__name__
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
        case Hardware.__name__, _:
            model_obj = Hardware.objects.filter(machine_node=item_id)
            model_name = Hardware.__name__
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


def register_handler_look(bot: TeleBot) -> None:
    bot.register_message_handler(
        main_menu, commands=["main_menu"], state=StateAuth.is_auth
    )

    bot.register_callback_query_handler(
        query_create_or_look,
        state=StateAuth.is_auth,
        func=lambda call: call.data.split(":")[0] == "ans",
        pass_bot=True,
    )

    bot.register_callback_query_handler(
        look_one_element,
        state=StateAuth.is_auth,
        func=lambda call: call.data.split(":")[0] == "one"
        and call.data.split(":")[1] == Element.__name__,
        pass_bot=True,
    )

    bot.register_callback_query_handler(
        choice_list_model,
        state=StateAuth.is_auth,
        func=lambda call: call.data.split(":")[0] == "one",
        pass_bot=True,
    )

    bot.register_callback_query_handler(
        look_page_model,
        func=lambda call: call.data.split(":")[0] == "page",
        pass_bot=True,
    )
