# freeze.py
from flask_frozen import Freezer
from main import app
from data import ROTEIROS_DB
import shutil
import os

# limpar docs antes de gerar
if os.path.exists("docs"):
    print("Removendo pasta docs antiga...")
    shutil.rmtree("docs")

app.config["FREEZER_DESTINATION"] = "docs"
app.config["FREEZER_BASE_URL"] = "https://marcelofcn.github.io/peregrinecomacancaonova/"
app.config["FREEZER_REMOVE_EXTRA_FILES"] = False

freezer = Freezer(app)

# único generator necessário
@freezer.register_generator
def roteiro_detalhe():
    for r in ROTEIROS_DB:
        yield 'roteiro_detalhe', {'id': r["id"]}

if __name__ == "__main__":
    print("Iniciando o processo de congelamento (freezing)...")
    freezer.freeze()
    print("✅ Freezer finalizado com sucesso!")
