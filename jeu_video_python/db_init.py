from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "Characters"
CHAPITRE_SELECTION = "chapitres"
FACTIONS_COLLECTION = "factions"
MONSTRES_COLLECTION = "monstres" 
CLIENT = MongoClient(MONGO_URI)
DB = CLIENT[DB_NAME]


def creation_db_et_collections(db):
    """Crée la BDD et les collections nécessaires."""
    for col in [CHAPITRE_SELECTION, FACTIONS_COLLECTION, MONSTRES_COLLECTION]:
        if col not in db.list_collection_names():
            db.create_collection(col)
            print(f"Collection '{col}' créée.")
        else:
            print(f"Collection '{col}' déjà existante.")


def ajout_chapitres(db):
    """Insère les chapitres Space Marines."""
    space_marines_id = db[FACTIONS_COLLECTION].find_one({"Nom": "Space Marines"})["_id"]
    db[CHAPITRE_SELECTION].delete_many({})
    chapitres = [
        {"IdFaction": space_marines_id, "Nom": "Ultra Marines", "Description": "Les Ultra Marines sont une légion de Space Marines réputée pour leur discipline et leur tactique.", "Spécialité": "Tactique", "Effectif": 10,
          "Statistiques": { "Attaque": 12, "Défense": 10, "Vie": 150 }
        },
        {"IdFaction": space_marines_id, "Nom": "Blood Angels", "Description": "Les Blood Angels sont connus pour leur bravoure et leur soif de combat, mais aussi pour leur malédiction génétique.", "Spécialité": "Assaut", "Effectif": 10,
         "Statistiques": { "Attaque": 18, "Défense": 9, "Vie": 130 }
        },
        {"IdFaction": space_marines_id, "Nom": "Dark Angels", "Description": "Les Dark Angels sont une légion mystérieuse, souvent entourée de secrets et de mysticisme.", "Spécialité": "Infanterie", "Effectif": 5,
         "Statistiques": { "Attaque": 15, "Défense": 15, "Vie": 200 }
        },
        {"IdFaction": space_marines_id, "Nom": "Raven Guard", "Description": "Les Raven Guard sont des maîtres de la guerre de guérilla et des opérations furtives.", "Spécialité": "Assassinat", "Effectif": 5,
         "Statistiques": { "Attaque": 20, "Défense": 7, "Vie": 120 }
        },
        {"IdFaction": space_marines_id, "Nom": "Imperial Fists", "Description": "Les Imperial Fists sont des maîtres de la défense et de la fortification, connus pour leur résilience.", "Spécialité": "Défense", "Effectif": 10,
         "Statistiques": { "Attaque": 10, "Défense": 18, "Vie": 160 }
        },
    ]
    db[CHAPITRE_SELECTION].insert_many(chapitres)
    print("Chapitres insérés.")


def ajout_factions(db):
    """Insère les Factions"""
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

def donnees_monstres():
    """Dictionnaire contenant les données des monstres."""
    return {
        "Chaos": [
            {"Nom": "Bloodletter", "Rôle": "Démon Infanterie", 
             "Statistiques": {"Attaque": 18, "Défense": 8, "Vie": 70}},
            {"Nom": "Plaguebearer", "Rôle": "Démon Infanterie", 
             "Statistiques": {"Attaque": 10, "Défense": 15, "Vie": 100}},
            {"Nom": "Daemonette", "Rôle": "Démon Infanterie", 
             "Statistiques": {"Attaque": 20, "Défense": 5, "Vie": 60}},
            {"Nom": "Chaos Space Marine", "Rôle": "Élite", 
             "Statistiques": {"Attaque": 15, "Défense": 12, "Vie": 150}},
        ],
        "Nécron": [
            {"Nom": "Guerrier Nécron", "Rôle": "Base", 
             "Statistiques": {"Attaque": 10, "Défense": 10, "Vie": 80}},
            {"Nom": "Immortel Nécron", "Rôle": "Infanterie Lourde", 
             "Statistiques": {"Attaque": 14, "Défense": 14, "Vie": 120}},
            {"Nom": "Destroyer", "Rôle": "Soutien Lourd", 
             "Statistiques": {"Attaque": 25, "Défense": 12, "Vie": 180}},
            {"Nom": "Spectre", "Rôle": "Assaut Rapide", 
             "Statistiques": {"Attaque": 18, "Défense": 8, "Vie": 100}},
        ],
        "Orcs": [
            {"Nom": "Boy Ork", "Rôle": "Base", 
             "Statistiques": {"Attaque": 12, "Défense": 8, "Vie": 90}},
            {"Nom": "Nob Ork", "Rôle": "Élite", 
             "Statistiques": {"Attaque": 16, "Défense": 12, "Vie": 130}},
            {"Nom": "Gretchin", "Rôle": "Troupaille", 
             "Statistiques": {"Attaque": 5, "Défense": 3, "Vie": 30}},
            {"Nom": "Killa Kan", "Rôle": "Véhicule Léger", 
             "Statistiques": {"Attaque": 20, "Défense": 15, "Vie": 200}},
        ],
        "Eldars": [
            {"Nom": "Gardien Eldar", "Rôle": "Base", 
             "Statistiques": {"Attaque": 12, "Défense": 6, "Vie": 70}},
            {"Nom": "Ranger", "Rôle": "Furtif", 
             "Statistiques": {"Attaque": 15, "Défense": 5, "Vie": 65}},
            {"Nom": "Vengeur Lugubre", "Rôle": "Élite", 
             "Statistiques": {"Attaque": 18, "Défense": 8, "Vie": 80}},
            {"Nom": "Seigneur Fantôme", "Rôle": "Monstrueux", 
             "Statistiques": {"Attaque": 30, "Défense": 20, "Vie": 400}},
        ],
        "Tyranides": [
            {"Nom": "Hormagaunt", "Rôle": "Essaim", 
             "Statistiques": {"Attaque": 10, "Défense": 4, "Vie": 50}},
            {"Nom": "Termagant", "Rôle": "Essaim (Tir)", 
             "Statistiques": {"Attaque": 8, "Défense": 5, "Vie": 50}},
            {"Nom": "Guerrier Tyranide", "Rôle": "Synapse", 
             "Statistiques": {"Attaque": 17, "Défense": 13, "Vie": 160}},
            {"Nom": "Carnifex", "Rôle": "Monstrueux", 
             "Statistiques": {"Attaque": 35, "Défense": 18, "Vie": 500}},
        ]
    }


def ajout_monstres(db):
    """Ajoute les monstres et unités pour les factions."""
    db[MONSTRES_COLLECTION].delete_many({})

    factions_ids = {f["Nom"]: f["_id"] 
                    for f in db[FACTIONS_COLLECTION].find({}, {"Nom": 1})}
    
    monstres_a_ajouter = []
    donnees_par_faction = donnees_monstres() 

    for nom_faction, liste_monstres in donnees_par_faction.items():
        id_faction = factions_ids.get(nom_faction)
        if id_faction:
            for monstre in liste_monstres:
                monstre["IdFaction"] = id_faction
                monstres_a_ajouter.append(monstre)

    if monstres_a_ajouter:
        db[MONSTRES_COLLECTION].insert_many(monstres_a_ajouter)
        print(f"{len(monstres_a_ajouter)} monstres et unités insérés.")
    else:
        print("Aucun monstre n'a été ajouté.")


if __name__ == "__main__":
    try:
        creation_db_et_collections(DB)
        ajout_chapitres(DB)
        ajout_factions(DB)
        ajout_monstres(DB)
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
    finally:
        CLIENT.close()