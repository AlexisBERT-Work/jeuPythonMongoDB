from pymongo import MongoClient

# --- Configuration de la DB ---
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "Characters"
CHAPITRE_SELECTION = "chapitres"
FACTIONS_COLLECTION = "factions"
CLIENT = MongoClient(MONGO_URI)
DB = CLIENT[DB_NAME]


def creation_db_et_collections(db):
    """Crée la BDD et les collections nécessaires."""
    print("--- Préparation de la base de données ---")
    for col in [CHAPITRE_SELECTION, FACTIONS_COLLECTION]:
        if col not in db.list_collection_names():
            db.create_collection(col)
            print(f"Collection '{col}' créée.")
        else:
            print(f"Collection '{col}' déjà existante.")


def ajout_chapitres(db):
    """ Insère les chapitres, et l'effectif par défaut."""
    db[CHAPITRE_SELECTION].delete_many({})
    chapitres = [
        {"Nom": "Ultra Marines", "Description": "Les Ultra Marines sont une légion de Space Marines réputée pour leur discipline et leur tactique.", "Spécialité": "Tactique", "Effectif": 10, 
         "Statistiques": {"Attaque": 12, "Défense": 10, "Vie": 150}
        },
        {"Nom": "Blood Angels", "Description": "Les Blood Angels sont connus pour leur bravoure et leur soif de combat, mais aussi pour leur malédiction génétique.", "Spécialité": "Assaut", "Effectif": 10,
         "Statistiques": {"Attaque": 18, "Défense": 9, "Vie": 130}
        },
        {"Nom": "Dark Angels", "Description": "Les Dark Angels sont une légion mystérieuse, souvent entourée de secrets et de mysticisme.", "Spécialité": "Infanterie", "Effectif": 5,
         "Statistiques": {"Attaque": 15, "Défense": 15, "Vie": 200}
        },
        {"Nom": "Raven Guard", "Description": "Les Raven Guard sont des maîtres de la guerre de guérilla et des opérations furtives.", "Spécialité": "Assassinat",
            "Effectif": 5,
            "Statistiques": {"Attaque": 20, "Défense": 7, "Vie": 120}
        },
        {"Nom": "Imperial Fists", "Description": "Les Imperial Fists sont des maîtres de la défense et de la fortification, connus pour leur résilience.", "Spécialité": "Défense", "Effectif": 10,
         "Statistiques": {"Attaque": 10, "Défense": 18, "Vie": 160}
        },
    ]
    db[CHAPITRE_SELECTION].insert_many(chapitres)
    print("Chapitres insérés.")


def ajout_factions(db):
    """Insère les Factions."""
    db[FACTIONS_COLLECTION].delete_many({})
    factions = [
        {"Nom": "Chaos"},
        {"Nom": "Nécron"},
        {"Nom": "Orcs"},
        {"Nom": "Eldars"},
        {"Nom": "Tyranides"},
        {"Nom": "Space Marines"},
    ]
    db[FACTIONS_COLLECTION].insert_many(factions)
    print("Factions insérées.")

if __name__ == "__main__":
    try:
        creation_db_et_collections(DB)
        ajout_chapitres(DB)
        ajout_factions(DB)
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
    finally:
        CLIENT.close()
        print("Connexion MongoDB fermée.")