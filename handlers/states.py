from aiogram.fsm.state import State, StatesGroup

class WelcomeStates(StatesGroup):
    waiting_welcome = State()

class ButtonStates(StatesGroup):
    waiting_add_button = State()
    waiting_del_button = State()

class ChannelStates(StatesGroup):
    waiting_add_channel = State()
    waiting_del_channel = State()

class BroadcastStates(StatesGroup):
    waiting_broadcast = State()
