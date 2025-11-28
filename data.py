# data.py - VERSÃO ULTRA SIMPLES (CARREGA TODOS OS ROTEIROS)
import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROTEIROS_FILE = os.path.join(BASE_DIR, 'roteiros.json')

print("="*70)
print("🔍 CARREGANDO ROTEIROS")
print(f"📄 Arquivo: {ROTEIROS_FILE}")
print(f"✅ Existe? {os.path.exists(ROTEIROS_FILE)}")

def carregar_roteiros():
    if not os.path.exists(ROTEIROS_FILE):
        print("❌ JSON não encontrado!")
        return []
    
    try:
        with open(ROTEIROS_FILE, 'r', encoding='utf-8') as f:
            roteiros_dict = json.load(f)
        
        print(f"✅ JSON válido: {len(roteiros_dict)} roteiros")
        
        lista = []
        
        for key, r in roteiros_dict.items():
            try:
                # Processar itinerário
                itinerario = r.get('itinerario', {})
                if isinstance(itinerario, dict):
                    itinerario_lista = [f"{k} – {v}" for k, v in sorted(itinerario.items())]
                else:
                    itinerario_lista = itinerario if isinstance(itinerario, list) else []
                
                # Diretor
                director = r.get('director', 'Equipe Canção Nova')
                if isinstance(director, list):
                    director_display = ', '.join(str(d) for d in director)
                else:
                    director_display = str(director)
                
                # Duração
                try:
                    start = datetime.strptime(r.get('start', '01/01/2025'), "%d/%m/%Y")
                    end = datetime.strptime(r.get('end', '10/01/2025'), "%d/%m/%Y")
                    duracao = f"{(end - start).days + 1} dias"
                except:
                    duracao = "Consultar"
                
                roteiro = {
                    'id': int(r.get('id', key)),
                    'title': r.get('title', 'Sem título'),
                    'img': r.get('img', 'placeholder.jpg'),
                    'start': r.get('start', '01/01/2025'),
                    'end': r.get('end', '10/01/2025'),
                    'duracao': duracao,
                    'preco': r.get('preco', 'Consultar'),
                    'director_display': director_display,
                    'director': director,
                    'empresa': r.get('empresa', ''),
                    'incluso': r.get('incluso', []) if isinstance(r.get('incluso'), list) else [str(r.get('incluso', ''))],
                    'nao_incluso': r.get('nao_incluso', []) if isinstance(r.get('nao_incluso'), list) else [str(r.get('nao_incluso', ''))],
                    'itinerario': itinerario_lista
                }
                
                lista.append(roteiro)
                print(f"   ✅ {roteiro['id']}: {roteiro['title']}")
                
            except Exception as e:
                print(f"   ❌ Erro em {key}: {e}")
        
        print(f"\n📊 TOTAL: {len(lista)} roteiros carregados")
        print("="*70)
        
        lista.sort(key=lambda x: x['id'])
        return lista
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return []

ROTEIROS_DB = carregar_roteiros()
ROTEIROS_BY_ID = {str(r['id']): r for r in ROTEIROS_DB}

SITE_CONFIG = {
    'site_name': 'Peregrine com a Canção Nova',
    'site_description': 'Roteiros de peregrinação, fé e espiritualidade — conheça nossos destinos e programe sua próxima viagem de fé.',
    'operator_name': 'Peregrine - Operadora de Viagens'
}

print(f"🎯 Exportado: {len(ROTEIROS_DB)} roteiros\n")
