from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_menu() -> InlineKeyboardMarkup:
    # Главное меню бота.
    builder = InlineKeyboardBuilder()
    builder.button(text="Подобрать тур", callback_data="menu:pick_tour")
    builder.button(text="Горящие туры", callback_data="menu:hot_tours")
    builder.button(text="Мои заявки", callback_data="menu:my_requests")
    builder.button(text="Оплатить", callback_data="menu:payment")
    builder.button(text="Помощь", callback_data="menu:help")
    builder.button(text="Чек-лист в поездку", callback_data="menu:checklist")
    builder.button(
        text="Отправить заявку менеджеру",
        callback_data="menu:send_to_manager",
    )
    builder.adjust(1)
    return builder.as_markup()


def get_back_to_menu_keyboard() -> InlineKeyboardMarkup:
    # Кнопка возврата в главное меню.
    builder = InlineKeyboardBuilder()
    builder.button(text="В главное меню", callback_data="menu:main")
    return builder.as_markup()


def get_budget_keyboard() -> InlineKeyboardMarkup:
    # Варианты бюджета для первого шага.
    builder = InlineKeyboardBuilder()
    builder.button(text="До 50 000 ₽", callback_data="tour_budget:50000")
    builder.button(text="50 000–100 000 ₽", callback_data="tour_budget:100000")
    builder.button(text="100 000–150 000 ₽", callback_data="tour_budget:150000")
    builder.button(text="От 150 000 ₽", callback_data="tour_budget:999999")
    builder.button(text="В главное меню", callback_data="menu:main")
    builder.adjust(1)
    return builder.as_markup()


def get_country_keyboard() -> InlineKeyboardMarkup:
    # Варианты стран для второго шага.
    builder = InlineKeyboardBuilder()
    builder.button(text="Турция", callback_data="tour_country:Турция")
    builder.button(text="Египет", callback_data="tour_country:Египет")
    builder.button(text="ОАЭ", callback_data="tour_country:ОАЭ")
    builder.button(text="Таиланд", callback_data="tour_country:Таиланд")
    builder.button(text="В главное меню", callback_data="menu:main")
    builder.adjust(2, 2, 1)
    return builder.as_markup()


def get_dates_keyboard() -> InlineKeyboardMarkup:
    # Готовые варианты дат для шага выбора периода.
    builder = InlineKeyboardBuilder()
    builder.button(text="Июнь 2026", callback_data="tour_dates:Июнь 2026")
    builder.button(text="Июль 2026", callback_data="tour_dates:Июль 2026")
    builder.button(text="Август 2026", callback_data="tour_dates:Август 2026")
    builder.button(text="Сентябрь 2026", callback_data="tour_dates:Сентябрь 2026")
    builder.button(text="В главное меню", callback_data="menu:main")
    builder.adjust(2, 2, 1)
    return builder.as_markup()


def get_stars_keyboard() -> InlineKeyboardMarkup:
    # Варианты звёздности отеля.
    builder = InlineKeyboardBuilder()
    builder.button(text="3★", callback_data="tour_stars:3")
    builder.button(text="4★", callback_data="tour_stars:4")
    builder.button(text="5★", callback_data="tour_stars:5")
    builder.button(text="В главное меню", callback_data="menu:main")
    builder.adjust(3, 1)
    return builder.as_markup()


def get_payment_keyboard() -> InlineKeyboardMarkup:
    # Клавиатура демо-оплаты.
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Сгенерировать ссылку на оплату",
        callback_data="payment:generate",
    )
    builder.button(text="В главное меню", callback_data="menu:main")
    builder.adjust(1)
    return builder.as_markup()


def get_checklist_keyboard() -> InlineKeyboardMarkup:
    # Клавиатура для выдачи PDF с чек-листом.
    builder = InlineKeyboardBuilder()
    builder.button(text="Скачать PDF", callback_data="checklist:pdf")
    builder.button(text="В главное меню", callback_data="menu:main")
    builder.adjust(1)
    return builder.as_markup()


def get_send_manager_keyboard() -> InlineKeyboardMarkup:
    # Кнопка подтверждения отправки заявки менеджеру.
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Отправить последнюю заявку",
        callback_data="manager:send_last_request",
    )
    builder.button(text="В главное меню", callback_data="menu:main")
    builder.adjust(1)
    return builder.as_markup()
