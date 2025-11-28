# app.py
from flask import Flask, render_template, send_from_directory, abort
import json

app = Flask(__name__)

BASE_PATH = "/peregrinecomacancaonova"
app.config['FREEZER_BASE_URL'] = f"https://marcelofcn.github.io{BASE_PATH}"
app.config['FREEZER_DESTINATION'] = "docs"
app.jinja_env.globals['BASE_PATH'] = BASE_PATH

# Arquivos estáticos SEM BASE_PATH
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# Database
with open("roteiros.json", "r", encoding="utf-8") as f:
    ROTEIROS_DB = json.load(f)

# ROTAS
@app.route(f"{BASE_PATH}/")
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
    ]
