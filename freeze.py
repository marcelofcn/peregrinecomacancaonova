#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, glob
from flask_frozen import Freezer
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app

app_instance = app.app
ROTEIROS_DB = app.ROTEIROS_DB

app_instance.config['FREEZER_DESTINATION'] = 'docs'
app_instance.config['FREEZER_RELATIVE_URLS'] = False
app_instance.config['FREEZER_BASE_URL'] = "https://marcelofcn.github.io/peregrinecomacancaonova"

freezer = Freezer(app_instance)
os.makedirs('docs', exist_ok=True)

# ==================== GERADORES ====================

@freezer.register_generator
def roteiro_detalhe():
    """Gera páginas de detalhes de cada roteiro"""
    for id in ROTEIROS_DB.keys():
        yield {'roteiro_id': int(id)}

@freezer.register_generator
def roteiros_por_mes():
    """Gera páginas de roteiros por mês"""
    meses_gerados = set()
    hoje = datetime.now()
    
    for r in ROTEIROS_DB.values():
        try:
            data = datetime.strptime(r["start"], "%d/%m/%Y")
            if data >= hoje:
                mes_ano = (data.year, data.month)
                if mes_ano not in meses_gerados:
                    meses_gerados.add(mes_ano)
                    yield {'ano': data.year, 'mes': data.month}
        except:
            continue

@freezer.register_generator
def static():
    """Gera arquivos estáticos"""
    for path in glob.glob('static/**/*.*', recursive=True):
        filename = path.replace("static/", "").replace("\\", "/")
        yield {'filename': filename}

# ==================== EXECUTAR ====================

if __name__ == '__main__':
    print("🔥 Iniciando geração do site estático...")
    freezer.freeze()
    
    print("🔧 Corrigindo caminhos nos arquivos HTML...")
    for filepath in glob.glob('docs/**/*.html', recursive=True):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Corrigir caminhos
        content = content.replace('href="/static/', 'href="/peregrinecomacancaonova/static/')
        content = content.replace('src="/static/', 'src="/peregrinecomacancaonova/static/')
        content = content.replace('href="/roteiro/', 'href="/peregrinecomacancaonova/roteiro/')
        content = content.replace('href="/roteiros/', 'href="/peregrinecomacancaonova/roteiros/')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print("✅ Site gerado com sucesso em /docs!")
    print(f"📊 Total de roteiros: {len(ROTEIROS_DB)}")
    print(f"📄 Arquivos HTML gerados: {len(list(glob.glob('docs/**/*.html', recursive=True)))}")
