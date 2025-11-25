from flask_frozen import Freezer
from main import app
from data_roteiros import ROTEIROS_DB

freezer = Freezer(app)

@freezer.register_generator
def roteiro_detalhe():
    for r in obter_roteiros_do_banco():
        yield {'id': r.id}


if __name__ == "__main__":
    freezer.freeze()
