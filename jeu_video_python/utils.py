# utils.py

from pymongo import MongoClient
import random
from models import Character, Score, Attack # S'assurer que Attack est importé

# --- Configuration de la DB ---
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "rpg_game_db"
CHARACTERS_COLLECTION = "characters"
MONSTERS_COLLECTION = "monsters"
SCORES_COLLECTION = "scores"

def get_db():
    """Retourne l'objet base de données."""
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        return client[DB_NAME]
    except Exception as e:
        # Ceci est important pour s'assurer que l'erreur de connexion est affichée
        print(f"❌ Impossible de se connecter à MongoDB. Assurez-vous que le serveur est lancé : {e}")
        exit()

# --- Fonction Helper pour créer un Character (DÉJÀ CORRIGÉ DANS MODELS.PY, MAIS ON ASSURE) ---

def _create_character_from_doc(doc: dict, is_player: bool) -> Character:
    """Crée et retourne un objet Character à partir d'un document MongoDB."""
    
    # La logique de conversion des attaques de dict à objet Attack est gérée dans Character.__init__
    return Character(
        name=doc["name"], 
        attack=doc["attack"], 
        defense=doc["defense"], 
        hp=doc["hp"], 
        is_player_char=is_player,
        attacks=doc.get("attacks") # Passe la liste de dicts (ou d'objets)
    )


def get_all_player_characters():
    """Récupère tous les personnages jouables de la DB et les retourne comme objets Character."""
    db = get_db()
    player_docs = list(db[CHARACTERS_COLLECTION].find())
    
    characters = [_create_character_from_doc(doc, True) for doc in player_docs]
    return characters

def get_random_monster():
    """Sélectionne un monstre aléatoire de la DB et le retourne comme objet Character."""
    db = get_db()
    
    count = db[MONSTERS_COLLECTION].count_documents({})
    if count == 0:
        print("❌ Aucune donnée de monstre trouvée. Veuillez exécuter db_init.py.")
        return None
    
    random_index = random.randint(0, count - 1)
    
    monster_doc = db[MONSTERS_COLLECTION].find().skip(random_index).limit(1)[0]
    
    monster = _create_character_from_doc(monster_doc, False)
    return monster

# --- Fonctions de Gestion des Scores (Score Data) ---

def save_score(username: str, waves_survived: int):
    """Crée un objet Score et l'insère dans la collection 'scores'."""
    db = get_db()
    new_score = Score(username, waves_survived)
    
    try:
        db[SCORES_COLLECTION].insert_one(new_score.to_dict())
        print(f"\n✨ Score sauvegardé ! {username} a survécu à {waves_survived} vagues.")
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde du score : {e}")

def get_top_scores(limit: int = 3):
    """Récupère les X meilleurs scores (par nombre de vagues) et les retourne."""
    db = get_db()
    
    top_scores = list(db[SCORES_COLLECTION]
                      .find()
                      .sort("score", -1)
                      .limit(limit))
    
    return top_scores

def display_ranking():
    """Affiche le classement des 3 meilleurs scores."""
    top_3 = get_top_scores(3)
    
    print("\n" + "="*30)
    print("🏆 CLASSEMENT DES MEILLEURS SCORES")
    print("="*30)
    
    if not top_3:
        print("Aucun score enregistré pour le moment.")
        print("="*30)
        return

    for i, score_doc in enumerate(top_3):
        username = score_doc.get("username", "Inconnu")
        waves = score_doc.get("score", 0)
        
        print(f"#{i+1}: {username:<15} - {waves} vagues")
    
    print("="*30)