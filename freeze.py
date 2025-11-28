#!/usr/bin/env python
# freeze.py
# -*- coding: utf-8 -*-
import sys, os, glob, json
from flask_frozen import Freezer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import app
    app_instance = app.app
    print("✅ Módulo 'app' importado")
except Exception as e:
    print(f"❌ Erro ao importar app: {e}")
    sys.exit(1)

# Ajuste do freezer
app_instance.config['FREEZER_DESTINATION'] = 'docs'
app_instance.config['FREEZER_RELATIVE_URLS'] = False
app_instance.config['FREEZER_BASE_URL'] = 'https://marcelofcn.github.io/peregrinecomacancaonova'

freezer = Freezer(app_instance)
os.makedirs('docs', exist_ok=True)

# Carrega base para gerar páginas dinâmicas
with open("roteiros.json", "r", encoding="utf-8") as f:
    ROTEIROS_DB = json.load(f)

MESES_SLUGS = [
    "janeiro","fevereiro","marco","abril","maio","junho",
    "julho","agosto","setembro","outubro","novembro","dezembro"
]

@freezer.register_generator
def roteiro_detalhe():
    for id in ROTEIROS_DB.keys():
        yield {'roteiro_id': int(id)}

@freezer.register_generator
def roteiros_por_mes():
    for mes in MESES_SLUGS:
        yield {'mes': mes}

# Opcional: criar a rota /roteiros/ (todos)
# freezer automaticamente pega a rota estática /peregrinecomacancaonova/roteiros/ se existir no app

if __name__ == '__main__':
    print("🚀 Gerando site estático...")
    freezer.freeze()
    print("✅ Freeze concluído. Ajustando caminhos estáticos...")

    # Ajuste simples: garantir que referências a "/static/" apontem para o root do repo
    for filepath in glob.glob('docs/**/*.html', recursive=True):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        content = content.replace('src="/static/', 'src="/peregrinecomacancaonova/static/')
        content = content.replace('href="/static/', 'href="/peregrinecomacancaonova/static/')
        content = content.replace('href="/roteiro/', 'href="/peregrinecomacancaonova/roteiro/')
        # se houver outras substituições necessárias, adicione aqui

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    print("🔧 Ajustes finais aplicados. Site em /docs")
