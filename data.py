# data.py (Revisado para o formato do seu JSON)

import json
import os
from datetime import datetime

# Define a localização do arquivo JSON
ROTEIROS_FILE = os.path.join(os.path.dirname(__file__), 'roteiros.json')

# --- Funções de Processamento ---

def calcular_duracao(start_date_str, end_date_str):
    """Calcula a duração em dias."""
    try:
        # Padrão DD/MM/YYYY
        start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
        end_date = datetime.strptime(end_date_str, "%d/%m/%Y")
        duration = (end_date - start_date).days + 1 # +1 para incluir o dia de partida/chegada
        return f"{duration} dias"
    except:
        return "Duração não informada"

def carregar_roteiros():
    """Carrega os roteiros do arquivo JSON e os formata em uma lista."""
    roteiros_processados = []
    
    if not os.path.exists(ROTEIROS_FILE):
        print(f"Erro: Arquivo não encontrado em {ROTEIROS_FILE}")
        return []

    try:
        with open(ROTEIROS_FILE, 'r', encoding='utf-8') as f:
            roteiros_dict = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        return []

    for key, roteiro in roteiros_dict.items():
        # O ID deve ser uma string se você usa no ROTEIROS_BY_ID.get(str(id))
        roteiro['id'] = key 
        
        # Adiciona a duração calculada
        roteiro['duracao'] = calcular_duracao(roteiro.get('start', ''), roteiro.get('end', ''))
        
        # Adiciona o diretor em uma única string
        director_data = roteiro.get('director')
        if isinstance(director_data, dict):
            roteiro['director_display'] = ', '.join(director_data.values())
        elif isinstance(director_data, str):
            roteiro['director_display'] = director_data
        else:
            roteiro['director_display'] = "CN Tur"

        roteiros_processados.append(roteiro)

    return roteiros_processados 

# --- VARIÁVEIS EXPORTADAS (Correção Principal) ---

# 1. Lista principal para exibição (Home, Freezer)
ROTEIROS_DB = carregar_roteiros()

# 2. Dicionário de busca rápida (main.py)
# Usa o campo 'id' que foi adicionado na função carregar_roteiros
ROTEIROS_BY_ID = {
    roteiro['id']: roteiro for roteiro in ROTEIROS_DB
}

# 3. Configurações globais (Seu main.py importa isso agora)
SITE_CONFIG = {
    'site_name': 'Canção Nova Viagens',
    'operator_name': 'CN Tur'
}
