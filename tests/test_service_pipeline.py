from app.config import load_config
from app.form_adapter import parse_form_data, to_template_fields
from app.service import apply_calculation_pipeline


config = load_config()


def test_full_pipeline_regression_case() -> None:
    fields = parse_form_data(
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
            "barentnahmenList": "10 + 20 + 3,5",
            "bareinZb": "180",
            "ectrinkZb": "2",
            "tagesumsatzZb": "245",
            "gutschein_bezahlt": "5",
            "s1": "4",
            "s2": "2",
            "s3": "2",
        },
        today="21.2.2026",
        config=config,
    )

    out = apply_calculation_pipeline(fields, config)
    dump = to_template_fields(out, config)

    assert dump["geldInKasse"] == "182,0 €"
    assert dump["barentnahmenSumme"] == "= 33,5 €"
    assert dump["ausgezaehlteBareinnahmen"] == "115,5 €"
    assert dump["total"] == "240,0 €"
    assert dump["trinkgeldGesamt"] == "-62,5 €"
    assert dump["geldInUmschlag"] == "144,5 €"
    assert dump["tg1"] == "-31,25 €"
    assert dump["tg2"] == "-15,62 €"
    assert dump["tg3"] == "-15,62 €"
