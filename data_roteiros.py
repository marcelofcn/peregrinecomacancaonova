import json

with open("roteiros.json", "r", encoding="utf-8") as f:
    ROTEIROS_DB = json.load(f)
