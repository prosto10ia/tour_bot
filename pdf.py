from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


CHECKLIST_LINES = [
    "Чек-лист в поездку",
    "",
    "Документы:",
    "- Загранпаспорт и копия",
    "- Ваучер / бронь отеля",
    "- Авиабилеты",
    "- Медицинская страховка",
    "- Банковская карта и немного наличных",
    "",
    "Вещи:",
    "- Телефон и зарядка",
    "- Аптечка",
    "- Солнцезащитные средства",
    "- Удобная обувь",
    "- Лёгкая одежда по погоде",
    "- Купальные принадлежности",
    "",
    "Полезно проверить:",
    "- Трансфер до отеля",
    "- Время выезда в аэропорт",
    "- Ограничения по багажу",
]


def _register_font() -> str:
    # Регистрируем системный шрифт с кириллицей для PDF.
    font_candidates = [
        Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
        Path("/Library/Fonts/Arial Unicode.ttf"),
        Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
    ]

    for font_path in font_candidates:
        if font_path.exists():
            pdfmetrics.registerFont(TTFont("ChecklistFont", str(font_path)))
            return "ChecklistFont"

    return "Helvetica"


def generate_checklist_pdf(output_path: Path) -> Path:
    # Генерируем простой PDF-файл с чек-листом.
    font_name = _register_font()
    pdf = canvas.Canvas(str(output_path), pagesize=A4)
    width, height = A4

    pdf.setTitle("travel_checklist")
    pdf.setFont(font_name, 14)

    y_position = height - 50
    for line in CHECKLIST_LINES:
        pdf.drawString(50, y_position, line)
        y_position -= 22
        if y_position < 60:
            pdf.showPage()
            pdf.setFont(font_name, 14)
            y_position = height - 50

    pdf.save()
    return output_path
