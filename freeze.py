from flask_frozen import Freezer
from main import app, ROTEIROS_DB

freezer = Freezer(app)

# Gerar páginas individuais de cada roteiro
@freezer.register_generator
def roteiro():
    for r in ROTEIROS_DB:
        yield {"id": r["id"]}


if __name__ == "__main__":
    freezer.freeze()
