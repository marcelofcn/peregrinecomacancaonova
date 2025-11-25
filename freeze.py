# freeze.py (Versão Corrigida)

from flask_frozen import Freezer
# Importa os dados do novo módulo
from data import ROTEIROS_DB
from main import app # Você precisa importar a instância 'app' de main

# Garante que o Freezer use o Base URL completo para URLs absolutas no GitHub Pages
# A configuração no main.py (com SERVER_NAME) e SCRIPT_NAME aqui deve resolver o erro.
# O FREEZER_BASE_URL para o Freezer deve ser o caminho absoluto para o script_name
# para satisfazer a asserção do Werkzeug.
app.config['FREEZER_BASE_URL'] = '/peregrinecomacancaonova' 
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
    
    # 🚨 SOLUÇÃO PARA O BUG/ASSERÇÃO DO WERKZEUG (script_name):
    # O Flask-Frozen não está detectando corretamente o script_name ao usar FREEZER_BASE_URL.
    # Forçamos o script_name para o nome do subdiretório (repositório).
    # O Freezer injeta este valor no ambiente da requisição.
    app.config['FREEZER_SCRIPT_NAME'] = '/peregrinecomacancaonova'
    
    freezer.freeze()
    print("✅ Congelamento concluído na pasta 'docs'!")
