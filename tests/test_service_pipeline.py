from app.config import load_config
from app.form_parser import parse_form_data
from app.service import apply_calculation_pipeline


config = load_config()


def test_full_pipeline_regression_case() -> None:
    form = parse_form_data(
        {
            "datum": "21.2.2026",
            "denom_betrag_ab_100": "20",
            "denom_scheine_50e": "1",
            "denom_scheine_20e": "2",
            "denom_scheine_10e": "3",
            "denom_scheine_5e": "4",
            "denom_muenzen_2e": "5",
            "denom_muenzen_1e": "6",
            "denom_muenzen_50ct": "7",
            "denom_muenzen_20ct": "8",
            "denom_muenzen_10ct": "9",
            "barentnahmen_liste": "10 + 20 + 3,5",
            "zbon_bargeld": "180",
            "ec_trinkgeld_zbon": "2",
            "tagesumsatz_zbon": "245",
            "mit_gutschein_bezahlt": "5",
            "trinkgeld_stunden_1": "4",
            "trinkgeld_stunden_2": "2",
            "trinkgeld_stunden_3": "2",
        },
        today="21.2.2026",
        config=config,
    )

    out = apply_calculation_pipeline(form, config)

    assert out.outputs.geld_in_kasse == "182,0 €"
    assert out.outputs.barentnahmen_summe == "= 33,5 €"
    assert out.outputs.ausgezaehlte_bareinnahmen == "115,5 €"
    assert out.outputs.total == "240,0 €"
    assert out.outputs.trinkgeld_gesamt == "-62,5 €"
    assert out.outputs.geld_in_umschlag == "144,5 €"
    assert out.tips[0].tip_formatted == "-31,25 €"
    assert out.tips[1].tip_formatted == "-15,62 €"
    assert out.tips[2].tip_formatted == "-15,62 €"
