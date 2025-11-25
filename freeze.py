# freeze.py (Versão Corrigida)

from flask_frozen import Freezer
# Importa os dados do novo módulo
from data import ROTEIROS_DB
from main import app # Você precisa importar a instância 'app' de main

# Garante que o Freezer use o Base URL completo para URLs absolutas no GitHub Pages
# Isso é duplicado do main.py, mas essencial para o Freezer funcionar corretamente.
app.config['FREEZER_BASE_URL'] = 'https://marcelofcn.github.io/peregrinecomacancaonova/'
app.config['FREEZER_DESTINATION'] = 'docs' 
freezer = Freezer(app)

@freezer.register_generator
def roteiro_detalhe():
    for r in ROTEIROS_DB:
        # NOTE: O generator do Flask-Frozen precisa que você use a rota do Flask
        # Certifique-se que o 'id' seja passado como string se for a chave do JSON
        yield 'roteiro_detalhe', {'id': r["id"]} 


if __name__ == "__main__":
    print("Iniciando o processo de congelamento (freezing)...")
    freezer.freeze()
    print("✅ Congelamento concluído na pasta 'docs'!")
