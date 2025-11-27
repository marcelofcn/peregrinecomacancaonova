# freeze.py - VERSÃO FINAL OTIMIZADA
from flask_frozen import Freezer
from main import app, ROTEIROS_DB
import shutil
import os

print("\n" + "="*70)
print("🚀 FLASK-FROZEN - GERANDO SITE ESTÁTICO")
print("="*70)
print(f"📊 Roteiros carregados: {len(ROTEIROS_DB)}")

if len(ROTEIROS_DB) > 0:
    print("✅ Roteiros encontrados:")
    for r in ROTEIROS_DB[:3]:
        print(f"   → {r['id']}: {r['title']}")
    if len(ROTEIROS_DB) > 3:
        print(f"   ... e mais {len(ROTEIROS_DB) - 3}")
else:
    print("❌ AVISO: Nenhum roteiro carregado!")

print("="*70 + "\n")

# Configurações
app.config["FREEZER_DESTINATION"] = "docs"
app.config["FREEZER_BASE_URL"] = "https://marcelofcn.github.io/peregrinecomacancaonova/"
app.config["FREEZER_REMOVE_EXTRA_FILES"] = False
app.config["FREEZER_RELATIVE_URLS"] = True

freezer = Freezer(app)

# Limpar docs
if os.path.exists("docs"):
    print("🗑️  Limpando docs...")
    git_path = os.path.join("docs", ".git")
    has_git = os.path.exists(git_path)
    
    if has_git:
        shutil.move(git_path, ".git_temp")
    
    shutil.rmtree("docs")
    os.makedirs("docs")
    
    if has_git:
        shutil.move(".git_temp", git_path)

# Registrar URLs de roteiros
@freezer.register_generator
def roteiro_detalhe():
    for r in ROTEIROS_DB:
        yield {'id': r['id']}

if __name__ == "__main__":
    print("🔄 Gerando páginas...\n")
    
    try:
        freezer.freeze()
        print("\n✅ Freeze concluído!")
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
    
    # Criar .nojekyll
    with open("docs/.nojekyll", 'w') as f:
        f.write('')
    print("✅ .nojekyll criado")
    
    # Criar 404.html
    with open("docs/404.html", 'w', encoding='utf-8') as f:
        f.write("""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0;url=https://marcelofcn.github.io/peregrinecomacancaonova/">
    <title>Redirecionando...</title>
</head>
<body style="font-family: sans-serif; text-align: center; padding: 50px;">
    <h1>Página não encontrada</h1>
    <p>Redirecionando para a página inicial...</p>
</body>
</html>""")
    print("✅ 404.html criado")
    
    # Verificar arquivos gerados
    print("\n" + "="*70)
    print("🔍 VERIFICAÇÃO:")
    print("="*70)
    
    index_path = "docs/index.html"
    if os.path.exists(index_path):
        size = os.path.getsize(index_path)
        print(f"✅ index.html: {size:,} bytes")
        
        # Verificar conteúdo
        with open(index_path, 'r', encoding='utf-8') as f:
            html = f.read()
            if 'Nenhum roteiro disponível' in html:
                print("   ⚠️  HTML contém 'Nenhum roteiro disponível'")
            elif len(ROTEIROS_DB) > 0 and ROTEIROS_DB[0]['title'] in html:
                print(f"   ✅ Roteiro '{ROTEIROS_DB[0]['title']}' encontrado!")
            else:
                print("   ⚠️  Não foi possível confirmar roteiros no HTML")
    
    # Verificar roteiros individuais
    roteiros_gerados = 0
    for r in ROTEIROS_DB:
        path = f"docs/roteiro/{r['id']}/index.html"
        if os.path.exists(path):
            roteiros_gerados += 1
    
    print(f"\n📊 Páginas de roteiros geradas: {roteiros_gerados}/{len(ROTEIROS_DB)}")
    
    if roteiros_gerados == len(ROTEIROS_DB) and len(ROTEIROS_DB) > 0:
        print("\n✅ SUCESSO! Site gerado corretamente!")
    else:
        print("\n⚠️  Alguns roteiros podem não ter sido gerados")
    
    print("="*70)
    print("\n🚀 Pronto para deploy!")
