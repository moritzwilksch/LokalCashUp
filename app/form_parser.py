from __future__ import annotations

from collections.abc import Mapping

from app.models import AppConfig, CashUpForm, ComputedOutputs, DenominationLine, TipLine, ZBonInput


def build_default_form(today: str, config: AppConfig) -> CashUpForm:
    return CashUpForm(
        datum=today,
        barentnahmen_liste="",
        denominations=[DenominationLine() for _ in config.denominations],
        zbon=ZBonInput(),
        tips=[TipLine() for _ in range(7)],
        outputs=ComputedOutputs(),
    )


def parse_form_data(raw: Mapping[str, object], today: str, config: AppConfig) -> CashUpForm:
    datum_wert = str(raw.get("datum", today))

    denominations = [
        DenominationLine(quantity_raw=str(raw.get(f"denom_{denom.key}", "")))
        for denom in config.denominations
    ]

    tips = [
        TipLine(
            person=str(raw.get(f"trinkgeld_person_{idx}", "Bitte wählen...")),
            hours_raw=str(raw.get(f"trinkgeld_stunden_{idx}", "")),
        )
        for idx in range(1, 8)
    ]

    return CashUpForm(
        datum=datum_wert,
        barentnahmen_liste=str(raw.get("barentnahmen_liste", "")),
        denominations=denominations,
        zbon=ZBonInput(
            bargeld_zbon=str(raw.get("zbon_bargeld", "")),
            ec_trinkgeld_zbon=str(raw.get("ec_trinkgeld_zbon", "")),
            tagesumsatz_zbon=str(raw.get("tagesumsatz_zbon", "")),
            mit_gutschein_bezahlt=str(raw.get("mit_gutschein_bezahlt", "")),
        ),
        tips=tips,
        outputs=ComputedOutputs(),
    )
