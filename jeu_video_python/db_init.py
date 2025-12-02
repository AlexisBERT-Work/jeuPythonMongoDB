from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "Characters"
PERSONNAGES_COLLECTION = "personnages"
MONSTRES_COLLECTION = "monstres"


def create_db_and_collections():
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

if __name__ == "__main__":
    create_db_and_collections()