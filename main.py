from flask import Flask, render_template, abort
import json
import os

app = Flask(__name__)

# ----------------------------
# Carregar dados
# ----------------------------
with open("roteiros.json", "r", encoding="utf-8") as f:
    ROTEIROS_DB = json.load(f)

# Config Frozen
app.config["FREEZER_RELATIVE_URLS"] = True

# ----------------------------
# Rotas
# ----------------------------

@app.route("/")
def home():
    # SOMENTE roteiros Canção Nova
    roteiros = [
        r for r in ROTEIROS_DB.values()
        if r["empresa"] == "cancaonova"
    ]

    return render_template("home.html", roteiros=roteiros)


@app.route("/roteiros/")
def lista_roteiros():
    roteiros = [
        r for r in ROTEIROS_DB.values()
        if r["empresa"] == "cancaonova"
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
