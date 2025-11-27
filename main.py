# main.py - VERSÃO DEFINITIVA SEM DEPENDÊNCIA DO data.py
from flask import Flask, render_template, redirect, url_for, abort, request, Response
import json
import os
from datetime import datetime

app = Flask(__name__, static_folder="static", template_folder="templates")

# Configurações
app.config['FREEZER_REMOVE_EXTRA_FILES'] = False
app.config['FREEZER_BASE_URL'] = 'https://marcelofcn.github.io/peregrinecomacancaonova/'
app.config['FREEZER_RELATIVE_URLS'] = True
app.config['SITE_YEAR'] = 2025

print("\n" + "="*70)
print("🚀 CARREGANDO ROTEIROS (main.py)")
print("="*70)

# CARREGAR ROTEIROS DIRETAMENTE
def carregar_roteiros_direto():
    """Carrega roteiros diretamente do JSON"""
    roteiros_file = os.path.join(os.path.dirname(__file__), 'roteiros.json')
    
    print(f"📄 Arquivo: {roteiros_file}")
    print(f"✅ Existe? {os.path.exists(roteiros_file)}")
    
    if not os.path.exists(roteiros_file):
        print("❌ Arquivo não encontrado!")
        return []
    
    try:
        with open(roteiros_file, 'r', encoding='utf-8') as f:
            roteiros_dict = json.load(f)
        
        print(f"✅ JSON válido: {len(roteiros_dict)} entradas")
        
        lista = []
        filtrados = 0
        
        for key, r in roteiros_dict.items():
            # Filtrar São José
            director = str(r.get('director', '')).lower()
            empresa = str(r.get('empresa', '')).lower()
            
            if any(x in director or x in empresa for x in ['sao jose', 'são josé', 'loja sao', 'loja são']):
                filtrados += 1
                continue
            
            try:
                # Processar itinerário
                itinerario = r.get('itinerario', {})
                if isinstance(itinerario, dict):
                    itinerario_lista = [f"{k} – {v}" for k, v in sorted(itinerario.items())]
                elif isinstance(itinerario, list):
                    itinerario_lista = itinerario
                else:
                    itinerario_lista = []
                
                # Processar diretor
                director_raw = r.get('director', 'Equipe Canção Nova')
                if isinstance(director_raw, list):
                    director_display = ', '.join(str(d) for d in director_raw)
                else:
                    director_display = str(director_raw)
                
                # Calcular duração
                try:
                    start = datetime.strptime(r.get('start', '01/01/2025'), "%d/%m/%Y")
                    end = datetime.strptime(r.get('end', '10/01/2025'), "%d/%m/%Y")
                    duracao = f"{(end - start).days + 1} dias"
                except:
                    duracao = "Consultar"
                
                roteiro = {
                    'id': int(r.get('id', key)),
                    'title': r.get('title', f'Roteiro {key}'),
                    'img': r.get('img', 'placeholder.jpg'),
                    'start': r.get('start', '01/01/2025'),
                    'end': r.get('end', '10/01/2025'),
                    'duracao': duracao,
                    'preco': r.get('preco', 'Consultar'),
                    'director_display': director_display,
                    'incluso': r.get('incluso', []) if isinstance(r.get('incluso'), list) else [str(r.get('incluso', ''))],
                    'nao_incluso': r.get('nao_incluso', []) if isinstance(r.get('nao_incluso'), list) else [str(r.get('nao_incluso', ''))],
                    'itinerario': itinerario_lista
                }
                
                lista.append(roteiro)
                
            except Exception as e:
                print(f"   ⚠️  Erro ao processar {key}: {e}")
                continue
        
        print(f"📊 Total: {len(roteiros_dict)} | Filtrados: {filtrados} | Válidos: {len(lista)}")
        print("="*70)
        
        lista.sort(key=lambda x: x['id'])
        return lista
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return []

# CARREGAR ROTEIROS
ROTEIROS_DB = carregar_roteiros_direto()
ROTEIROS_BY_ID = {str(r['id']): r for r in ROTEIROS_DB}

print(f"🎯 RESULTADO: {len(ROTEIROS_DB)} roteiros carregados\n")

# Variáveis globais
CONTACT_INFO = {
    'phone': '(67) 99892-7001',
    'whatsapp': '5567998927001',
    'email': 'contato@peregrinecomacancaonova.com'
}

SITE_CONFIG = {
    'site_name': 'Peregrine com a Canção Nova',
    'site_description': 'Roteiros de peregrinação, fé e espiritualidade — conheça nossos destinos e programe sua próxima viagem de fé.',
    'operator_name': 'Peregrine - Operadora de Viagens'
}

GLOBAL_VARS = {**CONTACT_INFO, **SITE_CONFIG}

@app.context_processor
def inject_global_vars():
    return GLOBAL_VARS

# ============ ROTAS ============

@app.route('/')
def home():
    return render_template('home.html', roteiros=ROTEIROS_DB)

@app.route('/roteiro/<int:id>/')
def roteiro_detalhe(id):
    roteiro = ROTEIROS_BY_ID.get(str(id))
    if not roteiro:
        abort(404)
    return render_template('detalhe.html', roteiro=roteiro)

@app.route('/contato/')
def contato():
    return redirect(url_for('home') + '#rodape-contato')

@app.route('/sobre/')
def sobre():
    return render_template('sobre.html', roteiros=ROTEIROS_DB)

@app.route('/sitemap.xml')
def sitemap():
    base = app.config.get('FREEZER_BASE_URL', request.url_root).rstrip('/')
    pages = []
    
    pages.append({
        'loc': f"{base}/",
        'lastmod': datetime.utcnow().date().isoformat(),
        'priority': '1.0'
    })
    
    for r in ROTEIROS_DB:
        pages.append({
            'loc': f"{base}/roteiro/{r['id']}/",
            'lastmod': datetime.utcnow().date().isoformat(),
            'priority': '0.8'
        })
    
    pages.append({
        'loc': f"{base}/sobre/",
        'lastmod': datetime.utcnow().date().isoformat(),
        'priority': '0.6'
    })
    
    xml = render_template('sitemap.xml', pages=pages)
    return Response(xml, mimetype='application/xml')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
