from flask import Flask, render_template, send_from_directory, abort
import os, json
from datetime import datetime

app = Flask(__name__)

# Configurações para GitHub Pages
BASE_PATH = "/peregrinecomacancaonova"
app.config['FREEZER_BASE_URL'] = f"https://marcelofcn.github.io{BASE_PATH}"
app.config['FREEZER_DESTINATION'] = 'docs'
app.jinja_env.globals['BASE_PATH'] = BASE_PATH

# Corrige bug do Frozen-Flask + Flask 3.x
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

# Carregar roteiros
with open("roteiros.json", "r", encoding="utf-8") as f:
    ROTEIROS_DB = json.load(f)

# ==================== CONTEXT PROCESSOR ====================
# Injeta variáveis em TODOS os templates automaticamente

@app.context_processor
def inject_menu_data():
    """Disponibiliza meses_menu em todos os templates"""
    return {
        'meses_menu': get_meses_disponiveis()
    }

# ==================== FUNÇÕES AUXILIARES ====================

def parse_date(date_str):
    """Converte string DD/MM/YYYY para objeto datetime"""
    try:
        return datetime.strptime(date_str, "%d/%m/%Y")
    except:
        return datetime(2099, 12, 31)  # Data futura para erros

def get_proximos_roteiros(limit=3):
    """Retorna os próximos N roteiros ordenados por data"""
    hoje = datetime.now()
    roteiros_futuros = []
    
    for r in ROTEIROS_DB.values():
        data_inicio = parse_date(r["start"])
        if data_inicio >= hoje:
            roteiros_futuros.append({
                "id": r["id"],
                "img": r["img"],
                "title": r["title"],
                "start": r["start"],
                "end": r["end"],
                "director": r["director"],
                "data_obj": data_inicio
            })
    
    # Ordenar por data e retornar os primeiros N
    roteiros_futuros.sort(key=lambda x: x["data_obj"])
    return roteiros_futuros[:limit]

def get_roteiros_por_mes(ano, mes):
    """Retorna roteiros de um mês específico"""
    roteiros = []
    for r in ROTEIROS_DB.values():
        data_inicio = parse_date(r["start"])
        if data_inicio.year == ano and data_inicio.month == mes:
            roteiros.append(r)
    
    roteiros.sort(key=lambda x: parse_date(x["start"]))
    return roteiros

def get_meses_disponiveis():
    """Retorna lista de meses que têm roteiros disponíveis"""
    meses = set()
    hoje = datetime.now()
    
    for r in ROTEIROS_DB.values():
        data = parse_date(r["start"])
        if data >= hoje:
            meses.add((data.year, data.month))
    
    meses_lista = sorted(list(meses))
    
    # Converte para formato legível
    nomes_meses = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }
    
    return [
        {
            "ano": ano,
            "mes": mes,
            "nome": f"{nomes_meses[mes]}/{ano}",
            "url": f"{BASE_PATH}/roteiros/{ano}/{mes:02d}/"
        }
        for ano, mes in meses_lista
    ]

# ==================== ROTAS ====================

@app.route('/')
def home():
    proximos = get_proximos_roteiros(3)
    meses = get_meses_disponiveis()
    
    return render_template(
        "home.html",
        destaque=proximos,
        meses_menu=meses
    )

@app.route('/roteiros/')
def roteiros_todos():
    """Lista TODOS os roteiros disponíveis"""
    hoje = datetime.now()
    todos = []
    
    for r in ROTEIROS_DB.values():
        data_inicio = parse_date(r["start"])
        if data_inicio >= hoje:
            todos.append(r)
    
    todos.sort(key=lambda x: parse_date(x["start"]))
    
    return render_template(
        "lista_roteiros.html",
        titulo="Todos os Roteiros",
        roteiros=todos
    )

@app.route('/roteiros/<int:ano>/<int:mes>/')
def roteiros_por_mes(ano, mes):
    """Lista roteiros de um mês específico"""
    nomes_meses = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }
    
    roteiros = get_roteiros_por_mes(ano, mes)
    titulo = f"Roteiros de {nomes_meses.get(mes, 'Mês')} {ano}"
    
    return render_template(
        "lista_roteiros.html",
        titulo=titulo,
        roteiros=roteiros
    )

@app.route('/roteiro/<int:roteiro_id>/')
def roteiro_detalhe(roteiro_id):
    roteiro = ROTEIROS_DB.get(str(roteiro_id))
    if not roteiro:
        abort(404)
    return render_template("detalhe.html", roteiro=roteiro)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
