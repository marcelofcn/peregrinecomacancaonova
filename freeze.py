from flask_frozen import Freezer
from main import app
from data_roteiros import ROTEIROS_DB

freezer = Freezer(app)

@freezer.register_generator
def roteiro_detalhe():
    for id_str, r in ROTEIROS_DB.items():
        yield {"roteiro_id": int(id_str)}

if __name__ == "__main__":
    freezer.freeze()
