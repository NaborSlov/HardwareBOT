from telebot.handler_backends import State, StatesGroup


class StateAuth(StatesGroup):
    login = State()
    password = State()
    is_auth = State()


class StateLookMachine(StatesGroup):
    industrial = State()
    machine_node = State()
    hardware = State()
    element = State()
