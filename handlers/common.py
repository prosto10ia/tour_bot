import os

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from dotenv import load_dotenv

from db import get_all_requests, get_user_requests
from keyboards.inline import (
    get_back_to_menu_keyboard,
    get_main_menu,
    get_manager_menu,
)


router = Router()

load_dotenv()
MANAGER_ID = os.getenv("MANAGER_ID")
MANAGER_USERNAME = os.getenv("MANAGER_USERNAME")


def _is_manager(user_id: int) -> bool:
    # Проверяем, является ли пользователь менеджером.
    return bool(MANAGER_ID) and str(user_id) == MANAGER_ID


async def _send_or_edit(callback: CallbackQuery, text: str, **kwargs) -> None:
    # Пытаемся отредактировать текущее сообщение, а если нельзя — отправляем новое.
    if callback.message:
        await callback.message.edit_text(text, **kwargs)
    else:
        await callback.bot.send_message(callback.from_user.id, text, **kwargs)


def _get_menu_text(is_manager: bool) -> str:
    # Текст главного меню в зависимости от роли.
    if is_manager:
        return "Меню менеджера. Выберите действие:"
    return "Главное меню турагентства. Выберите действие:"


def _get_menu_markup(is_manager: bool):
    # Клавиатура главного меню в зависимости от роли.
    return get_manager_menu() if is_manager else get_main_menu()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    # Приветствие и показ нужного главного меню.
    is_manager = _is_manager(message.from_user.id)
    await message.answer(_get_menu_text(is_manager), reply_markup=_get_menu_markup(is_manager))


@router.callback_query(F.data == "menu:main")
async def show_main_menu(callback: CallbackQuery) -> None:
    # Показываем главное меню по кнопке.
    is_manager = _is_manager(callback.from_user.id)
    await _send_or_edit(
        callback,
        _get_menu_text(is_manager),
        reply_markup=_get_menu_markup(is_manager),
    )
    await callback.answer()


@router.callback_query(F.data == "menu:my_requests")
async def show_my_requests(callback: CallbackQuery) -> None:
    # Показываем отправленные заявки пользователя.
    requests = get_user_requests(callback.from_user.id)
    if not requests:
        text = "У вас пока нет отправленных заявок."
    else:
        lines = ["<b>Мои заявки</b>", ""]
        for index, (_, title, country, season, hotel, price_text, status, _) in enumerate(
            requests,
            start=1,
        ):
            lines.append(f"<b>{index}. {title}</b>")
            lines.append(f"Страна: {country}")
            lines.append(f"Сезон: {season}")
            lines.append(f"Отель: {hotel}")
            lines.append(f"Цена: {price_text}")
            lines.append(f"Статус: {status}")
            lines.append("")
        text = "\n".join(lines).strip()

    await _send_or_edit(callback, text, reply_markup=get_back_to_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data == "menu:contact_manager")
async def contact_manager(callback: CallbackQuery) -> None:
    # Отправляем ссылку на менеджера.
    if MANAGER_USERNAME:
        username = MANAGER_USERNAME.lstrip("@")
        text = f"<b>Написать менеджеру:</b>\nhttps://t.me/{username}"
    else:
        text = "В .env не указан MANAGER_USERNAME. Добавьте username менеджера."

    await _send_or_edit(callback, text, reply_markup=get_back_to_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data == "manager:requests")
async def show_manager_requests(callback: CallbackQuery) -> None:
    # Показываем менеджеру список поступивших заявок.
    if not _is_manager(callback.from_user.id):
        await callback.answer("Раздел доступен только менеджеру", show_alert=True)
        return

    requests = get_all_requests()
    if not requests:
        text = "Поступивших заявок пока нет."
    else:
        lines = ["<b>Поступившие заявки</b>", ""]
        for index, (
            _request_id,
            user_id,
            username,
            full_name,
            title,
            country,
            season,
            hotel,
            price_text,
            status,
            created_at,
        ) in enumerate(requests, start=1):
            username_text = f"@{username}" if username else "без username"
            lines.append(f"<b>{index}. Пользователь:</b> {user_id}")
            lines.append(f"<b>Имя:</b> {full_name}")
            lines.append(f"<b>Username:</b> {username_text}")
            lines.append(f"<b>Тур:</b> {title}")
            lines.append(f"<b>Страна:</b> {country}")
            lines.append(f"<b>Сезон:</b> {season}")
            lines.append(f"<b>Отель:</b> {hotel}")
            lines.append(f"<b>Цена:</b> {price_text}")
            lines.append(f"<b>Статус:</b> {status}")
            lines.append(f"<b>Создана:</b> {created_at}")
            lines.append("")
        text = "\n".join(lines).strip()

    await _send_or_edit(callback, text, reply_markup=get_back_to_menu_keyboard())
    await callback.answer()
