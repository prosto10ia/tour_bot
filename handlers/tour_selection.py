import os
from datetime import datetime

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from dotenv import load_dotenv

from db import (
    get_available_countries,
    get_available_months,
    get_hot_months,
    get_hot_tours_by_month,
    get_tour_by_id,
    get_tours_by_filters,
    save_request,
)
from keyboards.inline import (
    get_back_to_menu_keyboard,
    get_options_keyboard,
    get_tour_card_keyboard,
    get_tour_type_keyboard,
    get_tours_list_keyboard,
)
from states.tour import HotTourSelection, TourSelection


router = Router()

load_dotenv()
MANAGER_ID = os.getenv("MANAGER_ID")


def _format_tour_list_header(country: str, month: str) -> str:
    # Заголовок списка туров.
    return f"<b>Туры: {country}, {month}</b>"


def _format_tour_list_item(index: int, tour: tuple) -> list[str]:
    # Форматируем один тур для списка.
    _, title, country, season, duration, hotel, price_text, description = tour
    return [
        f"<b>{index}. Тур:</b> {title}",
        f"<b>Страна:</b> {country}",
        f"<b>Сезон:</b> {season}",
        f"<b>Продолжительность:</b> {duration}",
        f"<b>Отель:</b> {hotel}",
        f"<b>Стоимость:</b> {price_text}",
        f"<b>Описание:</b> {description}",
        "",
    ]


def _format_tour_card(index_label: str, tour: tuple) -> str:
    # Полная карточка тура.
    _, _tour_type, title, country, season, duration, hotel, price_text, description = tour
    lines = [
        f"<b>Тур №{index_label}</b>",
        "",
        f"<b>Название:</b> {title}",
        f"<b>Страна:</b> {country}",
        f"<b>Сезон:</b> {season}",
        f"<b>Отель:</b> {hotel}",
        f"<b>Продолжительность:</b> {duration}",
        f"<b>Стоимость:</b> {price_text}",
        f"<b>Описание:</b> {description}",
    ]
    return "\n".join(lines)


async def _send_request_to_manager(callback: CallbackQuery, tour: tuple) -> None:
    # Дублируем заявку менеджеру, если задан MANAGER_ID.
    if not MANAGER_ID:
        return

    _, tour_type, title, country, season, duration, hotel, price_text, description = tour
    username = callback.from_user.username
    username_text = f"@{username}" if username else "без username"
    manager_text = (
        "Новая заявка\n\n"
        f"Клиент: {callback.from_user.full_name}\n"
        f"User ID: {callback.from_user.id}\n"
        f"Username: {username_text}\n"
        f"Тип тура: {tour_type}\n"
        f"Название: {title}\n"
        f"Страна: {country}\n"
        f"Сезон: {season}\n"
        f"Продолжительность: {duration}\n"
        f"Отель: {hotel}\n"
        f"Стоимость: {price_text}\n"
        f"Описание: {description}"
    )
    await callback.bot.send_message(chat_id=int(MANAGER_ID), text=manager_text)


async def _render_tours_list(
    callback: CallbackQuery,
    tours: list[tuple],
    header: str,
    back_callback: str,
) -> None:
    # Рисуем список туров с кнопками выбора.
    tour_ids = [tour[0] for tour in tours]
    lines = [header, ""]
    for index, tour in enumerate(tours, start=1):
        lines.extend(_format_tour_list_item(index, tour))

    await callback.message.edit_text(
        "\n".join(lines).strip(),
        reply_markup=get_tours_list_keyboard(tour_ids, back_callback=back_callback),
    )


@router.callback_query(F.data == "menu:pick_tour")
async def start_tour_selection(callback: CallbackQuery, state: FSMContext) -> None:
    # Начинаем подбор тура с выбора типа.
    await state.clear()
    await state.set_state(TourSelection.waiting_for_tour_type)
    await callback.message.edit_text(
        "Выберите тип тура:",
        reply_markup=get_tour_type_keyboard(),
    )
    await callback.answer()


