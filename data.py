# data.py

import json
import os

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
