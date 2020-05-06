from flask import Flask, request
from flask import render_template
import datetime

app = Flask(__name__)

# CONSTANTS
MALIST = ['Bitte wählen...', 'Sandrina', 'Eric', 'Nochwer']
TODAY = ".".join([str(getattr(datetime.date.today(), att)) for att in ['day', 'month', 'year']])
DEFAULT_FIELDS = {
    'gt100In': '1',
    'gt100Out': '0,00 €',
    '50eIn': '2',
    '50eOut': '0,00 €',
    '20eIn': '3',
    '20eOut': '0,00 €',
    '10eIn': '4',
    '10eOut': '0,00 €',
    '5eIn': '5',
    '5eOut': '0,00 €',
    '2eIn': '6',
    '2eOut': '0,00 €',
    '1eIn': '7',
    '1eOut': '0,00 €',
    '50ctIn': '8',
    '50ctOut': '0,00 €',
    '20ctIn': '9',
    '20ctOut': '0,00 €',
    '10ctIn': '10',
    '10ctOut': '0,00 €',
    'geldInKasse': '______ €',
    'ausgezaehlteBareinnahmen': '______ €',
}
TRINKGELD_TAGESANFANG = 250


# METHODS
def prep_convert_numeric_string(s: str) -> float:
    return float(s.lower()
                 .replace(',', '.')
                 .replace('€', '')
                 .replace("eur", '')
                 .replace('euro', '')
                 .replace('stk.', '')
                 .replace('stk', '')
                 .replace('=', '')
                 .strip()
                 )


def convert_to_string_output(n: float) -> str:
    """Converts result into outputable string (rounded to two DP, appends €, fixes US decimal point)"""
    return str(round(n, 2)).replace('.', ',') + " €"


def calculate_stueckelung(d: dict) -> dict:
    """Fetches Inputs (Stueckelung) from dict and calculates Outputs. Updates and returns the dict."""
    in_keys = ['gt100In', '50eIn', '20eIn', '10eIn', '5eIn', '2eIn', '1eIn', '50ctIn', '20ctIn', '10ctIn']
    out_keys = ['gt100Out', '50eOut', '20eOut', '10eOut', '5eOut', '2eOut', '1eOut', '50ctOut', '20ctOut', '10ctOut']
    factors = [1, 50, 20, 10, 5, 2, 1, 0.5, 0.2, 0.1]
    summe = 0

    for in_key, out_key, factor in zip(in_keys, out_keys, factors):
        input_anzahl = prep_convert_numeric_string(d.get(in_key, 0))
        value = input_anzahl * factor
        summe += value
        d.update({out_key: convert_to_string_output(value)})

    d.update({'geldInKasse': convert_to_string_output(summe)})
    return d


def sum_barentnahmen(s: str) -> float:
    """Sums all values in a string of shape: value + value + value"""
    l = s.split('+')
    l = [prep_convert_numeric_string(elem) for elem in l]
    return sum(l)


# ROUTES
@app.route('/')
def index():
    return render_template('input_form.html',
                           ma_list=MALIST,
                           today=TODAY,
                           fields=DEFAULT_FIELDS)


@app.route('/calculate', methods=['POST'])
def posttest():
    # load default values
    fields_to_be_shown = DEFAULT_FIELDS.copy()
    # load user input values
    fields_to_be_shown.update(dict(request.form))
    # Calculate light fields for stueckelung-card
    fields_to_be_shown = calculate_stueckelung(fields_to_be_shown)
    # Sum Barentnahmen List
    fields_to_be_shown.update({
        'barentnahmenSumme': "= " + convert_to_string_output(
            sum_barentnahmen(
                fields_to_be_shown.get('barentnahmenList', 0)
            )
        )}
    )

    fields_to_be_shown.update({'ausgezaehlteBareinnahmen': convert_to_string_output(
        (prep_convert_numeric_string(fields_to_be_shown.get('barentnahmenSumme', 0))
         + prep_convert_numeric_string(fields_to_be_shown.get('geldInKasse', 0))
         ) - TRINKGELD_TAGESANFANG
    )})

    print(request.form)
    return render_template('input_form.html',
                           ma_list=MALIST,
                           today=TODAY,
                           fields=fields_to_be_shown)


if __name__ == '__main__':
    app.run()