@router.callback_query(
    TourSelection.waiting_for_tour_type,
    F.data.startswith("tour_type:"),
)
async def process_tour_type(callback: CallbackQuery, state: FSMContext) -> None:
    # Сохраняем тип тура и показываем доступные страны.
    tour_type = callback.data.split(":", maxsplit=1)[1]
    countries = get_available_countries(tour_type)
    if not countries:
        await callback.message.edit_text(
            "Сейчас нет доступных туров этого типа.",
            reply_markup=get_back_to_menu_keyboard(),
        )
        await state.clear()
        await callback.answer()
        return

    await state.update_data(tour_type=tour_type)
    await state.set_state(TourSelection.waiting_for_country)
    await callback.message.edit_text(
        "Выберите страну:",
        reply_markup=get_options_keyboard(
            prefix="tour_country",
            options=countries,
            back_callback="menu:pick_tour",
        ),
    )
    await callback.answer()


@router.callback_query(
    TourSelection.waiting_for_country,
    F.data.startswith("tour_country:"),
)
async def process_country(callback: CallbackQuery, state: FSMContext) -> None:
    # Сохраняем страну и показываем месяцы.
    country = callback.data.split(":", maxsplit=1)[1]
    data = await state.get_data()
    tour_type = data["tour_type"]
    months = get_available_months(tour_type, country)

    await state.update_data(country=country)
    await state.set_state(TourSelection.waiting_for_month)
    await callback.message.edit_text(
        "Выберите месяц / сезон тура:",
        reply_markup=get_options_keyboard(
            prefix="tour_month",
            options=months,
            back_callback="menu:pick_tour",
        ),
    )
    await callback.answer()


@router.callback_query(
    TourSelection.waiting_for_month,
    F.data.startswith("tour_month:"),
)
async def process_month(callback: CallbackQuery, state: FSMContext) -> None:
    # Показываем список подходящих туров.
    month = callback.data.split(":", maxsplit=1)[1]
    data = await state.get_data()
    tour_type = data["tour_type"]
    country = data["country"]

    tours = get_tours_by_filters(tour_type, country, month)
    if not tours:
        await callback.message.edit_text(
            "По выбранным параметрам туров пока нет.",
            reply_markup=get_back_to_menu_keyboard(),
        )
        await state.clear()
        await callback.answer()
        return

    tour_ids = [tour[0] for tour in tours]
    await state.update_data(
        selected_month=month,
        current_tour_ids=tour_ids,
        tour_index_map={str(tour_id): index for index, tour_id in enumerate(tour_ids, start=1)},
        list_back_callback="tour_list_back",
    )
    await _render_tours_list(
        callback,
        tours,
        _format_tour_list_header(country, month),
        back_callback="menu:pick_tour",
    )
    await callback.answer()


@router.callback_query(F.data == "menu:hot_tours")
async def start_hot_tours(callback: CallbackQuery, state: FSMContext) -> None:
    # Запускаем сценарий горящих туров с выбора месяца.
    await state.clear()
    months = get_hot_months()
    if not months:
        await callback.message.edit_text(
            "Сейчас нет горящих туров.",
            reply_markup=get_back_to_menu_keyboard(),
        )
        await callback.answer()
        return

    await state.set_state(HotTourSelection.waiting_for_month)
    await callback.message.edit_text(
        "Выберите месяц / сезон горящего тура:",
        reply_markup=get_options_keyboard(
            prefix="hot_month",
            options=months,
            back_callback="menu:main",
        ),
    )
    await callback.answer()


