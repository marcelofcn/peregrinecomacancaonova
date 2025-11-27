# freeze.py - VERSÃO CORRIGIDA
from flask_frozen import Freezer
from main import app
from data import ROTEIROS_DB
import shutil
import os

# Configurações importantes
app.config["FREEZER_DESTINATION"] = "docs"
app.config["FREEZER_BASE_URL"] = "https://marcelofcn.github.io/peregrinecomacancaonova/"
app.config["FREEZER_REMOVE_EXTRA_FILES"] = False
app.config["FREEZER_RELATIVE_URLS"] = True  # IMPORTANTE para GitHub Pages

freezer = Freezer(app)

# Limpar pasta docs ANTES (mas preservar .git se existir)
if os.path.exists("docs"):
    print("🗑️  Limpando pasta docs antiga...")
    # Preserva a pasta .git se existir
    git_path = os.path.join("docs", ".git")
    has_git = os.path.exists(git_path)
    
    if has_git:
        shutil.move(git_path, ".git_temp")
    
    shutil.rmtree("docs")
    os.makedirs("docs")
    
    if has_git:
        shutil.move(".git_temp", git_path)

# Registrar rotas dinâmicas
@freezer.register_generator
def roteiro_detalhe():
    """Gera URLs para todos os roteiros"""
    for r in ROTEIROS_DB:
        yield {'id': r["id"]}

if __name__ == "__main__":
    print("🚀 Iniciando o processo de congelamento (freezing)...")
    
    # Executar o freeze
    freezer.freeze()
    
    # Criar arquivo .nojekyll (CRÍTICO para GitHub Pages)
    nojekyll_path = os.path.join("docs", ".nojekyll")
    with open(nojekyll_path, 'w') as f:
        f.write('')
    print("✅ Arquivo .nojekyll criado")
    
    # Criar arquivo 404.html personalizado (opcional mas recomendado)
    error_404_path = os.path.join("docs", "404.html")
    if not os.path.exists(error_404_path):
        with open(error_404_path, 'w', encoding='utf-8') as f:
            f.write("""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0;url=https://marcelofcn.github.io/peregrinecomacancaonova/">
    <title>Redirecionando...</title>
</head>
<body>
    <p>Redirecionando para a página inicial...</p>
</body>
</html>""")
        print("✅ Arquivo 404.html criado")
    
    # Verificar se os arquivos foram gerados
    print("\n📋 Verificando arquivos gerados:")
    for root, dirs, files in os.walk("docs"):
        level = root.replace("docs", "").count(os.sep)
        indent = " " * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = " " * 2 * (level + 1)
        for file in files[:5]:  # Mostra apenas os primeiros 5 arquivos
            print(f"{subindent}{file}")
        if len(files) > 5:
            print(f"{subindent}... e mais {len(files) - 5} arquivos")
    
    print("\n✅ Freezer finalizado com sucesso!")
    print("📦 Pasta 'docs' pronta para deploy no GitHub Pages")
    print("\n🔧 Próximos passos:")
    print("   1. git add docs/")
    print("   2. git commit -m 'Build estático atualizado'")
    print("   3. git push origin main")
