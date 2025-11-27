from flask import Flask, render_template, redirect, url_for, abort, request
from data import ROTEIROS_BY_ID, ROTEIROS_DB, SITE_CONFIG

app = Flask(__name__, static_folder="static", template_folder="templates")

# Freezer / GitHub Pages config (apenas para referência durante freeze)
app.config['FREEZER_REMOVE_EXTRA_FILES'] = False
app.config['FREEZER_BASE_URL'] = 'https://marcelofcn.github.io/peregrinecomacancaonova/'
app.config['SITE_YEAR'] = 2025


# --- VARIÁVEIS DE CONTATO (E outras globais) ---
CONTACT_INFO = {
    'phone': '(12) 3186-2600',
    'whatsapp': '5567998927001',
    'email': 'contato@seudominio.com'
}
GLOBAL_VARS = {**CONTACT_INFO, **SITE_CONFIG}

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
    roteiro = ROTEIROS_BY_ID.get(str(id))
    if not roteiro:
        abort(404)
    return render_template('detalhe.html', roteiro=roteiro)

# Contato: cria página /contato/ que redireciona para home + âncora
@app.route('/contato/')
def contato():
    return redirect(url_for('home') + '#rodape-contato')

# Sobre: página /sobre/
@app.route('/sobre/')
def sobre():
    return render_template('sobre.html', roteiros=ROTEIROS_DB)

# Sitemap simples dinâmico (ajuda SEO e o freezer gera a página)
@app.route('/sitemap.xml')
def sitemap():
    # Gera um sitemap básico com as URLs principais + roteiros
    from flask import Response
    base = app.config.get('FREEZER_BASE_URL', request.host_url)
    urls = []
    urls.append(base)
    urls.append(base + 'sobre/')
    urls.append(base + 'contato/')
    for r in ROTEIROS_DB:
        urls.append(base + f'roteiro/{r["id"]}/')
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        xml += '  <url>\n'
        xml += f'    <loc>{u}</loc>\n'
        xml += '  </url>\n'
    xml += '</urlset>'
    return Response(xml, mimetype='application/xml')

if __name__ == "__main__":
    app.run(debug=True)
