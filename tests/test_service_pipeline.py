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


def test_full_pipeline_realistic_receipt_regression_case() -> None:
    form = parse_form_data(
        {
            "datum": "22.2.2026",
            "denom_betrag_ab_100": "100",
            "denom_scheine_50e": "3",
            "denom_scheine_20e": "3",
            "denom_scheine_10e": "4",
            "denom_scheine_5e": "3",
            "denom_muenzen_2e": "11",
            "denom_muenzen_1e": "10",
            "denom_muenzen_50ct": "21",
            "denom_muenzen_20ct": "14",
            "denom_muenzen_10ct": "12",
            "barentnahmen_liste": "14,30+5,40",
            "zbon_bargeld": "305,90",
            "ec_trinkgeld_zbon": "70,10",
            "tagesumsatz_zbon": "1459,60",
            "mit_gutschein_bezahlt": "0",
            "trinkgeld_person_1": "Jule",
            "trinkgeld_stunden_1": "6",
            "trinkgeld_person_2": "Leon",
            "trinkgeld_stunden_2": "8,5",
            "trinkgeld_person_3": "Alina",
            "trinkgeld_stunden_3": "3,5",
            "trinkgeld_person_4": "Endric",
            "trinkgeld_stunden_4": "7",
            "trinkgeld_person_5": "Carallalola",
            "trinkgeld_stunden_5": "8",
            "trinkgeld_person_6": "Anke",
            "trinkgeld_stunden_6": "7",
        },
        today="22.2.2026",
        config=config,
    )

    out = apply_calculation_pipeline(form, config)

    assert out.denominations[0].amount_formatted == "100,0 €"
    assert out.denominations[1].amount_formatted == "150,0 €"
    assert out.denominations[2].amount_formatted == "60,0 €"
    assert out.denominations[3].amount_formatted == "40,0 €"
    assert out.denominations[4].amount_formatted == "15,0 €"
    assert out.denominations[5].amount_formatted == "22,0 €"
    assert out.denominations[6].amount_formatted == "10,0 €"
    assert out.denominations[7].amount_formatted == "10,5 €"
    assert out.denominations[8].amount_formatted == "2,8 €"
    assert out.denominations[9].amount_formatted == "1,2 €"

    assert out.outputs.geld_in_kasse == "411,5 €"
    assert out.outputs.barentnahmen_summe == "= 19,7 €"
    assert out.outputs.ausgezaehlte_bareinnahmen == "331,2 €"
    assert out.outputs.trinkgeld_gesamt == "95,4 €"
    assert out.outputs.geld_in_umschlag == "216,1 €"
    assert out.outputs.total == "1459,6 €"

    assert out.tips[0].tip_formatted == "14,31 €"
    assert out.tips[1].tip_formatted == "20,27 €"
    assert out.tips[2].tip_formatted == "8,35 €"
    assert out.tips[3].tip_formatted == "16,7 €"
    assert out.tips[4].tip_formatted == "19,08 €"
    assert out.tips[5].tip_formatted == "16,7 €"
