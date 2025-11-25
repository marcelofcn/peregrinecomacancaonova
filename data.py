# data.py (Revisado para o formato do seu JSON)

import json
import os
from datetime import datetime

# ... (código de carregamento carregar_roteiros igual) ...

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
    # ... (código de leitura do JSON) ...
    
    # Supondo que 'roteiros_lista' é o dicionário de dicionários lido do JSON
    roteiros_dict = json.load(f)
    
    roteiros_processados = []
    for key, roteiro in roteiros_dict.items():
        # Adiciona a duração calculada
        roteiro['duracao'] = calcular_duracao(roteiro.get('start', ''), roteiro.get('end', ''))
        # Adiciona o diretor em uma única string, se for um dicionário (como no Roteiro 16, etc.)
        if isinstance(roteiro.get('director'), dict):
             roteiro['director_display'] = ', '.join(roteiro['director'].values())
        elif isinstance(roteiro.get('director'), str):
             roteiro['director_display'] = roteiro['director']
        else:
             roteiro['director_display'] = "CN Tur"

        roteiros_processados.append(roteiro)

    return roteiros_processados # Retorna uma LISTA

# ... (o restante do data.py e ROTEIROS_BY_ID deve ser ajustado para usar a lista)
