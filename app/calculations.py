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


def calculate_total(tagesumsatz_zbon: str, mit_gutschein_bezahlt: str) -> float:
    return parse_fuzzy_number(tagesumsatz_zbon) - parse_fuzzy_number(mit_gutschein_bezahlt)


def calculate_ausgezaehlte_bareinnahmen(
    geld_in_kasse: str, barentnahmen_summe: float, wechselgeld_tagesanfang: float
) -> float:
    return (
        parse_fuzzy_number(geld_in_kasse)
        + barentnahmen_summe
        - wechselgeld_tagesanfang
    )


def calculate_trinkgeld_gesamt(
    ausgezaehlte_bareinnahmen: float, bargeld_zbon: str, ec_trinkgeld_zbon: str
) -> float:
    return (
        ausgezaehlte_bareinnahmen
        - parse_fuzzy_number(bargeld_zbon)
        + parse_fuzzy_number(ec_trinkgeld_zbon)
    )


def calculate_geld_in_umschlag(
    bargeld_zbon: str, ec_trinkgeld_zbon: str, barentnahmen_summe: float
) -> float:
    return (
        parse_fuzzy_number(bargeld_zbon)
        - parse_fuzzy_number(ec_trinkgeld_zbon)
        - barentnahmen_summe
    )


def calculate_tip_distribution(form: CashUpForm, trinkgeld_gesamt: float) -> TipDistribution:
    hour_values = [parse_fuzzy_number(tip.hours_raw) for tip in form.tips]
    total_hours = sum(hour_values)
    if total_hours == 0:
        total_hours = 0.000001

    values = [format_euro((hours / total_hours) * trinkgeld_gesamt) for hours in hour_values]
    return TipDistribution(values=values)


def calculate_barentnahmen_summe(barentnahmen_liste: str) -> float:
    return sum_barentnahmen(barentnahmen_liste)
