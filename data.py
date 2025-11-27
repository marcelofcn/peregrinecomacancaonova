# data.py - VERSÃO QUE TOLERA ERROS NO JSON
import json
import os
from datetime import datetime
from copy import deepcopy
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROTEIROS_FILE = os.path.join(BASE_DIR, 'roteiros.json')

print(f"🔍 DEBUG: Procurando arquivo em: {ROTEIROS_FILE}")
print(f"🔍 DEBUG: Arquivo existe? {os.path.exists(ROTEIROS_FILE)}")

_SAO_JOSE_KEYS = ['sao jose', 'são josé', 'sao-jose', 'loja são josé', 'loja sao jose']

def _eh_sao_jose(text):
    if not text:
        return False
    t = str(text).lower()
    return any(k in t for k in _SAO_JOSE_KEYS)

def limpar_json(texto):
    """Remove vírgulas extras que causam erro no JSON"""
    # Remove vírgulas antes de } ou ]
    texto = re.sub(r',(\s*[}\]])', r'\1', texto)
    return texto

def calcular_duracao(start_date_str, end_date_str):
    try:
        start = datetime.strptime(start_date_str, "%d/%m/%Y")
        end = datetime.strptime(end_date_str, "%d/%m/%Y")
        dias = (end - start).days + 1
        return f"{dias} dias"
    except:
        return "Consultar"

def carregar_roteiros():
    if not os.path.exists(ROTEIROS_FILE):
        print(f"❌ ERRO: Arquivo {ROTEIROS_FILE} NÃO ENCONTRADO!")
        return []
    
    # Ler e tentar corrigir JSON
    try:
        with open(ROTEIROS_FILE, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # Tentar limpar JSON
        conteudo_limpo = limpar_json(conteudo)
        
        try:
            roteiros_dict = json.loads(conteudo_limpo)
        except json.JSONDecodeError as e:
            print(f"❌ ERRO no JSON (linha {e.lineno}, coluna {e.colno}): {e.msg}")
            print(f"📍 Contexto: ...{e.doc[max(0, e.pos-50):e.pos+50]}...")
            print("\n⚠️  DICA: Verifique se há:")
            print("   - Vírgulas extras antes de } ou ]")
            print("   - Aspas faltando em chaves ou valores")
            print("   - Comentários (não permitidos em JSON)")
            return []
            
    except Exception as e:
        print(f"❌ ERRO ao ler arquivo: {e}")
        return []
    
    print(f"✅ JSON carregado: {len(roteiros_dict)} roteiros encontrados")
    
    lista = []
    roteiros_com_erro = 0
    roteiros_filtrados = 0
    
    for key, roteiro in roteiros_dict.items():
        try:
            # Filtrar São José
            director = roteiro.get('director', '')
            empresa = roteiro.get('empresa', '')
            
            if _eh_sao_jose(director) or _eh_sao_jose(empresa):
                roteiros_filtrados += 1
                continue
            
            r = deepcopy(roteiro)
            
            # ID
            try:
                r['id'] = int(r.get('id', key))
            except:
                r['id'] = len(lista) + 1
            
            # Itinerário
            itinerario = r.get('itinerario', [])
            if isinstance(itinerario, dict):
                r['itinerario'] = [f"{k} – {v}" for k, v in sorted(itinerario.items())]
            elif isinstance(itinerario, list):
                r['itinerario'] = itinerario
            else:
                r['itinerario'] = [str(itinerario)] if itinerario else ["Consultar programação"]
            
            # Inclusos
            r['incluso'] = r.get('incluso', []) if isinstance(r.get('incluso'), list) else [r.get('incluso', 'Consultar')]
            r['nao_incluso'] = r.get('nao_incluso', []) if isinstance(r.get('nao_incluso'), list) else [r.get('nao_incluso', 'Consultar')]
            
            # Preço
            r['preco'] = r.get('preco', 'Consultar')
            
            # Diretor
            director_data = r.get('director')
            if isinstance(director_data, list):
                r['director_display'] = ', '.join(str(d) for d in director_data)
            else:
                r['director_display'] = str(director_data) if director_data else "Equipe Canção Nova"
            
            # Duração
            r['duracao'] = calcular_duracao(
                r.get('start', '01/01/2025'), 
                r.get('end', '02/01/2025')
            )
            
            # Imagem - IMPORTANTE: não usar default.jpg se não existir
            if not r.get('img'):
                r['img'] = 'placeholder.jpg'  # Será tratado no template
            
            # Título obrigatório
            if not r.get('title'):
                r['title'] = f"Roteiro {r['id']}"
            
            lista.append(r)
            print(f"   ✅ Roteiro {r['id']}: {r['title']}")
            
        except Exception as e:
            roteiros_com_erro += 1
            print(f"   ⚠️  Erro ao processar roteiro {key}: {e}")
            continue
    
    print(f"\n📊 Resumo:")
    print(f"   Total no JSON: {len(roteiros_dict)}")
    print(f"   Filtrados (São José): {roteiros_filtrados}")
    print(f"   Com erro: {roteiros_com_erro}")
    print(f"   Roteiros válidos: {len(lista)}")
    
    if len(lista) == 0:
        print("\n❌ NENHUM roteiro válido! Verifique o JSON.")
        return []
    
    # Ordenar
    lista.sort(key=lambda x: int(x['id']) if str(x['id']).isdigit() else 999)
    
    return lista

# Carregar
print("\n" + "="*60)
print("🚀 INICIANDO CARREGAMENTO DE ROTEIROS")
print("="*60)

ROTEIROS_DB = carregar_roteiros()
ROTEIROS_BY_ID = {str(r['id']): r for r in ROTEIROS_DB}

print(f"\n✅ {len(ROTEIROS_DB)} roteiros carregados")
print("="*60 + "\n")

SITE_CONFIG = {
    'site_name': 'Peregrine com a Canção Nova',
    'site_description': 'Roteiros de peregrinação, fé e espiritualidade — conheça nossos destinos e programe sua próxima viagem de fé.',
    'operator_name': 'Peregrine - Operadora de Viagens'
}
