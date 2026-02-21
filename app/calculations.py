from __future__ import annotations

from app.models import CashUpForm, DenominationConfig, TipDistribution
from app.parsing import format_euro, parse_fuzzy_number, sum_barentnahmen


def calculate_stueckelung(form: CashUpForm, denominations: list[DenominationConfig]) -> float:
    total = 0.0
    for line, denomination in zip(form.denominations, denominations, strict=True):
        amount = parse_fuzzy_number(line.quantity_raw) * denomination.factor
        line.amount_formatted = format_euro(amount)
        total += amount

    form.outputs.geld_in_kasse = format_euro(total)
    return total


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


def calculate_tip_distribution(form: CashUpForm, trinkgeld_gesamt: float) -> TipDistribution:
    hour_values = [parse_fuzzy_number(tip.hours_raw) for tip in form.tips]
    total_hours = sum(hour_values)
    if total_hours == 0:
        total_hours = 0.000001

    values = [format_euro((hours / total_hours) * trinkgeld_gesamt) for hours in hour_values]
    return TipDistribution(values=values)


def calculate_barentnahmen_summe(barentnahmen_list: str) -> float:
    return sum_barentnahmen(barentnahmen_list)
