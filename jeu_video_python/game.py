import time
from typing import List
from models import Personnage 
from utils import equipe_est_vivante, reset_vies_equipe, realiser_vague, monstre_aleatoire, afficher_monstre 


def lancer_combat(db, equipe: List[Personnage]) -> bool:
    """Lance les vagues de combat contre des monstres aléatoires."""
    
    reset_vies_equipe(equipe)
    print("\n--- DÉBUT DE LA BATAILLE ---")

    vagues_vaincues = 0

    while equipe_est_vivante(equipe):
        monstre = monstre_aleatoire(db)
        if monstre is None:
            print("Impossible de trouver un monstre aléatoire. Fin du combat.")
            break

        vagues_vaincues += 1
        print(f"\n       VAGUE {vagues_vaincues} : ATTENTION !       ")
        afficher_monstre(monstre)
        time.sleep(3)

        combattre_vague(equipe, monstre)

        if not equipe_est_vivante(equipe):
            print("\n*** DÉFAITE : Votre équipe a été anéantie. ***")
            return False
        
        print(f"Vague {vagues_vaincues} vaincue !")

        if not demander_continuer():
            print(f"\nVous vous retirez. *** FIN DU COMBAT : {vagues_vaincues} vagues vaincues ! ***")
            return True

    print(f"\n*** FIN DU COMBAT : {vagues_vaincues} vagues vaincues ! ***")
    return True

def combattre_vague(equipe, monstre):
    """Boucle de combat pour une vague."""
    while equipe_est_vivante(equipe) and monstre.est_vivant():
        print("\n--------- Tour de Combat ---------")
        realiser_vague(equipe, monstre)
        time.sleep(2)


def demander_continuer() -> bool:
    """Demande au joueur s'il veut continuer vers la prochaine vague."""
    while True:
        print("\nQue souhaitez-vous faire ?")
        choix = input("1. Continuer vers la prochaine vague | 2. Partir avec la victoire actuelle : ")

        if choix == '1':
            print("\nPréparation pour la prochaine vague.")
            return True
        elif choix == '2':
            return False
        else:
            print("Veuillez entrer '1' ou '2'.")
