from fastapi.testclient import TestClient

from app.web import app, default_employee_options, parse_employee_list, resolve_employee_options


client = TestClient(app)


def test_parse_employee_list_trims_dedupes_and_filters_invalid() -> None:
    raw = "\n  Anna  \nANNA\n\nBob\n" + ("x" * 41) + "\n"

    parsed = parse_employee_list(raw)

    assert parsed == ["Anna", "Bob"]


def test_resolve_employee_options_uses_provided_list_or_defaults() -> None:
    parsed = resolve_employee_options("  anna \nmax\nAnna\n")
    defaults = resolve_employee_options("")

    assert parsed == ["anna", "max"]
    assert defaults == default_employee_options()


def test_calculate_renders_temporary_employees_and_keeps_selection() -> None:
    response = client.post(
        "/calculate",
        data={
            "datum": "21.2.2026",
            "barentnahmen_liste": "",
            "zbon_bargeld": "",
            "ec_trinkgeld_zbon": "",
            "tagesumsatz_zbon": "",
            "mit_gutschein_bezahlt": "",
            "employee_list": "Nina\nTom\nnina",
            "trinkgeld_person_1": "Nina",
            "trinkgeld_stunden_1": "3",
        },
    )

    assert response.status_code == 200
    assert '<option selected>Nina</option>' in response.text
    assert response.text.count(">Nina</option>") >= 1
    assert response.text.count(">Tom</option>") >= 1
