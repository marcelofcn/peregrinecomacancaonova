# app.py  (base inspirado no seu /mnt/data/app.py)
from flask import Flask, render_template, abort, url_for

app = Flask(__name__)
app.secret_key = 'sua-chave-secreta-aqui'

# --- Cole aqui o dicionário ROTEIROS_DB do seu /mnt/data/app.py ---
# Para evitar duplicação no response, assumimos que você manteve exatamente o ROTEIROS_DB
# presente no arquivo /mnt/data/app.py e o colocou aqui.
from data_roteiros import ROTEIROS_DB  # alternativa: mantenha ROTEIROS_DB diretamente neste arquivo

# ==================== ROTAS ====================

@app.route('/')
def home():
    """Página inicial com destaque apenas para roteiros Canção Nova"""
    # Hero texts agora serão renderizados sobre o banner; mantemos strings caso queira usar.
    hero_texts = [
        "Roteiros de Espiritualidade",
        "Roteiros Turísticos com Fé",
        "Experiências que transformam"
    ]

    roteiros_cn = [
        {
            "id": r["id"],
            "img": r["img"],
            "title": r["title"],
            "date": f"{r['start']} a {r['end']}",
            "url": f"/roteiro/{r['id']}"
        }
        for r in ROTEIROS_DB.values()
        if r.get("empresa") == "cancaonova"
    ]

    # destaque: próximos 4
    destaque = roteiros_cn[:4]

    return render_template('home.html', hero_texts=hero_texts, destaque=destaque)

@app.route('/roteiros')
def roteiros():
    roteiros_cn = [
        r for r in ROTEIROS_DB.values() if r.get("empresa") == "cancaonova"
    ]
    return render_template('roteiros.html', roteiros=roteiros_cn)

@app.route('/roteiro/<int:roteiro_id>')
def roteiro_detalhe(roteiro_id):
    roteiro = ROTEIROS_DB.get(roteiro_id)
    if not roteiro or roteiro.get("empresa") != "cancaonova":
        abort(404)
    return render_template('detalhe.html', roteiro=roteiro)

@app.route('/institucional')
def institucional():
    return render_template('institucional.html')

@app.route('/contato')
def contato():
    # contatos permanecem com São José
    contato_info = {
        "whatsapp": "+5567998927001",
        "telefone": "(67) 3211-7001",
        "empresa": "São José Viagens"
    }
    return render_template('contato.html', contato=contato_info)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
