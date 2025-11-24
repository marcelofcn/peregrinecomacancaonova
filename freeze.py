from flask_frozen import Freezer
from main import app, ROTEIROS_DB

freezer = Freezer(app)

# Gerar páginas individuais de cada roteiro
@freezer.register_generator
def roteiro_detalhe():
    for id, r in ROTEIROS_DB.items():
        yield {"roteiro_id": int(id)}

if __name__ == "__main__":
    freezer.freeze()
