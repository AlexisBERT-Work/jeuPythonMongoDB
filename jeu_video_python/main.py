import sys
from utils import get_db, choisir_equipe
from game import lancer_combat

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "Characters"


def menu_affichage():    
    """Affiche le menu principal du jeu."""
    print("  JEU DE COMBAT - MENU")
    print("1. Lancer un nouveau combat")
    print("2. Classement")
    print("3. Quitter le jeu")


def menu_principal(db):
    """Affiche le menu principal et gère les choix de l'utilisateur."""
    while True:
        menu_affichage()
        choix = input("Votre choix : ")
        
        if choix == '1':
            pseudo = input("Choisissez votre pseudo : ")
            equipe = choisir_equipe(db, taille_equipe=3)
            if equipe:
                lancer_combat(db, equipe, pseudo)
            
        elif choix == '2':
            print("\n      Classement des joueurs")
            scores_coll = db["scores"]
            top_scores = scores_coll.find().sort("score", -1).limit(3)
            for i, score_entry in enumerate(top_scores, start=1):
                print(f"{i}. {score_entry['nom']} - {score_entry['score']} points")
            print("------------------------------\n")
        
        elif choix == '3':
            print("Merci d'avoir joué. Au revoir !")
            sys.exit(0)
            
        else:
            print("Choix invalide. Veuillez réessayer.")


if __name__ == "__main__":
    db = get_db(MONGO_URI, DB_NAME)
    menu_principal(db)