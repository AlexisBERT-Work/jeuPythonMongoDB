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

def selectionner_personnage(disponibles: list, index_humain: int) -> Personnage:
    """Retire et retourne le personnage de la liste des disponibles en utilisant l'index"""
    index_python = index_humain - 1
    perso = disponibles.pop(index_python) 
    
    return perso

def choisir_equipe(db, taille_equipe: int = 3, collection_name: str = CHAPITRES_COLLECTION) -> List[Personnage]:
    personnages = recup_personnages(db, collection_name)
    if not personnages:
        print("Impossible de créer une équipe.")
        return []

    selection = []
    disponibles = personnages.copy()

    print("Sélectionnez vos personnages :")
    while len(selection) < taille_equipe:
        afficher_personnages(disponibles)
        
        max_choix = len(disponibles)
        prompt = f"Choix {len(selection)+1}/{taille_equipe} (1-{max_choix}) : "
        choix_index_humain = lire_choix_valide(max_choix, prompt)
    
        perso = selectionner_personnage(disponibles, choix_index_humain)
        
        
        selection.append(perso)
        # pop les persos 

        print(f"-> {perso.nom} ajouté à l'équipe.\n")

    print("Équipe constituée :")
    afficher_personnages(selection)
    return selection

def equipe_est_vivante(equipe: List[Personnage]) -> bool:
    return any(p.est_vivant() for p in equipe)


def reset_vies_equipe(equipe: List[Personnage]) -> None:
    for p in equipe:
        p.vie_actuelle = p.vie_max


def clone_equipe_from_docs(team_docs: List[dict]) -> List[Personnage]:
    return [Personnage(doc) for doc in team_docs]


def realiser_vague(equipe: List[Personnage], monstre: Monstre) -> Tuple[bool, Monstre]:

    for p in equipe:
        if not p.est_vivant():
            continue
        degats = p.attaquer(monstre)
        print(f"{p.nom} attaque {monstre.nom} et inflige {degats} dégâts. ({monstre.vie_actuelle}/{monstre.vie_max} PV)")
        
        if not monstre.est_vivant():
            print(f"{monstre.nom} est vaincu !")
            return True, monstre 

    if monstre.est_vivant():
        cibles_vivantes = [p for p in equipe if p.est_vivant()]
        if cibles_vivantes:
            cible = random.choice(cibles_vivantes)
            degats_monstre = monstre.attaquer(cible)
            print(f"{monstre.nom} attaque {cible.nom} et inflige {degats_monstre} dégâts. ({cible.vie_actuelle}/{cible.vie_max} PV)")
    return False, monstre