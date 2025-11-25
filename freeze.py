# freeze.py (Versão Corrigida para GitHub Pages Subdiretório e rotas)

from flask_frozen import Freezer
# Importa os dados do novo módulo
from data import ROTEIROS_DB
from main import app # Você precisa importar a instância 'app' de main

# Garante que o Freezer use o Base URL COMPLETO para a implantação no GitHub Pages.
# A barra final é importante!
app.config['FREEZER_BASE_URL'] = 'https://marcelofcn.github.io/peregrinecomacancaonova/' 
app.config['FREEZER_DESTINATION'] = 'docs' 
freezer = Freezer(app)

@freezer.register_generator
def roteiro_detalhe():
    for r in ROTEIROS_DB:
        # NOTE: O generator do Flask-Frozen precisa que você use a rota do Flask
        # Certifique-se que o 'id' seja passado como string se for a chave do JSON
        yield 'roteiro_detalhe', {'id': r["id"]} 

@freezer.register_generator
def sobre():
    # Se a rota for @app.route('/sobre.html'), o nome da função é 'sobre'
    yield 'sobre' 


if __name__ == "__main__":
    print("Iniciando o processo de congelamento (freezing)...")
    
    # 🚨 SOLUÇÃO DE CONTORNO PARA ASSERÇÃO (DEVE SER USADA JUNTO COM A CORREÇÃO NO main.py):
    # Forçamos o script_name para o nome do subdiretório.
    app.config['FREEZER_SCRIPT_NAME'] = '/peregrinecomacancaonova'
    
    freezer.freeze()
    print("✅ Congelamento concluído na pasta 'docs'!")
