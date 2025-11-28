# app.py
from flask import Flask, render_template, send_from_directory, url_for, abort
import os, json, datetime

app = Flask(__name__)

# BASE_PATH único e correto (sem barra final)
BASE_PATH = "/peregrinecomacancaonova"
app.config['FREEZER_BASE_URL'] = f"https://marcelofcn.github.io{BASE_PATH}"
app.jinja_env.globals['BASE_PATH'] = BASE_PATH
app.config['FREEZER_DESTINATION'] = 'docs'

# Corrige bug do Frozen-Flask + Flask 3.x (serve arquivos estáticos localmente)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

# Carregar base de dados (roteiros.json deve estar no mesmo diretório)
with open("roteiros.json", "r", encoding="utf-8") as f:
    ROTEIROS_DB = json.load(f)

# ----------------- helpers -----------------
MESES = {
    1: ("janeiro", "Janeiro"),
    2: ("fevereiro", "Fevereiro"),
    3: ("marco", "Março"),
    4: ("abril", "Abril"),
    5: ("maio", "Maio"),
    6: ("junho", "Junho"),
    7: ("julho", "Julho"),
    8: ("agosto", "Agosto"),
    9: ("setembro", "Setembro"),
    10: ("outubro", "Outubro"),
    11: ("novembro", "Novembro"),
    12: ("dezembro", "Dezembro"),
}

def extrair_mes_do_start(start_str):
    """
    Espera datas no formato 'dd/mm/aaaa' ou 'dd/mm/aa'.
    Retorna o slug do mês sem acento ('janeiro', 'fevereiro', 'marco', ...)
    """
    try:
        partes = start_str.split('/')
        if len(partes) >= 2:
            mes = int(partes[1])
            return MESES.get(mes, (None, None))[0]
    except Exception:
        pass
    return None

# ----------------- ROTAS -----------------
@app.route(f"{BASE_PATH}/")
@app.route('/')  # manter para dev local
def home():
    hero_texts = [
        "P R O J E T O  E M  C O N S T R U Ç Ã O",
        "P O D E    C O N T E R   E R R O S",
        "F A V O R  E N T R A R  E M  C O N T A T O",
        "Roteiros de Espiritualidade", "Experiências que transformam"
    ]

    # Mostrar até 4 roteiros (filtrado como espiritualidade se desejar)
    roteiros_espirituais = [
        {
            "id": r["id"],
            "img": r["img"],
            "title": r["title"],
            "date": f"{r.get('start','')} a {r.get('end','')}",
            "url": f"{BASE_PATH}/roteiro/{r['id']}/"
        }
        for r in ROTEIROS_DB.values()
    ][:4]

    return render_template("home.html",
                           hero_texts=hero_texts,
                           roteiros_espirituais=roteiros_espirituais)

@app.route(f"{BASE_PATH}/roteiros/")
@app.route('/roteiros/')  # dev local
def todos_roteiros():
    roteiros = list(ROTEIROS_DB.values())
    return render_template("lista_roteiros.html",
                           titulo="Todos os Roteiros",
                           roteiros=roteiros)

@app.route(f"{BASE_PATH}/roteiros/mes/<mes>/")
@app.route('/roteiros/mes/<mes>/')  # dev local
def roteiros_por_mes(mes):
    mes = mes.lower()
    roteiros = []
    for r in ROTEIROS_DB.values():
        start = r.get("start", "")
        mes_do_roteiro = extrair_mes_do_start(start)
        if mes_do_roteiro == mes:
            roteiros.append(r)

    titulo = f"Roteiros — {MESES.get(list(MESES.keys())[list(MESES.values()).index(next(filter(lambda x: x[0]==mes, MESES.values())))][0] if any(v[0]==mes for v in MESES.values()) else mes.capitalize()}" \
             if False else f"Roteiros — {mes.capitalize()}"
    # Simples: usar mes capitalizado
    return render_template("lista_roteiros.html",
                           titulo=f"Roteiros — {mes.capitalize()}",
                           roteiros=roteiros)

@app.route(f"{BASE_PATH}/roteiro/<int:roteiro_id>/")
@app.route('/roteiro/<int:roteiro_id>/')  # dev local
def roteiro_detalhe(roteiro_id):
    roteiro = ROTEIROS_DB.get(str(roteiro_id))
    if not roteiro:
        abort(404)
    return render_template("detalhe.html", roteiro=roteiro)

# 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Executa em dev local
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
