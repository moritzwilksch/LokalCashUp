from flask import Flask
from flask import render_template

import datetime

app = Flask(__name__)

MALIST = ['Bitte wählen...', 'Sandrina', 'Eric', 'Nochwer']
TODAY = ".".join([str(getattr(datetime.date.today(), att)) for att in ['day', 'month', 'year']])
DEFAULT_FIELDS = {
    'gt100In': '42',
    'gt100Out': '42,00 €'
}


@app.route('/')
def hello_world():
    return render_template('input_form.html',
                           ma_list=MALIST,
                           today=TODAY,
                           fields=DEFAULT_FIELDS)


if __name__ == '__main__':
    app.run()
