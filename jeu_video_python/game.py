import time
from typing import List
from models import Personnage 
from utils import equipe_est_vivante, reset_vies_equipe, realiser_vague, monstre_aleatoire, afficher_monstre 


def lancer_combat(db, equipe: List[Personnage]) -> bool:
    reset_vies_equipe(equipe)
    print("\n--- DÉBUT DE LA BATAILLE ---")
    
    vagues_vaincues = 0

    while equipe_est_vivante(equipe):
        monstre = monstre_aleatoire(db)
        if monstre is None:
            print("Impossible de trouver un monstre aléatoire. Fin du combat.")
            break
            
        vagues_vaincues += 1
        print(f"       VAGUE {vagues_vaincues} : ATTENTION !       ")
        afficher_monstre(monstre)
        time.sleep(3)
        while equipe_est_vivante(equipe) and monstre.est_vivant():
            print("\n--------- Tour de Combat ---------")       
            False , monstre == realiser_vague(equipe, monstre)
            time.sleep(2)

        if not equipe_est_vivante(equipe):
            print("\n*** DÉFAITE : Votre équipe a été anéantie. ***")
            return False
            
        if not monstre.est_vivant():
            print(f"Vague {vagues_vaincues} vaincue !")

        if equipe_est_vivante(equipe):
            while True:
                print("\nQue souhaitez-vous faire ?")
                choix = input("1. Continuer vers la prochaine vague | 2. Partir avec la victoire actuelle : ")
                
                if choix == '1':
                    print("\nPréparation pour la prochaine vague.")
                    break 
                elif choix == '2':
                    print(f"\nVous vous retirez. *** FIN DU COMBAT : {vagues_vaincues} vagues vaincues ! ***")
                    return True
                else:
                    print("Veuillez entrer '1' ou '2'.")
    print(f"\n*** FIN DU COMBAT : {vagues_vaincues} vagues vaincues ! ***")
    return True