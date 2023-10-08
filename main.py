import datetime

from flask import Flask, redirect, render_template, request

app = Flask(__name__)


# CONSTANTS
MALIST = [
    "Bitte wählen...",
    "Susanne",
    "Jule",
    "Carallalola",
    "Anke",
    "Katia",
    "Felix",
    "Philip",
    "Saphira",
    "Alina",
    "Michele",
    "Marc",
    "Aushilfe",
]
TODAY = ".".join(
    [str(getattr(datetime.date.today(), att)) for att in ["day", "month", "year"]]
)
DEFAULT_FIELDS = {
    "gt100In": "",
    "gt100Out": "0,00 €",
    "50eIn": "",
    "50eOut": "0,00 €",
    "20eIn": "",
    "20eOut": "0,00 €",
    "10eIn": "",
    "10eOut": "0,00 €",
    "5eIn": "",
    "5eOut": "0,00 €",
    "2eIn": "",
    "2eOut": "0,00 €",
    "1eIn": "",
    "1eOut": "0,00 €",
    "50ctIn": "",
    "50ctOut": "0,00 €",
    "20ctIn": "",
    "20ctOut": "0,00 €",
    "10ctIn": "",
    "10ctOut": "0,00 €",
    "geldInKasse": "________ €",
    "ausgezaehlteBareinnahmen": "________ €",
    "trinkgeldGesamt": "________ €",
    "geldInUmschlag": "________ €",
    "barentnahmenSumme": "= ________ €",
    "tg1": "________ €",
    "tg2": "________ €",
    "tg3": "________ €",
    "tg4": "________ €",
    "tg5": "________ €",
    "tg6": "________ €",
    "tg7": "________ €",
    "total": "________ €",
}
WECHSELGELD_TAGESANFANG = 100
fields_to_be_shown = {}

# METHODS
def prep_convert_numeric_string(s: str) -> float:
    if s == "":
        return 0
    else:
        return float(
            s.lower()
            .replace(",", ".")
            .replace("€", "")
            .replace("eur", "")
            .replace("euro", "")
            .replace("stk.", "")
            .replace("stk", "")
            .replace("=", "")
            .strip()
        )


def convert_to_string_output(n: float) -> str:
    """Converts result into outputable string (rounded to two DP, appends €, fixes US decimal point)"""
    return str(round(n, 2)).replace(".", ",") + " €"


def calculate_stueckelung(d: dict) -> dict:
    """Fetches Inputs (Stueckelung) from dict and calculates Outputs. Updates and returns the dict."""
    in_keys = [
        "gt100In",
        "50eIn",
        "20eIn",
        "10eIn",
        "5eIn",
        "2eIn",
        "1eIn",
        "50ctIn",
        "20ctIn",
        "10ctIn",
    ]
    out_keys = [
        "gt100Out",
        "50eOut",
        "20eOut",
        "10eOut",
        "5eOut",
        "2eOut",
        "1eOut",
        "50ctOut",
        "20ctOut",
        "10ctOut",
    ]
    factors = [1, 50, 20, 10, 5, 2, 1, 0.5, 0.2, 0.1]
    summe = 0

    for in_key, out_key, factor in zip(in_keys, out_keys, factors):
        input_anzahl = prep_convert_numeric_string(d.get(in_key, "0"))
        value = input_anzahl * factor
        summe += value
        d.update({out_key: convert_to_string_output(value)})

    d.update({"geldInKasse": convert_to_string_output(summe)})
    return d


def sum_barentnahmen(s: str) -> float:
    """Sums all values in a string of shape: value + value + value"""
    try:
        s = str(s)
    except:
        pass
    l = s.split("+")
    l = [prep_convert_numeric_string(elem) for elem in l]
    return sum(l)


