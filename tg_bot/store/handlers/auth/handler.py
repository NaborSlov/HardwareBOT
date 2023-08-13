from telebot import TeleBot
from telebot.types import Message

from tg_bot.models import TgUser
from tg_bot.store.handlers.state import StateAuth
from tg_bot.store.utils.buttons import quest_after_auth


def start_login(msg: Message, bot: TeleBot) -> None:
    bot.set_state(msg.from_user.id, StateAuth.login, msg.chat.id)
    bot.send_message(msg.chat.id, "Введите логин")


def start_auth_user(msg: Message, bot: TeleBot) -> None:
    user = TgUser.objects.filter(tg_login=msg.from_user.id).first()
    if not user:
        bot.delete_state(msg.from_user.id, msg.chat.id)
        bot.send_message(
            msg.chat.id,
            ("Вы не авторизованы,\n" "авторизуйтесь по команде\n" "/login"),
        )
        return None

    bot.set_state(msg.from_user.id, StateAuth.is_auth, msg.chat.id)
    bot.send_message(
        msg.chat.id,
        text="Выберите чтение или создание",
        reply_markup=quest_after_auth,
    )


def exit_bot(msg: Message, bot: TeleBot) -> None:
    bot.delete_state(msg.from_user.id, msg.chat.id)
    bot.send_message(
        msg.chat.id,
        (
            "Вы вышли из аккаунта,\n"
            "для новой авторизации воспользуйтесь командой\n"
            "/login"
        ),
    )


def auth_login(msg: Message, bot: TeleBot) -> None:
    bot.set_state(msg.from_user.id, StateAuth.password, msg.chat.id)
    with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
        data["login"] = msg.text
    bot.send_message(msg.chat.id, "Введите пароль")


def auth_password(msg: Message, bot: TeleBot) -> None:
    with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
        try:
            tg_user = TgUser.objects.get(login=data.get("login"))
        except TgUser.DoesNotExist:
            bot.set_state(msg.from_user.id, StateAuth.login, msg.chat.id)
            bot.send_message(
                msg.chat.id,
                "Неправильный логин или пароль.\nПопробуйте еще раз.",
            )
            return None

        tg_user.tg_login = msg.from_user.id
        tg_user.save()

        bot.set_state(msg.from_user.id, StateAuth.is_auth, msg.chat.id)
        bot.send_message(
            msg.chat.id,
            text="Вы авторизованны,\nвыберите чтение или создание",
            reply_markup=quest_after_auth,
        )
