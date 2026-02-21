from __future__ import annotations


def parse_fuzzy_number(value: str | float | int | None) -> float:
    """Leniently parse numbers from cash-up form inputs."""
    if value is None or value == "":
        return 0.0

    raw = str(value).lower()
    normalized = (
        raw.replace(",", ".")
        .replace("€", "")
        .replace("euro", "")
        .replace("eur", "")
        .replace("stk.", "")
        .replace("stk", "")
        .replace("=", "")
        .strip()
    )
    if normalized == "":
        return 0.0
    try:
        return float(normalized)
    except ValueError:
        return 0.0


def format_euro(value: float) -> str:
    """Format as historic app output: round(2), comma decimal separator, euro suffix."""
    return str(round(value, 2)).replace(".", ",") + " €"


def sum_barentnahmen(raw_list: str | float | int | None) -> float:
    text = str(raw_list)
    return sum(parse_fuzzy_number(chunk) for chunk in text.split("+"))