def calculate_tip_distribution(d: dict) -> dict:
    """Calculates weighted distribution of tips from dict. Returns dict."""
    hours = ["s1", "s2", "s3", "s4", "s5", "s6", "s7"]
    tgs = ["tg1", "tg2", "tg3", "tg4", "tg5", "tg6", "tg7"]

    hour_values = [prep_convert_numeric_string(d.get(x, "0")) for x in hours]
    total_hours = sum(hour_values)
    if total_hours == 0:
        total_hours = 0.000001

    for stunden, trinkgeld in zip(hours, tgs):
        d.update(
            {
                trinkgeld: convert_to_string_output(
                    prep_convert_numeric_string(d.get(stunden, "0"))
                    / total_hours
                    * prep_convert_numeric_string(d.get("trinkgeldGesamt", "0"))
                )
            }
        )

    return d


# ROUTES
@app.route("/")
def index():
    return render_template(
        "input_form.html", ma_list=MALIST, today=TODAY, fields=DEFAULT_FIELDS
    )


@app.route("/calculate", methods=["POST"])
def calculate():
    # load default values
    global fields_to_be_shown
    fields_to_be_shown = DEFAULT_FIELDS.copy()

    # load user input values
    fields_to_be_shown.update(dict(request.form))

    # Calculate light fields for stueckelung-card
    fields_to_be_shown = calculate_stueckelung(fields_to_be_shown)

    # Sum Barentnahmen List
    fields_to_be_shown.update(
        {
            "barentnahmenSumme": "= "
            + convert_to_string_output(
                sum_barentnahmen(fields_to_be_shown.get("barentnahmenList", "0"))
            )
        }
    )

    # Calculate ausgezaehlte Bareinnahmen
    fields_to_be_shown.update(
        {
            "ausgezaehlteBareinnahmen": convert_to_string_output(
                (
                    prep_convert_numeric_string(
                        fields_to_be_shown.get("barentnahmenSumme", "0")
                    )
                    + prep_convert_numeric_string(
                        fields_to_be_shown.get("geldInKasse", "0")
                    )
                )
                - WECHSELGELD_TAGESANFANG
            )
        }
    )

    # Calculate Total
    fields_to_be_shown.update(
        {
            "total": convert_to_string_output(
                prep_convert_numeric_string(
                    fields_to_be_shown.get("tagesumsatzZb", "0")
                )
                - prep_convert_numeric_string(
                    fields_to_be_shown.get("gutschein_bezahlt", "0")
                )
            )
        }
    )

    # Calculate Trinkgeld gesamt
    fields_to_be_shown.update(
        {
            "trinkgeldGesamt": convert_to_string_output(
                prep_convert_numeric_string(
                    fields_to_be_shown.get("ausgezaehlteBareinnahmen", "0")
                )
                - prep_convert_numeric_string(fields_to_be_shown.get("bareinZb", "0"))
                + prep_convert_numeric_string(fields_to_be_shown.get("ectrinkZb", "0"))
            )
        }
    )

    # Calculate Geld im Umschlag
    fields_to_be_shown.update(
        {
            "geldInUmschlag": convert_to_string_output(
                prep_convert_numeric_string(fields_to_be_shown.get("bareinZb", "0"))
                - prep_convert_numeric_string(fields_to_be_shown.get("ectrinkZb", "0"))
                - prep_convert_numeric_string(
                    fields_to_be_shown.get("barentnahmenSumme", "0")
                )
            )
        }
    )

    # Calculate tip distribution
    fields_to_be_shown = calculate_tip_distribution(fields_to_be_shown)

    print(request.form)
    return render_template(
        "input_form.html", ma_list=MALIST, today=TODAY, fields=fields_to_be_shown
    )


@app.route("/resetFields")
def reset_fields():
    return redirect("/")


@app.route("/printPage")
def print_page():
    return render_template(
        "printable_output.html",
        today=TODAY,
        fields=fields_to_be_shown,
        wechselgeld=WECHSELGELD_TAGESANFANG,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1605)
