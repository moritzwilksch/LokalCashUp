from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class DenominationConfig(BaseModel):
    ui_label: str
    input_field: str
    output_field: str
    factor: float


class AppConfig(BaseModel):
    wechselgeld_tagesanfang: float
    employees: list[str]
    denominations: list[DenominationConfig]


class CashFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    date_in: str = Field(default="", alias="dateIn")

    gt100_in: str = Field(default="", alias="gt100In")
    gt100_out: str = Field(default="0,00 €", alias="gt100Out")
    fifty_e_in: str = Field(default="", alias="50eIn")
    fifty_e_out: str = Field(default="0,00 €", alias="50eOut")
    twenty_e_in: str = Field(default="", alias="20eIn")
    twenty_e_out: str = Field(default="0,00 €", alias="20eOut")
    ten_e_in: str = Field(default="", alias="10eIn")
    ten_e_out: str = Field(default="0,00 €", alias="10eOut")
    five_e_in: str = Field(default="", alias="5eIn")
    five_e_out: str = Field(default="0,00 €", alias="5eOut")
    two_e_in: str = Field(default="", alias="2eIn")
    two_e_out: str = Field(default="0,00 €", alias="2eOut")
    one_e_in: str = Field(default="", alias="1eIn")
    one_e_out: str = Field(default="0,00 €", alias="1eOut")
    fifty_ct_in: str = Field(default="", alias="50ctIn")
    fifty_ct_out: str = Field(default="0,00 €", alias="50ctOut")
    twenty_ct_in: str = Field(default="", alias="20ctIn")
    twenty_ct_out: str = Field(default="0,00 €", alias="20ctOut")
    ten_ct_in: str = Field(default="", alias="10ctIn")
    ten_ct_out: str = Field(default="0,00 €", alias="10ctOut")

    geld_in_kasse: str = Field(default="________ €", alias="geldInKasse")

    barentnahmen_list: str = Field(default="", alias="barentnahmenList")
    barentnahmen_summe: str = Field(default="= ________ €", alias="barentnahmenSumme")
    ausgezaehlte_bareinnahmen: str = Field(
        default="________ €", alias="ausgezaehlteBareinnahmen"
    )

    barein_zb: str = Field(default="", alias="bareinZb")
    ectrink_zb: str = Field(default="", alias="ectrinkZb")
    tagesumsatz_zb: str = Field(default="", alias="tagesumsatzZb")
    gutschein_bezahlt: str = Field(default="", alias="gutschein_bezahlt")

    total: str = Field(default="________ €", alias="total")
    trinkgeld_gesamt: str = Field(default="________ €", alias="trinkgeldGesamt")
    geld_in_umschlag: str = Field(default="________ €", alias="geldInUmschlag")

    p1: str = "Bitte wählen..."
    p2: str = "Bitte wählen..."
    p3: str = "Bitte wählen..."
    p4: str = "Bitte wählen..."
    p5: str = "Bitte wählen..."
    p6: str = "Bitte wählen..."
    p7: str = "Bitte wählen..."

    s1: str = ""
    s2: str = ""
    s3: str = ""
    s4: str = ""
    s5: str = ""
    s6: str = ""
    s7: str = ""

    tg1: str = Field(default="________ €", alias="tg1")
    tg2: str = Field(default="________ €", alias="tg2")
    tg3: str = Field(default="________ €", alias="tg3")
    tg4: str = Field(default="________ €", alias="tg4")
    tg5: str = Field(default="________ €", alias="tg5")
    tg6: str = Field(default="________ €", alias="tg6")
    tg7: str = Field(default="________ €", alias="tg7")


class TipDistribution(BaseModel):
    tg1: str
    tg2: str
    tg3: str
    tg4: str
    tg5: str
    tg6: str
    tg7: str
