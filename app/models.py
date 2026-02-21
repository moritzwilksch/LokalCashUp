from __future__ import annotations

from pydantic import BaseModel


class DenominationConfig(BaseModel):
    ui_label: str
    input_field: str
    output_field: str
    factor: float


class AppConfig(BaseModel):
    wechselgeld_tagesanfang: float
    employees: list[str]
    denominations: list[DenominationConfig]


class DenominationLine(BaseModel):
    quantity_raw: str = ""
    amount_formatted: str = "0,00 €"


class ZBonInput(BaseModel):
    barein_zb: str = ""
    ectrink_zb: str = ""
    tagesumsatz_zb: str = ""
    gutschein_bezahlt: str = ""


class TipLine(BaseModel):
    person: str = "Bitte wählen..."
    hours_raw: str = ""
    tip_formatted: str = "________ €"


class ComputedOutputs(BaseModel):
    geld_in_kasse: str = "________ €"
    barentnahmen_summe: str = "= ________ €"
    ausgezaehlte_bareinnahmen: str = "________ €"
    total: str = "________ €"
    trinkgeld_gesamt: str = "________ €"
    geld_in_umschlag: str = "________ €"


class CashUpForm(BaseModel):
    date_in: str
    barentnahmen_list: str = ""
    denominations: list[DenominationLine]
    zbon: ZBonInput
    tips: list[TipLine]
    outputs: ComputedOutputs


class TipDistribution(BaseModel):
    values: list[str]
