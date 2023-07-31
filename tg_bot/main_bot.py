from django.conf import settings
import telebot
from telebot.custom_filters import StateFilter
from telebot.types import Message
from tg_bot.store.state import StateAuth
from tg_bot.models import TgUser
from tg_bot.store.buttons import quest_db

bot = telebot.TeleBot(token=settings.API_TOKEN)
bot.add_custom_filter(StateFilter(bot))


@bot.message_handler(commands=["login"])
def start_login(msg: Message) -> None:
    bot.set_state(msg.from_user.id, StateAuth.login, msg.chat.id)
    bot.send_message(msg.chat.id, "Введите логин")


@bot.message_handler(commands=["exit"])
def exit_bot(msg: Message) -> None:
    bot.delete_state(msg.from_user.id, msg.chat.id)


@bot.message_handler(state=StateAuth.login)
def auth_login(msg: Message) -> None:
    bot.set_state(msg.from_user.id, StateAuth.password, msg.chat.id)
    with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
        data["login"] = msg.text
    bot.send_message(msg.chat.id, "Введите пароль")


@bot.message_handler(state=StateAuth.password)
def auth_password(msg: Message) -> None:
    with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
        try:
            tg_user: TgUser = TgUser.objects.get(login=data.get("login"))
        except TgUser.DoesNotExist:
            tg_user = False

    if not tg_user or not tg_user.check_password(msg.text):
        bot.set_state(msg.from_user.id, StateAuth.login, msg.chat.id)
        bot.send_message(
            msg.chat.id,
            "Неправильный логин или пароль.\nПопробуйте еще раз ввести логин и пароль.",
        )
        return None

    bot.set_state(msg.from_user.id, StateAuth.is_auth, msg.chat.id)
    bot.send_message(
        msg.chat.id,
        text="Вы авторизованны,\nвыберите чтение или создание",
        reply_markup=quest_db,
    )


@bot.message_handler(commands=["read_hard"])
def test_read(msg: Message):
    bot.send_message(msg.chat.id, "test")
