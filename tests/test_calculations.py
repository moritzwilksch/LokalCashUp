from app.calculations import (
    calculate_ausgezaehlte_bareinnahmen,
    calculate_geld_in_umschlag,
    calculate_stueckelung,
    calculate_tip_distribution,
    calculate_total,
    calculate_trinkgeld_gesamt,
)
from app.config import load_config
from app.models import CashFields


config = load_config()


def test_calculate_stueckelung_outputs_and_sum() -> None:
    fields = CashFields.model_validate(
        {
            "gt100In": "20",
            "50eIn": "1",
            "20eIn": "2",
            "10eIn": "3",
            "5eIn": "4",
            "2eIn": "5",
            "1eIn": "6",
            "50ctIn": "7",
            "20ctIn": "8",
            "10ctIn": "9",
        }
    )

    updates, total = calculate_stueckelung(fields, config.denominations)

    assert updates["gt100Out"] == "20,0 €"
    assert updates["50eOut"] == "50,0 €"
    assert updates["20eOut"] == "40,0 €"
    assert updates["10eOut"] == "30,0 €"
    assert updates["5eOut"] == "20,0 €"
    assert updates["2eOut"] == "10,0 €"
    assert updates["1eOut"] == "6,0 €"
    assert updates["50ctOut"] == "3,5 €"
    assert updates["20ctOut"] == "1,6 €"
    assert updates["10ctOut"] == "0,9 €"
    assert updates["geldInKasse"] == "182,0 €"
    assert total == 182.0


def test_calculate_other_core_values() -> None:
    assert calculate_total("100", "5") == 95
    assert calculate_ausgezaehlte_bareinnahmen("200", 10, 100) == 110
    assert calculate_trinkgeld_gesamt(110, "100", "4") == 14
    assert calculate_geld_in_umschlag("100", "4", 10) == 86


def test_tip_distribution_zero_hours_keeps_zero_result() -> None:
    fields = CashFields.model_validate({"trinkgeldGesamt": "30"})
    tips = calculate_tip_distribution(fields, 30)
    assert tips.tg1 == "0,0 €"
    assert tips.tg7 == "0,0 €"


def test_tip_distribution_weighted() -> None:
    fields = CashFields.model_validate({"s1": "2", "s2": "1"})
    tips = calculate_tip_distribution(fields, 30)
    assert tips.tg1 == "20,0 €"
    assert tips.tg2 == "10,0 €"
    assert tips.tg3 == "0,0 €"
