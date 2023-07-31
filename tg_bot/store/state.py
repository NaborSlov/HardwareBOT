from telebot.handler_backends import StatesGroup, State


class StateAuth(StatesGroup):
    login = State()
    password = State()
    is_auth = State()
    

class StateView(StatesGroup):
    indust_unit = State()
    machine_node = State()
    hardware = State()
    element = State()
    
    