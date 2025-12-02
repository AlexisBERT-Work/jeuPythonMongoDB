from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "Characters"
PERSONNAGES_COLLECTION = "personnages"
MONSTRES_COLLECTION = "monstres"


def creation_db_et_collections():
    """Crée la BDD et les deux collections."""
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]

    if PERSONNAGES_COLLECTION not in db.list_collection_names():
        db.create_collection(PERSONNAGES_COLLECTION)
        print(f"Collection '{PERSONNAGES_COLLECTION}' créée.")
    else:
        print(f"Collection '{PERSONNAGES_COLLECTION}' déjà existante.")

    if MONSTRES_COLLECTION not in db.list_collection_names():
        db.create_collection(MONSTRES_COLLECTION)
        print(f"Collection '{MONSTRES_COLLECTION}' créée.")
    else:
        print(f"Collection '{MONSTRES_COLLECTION}' déjà existante.")

    client.close()

def ajout_personnages():
    """Insère les personnages."""
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    db[PERSONNAGES_COLLECTION].delete_many({})
    personnages = [
        {"Classe": "Guerrier", "Attaque": 10, "Défense": 5, "PV": 150, "Mana": 30},
        {"Classe": "Archer", "Attaque": 13, "Défense": 3, "PV": 100, "Mana": 50},
        {"Classe": "Mage", "Attaque": 15, "Défense": 2, "PV": 80, "Mana": 100},
    ]
    db[PERSONNAGES_COLLECTION].insert_many(personnages)
    client.close()

def ajout_monstres():
    """Insère les monstres."""
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    db[MONSTRES_COLLECTION].delete_many({})
    monstres = [
        {"Nom": "Gobelin", "Attaque": 8, "Défense": 2, "PV": 50},
        {"Nom": "Orc", "Attaque": 12, "Défense": 4, "PV": 80},
        {"Nom": "Dragon", "Attaque": 20, "Défense": 10, "PV": 300},
    ]
    db[MONSTRES_COLLECTION].insert_many(monstres)
    client.close()


if __name__ == "__main__":
    creation_db_et_collections()
    ajout_personnages()
    ajout_monstres()