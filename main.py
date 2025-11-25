from flask import Flask, render_template, abort
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

def carregar_roteiros():
    """Carrega os roteiros do arquivo JSON"""
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            roteiros_lista = json.load(f)
        return roteiros_lista
    except FileNotFoundError:
        print(f"ERRO: Arquivo {JSON_PATH} não encontrado!")
        return []
    except json.JSONDecodeError as e:
        print(f"ERRO ao ler JSON: {e}")
        return []

ROTEIROS_DB = carregar_roteiros()
ROTEIROS_BY_ID = {str(r["id"]): r for r in ROTEIROS_DB}

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
    if not roteiro:
        abort(404)
    return render_template("detalhe.html", roteiro=roteiro)

@app.route("/sobre/")
def sobre():
    """Página sobre a Canção Nova"""
    return render_template("sobre.html")

@app.route("/contato/")
def contato():
    """Página de contato"""
    return render_template("contato.html")

@app.errorhandler(404)
def erro_404(e):
    """Tratamento de erro 404"""
    return render_template("404.html"), 404

# ---------------------------------------
# Context Processor (variáveis globais para templates)
# ---------------------------------------
@app.context_processor
def inject_globals():
    """Injeta variáveis globais em todos os templates"""
    return {
        'site_name': 'Peregrine com a Canção Nova',
        'site_description': 'Experiências que transformam vidas através do turismo religioso',
        'operator_name': 'São José Turismo Religioso',
        'phone': '(12) 3144-7777',
        'email': 'contato@saojoseturismo.com.br'
    }

if __name__ == "__main__":
    print(f"📍 Roteiros carregados: {len(ROTEIROS_DB)}")
    app.run(debug=True, host='0.0.0.0', port=5000)
