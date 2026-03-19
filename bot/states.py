from aiogram.fsm.state import State, StatesGroup


class SearchStates(StatesGroup):
    waiting_for_query = State()


class PromoStates(StatesGroup):
    waiting_for_code = State()
