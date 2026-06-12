from aiogram.fsm.state import State, StatesGroup


class TourSelection(StatesGroup):
    # Состояния сценария обычного подбора тура.
    waiting_for_tour_type = State()
    waiting_for_country = State()
    waiting_for_month = State()


class HotTourSelection(StatesGroup):
    # Состояние сценария горящих туров.
    waiting_for_month = State()
