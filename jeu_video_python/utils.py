from datetime import datetime
from pymongo import MongoClient
from typing import List, Tuple, Optional
import random
from models import Combattant, Personnage, Monstre


MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "Characters"
CHAPITRES_COLLECTION = "chapitres"
MONSTRES_COLLECTION = "monstres"
SCORES_COLLECTION = "scores"

def get_db(mongo_uri: str = MONGO_URI, db_name: str = DB_NAME):
    client = MongoClient(mongo_uri)
    return client[db_name]

def recup_personnages(db, collection_name: str = CHAPITRES_COLLECTION) -> List[Personnage]:
    docs = list(db[collection_name].find({}))
    return [Personnage(doc) for doc in docs]


def recup_monstres(db, collection_name: str = MONSTRES_COLLECTION) -> List[Monstre]:
    docs = list(db[collection_name].find({}))
    return [Monstre(doc) for doc in docs]


def monstre_aleatoire(db, collection_name: str = MONSTRES_COLLECTION) -> Optional[Monstre]:
    count = db[collection_name].count_documents({})
    if count == 0:
        return None
    idx = random.randrange(0, count)
    doc = db[collection_name].find().skip(idx).limit(1)
    doc = list(doc)
    if not doc:
        return None
    return Monstre(doc[0])


def afficher_personnages(personnages: List[Personnage]) -> None:
    if not personnages:
        print("Aucun personnage disponible.")
        return
    for i, p in enumerate(personnages, start=1):
        print(f"{i}. {p}")


def afficher_monstre(monstre: Monstre) -> None:
    if monstre is None:
        print("(Aucun monstre)")
    else:
        print(f"Monstre rencontré : {monstre}")


def lire_choix_valide(max_choix: int, prompt: str) -> int:
    """Vérifier que l'entrée utilisateur est un entier valide entre 1 et max_choix."""
    while True:
        choix_str = input(prompt)
        try:
            choix_index_humain = int(choix_str)
        except ValueError:
            print("Veuillez entrer un nombre.")
            continue

        if 1 <= choix_index_humain <= max_choix:
            return choix_index_humain
        else:
            print(f"Veuillez entrer un numéro entre 1 et {max_choix}.") 


def demander_choix_personnage(disponibles: List[Personnage], equipe: List[Personnage], taille_equipe: int) -> int:
    """Affiche la liste, construit le prompt et retourne l'index (1-based) choisi par l'utilisateur."""
    afficher_personnages(disponibles)
    max_choix = len(disponibles)
    prompt = f"Choix {len(equipe) + 1}/{taille_equipe} (1-{max_choix}) : "
    return lire_choix_valide(max_choix, prompt)


def selectionner_personnage(disponibles: List[Personnage], choix_1_based: int) -> Personnage:
    """Retire et renvoie le personnage choisi via pop()."""
    return disponibles.pop(choix_1_based - 1)


def choisir_equipe(db, taille_equipe: int = 3, collection_name: str = CHAPITRES_COLLECTION) -> List[Personnage]:
    disponibles = recup_personnages(db, collection_name)

    if not disponibles:
        print("Impossible de créer une équipe.")
        return []

    equipe = []
    print("Sélectionnez vos personnages :")

    while len(equipe) < taille_equipe:
        choix = demander_choix_personnage(disponibles, equipe, taille_equipe)
        perso = selectionner_personnage(disponibles, choix)

        equipe.append(perso)
        print(f"-> {perso.nom} ajouté à l'équipe.\n")

    print("Équipe constituée :")
    afficher_personnages(equipe)

    return equipe

def equipe_est_vivante(equipe: List[Personnage]) -> bool:
    return any(p.est_vivant() for p in equipe)


def reset_vies_equipe(equipe: List[Personnage]) -> None:
    for p in equipe:
        p.vie_actuelle = p.vie_max


def clone_equipe_from_docs(team_docs: List[dict]) -> List[Personnage]:
    return [Personnage(doc) for doc in team_docs]


def attaque_personnage_sur_monstre(personnage: Personnage, monstre: Monstre) -> int:
    degats = personnage.attaquer(monstre)
    print(f"{personnage.nom} attaque {monstre.nom} et inflige {degats} dégâts. "
          f"Il lui reste {monstre.vie_actuelle} PV.")
    return degats


def attaque_monstre_sur_equipe(monstre: Monstre, equipe: List[Personnage]) -> Optional[int]:
    cibles_vivantes = [p for p in equipe if p.est_vivant()]
    if not cibles_vivantes:
        return None

    cible = random.choice(cibles_vivantes)
    degats = monstre.attaquer(cible)
    print("============================")
    print(f"{monstre.nom} attaque {cible.nom} et inflige {degats} dégâts !, il lui reste {cible.vie_actuelle} PV.")
    return degats


def realiser_vague(equipe: List[Personnage], monstre: Monstre) -> Tuple[bool, Monstre]:
    """Gère une vague de combat : l'équipe attaque, puis le monstre riposte."""

    for personnage in equipe:
        if not personnage.est_vivant():
            continue

        attaque_personnage_sur_monstre(personnage, monstre)

        if not monstre.est_vivant():
            print(f"*** {monstre.nom} est vaincu ! ***")
            return True, monstre

    if monstre.est_vivant():
        attaque_monstre_sur_equipe(monstre, equipe)

    return False, monstre

def enregistrer_score(db, player_name: str, score: int, collection_name: str = "scores") -> None:
    """Enregistre ou met à jour le score. """
    coll = db[collection_name]
    score_existant = coll.find_one({"nom": player_name})
    score_int = int(score)

    if score_existant:
        ancien_score = score_existant.get("score", 0)
        if score_int > ancien_score:
            coll.update_one(
                {"nom": player_name},
                {"$set": {"score": score_int, "date": datetime.utcnow()}}
            )
            
    else:
        coll.insert_one({
            "nom": player_name,
            "score": score_int,
            "date": datetime.utcnow()
        })