from flask import Flask, render_template, abort, url_for
import json
import os

# ---------------------------------------
# Configuração principal do Flask
# ---------------------------------------
app = Flask(__name__, static_folder="static", template_folder="templates")

# ---------------------------------------
# Configurações do Frozen-Flask
# ---------------------------------------
app.config["FREEZER_DESTINATION"] = "docs"
app.config["FREEZER_RELATIVE_URLS"] = True
app.config["FREEZER_REMOVE_EXTRA_FILES"] = False

# ---------------------------------------
# Carregar dados de roteiros
# ---------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "roteiros.json")

with open(JSON_PATH, "r", encoding="utf-8") as f:
    ROTEIROS_DB = json.load(f)

# ---------------------------------------
# Rotas
# ---------------------------------------

@app.route("/")
def home():
    roteiros = [
        r for r in ROTEIROS_DB.values()
        if r.get("empresa") == "cancaonova"
    ]
    return render_template("home.html", roteiros=roteiros)


@app.route("/roteiros/")
def lista_roteiros():
    roteiros = [
        r for r in ROTEIROS_DB.values()
        if r.get("empresa") == "cancaonova"
    ]
    return render_template("lista.html", roteiros=roteiros)


@app.route("/roteiro/<int:roteiro_id>/")
def roteiro_detalhe(roteiro_id):
    roteiro = ROTEIROS_DB.get(str(roteiro_id))
    if not roteiro:
        abort(404)
    return render_template("detalhe.html", roteiro=roteiro)


@app.errorhandler(404)
def erro_404(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
