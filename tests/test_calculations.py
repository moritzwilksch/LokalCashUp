from app.calculations import (
    calculate_ausgezaehlte_bareinnahmen,
    calculate_geld_in_umschlag,
    calculate_stueckelung,
    calculate_tip_distribution,
    calculate_total,
    calculate_trinkgeld_gesamt,
)
from app.config import load_config
from app.form_adapter import build_default_form


config = load_config()


def test_calculate_stueckelung_outputs_and_sum() -> None:
    fields = build_default_form("21.2.2026", config)
    values = ["20", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for line, value in zip(fields.denominations, values, strict=True):
        line.quantity_raw = value

    total = calculate_stueckelung(fields, config.denominations)

    assert fields.denominations[0].amount_formatted == "20,0 €"
    assert fields.denominations[1].amount_formatted == "50,0 €"
    assert fields.denominations[2].amount_formatted == "40,0 €"
    assert fields.denominations[3].amount_formatted == "30,0 €"
    assert fields.denominations[4].amount_formatted == "20,0 €"
    assert fields.denominations[5].amount_formatted == "10,0 €"
    assert fields.denominations[6].amount_formatted == "6,0 €"
    assert fields.denominations[7].amount_formatted == "3,5 €"
    assert fields.denominations[8].amount_formatted == "1,6 €"
    assert fields.denominations[9].amount_formatted == "0,9 €"
    assert fields.outputs.geld_in_kasse == "182,0 €"
    assert total == 182.0


def test_calculate_other_core_values() -> None:
    assert calculate_total("100", "5") == 95
    assert calculate_ausgezaehlte_bareinnahmen("200", 10, 100) == 110
    assert calculate_trinkgeld_gesamt(110, "100", "4") == 14
    assert calculate_geld_in_umschlag("100", "4", 10) == 86


def test_tip_distribution_zero_hours_keeps_zero_result() -> None:
    fields = build_default_form("21.2.2026", config)
    tips = calculate_tip_distribution(fields, 30)
    assert tips.values[0] == "0,0 €"
    assert tips.values[6] == "0,0 €"


def test_tip_distribution_weighted() -> None:
    fields = build_default_form("21.2.2026", config)
    fields.tips[0].hours_raw = "2"
    fields.tips[1].hours_raw = "1"
    tips = calculate_tip_distribution(fields, 30)
    assert tips.values[0] == "20,0 €"
    assert tips.values[1] == "10,0 €"
    assert tips.values[2] == "0,0 €"
