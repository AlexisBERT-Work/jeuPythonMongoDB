# db_init.py

from pymongo import MongoClient
from models import Character, Attack

# Configuration de la base de données
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "Characters"
CHARACTERS_COLLECTION = "characters"
MONSTERS_COLLECTION = "monsters"


def get_db_client():
    """Initialise et retourne le client MongoDB."""
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        return client
    except Exception as e:
        print(f"Erreur: Impossible de se connecter à MongoDB sur {MONGO_URI}.")
        print(f"Veuillez vérifier que le serveur est démarré.")
        print(f"Détails: {e}")
        exit(1)


def create_attack_sets():
    """Crée et retourne les ensembles d'attaques pour les joueurs et les monstres."""
    base_attack = Attack("Coup Standard", 0, 1.0)
    power_attack = Attack("Attaque Puissante", 0, 1.5)
    fast_attack = Attack("Attaque Rapide", 0, 0.8)
    
    player_attacks = [base_attack, power_attack, fast_attack]
    monster_attacks = [base_attack]
    
    return player_attacks, monster_attacks


def get_player_data(player_attacks):
    """Retourne les données brutes des personnages joueurs."""
    return [
        ("Guerrier", 15, 10, 100, player_attacks),
        ("Mage", 20, 5, 80, player_attacks),
        ("Archer", 18, 7, 90, player_attacks),
        ("Voleur", 22, 8, 85, player_attacks),
        ("Paladin", 14, 12, 110, player_attacks),
        ("Sorcier", 25, 3, 70, player_attacks),
        ("Chevalier", 17, 15, 120, player_attacks),
        ("Moine", 19, 9, 95, player_attacks),
        ("Berserker", 23, 6, 105, player_attacks),
        ("Chasseur", 16, 11, 100, player_attacks)
    ]


def get_monster_data(monster_attacks):
    """Retourne les données brutes des monstres."""
    return [
        ("Gobelin", 10, 5, 50, monster_attacks),
        ("Orc", 20, 8, 120, monster_attacks),
        ("Dragon", 35, 20, 300, monster_attacks),
        ("Zombie", 12, 6, 70, monster_attacks),
        ("Troll", 25, 15, 200, monster_attacks),
        ("Spectre", 18, 10, 100, monster_attacks),
        ("Golem", 30, 25, 250, monster_attacks),
        ("Vampire", 22, 12, 150, monster_attacks),
        ("Loup-garou", 28, 18, 180, monster_attacks),
        ("Squelette", 15, 7, 90, monster_attacks)
    ]


def convert_to_documents(data_tuples, is_player_char=True):
    """Convertit une liste de tuples en documents MongoDB."""
    documents = []
    for name, atk, defs, hp, attacks in data_tuples:
        character = Character(name, atk, defs, hp, is_player_char=is_player_char, attacks=attacks)
        documents.append(character.to_dict())
    return documents


def clear_collections(db):
    """Vide les collections existantes."""
    db[CHARACTERS_COLLECTION].delete_many({})
    db[MONSTERS_COLLECTION].delete_many({})


def insert_data(db, player_docs, monster_docs):
    """Insère les documents dans les collections appropriées."""
    db[CHARACTERS_COLLECTION].insert_many(player_docs)
    db[MONSTERS_COLLECTION].insert_many(monster_docs)


def verify_insertion(db):
    """Vérifie et affiche le nombre de documents insérés."""
    player_count = db[CHARACTERS_COLLECTION].count_documents({})
    monster_count = db[MONSTERS_COLLECTION].count_documents({})
    
    print(f"Base de données '{DB_NAME}' initialisée avec succès.")
    print(f"{player_count} personnages insérés dans '{CHARACTERS_COLLECTION}'.")
    print(f"{monster_count} monstres insérés dans '{MONSTERS_COLLECTION}'.")


def initialize_db():
    """
    Initialise la base de données : se connecte, vide les collections existantes
    et insère les données initiales avec les attaques.
    """
    client = get_db_client()
    db = client[DB_NAME]

    try:
        # Création des attaques
        player_attacks, monster_attacks = create_attack_sets()
        
        # Récupération des données
        player_data = get_player_data(player_attacks)
        monster_data = get_monster_data(monster_attacks)
        
        # Conversion en documents MongoDB
        player_docs = convert_to_documents(player_data, is_player_char=True)
        monster_docs = convert_to_documents(monster_data, is_player_char=False)
        
        # Nettoyage et insertion
        clear_collections(db)
        insert_data(db, player_docs, monster_docs)
        
        # Vérification
        verify_insertion(db)

    except Exception as e:
        print(f"Erreur lors de l'insertion des documents: {e}")

    finally:
        client.close()


if __name__ == "__main__":
    initialize_db()