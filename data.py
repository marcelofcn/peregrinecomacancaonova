# data.py - VERSÃO COM DEBUG E CORREÇÕES
import json
import os
from datetime import datetime
from copy import deepcopy

# Caminho absoluto para garantir que sempre encontra o arquivo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROTEIROS_FILE = os.path.join(BASE_DIR, 'roteiros.json')

print(f"🔍 DEBUG: Procurando arquivo em: {ROTEIROS_FILE}")
print(f"🔍 DEBUG: Arquivo existe? {os.path.exists(ROTEIROS_FILE)}")

# Palavras-chave para filtrar
_SAO_JOSE_KEYS = ['sao jose', 'são josé', 'sao-jose', 'loja são josé', 'loja sao jose']

def _eh_sao_jose(text):
    """Verifica se o texto contém referências a São José"""
    if not text:
        return False
    t = str(text).lower()
    return any(k in t for k in _SAO_JOSE_KEYS)

def calcular_duracao(start_date_str, end_date_str):
    """Calcula duração entre duas datas"""
    try:
        start = datetime.strptime(start_date_str, "%d/%m/%Y")
        end = datetime.strptime(end_date_str, "%d/%m/%Y")
        dias = (end - start).days + 1
        return f"{dias} dias"
    except Exception as e:
        print(f"⚠️  Erro ao calcular duração: {e}")
        return "Consultar"

def carregar_roteiros():
    """Carrega e processa os roteiros do JSON"""
    
    # Verificar se arquivo existe
    if not os.path.exists(ROTEIROS_FILE):
        print(f"❌ ERRO: Arquivo {ROTEIROS_FILE} NÃO ENCONTRADO!")
        print(f"📂 Arquivos na pasta atual:")
        for f in os.listdir(BASE_DIR):
            print(f"   - {f}")
        return []
    
    # Ler arquivo JSON
    try:
        with open(ROTEIROS_FILE, 'r', encoding='utf-8') as f:
            roteiros_dict = json.load(f)
        print(f"✅ JSON carregado: {len(roteiros_dict)} roteiros encontrados")
    except json.JSONDecodeError as e:
        print(f"❌ ERRO ao decodificar JSON: {e}")
        return []
    except Exception as e:
        print(f"❌ ERRO ao ler arquivo: {e}")
        return []
    
    lista = []
    roteiros_filtrados = 0
    
    for key, roteiro in roteiros_dict.items():
        # Filtrar São José
        director = roteiro.get('director') or ''
        empresa = roteiro.get('empresa') or ''
        
        if _eh_sao_jose(director) or _eh_sao_jose(empresa):
            roteiros_filtrados += 1
            continue
        
        r = deepcopy(roteiro)
        
        # Garantir ID como inteiro
        try:
            r['id'] = int(r.get('id', key))
        except:
            try:
                r['id'] = int(key)
            except:
                print(f"⚠️  Aviso: ID inválido para roteiro {key}, usando chave como string")
                r['id'] = key
        
        # Normalizar itinerário
        itinerario = r.get('itinerario', [])
        if isinstance(itinerario, dict):
            items = [f"{k} – {v}" for k, v in sorted(itinerario.items())]
            r['itinerario'] = items
        elif isinstance(itinerario, list):
            r['itinerario'] = itinerario
        else:
            r['itinerario'] = [str(itinerario)] if itinerario else []
        
        # Normalizar inclusos
        if not isinstance(r.get('incluso', []), list):
            r['incluso'] = [r.get('incluso', '')] if r.get('incluso') else []
        
        if not isinstance(r.get('nao_incluso', []), list):
            r['nao_incluso'] = [r.get('nao_incluso', '')] if r.get('nao_incluso') else []
        
        # Preço
        r['preco'] = r.get('preco', 'Consultar')
        
        # Diretor display
        director_data = r.get('director')
        if isinstance(director_data, list):
            r['director_display'] = ', '.join(director_data)
        else:
            r['director_display'] = str(director_data) if director_data else "Equipe Canção Nova"
        
        # Duração
        r['duracao'] = calcular_duracao(r.get('start', '01/01/2025'), r.get('end', '02/01/2025'))
        
        # Garantir que tenha imagem
        if not r.get('img'):
            r['img'] = 'default.jpg'
        
        lista.append(r)
        print(f"   ✅ Roteiro {r['id']}: {r.get('title', 'Sem título')}")
    
    print(f"\n📊 Resumo:")
    print(f"   Total no JSON: {len(roteiros_dict)}")
    print(f"   Filtrados (São José): {roteiros_filtrados}")
    print(f"   Roteiros finais: {len(lista)}")
    
    # Ordenar por ID
    lista.sort(key=lambda x: int(x['id']) if isinstance(x['id'], (int, str)) and str(x['id']).isdigit() else 999)
    
    return lista

# Carregar dados
print("\n" + "="*60)
print("🚀 INICIANDO CARREGAMENTO DE ROTEIROS")
print("="*60)

ROTEIROS_DB = carregar_roteiros()
ROTEIROS_BY_ID = {str(r['id']): r for r in ROTEIROS_DB}

print(f"\n✅ {len(ROTEIROS_DB)} roteiros disponíveis")
print("="*60 + "\n")

# Configurações do site
SITE_CONFIG = {
    'site_name': 'Peregrine com a Canção Nova',
    'site_description': 'Roteiros de peregrinação, fé e espiritualidade — conheça nossos destinos e programe sua próxima viagem de fé.',
    'operator_name': 'Peregrine - Operadora de Viagens'
}

# Se não houver roteiros, criar um de exemplo para debug
if len(ROTEIROS_DB) == 0:
    print("⚠️  AVISO: Nenhum roteiro carregado! Criando roteiro de exemplo...")
    ROTEIRO_EXEMPLO = {
        'id': 999,
        'title': 'Roteiro de Teste',
        'img': 'default.jpg',
        'start': '01/01/2025',
        'end': '10/01/2025',
        'duracao': '10 dias',
        'preco': 'R$ 5.000,00',
        'director_display': 'Equipe Teste',
        'incluso': ['Teste 1', 'Teste 2'],
        'nao_incluso': ['Teste 3'],
        'itinerario': ['Dia 1 – Teste']
    }
    ROTEIROS_DB = [ROTEIRO_EXEMPLO]
    ROTEIROS_BY_ID = {'999': ROTEIRO_EXEMPLO}
