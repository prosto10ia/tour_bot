import os
from datetime import datetime
from pathlib import Path
from urllib.parse import quote_plus

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import BufferedInputFile, CallbackQuery, Message
from dotenv import load_dotenv

from db import get_hot_tours, get_last_user_request, get_user_requests
from keyboards.inline import (
    get_back_to_menu_keyboard,
    get_checklist_keyboard,
    get_main_menu,
    get_payment_keyboard,
    get_send_manager_keyboard,
)
from pdf import CHECKLIST_LINES, generate_checklist_pdf


router = Router()

load_dotenv()
MANAGER_CHAT_ID = os.getenv("MANAGER_CHAT_ID")

FAQ_TEXT = """
<b>Контакты менеджера</b>
Менеджер: Крис
Telegram: @@kkriisstiii
Телефон: нискажу

<b>FAQ</b>
1. Как подобрать тур?
Нажмите «Подобрать тур» и ответьте на 4 шага.

2. Где посмотреть свои заявки?
В разделе «Мои заявки».

3. Можно ли оплатить онлайн?
В боте доступен учебный демо-сценарий оплаты.
""".strip()


async def _send_or_edit(callback: CallbackQuery, text: str, **kwargs) -> None:
    # Пытаемся отредактировать текущее сообщение, а если нельзя — отправляем новое.
    if callback.message:
        await callback.message.edit_text(text, **kwargs)
    else:
        await callback.bot.send_message(callback.from_user.id, text, **kwargs)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    # Приветствие и показ главного меню.
    text = (
        "Привет! Я бот турагентства «Мои каникулы».\n\n"
        "Помогу подобрать тур, показать горящие предложения, сохранить ваши заявки, "
        "сформировать чек-лист и отправить запрос менеджеру.\n\n"
        "Выберите нужный раздел ниже."
    )
    await message.answer(text, reply_markup=get_main_menu())


@router.callback_query(F.data == "menu:main")
async def show_main_menu(callback: CallbackQuery) -> None:
    # Показываем главное меню по кнопке.
    text = (
        "Главное меню турагентства «Мои каникулы».\n"
        "Выберите действие:"
    )
    await _send_or_edit(callback, text, reply_markup=get_main_menu())
    await callback.answer()


@router.callback_query(F.data == "menu:hot_tours")
async def show_hot_tours(callback: CallbackQuery) -> None:
    # Выводим список горящих туров из базы.
    hot_tours = get_hot_tours()
    if hot_tours:
        lines = ["<b>Горящие туры</b>", ""]
        lines.extend(
            f"{index}. {title} — {price} ₽ вместо {old_price} ₽"
            for index, (title, price, old_price) in enumerate(hot_tours, start=1)
        )
        text = "\n".join(lines)
    else:
        text = "Сейчас горящих туров нет, но мы скоро обновим подборку."
    await _send_or_edit(callback, text, reply_markup=get_back_to_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data == "menu:my_requests")
async def show_my_requests(callback: CallbackQuery) -> None:
    # Показываем сохранённые заявки конкретного пользователя.
    requests = get_user_requests(callback.from_user.id)
    if not requests:
        text = "У вас пока нет сохранённых заявок."
    else:
        lines = ["<b>Мои заявки</b>", ""]
        for request_id, _, request_type, text_value, created_at in requests:
            lines.append(
                f"#{request_id} | {request_type} | {created_at}\n{text_value}\n"
            )
        text = "\n".join(lines)

    await _send_or_edit(callback, text, reply_markup=get_back_to_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data == "menu:payment")
async def show_payment_menu(callback: CallbackQuery) -> None:
    # Открываем демо-раздел оплаты.
    text = (
        "<b>Демо-оплата</b>\n\n"
        "Это учебный режим. Нажмите кнопку ниже, и бот сгенерирует фейковую ссылку."
    )
    await _send_or_edit(callback, text, reply_markup=get_payment_keyboard())
    await callback.answer()


