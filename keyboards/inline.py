from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_menu() -> InlineKeyboardMarkup:
    # Главное меню пользователя.
    builder = InlineKeyboardBuilder()
    builder.button(text="Подобрать тур", callback_data="menu:pick_tour")
    builder.button(text="Горящие туры", callback_data="menu:hot_tours")
    builder.button(text="Мои заявки", callback_data="menu:my_requests")
    builder.button(text="Написать менеджеру", callback_data="menu:contact_manager")
    builder.adjust(1)
    return builder.as_markup()


def get_manager_menu() -> InlineKeyboardMarkup:
    # Главное меню менеджера.
    builder = InlineKeyboardBuilder()
    builder.button(text="Заявки", callback_data="manager:requests")
    builder.adjust(1)
    return builder.as_markup()


def get_back_to_menu_keyboard() -> InlineKeyboardMarkup:
    # Кнопка возврата в главное меню.
    builder = InlineKeyboardBuilder()
    builder.button(text="В главное меню", callback_data="menu:main")
    return builder.as_markup()


def get_tour_type_keyboard() -> InlineKeyboardMarkup:
    # Выбор типа тура.
    builder = InlineKeyboardBuilder()
    builder.button(text="Школьные туры", callback_data="tour_type:school")
    builder.button(
        text="Туры для сборных групп туристов",
        callback_data="tour_type:group",
    )
    builder.button(text="Индивидуальные туры", callback_data="tour_type:individual")
    builder.button(text="В главное меню", callback_data="menu:main")
    builder.adjust(1)
    return builder.as_markup()


def get_options_keyboard(
    prefix: str,
    options: list[str],
    back_callback: str = "menu:main",
    back_text: str = "Назад",
) -> InlineKeyboardMarkup:
    # Универсальная клавиатура для динамического списка опций.
    builder = InlineKeyboardBuilder()
    for option in options:
        builder.button(text=option, callback_data=f"{prefix}:{option}")
    builder.button(text=back_text, callback_data=back_callback)
    builder.adjust(1)
    return builder.as_markup()


def get_tours_list_keyboard(
    tour_ids: list[int],
    back_callback: str,
) -> InlineKeyboardMarkup:
    # Кнопки выбора тура из списка по номеру.
    builder = InlineKeyboardBuilder()
    for index, tour_id in enumerate(tour_ids, start=1):
        builder.button(text=str(index), callback_data=f"tour_view:{tour_id}")
    builder.button(text="Назад", callback_data=back_callback)
    builder.adjust(3, 1)
    return builder.as_markup()


def get_tour_card_keyboard(
    tour_id: int,
    back_callback: str,
) -> InlineKeyboardMarkup:
    # Кнопки карточки тура.
    builder = InlineKeyboardBuilder()
    builder.button(text="Отправить заявку", callback_data=f"tour_request:{tour_id}")
    builder.button(text="Назад к списку туров", callback_data=back_callback)
    builder.adjust(1)
    return builder.as_markup()
