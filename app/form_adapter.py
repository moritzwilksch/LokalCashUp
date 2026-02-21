from __future__ import annotations

from collections.abc import Mapping

from app.models import AppConfig, CashUpForm, ComputedOutputs, DenominationLine, TipLine, ZBonInput


def build_default_form(today: str, config: AppConfig) -> CashUpForm:
    return CashUpForm(
        date_in=today,
        barentnahmen_list="",
        denominations=[DenominationLine() for _ in config.denominations],
        zbon=ZBonInput(),
        tips=[TipLine() for _ in range(7)],
        outputs=ComputedOutputs(),
    )


def parse_form_data(raw: Mapping[str, object], today: str, config: AppConfig) -> CashUpForm:
    date_in = str(raw.get("dateIn", today))

    denominations = [
        DenominationLine(quantity_raw=str(raw.get(denom.input_field, "")))
        for denom in config.denominations
    ]

    tips = [
        TipLine(
            person=str(raw.get(f"p{idx}", "Bitte wählen...")),
            hours_raw=str(raw.get(f"s{idx}", "")),
        )
        for idx in range(1, 8)
    ]

    return CashUpForm(
        date_in=date_in,
        barentnahmen_list=str(raw.get("barentnahmenList", "")),
        denominations=denominations,
        zbon=ZBonInput(
            barein_zb=str(raw.get("bareinZb", "")),
            ectrink_zb=str(raw.get("ectrinkZb", "")),
            tagesumsatz_zb=str(raw.get("tagesumsatzZb", "")),
            gutschein_bezahlt=str(raw.get("gutschein_bezahlt", "")),
        ),
        tips=tips,
        outputs=ComputedOutputs(),
    )


def to_template_fields(form: CashUpForm, config: AppConfig) -> dict[str, str]:
    fields: dict[str, str] = {
        "dateIn": form.date_in,
        "barentnahmenList": form.barentnahmen_list,
        "barentnahmenSumme": form.outputs.barentnahmen_summe,
        "ausgezaehlteBareinnahmen": form.outputs.ausgezaehlte_bareinnahmen,
        "geldInKasse": form.outputs.geld_in_kasse,
        "bareinZb": form.zbon.barein_zb,
        "ectrinkZb": form.zbon.ectrink_zb,
        "tagesumsatzZb": form.zbon.tagesumsatz_zb,
        "gutschein_bezahlt": form.zbon.gutschein_bezahlt,
        "total": form.outputs.total,
        "trinkgeldGesamt": form.outputs.trinkgeld_gesamt,
        "geldInUmschlag": form.outputs.geld_in_umschlag,
    }

    for line, denom in zip(form.denominations, config.denominations, strict=True):
        fields[denom.input_field] = line.quantity_raw
        fields[denom.output_field] = line.amount_formatted

    for idx, tip in enumerate(form.tips, start=1):
        fields[f"p{idx}"] = tip.person
        fields[f"s{idx}"] = tip.hours_raw
        fields[f"tg{idx}"] = tip.tip_formatted

    return fields
