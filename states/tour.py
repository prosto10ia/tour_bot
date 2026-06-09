from aiogram.fsm.state import State, StatesGroup


class TourSelection(StatesGroup):
    # Состояния пошагового подбора тура.
    waiting_for_budget = State()
    waiting_for_country = State()
    waiting_for_dates = State()
    waiting_for_hotel_stars = State()
