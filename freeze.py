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
    ROTEIROS_DB = app.ROTEIROS_DB

    print(f"✅ {len(ROTEIROS_DB)} roteiros encontrados")

except Exception as e:
    print(f"❌ Erro ao importar app: {e}")
    sys.exit(1)

# ------------------------------------------------------
# Configurações do Freezer
# ------------------------------------------------------
app_instance.config['FREEZER_DESTINATION'] = 'docs'
app_instance.config['FREEZER_RELATIVE_URLS'] = False
app_instance.config['FREEZER_BASE_URL'] = "https://marcelofcn.github.io/peregrinecomacancaonova"

freezer = Freezer(app_instance)
os.makedirs('docs', exist_ok=True)

# ------------------------------------------------------
# Rotas dinâmicas
# ------------------------------------------------------
@freezer.register_generator
def roteiro_detalhe():
    """
    Gera automaticamente todas as rotas
    /peregrinecomacancaonova/roteiro/<id>/
    para o Flask-Frozen.
    """
    for id in ROTEIROS_DB.keys():
        yield {'roteiro_id': int(id)}

# ------------------------------------------------------
# Execução
# ------------------------------------------------------
if __name__ == '__main__':
    print("🚀 Gerando site estático com Flask-Frozen...")
    
    try:
        freezer.freeze()
    except Exception as e:
        print(f"❌ Erro durante a geração: {e}")
        sys.exit(1)

    # --------------------------------------------------
    # Ajuste de caminhos nos HTML para GitHub Pages
    # --------------------------------------------------
    print("🔧 Ajustando caminhos para GitHub Pages...")

    for filepath in glob.glob('docs/**/*.html', recursive=True):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Corrige referências estáticas
        content = content.replace('href="/static/', 'href="/peregrinecomacancaonova/static/')
        content = content.replace('src="/static/', 'src="/peregrinecomacancaonova/static/')

        # Corrige rotas de detalhes
        content = content.replace('href="/roteiro/', 'href="/peregrinecomacancaonova/roteiro/')

        # Corrige rota lista geral /roteiros/
        content = content.replace('href="/roteiros/', 'href="/peregrinecomacancaonova/roteiros/')

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    print("✅ Caminhos ajustados!")
    print("✅ Site estático gerado em: /docs")
