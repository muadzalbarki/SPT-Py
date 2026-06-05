import re
from datetime import datetime


def indonesian_date(date_obj: datetime = None) -> str:
    if date_obj is None:
        date_obj = datetime.now()
    months = [
        "Januari", "Februari", "Maret", "April", "Mei", "Juni",
        "Juli", "Agustus", "September", "Oktober", "November", "Desember",
    ]
    return f"{date_obj.day} {months[date_obj.month - 1]} {date_obj.year}"


def clean_placeholder(text: str) -> str:
    return text.strip("{} ")


def detect_placeholders(text: str) -> list[str]:
    matches = re.findall(r'\{([^}]+)\}', text)
    return [m.strip() for m in matches if not re.match(r'^[A-F0-9-]{20,}$', m)]


def format_nip(nip: str) -> str:
    nip = re.sub(r'\D', '', nip)
    if len(nip) != 18:
        nip = nip.ljust(18, '0')[:18]
    return nip


def truncate(text: str, max_len: int = 60) -> str:
    return text[:max_len] + "..." if len(text) > max_len else text
