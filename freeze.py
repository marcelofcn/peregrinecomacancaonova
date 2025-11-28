#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, glob
from flask_frozen import Freezer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import app

app_instance = app.app
ROTEIROS_DB = app.ROTEIROS_DB

app_instance.config['FREEZER_DESTINATION'] = 'docs'
app_instance.config['FREEZER_RELATIVE_URLS'] = False
app_instance.config['FREEZER_BASE_URL'] = "https://marcelofcn.github.io/peregrinecomacancaonova"

freezer = Freezer(app_instance)
os.makedirs('docs', exist_ok=True)

# 🔥 GERAR PÁGINAS DE DETALHE
@freezer.register_generator
def roteiro_detalhe():
    for id in ROTEIROS_DB.keys():
        yield {'roteiro_id': int(id)}

# 🔥 GERAR ARQUIVOS ESTÁTICOS
@freezer.register_generator
def static():
    for path in glob.glob('static/**/*.*', recursive=True):
        filename = path.replace("static/", "")
        yield {'filename': filename}

# EXECUTAR
if __name__ == '__main__':
    freezer.freeze()

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
