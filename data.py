# data.py - LÊ JSON COM DEBUG COMPLETO
import json
import os
import sys
from datetime import datetime
from copy import deepcopy

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROTEIROS_FILE = os.path.join(BASE_DIR, 'roteiros.json')

print("="*70)
print("🔍 DEBUG - CARREGAMENTO DE ROTEIROS")
print("="*70)
print(f"📂 Diretório base: {BASE_DIR}")
print(f"📄 Arquivo JSON: {ROTEIROS_FILE}")
print(f"✅ Arquivo existe? {os.path.exists(ROTEIROS_FILE)}")

if os.path.exists(ROTEIROS_FILE):
    file_size = os.path.getsize(ROTEIROS_FILE)
    print(f"📊 Tamanho do arquivo: {file_size} bytes")
else:
    print("❌ ARQUIVO NÃO ENCONTRADO!")
    print(f"📂 Arquivos na pasta:")
    for f in os.listdir(BASE_DIR):
        print(f"   - {f}")

# Palavras-chave para filtrar São José
_SAO_JOSE_KEYS = ['sao jose', 'são josé', 'sao-jose', 'loja são josé', 'loja sao jose']

def _eh_sao_jose(text):
    """Verifica se contém referência a São José"""
    if not text:
        return False
    t = str(text).lower()
    for key in _SAO_JOSE_KEYS:
        if key in t:
            print(f"   🚫 Filtrado por conter '{key}': {text[:50]}...")
            return True
    return False

def calcular_duracao(start_date_str, end_date_str):
    """Calcula duração entre datas"""
    try:
        start = datetime.strptime(start_date_str, "%d/%m/%Y")
        end = datetime.strptime(end_date_str, "%d/%m/%Y")
        dias = (end - start).days + 1
        return f"{dias} dias"
    except Exception as e:
        print(f"   ⚠️  Erro ao calcular duração: {e}")
        return "Consultar"

def carregar_roteiros():
    """Carrega roteiros do JSON com debug detalhado"""
    
    if not os.path.exists(ROTEIROS_FILE):
        print("❌ Arquivo roteiros.json NÃO ENCONTRADO!")
        return []
    
    # Ler JSON
    try:
        with open(ROTEIROS_FILE, 'r', encoding='utf-8') as f:
            roteiros_dict = json.load(f)
        print(f"✅ JSON carregado com sucesso!")
        print(f"📊 Total de entradas no JSON: {len(roteiros_dict)}")
    except json.JSONDecodeError as e:
        print(f"❌ ERRO ao decodificar JSON:")
        print(f"   Linha {e.lineno}, Coluna {e.colno}")
        print(f"   Mensagem: {e.msg}")
        return []
    except Exception as e:
        print(f"❌ ERRO ao ler arquivo: {e}")
        return []
    
    # Processar roteiros
    lista = []
    estatisticas = {
        'total': len(roteiros_dict),
        'filtrados_sao_jose': 0,
        'erro_processamento': 0,
        'sucesso': 0
    }
    
    print("\n🔄 Processando roteiros:")
    print("-"*70)
    
    for key, roteiro in roteiros_dict.items():
        try:
            # Verificar filtro São José
            director = roteiro.get('director', '')
            empresa = roteiro.get('empresa', '')
            
            print(f"\n📋 Roteiro {key}:")
            print(f"   Título: {roteiro.get('title', 'SEM TÍTULO')}")
            print(f"   Diretor: {director}")
            print(f"   Empresa: {empresa}")
            
            if _eh_sao_jose(director) or _eh_sao_jose(empresa):
                estatisticas['filtrados_sao_jose'] += 1
                continue
            
            r = deepcopy(roteiro)
            
            # ID
            try:
                r['id'] = int(r.get('id', key))
            except:
                r['id'] = key
            
            # Itinerário
            itinerario = r.get('itinerario', [])
            if isinstance(itinerario, dict):
                r['itinerario'] = [f"{k} – {v}" for k, v in sorted(itinerario.items())]
            elif isinstance(itinerario, list):
                r['itinerario'] = itinerario
            else:
                r['itinerario'] = [str(itinerario)] if itinerario else []
            
            # Inclusos
            if not isinstance(r.get('incluso', []), list):
                r['incluso'] = [r.get('incluso', '')] if r.get('incluso') else []
            
            if not isinstance(r.get('nao_incluso', []), list):
                r['nao_incluso'] = [r.get('nao_incluso', '')] if r.get('nao_incluso') else []
            
            # Preço
            r['preco'] = r.get('preco', 'Consultar')
            
            # Diretor display
            if isinstance(director, list):
                r['director_display'] = ', '.join(str(d) for d in director)
            else:
                r['director_display'] = str(director) if director else "Equipe Canção Nova"
            
            # Duração
            r['duracao'] = calcular_duracao(
                r.get('start', '01/01/2025'),
                r.get('end', '02/01/2025')
            )
            
            # Imagem
            if not r.get('img'):
                r['img'] = 'placeholder.jpg'
            
            # Título
            if not r.get('title'):
                r['title'] = f"Roteiro {r['id']}"
            
            lista.append(r)
            estatisticas['sucesso'] += 1
            print(f"   ✅ ADICIONADO à lista final")
            
        except Exception as e:
            estatisticas['erro_processamento'] += 1
            print(f"   ❌ ERRO ao processar: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    # Relatório final
    print("\n" + "="*70)
    print("📊 RELATÓRIO FINAL:")
    print("="*70)
    print(f"   Total no JSON: {estatisticas['total']}")
    print(f"   Filtrados (São José): {estatisticas['filtrados_sao_jose']}")
    print(f"   Erros de processamento: {estatisticas['erro_processamento']}")
    print(f"   ✅ ROTEIROS VÁLIDOS: {estatisticas['sucesso']}")
    print("="*70)
    
    if estatisticas['sucesso'] == 0:
        print("\n❌ NENHUM roteiro foi carregado!")
        print("🔍 Possíveis causas:")
        print("   1. Todos foram filtrados por 'São José'")
        print("   2. Todos tiveram erro no processamento")
        print("   3. JSON está vazio")
    
    # Ordenar
    if lista:
        lista.sort(key=lambda x: int(x['id']) if str(x['id']).isdigit() else 999)
    
    return lista

# EXECUTAR CARREGAMENTO
ROTEIROS_DB = carregar_roteiros()
ROTEIROS_BY_ID = {str(r['id']): r for r in ROTEIROS_DB}

print(f"\n🎯 RESULTADO: {len(ROTEIROS_DB)} roteiros disponíveis para o site")
print("="*70 + "\n")

# Configurações do site
SITE_CONFIG = {
    'site_name': 'Peregrine com a Canção Nova',
    'site_description': 'Roteiros de peregrinação, fé e espiritualidade — conheça nossos destinos e programe sua próxima viagem de fé.',
    'operator_name': 'Peregrine - Operadora de Viagens'
}
