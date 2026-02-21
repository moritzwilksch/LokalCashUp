from __future__ import annotations

from app.models import CashFields, DenominationConfig, TipDistribution
from app.parsing import format_euro, parse_fuzzy_number, sum_barentnahmen


def calculate_stueckelung(
    fields: CashFields, denominations: list[DenominationConfig]
) -> tuple[dict[str, str], float]:
    updates: dict[str, str] = {}
    total = 0.0

    raw_values = fields.model_dump(by_alias=True)
    for denomination in denominations:
        input_value = parse_fuzzy_number(raw_values.get(denomination.input_field, "0"))
        amount = input_value * denomination.factor
        total += amount
        updates[denomination.output_field] = format_euro(amount)

    updates["geldInKasse"] = format_euro(total)
    return updates, total


def calculate_total(tagesumsatz_zb: str, gutschein_bezahlt: str) -> float:
    return parse_fuzzy_number(tagesumsatz_zb) - parse_fuzzy_number(gutschein_bezahlt)


def calculate_ausgezaehlte_bareinnahmen(
    geld_in_kasse: str, barentnahmen_summe: float, wechselgeld_tagesanfang: float
) -> float:
    return (
        parse_fuzzy_number(geld_in_kasse)
        + barentnahmen_summe
        - wechselgeld_tagesanfang
    )


def calculate_trinkgeld_gesamt(
    ausgezaehlte_bareinnahmen: float, barein_zb: str, ectrink_zb: str
) -> float:
    return (
        ausgezaehlte_bareinnahmen
        - parse_fuzzy_number(barein_zb)
        + parse_fuzzy_number(ectrink_zb)
    )


def calculate_geld_in_umschlag(
    barein_zb: str, ectrink_zb: str, barentnahmen_summe: float
) -> float:
    return (
        parse_fuzzy_number(barein_zb)
        - parse_fuzzy_number(ectrink_zb)
        - barentnahmen_summe
    )


def calculate_tip_distribution(fields: CashFields, trinkgeld_gesamt: float) -> TipDistribution:
    hour_values = [
        parse_fuzzy_number(fields.s1),
        parse_fuzzy_number(fields.s2),
        parse_fuzzy_number(fields.s3),
        parse_fuzzy_number(fields.s4),
        parse_fuzzy_number(fields.s5),
        parse_fuzzy_number(fields.s6),
        parse_fuzzy_number(fields.s7),
    ]
    total_hours = sum(hour_values)
    if total_hours == 0:
        total_hours = 0.000001

    tips = [format_euro((hours / total_hours) * trinkgeld_gesamt) for hours in hour_values]
    return TipDistribution(
        tg1=tips[0],
        tg2=tips[1],
        tg3=tips[2],
        tg4=tips[3],
        tg5=tips[4],
        tg6=tips[5],
        tg7=tips[6],
    )


def calculate_barentnahmen_summe(barentnahmen_list: str) -> float:
    return sum_barentnahmen(barentnahmen_list)
