from flask import Flask, render_template, redirect, url_for, abort
from data import ROTEIROS_BY_ID, ROTEIROS_DB 
# Importe também as variáveis de configuração globais para o Freezer, se necessário (ex: site_name)
from data import SITE_CONFIG 

app = Flask(__name__)

# --- VARIÁVEIS DE CONTATO (E outras globais) ---
CONTACT_INFO = {
    'phone': '(12) 3186-2600',
    'whatsapp': '5512999999999', # Apenas números
    'email': 'viagenscn@cancaonova.com'
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
    return render_template('home.html', roteiros=ROTEIROS_DB)

# Rota para detalhes do roteiro
@app.route('/roteiro/<int:id>/')
def roteiro_detalhe(id):
    # Usando o ID como string se as chaves do ROTEIROS_BY_ID forem strings (mais comum em JSON)
    roteiro = ROTEIROS_BY_ID.get(str(id)) 
    if not roteiro:
        abort(404)
    return render_template('detalhe.html', roteiro=roteiro)

# Rota de redirecionamento para o contato (Ancora no Rodapé)
@app.route('/contato')
def contato():
    # Redireciona para a home e força o scroll para a âncora do rodapé
    return redirect(url_for('home') + '#rodape-contato')

# Rota para a página "Sobre"
@app.route('/sobre')
def sobre():
    # Por enquanto, podemos usar um template básico ou redirecionar para uma seção da home.
    # Se você não tiver um 'sobre.html', pode criar um simples:
    # return render_template('sobre.html')
    
    # Ou, se o conteúdo Sobre for no rodapé ou na Home:
    # Retornar um 404 temporário é arriscado para o Freezer. 
    # O ideal é criar o arquivo 'sobre.html' ou fazer um redirecionamento útil:
    return render_template('home.html', roteiros=ROTEIROS_DB) # Ou use um template simples "placeholder.html"

# Certifique-se de que todas as rotas mencionadas no base.html existam aqui!

if __name__ == "__main__":
    app.run(debug=True)
