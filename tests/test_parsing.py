from app.parsing import format_euro, parse_fuzzy_number, sum_barentnahmen


def test_parse_fuzzy_number_supports_common_inputs() -> None:
    assert parse_fuzzy_number("12,50") == 12.5
    assert parse_fuzzy_number("12.50 €") == 12.5
    assert parse_fuzzy_number("12 EUR") == 12
    assert parse_fuzzy_number("12 euro") == 12
    assert parse_fuzzy_number("5 stk.") == 5
    assert parse_fuzzy_number("= 17") == 17


def test_parse_fuzzy_number_empty_is_zero() -> None:
    assert parse_fuzzy_number("") == 0
    assert parse_fuzzy_number(None) == 0


def test_sum_barentnahmen() -> None:
    assert sum_barentnahmen("10 + 2,5 + 1€") == 13.5


def test_format_euro_shape() -> None:
    assert format_euro(1) == "1 €"
    assert format_euro(1.5) == "1,5 €"
    assert format_euro(1.234) == "1,23 €"
