# freeze.py (Versão Corrigida)

from flask_frozen import Freezer
# Importa os dados do novo módulo
from data import ROTEIROS_DB # <--- 💡 MUDANÇA AQUI!
from main import app # Você precisa importar a instância 'app' de main

freezer = Freezer(app) # <--- 💡 MUDANÇA AQUI: Passar a instância do app

@freezer.register_generator
def roteiro_detalhe():
    for r in ROTEIROS_DB:
        # NOTE: O generator do Flask-Frozen precisa que você use a rota do Flask
        yield 'roteiro_detalhe', {'id': r["id"]} # <--- 💡 MUDANÇA AQUI: Passar o nome da função e os argumentos

if __name__ == "__main__":
    print("Iniciando o processo de congelamento (freezing)...")
    freezer.freeze()
    print("✅ Congelamento concluído na pasta 'docs'!")
