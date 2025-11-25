from flask import Flask, render_template, redirect, url_for, abort
from data import ROTEIROS_BY_ID, ROTEIROS_DB, SITE_CONFIG 

app = Flask(__name__)

# --- Configuração do Flask/Freezer para GitHub Pages ---
# 1. Definir o nome do servidor (importante para url_for funcionar corretamente com subdiretórios)
app.config['FREEZER_REMOVE_EXTRA_FILES'] = False


# 2. Definir o Base URL com a barra final (CRÍTICO)
app.config['FREEZER_BASE_URL'] = 'https://marcelofcn.github.io/peregrinecomacancaonova/'
# --------------------------------------------------------

# --- VARIÁVEIS DE CONTATO (E outras globais) ---
CONTACT_INFO = {
    'phone': '(12) 3186-2600',
    'whatsapp': '5567998927001', # Apenas números
    
}
# Juntar info de contato com outras configurações do SITE_CONFIG para uso global
GLOBAL_VARS = {**CONTACT_INFO, **SITE_CONFIG} 
# -----------------------------

# Adiciona variáveis ao contexto de todos os templates
@app.context_processor
def inject_global_vars():
    return GLOBAL_VARS

# Rota para a página inicial
@app.route('/')
def home():
    # Use _external=True para que o Flask use o SERVER_NAME e FREEZER_BASE_URL para construir a URL
    # mas o Freezer já deve cuidar disso.
    return render_template('home.html', roteiros=ROTEIROS_DB)

# Rota para detalhes do roteiro
@app.route('/roteiro/<int:id>/')
def roteiro_detalhe(id):
    # Usando o ID como string se as chaves do ROTEIROS_BY_ID forem strings (mais comum em JSON)
    roteiro = ROTEIROS_BY_ID.get(str(id)) 
    if not roteiro:
        abort(404)
    return render_template('detalhe.html', roteiro=roteiro)

# main.py
# ...

# Rota de redirecionamento para o contato (Ancora no Rodapé)
# Mude de @app.route('/contato') para:
@app.route('/contato.html') # Salvar como arquivo .html explícito
def contato():
    # Redireciona para a home e força o scroll para a âncora do rodapé
    return redirect(url_for('home') + '#rodape-contato')

# Mude de @app.route('/sobre') para:
@app.route('/sobre.html') # Salvar como arquivo .html explícito
def sobre():
    return render_template('sobre.html', roteiros=ROTEIROS_DB) # Assumindo que sobre.html existe

# Certifique-se de que todas as rotas mencionadas no base.html existam aqui!

if __name__ == "__main__":
    app.run(debug=True)
