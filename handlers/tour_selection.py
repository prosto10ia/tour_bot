from datetime import datetime

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from db import get_fallback_tours, get_matching_tours, save_request
from keyboards.inline import (
    get_back_to_menu_keyboard,
    get_budget_keyboard,
    get_country_keyboard,
    get_dates_keyboard,
    get_stars_keyboard,
)
from states.tour import TourSelection


router = Router()


@router.callback_query(F.data == "menu:pick_tour")
async def start_tour_selection(callback: CallbackQuery, state: FSMContext) -> None:
    # Запускаем сценарий подбора тура с первого шага.
    await state.clear()
    await state.set_state(TourSelection.waiting_for_budget)
    await callback.message.edit_text(
        "Шаг 1 из 4. Выберите бюджет поездки:",
        reply_markup=get_budget_keyboard(),
    )
    await callback.answer()


@router.callback_query(
    TourSelection.waiting_for_budget,
    F.data.startswith("tour_budget:"),
)
async def process_budget(callback: CallbackQuery, state: FSMContext) -> None:
    # Сохраняем бюджет и переходим к выбору страны.
    budget = int(callback.data.split(":", maxsplit=1)[1])
    await state.update_data(budget=budget)
    await state.set_state(TourSelection.waiting_for_country)
    await callback.message.edit_text(
        "Шаг 2 из 4. Выберите страну:",
        reply_markup=get_country_keyboard(),
    )
    await callback.answer()


@router.callback_query(
    TourSelection.waiting_for_country,
    F.data.startswith("tour_country:"),
)
async def process_country(callback: CallbackQuery, state: FSMContext) -> None:
    # Сохраняем страну и спрашиваем желаемые даты.
    country = callback.data.split(":", maxsplit=1)[1]
    await state.update_data(country=country)
    await state.set_state(TourSelection.waiting_for_dates)
    await callback.message.edit_text(
        "Шаг 3 из 4. Выберите даты поездки:",
        reply_markup=get_dates_keyboard(),
    )
    await callback.answer()


@router.callback_query(
    TourSelection.waiting_for_dates,
    F.data.startswith("tour_dates:"),
)
async def process_dates(callback: CallbackQuery, state: FSMContext) -> None:
    # Сохраняем даты и переходим к звёздности.
    dates = callback.data.split(":", maxsplit=1)[1]
    await state.update_data(dates=dates)
    await state.set_state(TourSelection.waiting_for_hotel_stars)
    await callback.message.edit_text(
        "Шаг 4 из 4. Выберите звёздность отеля:",
        reply_markup=get_stars_keyboard(),
    )
    await callback.answer()


@router.callback_query(
    TourSelection.waiting_for_hotel_stars,
    F.data.startswith("tour_stars:"),
)
async def process_stars(callback: CallbackQuery, state: FSMContext) -> None:
    # Подбираем варианты после финального шага и сохраняем заявку в базе.
    stars = int(callback.data.split(":", maxsplit=1)[1])
    await state.update_data(stars=stars)
    data = await state.get_data()

    matched_tours = get_matching_tours(
        country=data["country"],
        dates=data["dates"],
        stars=data["stars"],
        budget=data["budget"],
    )
    fallback_tours = []
    if not matched_tours:
        fallback_tours = get_fallback_tours(
            country=data["country"],
            dates=data["dates"],
            stars=data["stars"],
        )

    request_text = (
        f"Бюджет: до {data['budget']} ₽\n"
        f"Страна: {data['country']}\n"
        f"Даты: {data['dates']}\n"
        f"Отель: {data['stars']}★"
    )
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_request(
        user_id=callback.from_user.id,
        username=callback.from_user.username,
        request_type="Подбор тура",
        text=request_text,
        created_at=created_at,
    )

    if matched_tours:
        lines = [
            "<b>Подходящие варианты</b>",
            "",
            *[
                f"{index}. {title} — {price} ₽"
                for index, (title, price) in enumerate(matched_tours, start=1)
            ],
            "",
            "Заявка сохранена. При желании её можно отправить менеджеру из главного меню.",
        ]
    elif fallback_tours:
        lines = [
            "<b>Точных вариантов в рамках бюджета не найдено</b>",
            "",
            "Но есть ближайшие предложения по тем же параметрам:",
            "",
            *[
                f"{index}. {title} — {price} ₽"
                for index, (title, price) in enumerate(fallback_tours, start=1)
            ],
            "",
            "Заявка сохранена. Если хотите, её можно отправить менеджеру из главного меню.",
        ]
    else:
        lines = [
            "<b>Подходящих туров пока не найдено</b>",
            "",
            "Мы всё равно сохранили ваш запрос:",
            request_text,
            "",
            "Попробуйте изменить параметры или отправьте заявку менеджеру.",
        ]

    await callback.message.edit_text(
        "\n".join(lines),
        reply_markup=get_back_to_menu_keyboard(),
    )
    await state.clear()
    await callback.answer("Подбор завершён")
