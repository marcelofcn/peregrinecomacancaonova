from flask_frozen import Freezer
from data import ROTEIROS_DB
from main import app

app.config['FREEZER_BASE_URL'] = 'https://marcelofcn.github.io/peregrinecomacancaonova/'
app.config['FREEZER_DESTINATION'] = 'docs'

freezer = Freezer(app)

@freezer.register_generator
def roteiro_detalhe():
    for id_str, r in ROTEIROS_DB.items():
        yield 'roteiro_detalhe', {'id': int(id_str)}

@freezer.register_generator
def sobre():
    yield 'sobre'

if __name__ == "__main__":
    print("Iniciando o processo de congelamento (freezing)...")
    freezer.freeze()
    print("✅ Congelamento concluído!")
