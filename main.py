# main.py - VERSÃO AJUSTADA
from flask import Flask, render_template, redirect, url_for, abort, request, Response
from data import ROTEIROS_BY_ID, ROTEIROS_DB, SITE_CONFIG

app = Flask(__name__, static_folder="static", template_folder="templates")

# Configurações
app.config['FREEZER_REMOVE_EXTRA_FILES'] = False
app.config['FREEZER_BASE_URL'] = 'https://marcelofcn.github.io/peregrinecomacancaonova/'
app.config['FREEZER_RELATIVE_URLS'] = True  # IMPORTANTE
app.config['SITE_YEAR'] = 2025

# Variáveis de contato
CONTACT_INFO = {
    'phone': '(67) 99892-7001',
    'whatsapp': '5567998927001',
    'email': 'contato@peregrinecomacancaonova.com'
}

GLOBAL_VARS = {**CONTACT_INFO, **SITE_CONFIG}

@app.context_processor
def inject_global_vars():
    return GLOBAL_VARS

# ============ ROTAS ============

@app.route('/')
def home():
    return render_template('home.html', roteiros=ROTEIROS_DB)

# IMPORTANTE: Remover trailing slash para melhor compatibilidade
@app.route('/roteiro/<int:id>')
@app.route('/roteiro/<int:id>/')
def roteiro_detalhe(id):
    """Aceita URL com ou sem barra final"""
    roteiro = ROTEIROS_BY_ID.get(str(id))
    if not roteiro:
        abort(404)
    return render_template('detalhe.html', roteiro=roteiro)

@app.route('/contato')
@app.route('/contato/')
def contato():
    """Redireciona para home com âncora"""
    return redirect(url_for('home') + '#rodape-contato')

@app.route('/sobre')
@app.route('/sobre/')
def sobre():
    return render_template('sobre.html', roteiros=ROTEIROS_DB)

@app.route('/sitemap.xml')
def sitemap():
    """Sitemap XML dinâmico"""
    from datetime import datetime
    
    base = app.config.get('FREEZER_BASE_URL', request.url_root).rstrip('/')
    pages = []
    
    # Página inicial
    pages.append({
        'loc': f"{base}/",
        'lastmod': datetime.utcnow().date().isoformat(),
        'priority': '1.0'
    })
    
    # Roteiros
    for r in ROTEIROS_DB:
        pages.append({
            'loc': f"{base}/roteiro/{r['id']}/",
            'lastmod': datetime.utcnow().date().isoformat(),
            'priority': '0.8'
        })
    
    # Sobre
    pages.append({
        'loc': f"{base}/sobre/",
        'lastmod': datetime.utcnow().date().isoformat(),
        'priority': '0.6'
    })
    
    xml = render_template('sitemap.xml', pages=pages)
    return Response(xml, mimetype='application/xml')

# Handler de erro 404
@app.errorhandler(404)
def page_not_found(e):
    """Página customizada de erro 404"""
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
