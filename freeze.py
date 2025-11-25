from flask_frozen import Freezer
from data_roteiros import ROTEIROS_DB

freezer = Freezer()

@freezer.register_generator
def roteiro_detalhe():
    for r in ROTEIROS_DB:
        yield {'id': r["id"]}



if __name__ == "__main__":
    freezer.freeze()
