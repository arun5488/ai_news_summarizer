import re
from datetime import datetime

def _extract_year(user_text: str) -> int | None:
    # picks first 4-digit year like 2024
    m = re.search(r"\b(19|20)\d{2}\b", user_text)
    return int(m.group(0)) if m else None

def _in_year(published_date: str, year: int) -> bool:
    # works for ISO-like strings: "2024-05-10", "2024-05-10T..."
    if not published_date:
        return False
    return str(published_date).startswith(str(year))