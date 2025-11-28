#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, glob
from flask_frozen import Freezer

# Garante que o diretório atual esteja no path do Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ------------------------------------------------------
# Importa o app Flask e o banco de roteiros
# ------------------------------------------------------
try:
    import app  # importa o módulo inteiro
    print("✅ Módulo 'app' importado com sucesso")
    app_instance = app.app  # pega o objeto Flask
    print(f"✅ {len(app.ROTEIROS_DB)} roteiros encontrados")
except Exception as e:
    print(f"❌ Erro ao importar app: {e}")
    sys.exit(1)

# ------------------------------------------------------
# Configurações do Freezer
# ------------------------------------------------------
app_instance.config['FREEZER_DESTINATION'] = 'docs'
app_instance.config['FREEZER_RELATIVE_URLS'] = False
app_instance.config['FREEZER_BASE_URL'] = 'https://marcelofcn.github.io/sao-jose-peregrinacoes'

freezer = Freezer(app_instance)
os.makedirs('docs', exist_ok=True)

# ------------------------------------------------------
# Rotas dinâmicas
# ------------------------------------------------------
@freezer.register_generator
def roteiro_detalhe():
    for id in app.ROTEIROS_DB.keys():
        yield {'roteiro_id': int(id)}

# ------------------------------------------------------
# Execução
# ------------------------------------------------------
if __name__ == '__main__':
    print("🚀 Gerando site estático...")
    freezer.freeze()

    # --------------------------------------------------
    # Ajuste de caminhos no HTML gerado (para GitHub Pages)
    # --------------------------------------------------
    print("🔧 Corrigindo caminhos estáticos para o GitHub Pages...")
    for filepath in glob.glob('docs/**/*.html', recursive=True):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Substitui caminhos absolutos por caminhos relativos ao repositório
        content = content.replace('src="/static/', 'src="/sao-jose-peregrinacoes/static/')
        content = content.replace('href="/static/', 'href="/sao-jose-peregrinacoes/static/')
        content = content.replace('href="/roteiro/', 'href="/sao-jose-peregrinacoes/roteiro/')

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    print("✅ Caminhos ajustados!")
    print("✅ Site estático gerado em /docs")
