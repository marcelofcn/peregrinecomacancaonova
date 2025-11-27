from flask_frozen import Freezer
import shutil
import os
from main import app
from data import ROTEIROS_DB

# Base URL completa para GitHub Pages (subdiretório)
app.config['FREEZER_BASE_URL'] = 'https://marcelofcn.github.io/peregrinecomacancaonova/'
app.config['FREEZER_DESTINATION'] = 'docs'
# opcionalmente ajuste script name se precisar:
# app.config['FREEZER_SCRIPT_NAME'] = '/peregrinecomacancaonova'

freezer = Freezer(app)

@freezer.register_generator
def roteiro_detalhe():
    # ROTEIROS_DB é uma lista de dicts (cada um com 'id' int)
    for r in ROTEIROS_DB:
        # yield route name and params
        yield 'roteiro_detalhe', {'id': r['id']}

@freezer.register_generator
def sobre():
    yield 'sobre', {}

@freezer.register_generator
def contato():
    yield 'contato', {}

@freezer.register_generator
def sitemap():
    yield 'sitemap'


if __name__ == "__main__":
    print("Iniciando o processo de congelamento (freezing)...")

    # Remove a pasta docs antiga para evitar conflitos de diretório/arquivo
    docs_path = os.path.join(os.path.dirname(__file__), 'docs')
    if os.path.exists(docs_path):
        print("Removendo pasta docs antiga...")
        shutil.rmtree(docs_path)

    # Cria pasta docs vazia
    os.makedirs(docs_path, exist_ok=True)

    freezer.freeze()
    print("✅ Congelamento concluído na pasta 'docs'!")
