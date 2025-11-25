# main.py (Versão Corrigida/Refatorada)

from flask import Flask, render_template, abort
# Importa os dados do novo módulo
from data import ROTEIROS_DB, ROTEIROS_BY_ID # <--- 💡 MUDANÇA AQUI!
import os # Manter se necessário para outras coisas, mas não para o JSON

# ... Configuração principal do Flask (igual) ...

# ---------------------------------------
# Rotas
# ---------------------------------------
@app.route("/")
def home():
    """Página inicial com todos os roteiros"""
    return render_template("home.html", roteiros=ROTEIROS_DB)

@app.route("/roteiro/<int:id>/")
def roteiro_detalhe(id):
    """Página de detalhe de um roteiro específico"""
    roteiro = ROTEIROS_BY_ID.get(str(id))
    # ... (Restante da rota igual) ...

# main.py (Exemplo de como adicionar as informações de contato)

from flask import Flask, render_template, redirect, url_for, abort
from data import ROTEIROS_BY_ID, ROTEIROS_DB # Garanta que estas variáveis estão corretas após a correção

app = Flask(__name__)

# --- VARIÁVEIS DE CONTATO ---
CONTACT_INFO = {
    'phone': '(12) 3186-2600',
    'whatsapp': '5512999999999', # Apenas números para link no WhatsApp
    'email': 'viagenscn@cancaonova.com'
}
# -----------------------------

# Adicione estas informações ao contexto de todos os templates, se necessário
@app.context_processor
def inject_global_vars():
    # Isso permite usar 'phone', 'whatsapp', 'email' em qualquer template sem passar na rota
    return CONTACT_INFO

# ... (outras rotas) ...

# Rota para a página inicial
@app.route('/')
def home():
    return render_template('home.html', roteiros=ROTEIROS_DB)

# Rota de redirecionamento para o contato (Ancora)
@app.route('/contato')
def contato():
    # Redireciona para a página inicial (ou detalhe), forçando o scroll para o rodapé ou CTA
    # Redirecionar para a home com uma âncora é a forma mais simples de "simular" a rota
    # Se você quiser uma página de contato separada futuramente, mude esta função.
    return redirect(url_for('home') + '#rodape-contato') # Vamos criar esta âncora no base.html
    # OU se você quiser ser mais simples, basta pedir ao usuário para ligar/chamar.
    # Como não temos um contato.html, usaremos o link do WhatsApp/Telefone diretamente no template.


# Rota para detalhes do roteiro
@app.route('/roteiro/<int:id>/')
def roteiro_detalhe(id):
    roteiro = ROTEIROS_BY_ID.get(id)
    if not roteiro:
        abort(404)
    return render_template('detalhe.html', roteiro=roteiro)