@router.callback_query(F.data == "payment:generate")
async def generate_payment_link(callback: CallbackQuery) -> None:
    # Генерируем учебную ссылку на оплату без реальной платёжной системы.
    username = callback.from_user.username or f"user_{callback.from_user.id}"
    fake_url = (
        "https://example-pay.local/checkout?"
        f"order={callback.from_user.id}-{int(datetime.now().timestamp())}"
        f"&user={quote_plus(username)}"
    )
    text = (
        "<b>Учебная ссылка готова</b>\n\n"
        f"{fake_url}\n\n"
        "Ссылка фейковая и нужна только для демонстрации."
    )
    await _send_or_edit(callback, text, reply_markup=get_back_to_menu_keyboard())
    await callback.answer("Ссылка сгенерирована")


@router.callback_query(F.data == "menu:help")
async def show_help(callback: CallbackQuery) -> None:
    # Показываем контакты и краткий FAQ.
    await _send_or_edit(callback, FAQ_TEXT, reply_markup=get_back_to_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data == "menu:checklist")
async def show_checklist(callback: CallbackQuery) -> None:
    # Показываем текстовый чек-лист и кнопку на PDF.
    text = "\n".join(CHECKLIST_LINES)
    await _send_or_edit(callback, text, reply_markup=get_checklist_keyboard())
    await callback.answer()


@router.callback_query(F.data == "checklist:pdf")
async def send_checklist_pdf(callback: CallbackQuery) -> None:
    # Генерируем PDF и отправляем его пользователю.
    pdf_path = Path(__file__).resolve().parent.parent / "travel_checklist.pdf"
    generate_checklist_pdf(pdf_path)

    file_bytes = pdf_path.read_bytes()
    document = BufferedInputFile(file_bytes, filename="travel_checklist.pdf")

    await callback.message.answer_document(
        document=document,
        caption="Ваш чек-лист в PDF.",
        reply_markup=get_back_to_menu_keyboard(),
    )
    await callback.answer("PDF готов")


@router.callback_query(F.data == "menu:send_to_manager")
async def show_send_to_manager(callback: CallbackQuery) -> None:
    # Предлагаем отправить последнюю заявку менеджеру.
    last_request = get_last_user_request(callback.from_user.id)
    if last_request is None:
        text = (
            "Сначала создайте хотя бы одну заявку через раздел «Подобрать тур», "
            "после этого её можно будет отправить менеджеру."
        )
        markup = get_back_to_menu_keyboard()
    else:
        _, _, request_type, text_value, created_at = last_request
        text = (
            "<b>Последняя заявка</b>\n\n"
            f"Тип: {request_type}\n"
            f"Дата: {created_at}\n"
            f"{text_value}\n\n"
            "Отправить её менеджеру?"
        )
        markup = get_send_manager_keyboard()

    await _send_or_edit(callback, text, reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data == "manager:send_last_request")
async def send_last_request_to_manager(callback: CallbackQuery) -> None:
    # Пересылаем текст последней заявки в чат менеджера.
    if not MANAGER_CHAT_ID:
        await _send_or_edit(
            callback,
            "В .env не указан MANAGER_CHAT_ID. Добавьте chat_id группы менеджеров.",
            reply_markup=get_back_to_menu_keyboard(),
        )
        await callback.answer()
        return

    last_request = get_last_user_request(callback.from_user.id)
    if last_request is None:
        await _send_or_edit(
            callback,
            "У вас пока нет заявок для отправки менеджеру.",
            reply_markup=get_back_to_menu_keyboard(),
        )
        await callback.answer()
        return

    _, username, request_type, text_value, created_at = last_request
    sender = callback.from_user.full_name
    username_text = f"@{username}" if username else "без username"
    manager_text = (
        "Новая заявка в группу «Мои каникулы»\n\n"
        f"Клиент: {sender} ({username_text})\n"
        f"User ID: {callback.from_user.id}\n"
        f"Тип: {request_type}\n"
        f"Дата: {created_at}\n\n"
        f"{text_value}"
    )

    await callback.bot.send_message(chat_id=int(MANAGER_CHAT_ID), text=manager_text)
    await _send_or_edit(
        callback,
        "Заявка отправлена менеджеру.",
        reply_markup=get_back_to_menu_keyboard(),
    )
    await callback.answer("Отправлено")
