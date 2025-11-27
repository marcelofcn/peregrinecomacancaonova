import json
import os
from datetime import datetime
from copy import deepcopy

ROTEIROS_FILE = os.path.join(os.path.dirname(__file__), 'roteiros.json')

# Palavras-chave para identificar e excluir roteiros "São José"
_SAO_JOSE_KEYS = ['sao jose', 'são josé', 'sao-jose', 'loja são josé', 'loja sao jose']

def _eh_sao_jose(text):
    if not text:
        return False
    t = str(text).lower()
    for k in _SAO_JOSE_KEYS:
        if k in t:
            return True
    return False

def calcular_duracao(start_date_str, end_date_str):
    try:
        # aceita formatos dd/mm/yyyy e d/m/yyyy
        start = datetime.strptime(start_date_str, "%d/%m/%Y")
        end = datetime.strptime(end_date_str, "%d/%m/%Y")
        return f"{(end - start).days + 1} dias"
    except Exception:
        return "Duração não informada"

def carregar_roteiros():
    if not os.path.exists(ROTEIROS_FILE):
        print(f"Arquivo {ROTEIROS_FILE} não encontrado.")
        return []

    try:
        with open(ROTEIROS_FILE, 'r', encoding='utf-8') as f:
            roteiros_dict = json.load(f)
    except Exception as e:
        print("Erro ao ler JSON:", e)
        return []

    lista = []
    for key, roteiro in roteiros_dict.items():
        # Filtra roteiros relacionados a São José (solicitado)
        director = roteiro.get('director') or ''
        empresa = roteiro.get('empresa') or ''
        if _eh_sao_jose(director) or _eh_sao_jose(empresa):
            # desconsiderar este roteiro
            continue

        r = deepcopy(roteiro)

        # Garantir id como int
        try:
            r['id'] = int(r.get('id', key))
        except Exception:
            try:
                r['id'] = int(key)
            except:
                r['id'] = key

        # Normalizar itinerario: transformar dict -> list de strings "Dia X – texto"
        itinerario = r.get('itinerario', [])
        if isinstance(itinerario, dict):
            # manter ordem por chave se possível
            items = []
            for k, v in sorted(itinerario.items(), key=lambda x: x[0]):
                items.append(f"{k} – {v}")
            r['itinerario'] = items
        elif isinstance(itinerario, list):
            r['itinerario'] = itinerario
        else:
            # string -> colocar como único item
            r['itinerario'] = [str(itinerario)]

        # Inclusos / nao_incluso como listas
        if not isinstance(r.get('incluso', []), list):
            r['incluso'] = [r.get('incluso', '')] if r.get('incluso') else []
        if not isinstance(r.get('nao_incluso', []), list):
            r['nao_incluso'] = [r.get('nao_incluso', '')] if r.get('nao_incluso') else []

        # Preco — manter string (pode ser formatado no template)
        r['preco'] = r.get('preco', 'Consultar')

        # diretor_display (string amigável)
        director_data = r.get('director')
        if isinstance(director_data, list):
            r['director_display'] = ', '.join(director_data)
        else:
            r['director_display'] = str(director_data) if director_data else "Equipe"

        # duração calculada
        r['duracao'] = calcular_duracao(r.get('start', ''), r.get('end', ''))

        lista.append(r)

    # Ordena por id para previsibilidade
    
    return lista

# Exportados
ROTEIROS_DB = carregar_roteiros()
ROTEIROS_BY_ID = { str(r['id']): r for r in ROTEIROS_DB }

SITE_CONFIG = {
    'site_name': 'Peregrine com a Canção Nova',
    'site_description': 'Roteiros de peregrinação, fé e espiritualidade — conheça nossos destinos e programe sua próxima viagem de fé.',
    'operator_name': 'Peregrine - Operadora de Viagens'
}
