# app.py
from flask import Flask, render_template, send_from_directory, url_for, abort
import os, json

app = Flask(__name__)

# Caminho base usado no GitHub Pages
BASE_PATH = "/peregrinecomacancaonova"
app.config['FREEZER_BASE_URL'] = f"https://marcelofcn.github.io{BASE_PATH}"
app.jinja_env.globals['BASE_PATH'] = BASE_PATH
app.config['FREEZER_DESTINATION'] = 'docs'

# Corrige bug do Frozen-Flask + Flask 3.x
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

# Carregar base de dados
with open("roteiros.json", "r", encoding="utf-8") as f:
    ROTEIROS_DB = json.load(f)

# ==================== ROTAS ====================

@app.route(f"{BASE_PATH}/")
@app.route("/")
def home():
    hero_texts = [
        "P R O J E T O  E M  C O N S T R U C A O",
        "P O D E   C O N T E R   E R R O S",
        "F A V O R   E N T R A R   E M   C O N T A T O",
        "Roteiros de Espiritualidade",
        "Roteiros da Cancao Nova",
        "Experiencias que transformam"
    ]

    roteiros_espirituais = [
        {
            "id": r["id"],
            "img": r["img"],
            "title": r["title"],
            "date": f"{r['start']} a {r['end']}",
            "url": f"{BASE_PATH}/roteiro/{r['id']}/"
        }
        for r in ROTEIROS_DB.values()
        if r["categoria"] == "espiritualidade"
    ][:4]

    return render_template("home.html",
                           hero_texts=hero_texts,
                           roteiros_espirituais=roteiros_espirituais)


# LISTA DE ROTEIROS (MENU “Roteiros”)
@app.route(f"{BASE_PATH}/roteiros/")
def lista_roteiros():
    roteiros = list(ROTEIROS_DB.values())

    return render_template(
        "lista_roteiros.html",
        titulo="Roteiros",
        roteiros=roteiros
    )


# DETALHES DO ROTEIRO
@app.route(f"{BASE_PATH}/roteiro/<int:roteiro_id>/")
@app.route("/roteiro/<int:roteiro_id>/")
def roteiro_detalhe(roteiro_id):
    roteiro = ROTEIROS_DB.get(str(roteiro_id))
    if not roteiro:
        abort(404)
    return render_template("detalhe.html", roteiro=roteiro)


# ERRO 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# APP
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
