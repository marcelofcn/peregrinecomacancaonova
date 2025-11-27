# freeze.py

from flask_frozen import Freezer
from data import ROTEIROS_DB
from main import app

# Apenas destino — NÃO repetir BASE_URL aqui
app.config['FREEZER_DESTINATION'] = 'docs'

# Necessário para GitHub Pages em subdiretório
app.config['FREEZER_SCRIPT_NAME'] = '/peregrinecomacancaonova'

freezer = Freezer(app)


@freezer.register_generator
def roteiro_detalhe():
    for r in ROTEIROS_DB:
        yield 'roteiro_detalhe', {'id': r["id"]}


@freezer.register_generator
def contato():
    yield 'contato'


if __name__ == "__main__":
    print("Iniciando o processo de congelamento (freezing)...")
    freezer.freeze()
    print("✅ Congelamento concluído na pasta 'docs'!")