@router.callback_query(
    HotTourSelection.waiting_for_month,
    F.data.startswith("hot_month:"),
)
async def process_hot_month(callback: CallbackQuery, state: FSMContext) -> None:
    # Показываем список горящих туров за выбранный месяц.
    month = callback.data.split(":", maxsplit=1)[1]
    tours = get_hot_tours_by_month(month)
    if not tours:
        await callback.message.edit_text(
            "На этот месяц горящих туров пока нет.",
            reply_markup=get_back_to_menu_keyboard(),
        )
        await state.clear()
        await callback.answer()
        return

    tour_ids = [tour[0] for tour in tours]
    await state.update_data(
        current_tour_ids=tour_ids,
        tour_index_map={str(tour_id): index for index, tour_id in enumerate(tour_ids, start=1)},
        list_back_callback="hot_list_back",
        hot_month=month,
    )
    await _render_tours_list(
        callback,
        tours,
        f"<b>Горящие туры: {month}</b>",
        back_callback="menu:hot_tours",
    )
    await callback.answer()


@router.callback_query(F.data == "tour_list_back")
async def back_to_tour_list(callback: CallbackQuery, state: FSMContext) -> None:
    # Возвращаемся к последнему списку обычных туров.
    data = await state.get_data()
    tour_ids = data.get("current_tour_ids", [])
    selected_month = data.get("selected_month")
    country = data.get("country")
    if not tour_ids or not selected_month or not country:
        await callback.message.edit_text(
            "Список туров больше недоступен.",
            reply_markup=get_back_to_menu_keyboard(),
        )
        await callback.answer()
        return

    tours = [tour for tour_id in tour_ids if (tour := get_tour_by_id(tour_id))]
    await _render_tours_list(
        callback,
        tours,
        _format_tour_list_header(country, selected_month),
        back_callback="menu:pick_tour",
    )
    await callback.answer()


@router.callback_query(F.data == "hot_list_back")
async def back_to_hot_tours_list(callback: CallbackQuery, state: FSMContext) -> None:
    # Возвращаемся к последнему списку горящих туров.
    data = await state.get_data()
    tour_ids = data.get("current_tour_ids", [])
    month = data.get("hot_month")
    if not tour_ids or not month:
        await callback.message.edit_text(
            "Список туров больше недоступен.",
            reply_markup=get_back_to_menu_keyboard(),
        )
        await callback.answer()
        return

    tours = [tour for tour_id in tour_ids if (tour := get_tour_by_id(tour_id))]
    await _render_tours_list(
        callback,
        tours,
        f"<b>Горящие туры: {month}</b>",
        back_callback="menu:hot_tours",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("tour_view:"))
async def show_tour_card(callback: CallbackQuery, state: FSMContext) -> None:
    # Показываем карточку выбранного тура.
    tour_id = int(callback.data.split(":", maxsplit=1)[1])
    tour = get_tour_by_id(tour_id)
    if tour is None:
        await callback.answer("Тур не найден", show_alert=True)
        return

    data = await state.get_data()
    tour_index_map = data.get("tour_index_map", {})
    index_label = str(tour_index_map.get(str(tour_id), 1))
    back_callback = data.get("list_back_callback", "menu:main")

    await callback.message.edit_text(
        _format_tour_card(index_label, tour),
        reply_markup=get_tour_card_keyboard(tour_id, back_callback=back_callback),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("tour_request:"))
async def request_tour(callback: CallbackQuery, state: FSMContext) -> None:
    # Сохраняем заявку и отправляем её менеджеру.
    tour_id = int(callback.data.split(":", maxsplit=1)[1])
    tour = get_tour_by_id(tour_id)
    if tour is None:
        await callback.answer("Тур не найден", show_alert=True)
        return

    _, tour_type, title, country, season, duration, hotel, price_text, _description = tour
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_request(
        user_id=callback.from_user.id,
        username=callback.from_user.username,
        full_name=callback.from_user.full_name,
        tour_id=tour_id,
        tour_type=tour_type,
        title=title,
        country=country,
        season=season,
        duration=duration,
        hotel=hotel,
        price_text=price_text,
        created_at=created_at,
    )
    await _send_request_to_manager(callback, tour)
    await state.clear()
    await callback.message.edit_text(
        "Заявка отправлена. С вами свяжется наш менеджер.",
        reply_markup=get_back_to_menu_keyboard(),
    )
    await callback.answer("Заявка отправлена")
