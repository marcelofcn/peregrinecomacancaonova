# main.py (Versão Corrigida/Refatorada)

from flask import Flask, render_template, abort
# Importa os dados do novo módulo
from data import ROTEIROS_DB, ROTEIROS_BY_ID # <--- 💡 MUDANÇA AQUI!
import os # Manter se necessário para outras coisas, mas não para o JSON

# ... Configuração principal do Flask (igual) ...

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
    # ... (Restante da rota igual) ...
