from flask_frozen import Freezer
from data import ROTEIROS_DB
from main import app

# Configurações obrigatórias
app.config['FREEZER_BASE_URL'] = 'https://marcelofcn.github.io/peregrinecomacancaonova/'
app.config['FREEZER_DESTINATION'] = 'docs'
app.config['FREEZER_RELATIVE_URLS'] = False
app.config['FREEZER_REMOVE_EXTRA_FILES'] = False

freezer = Freezer(app)

# ---------------------------
# 🔥 GERAR DETALHES DOS ROTEIROS
# ---------------------------
@freezer.register_generator
def roteiro_detalhe():
    # ROTEIROS_DB é um dict: {'3': {...}, '8': {...}}
    for id_str in ROTEIROS_DB.keys():
        yield 'roteiro_detalhe', {'id': int(id_str)}

# ---------------------------
# 🔥 GERAR PÁGINAS SOBRE E CONTATO
# ---------------------------
@freezer.register_generator
def sobre():
    yield 'sobre'   # sua rota é /sobre/

@freezer.register_generator
def contato():
    yield 'contato'  # sua rota é /contato/

# ---------------------------

if __name__ == "__main__":
    print("Iniciando o processo de congelamento (freezing)...")
    freezer.freeze()
    print("✅ Congelamento concluído!")
