# freeze.py
from flask_frozen import Freezer
from app import app
from data_roteiros import ROTEIROS_DB

app.config['FREEZER_DESTINATION'] = 'build'
freezer = Freezer(app)

@freezer.register_generator
def roteiro_detalhe():
    for r in ROTEIROS_DB.values():
        if r.get('empresa') == 'cancaonova':
            yield {'roteiro_id': r['id']}

if __name__ == '__main__':
    freezer.freeze()
