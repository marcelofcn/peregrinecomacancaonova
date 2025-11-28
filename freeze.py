# freeze.py - VERSÃO COM CÓPIA DE STATIC
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
app.config["FREEZER_STATIC_IGNORE"] = []  # Não ignorar nada

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
    
    # CRÍTICO: Copiar pasta static manualmente
    print("\n📂 Copiando arquivos estáticos...")
    static_src = "static"
    static_dst = "docs/static"
    
    if os.path.exists(static_src):
        if os.path.exists(static_dst):
            shutil.rmtree(static_dst)
        
        shutil.copytree(static_src, static_dst)
        print(f"✅ Pasta static copiada ({static_src} → {static_dst})")
        
        # Verificar imagens
        img_dir = os.path.join(static_dst, "img")
        if os.path.exists(img_dir):
            img_count = len([f for f in os.listdir(img_dir) if f.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))])
            print(f"   📸 {img_count} imagens encontradas em static/img/")
        else:
            print("   ⚠️  Pasta static/img/ não encontrada!")
    else:
        print("⚠️  Pasta static/ não existe no projeto!")
    
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
    print("🔍 VERIFICAÇÃO FINAL:")
    print("="*70)
    
    index_path = "docs/index.html"
    if os.path.exists(index_path):
        size = os.path.getsize(index_path)
        print(f"✅ index.html: {size:,} bytes")
        
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
    
    print(f"\n📊 Páginas de roteiros: {roteiros_gerados}/{len(ROTEIROS_DB)}")
    print(f"📂 Pasta static copiada: {'✅' if os.path.exists('docs/static') else '❌'}")
    
    if roteiros_gerados == len(ROTEIROS_DB) and len(ROTEIROS_DB) > 0:
        print("\n✅ SUCESSO TOTAL! Site gerado corretamente!")
    else:
        print("\n⚠️  Alguns roteiros podem não ter sido gerados")
    
    print("="*70)
    print("\n🚀 Pronto para deploy!")
