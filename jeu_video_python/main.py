import sys
from utils import get_all_player_characters, display_ranking
from game import start_combat
from models import Character


def select_username() -> str:
    """Demande et retourne le nom d'utilisateur."""
    while True:
        username = input("Veuillez entrer votre nom d'utilisateur (minimum 3 caractères) : ").strip()
        if len(username) >= 3:
            return username
        else:
            print("Le nom d'utilisateur doit contenir au moins 3 caractères.")


def display_available_characters(all_characters: list[Character], available_indices: list[int]):
    """Affiche la liste des personnages encore disponibles."""
    print("\nPersonnages disponibles :")
    for index in available_indices:
        char = all_characters[index]
        print(f"[{index + 1}] {char.name:<10} | ATK: {char.attack:<3} | DEF: {char.defense:<3} | PV: {char.max_hp}")


def validate_character_choice(choice_str: str, available_indices: list[int]) -> int:
    """
    Valide le choix de l'utilisateur et retourne l'index choisi.
    Lève ValueError si l'entrée est invalide.
    """
    if not choice_str.strip():
        raise ValueError("Entrée vide")
    
    choice = int(choice_str) - 1
    
    if choice not in available_indices:
        raise ValueError("Choix invalide ou personnage déjà sélectionné")
    
    return choice


def create_character_copy(character: Character) -> Character:
    """Crée une copie d'un personnage avec toutes ses propriétés."""
    return Character(
        character.name,
        character.attack,
        character.defense,
        character.max_hp,
        attacks=character.attacks
    )


def select_single_character(all_characters: list[Character], available_indices: list[int], position: int) -> Character:
    """
    Gère la sélection d'un seul personnage.
    Retourne le personnage sélectionné et met à jour la liste des indices disponibles.
    """
    print(f"\n--- Sélection du Personnage #{position} ---")
    display_available_characters(all_characters, available_indices)
    
    while True:
        try:
            choice_str = input(f"Choisissez un personnage [{position}/3] : ")
            choice = validate_character_choice(choice_str, available_indices)
            
            selected_char_data = all_characters[choice]
            selected_char = create_character_copy(selected_char_data)
            
            available_indices.remove(choice)
            
            print(f"{selected_char.name} a rejoint l'équipe !")
            return selected_char
            
        except ValueError as e:
            if "invalid literal" in str(e):
                print("Entrée invalide. Veuillez saisir un nombre.")
            else:
                print(f"Erreur : {e}. Veuillez réessayer.")
        
        except IndexError:
            print("Choix hors limites. Veuillez saisir un nombre dans la liste.")


def display_team_summary(team: list[Character]):
    """Affiche le résumé de l'équipe constituée."""
    print("\n" + "="*40)
    print("Équipe Complète :")
    for char in team:
        print(f"-> {char.name} (PV: {char.max_hp}, ATK: {char.attack}, DEF: {char.defense})")
    print("="*40)


def create_team(all_characters: list[Character]) -> list[Character]:
    """
    Gère la sélection des 3 personnages pour l'équipe.
    Chaque personnage ne peut être sélectionné qu'une seule fois.
    """
    team = []
    available_indices = list(range(len(all_characters)))
    
    print("\n" + "="*40)
    print("CRÉATION DE L'ÉQUIPE (Sélectionnez 3 personnages)")
    print("="*40)
    
    for i in range(3):
        selected_char = select_single_character(all_characters, available_indices, i + 1)
        team.append(selected_char)
    
    display_team_summary(team)
    return team


def handle_start_game():
    """Gère le démarrage d'une nouvelle partie."""
    try:
        all_characters = get_all_player_characters()
        
        if not all_characters:
            print("Erreur: Impossible de récupérer les personnages. Base de données vide ?")
            return
        
        username = select_username()
        team = create_team(all_characters)
        
        if team:
            start_combat(username, team)
    
    except Exception as e:
        print(f"Une erreur inattendue est survenue : {e}")


def handle_display_ranking():
    """Gère l'affichage du classement."""
    display_ranking()


def handle_quit():
    """Gère la fermeture du programme."""
    print("Merci d'avoir joué ! Au revoir.")
    sys.exit()


def display_main_menu():
    """Affiche le menu principal."""
    print("\n" + "#"*40)
    print("         BIENVENUE DANS L'ARENA RPG")
    print("#"*40)
    print("[1] Démarrer le jeu (Créer une équipe)")
    print("[2] Afficher le classement")
    print("[3] Quitter")
    print("#"*40)


def process_menu_choice(choice: str):
    """Traite le choix de l'utilisateur dans le menu."""
    if choice == '1':
        handle_start_game()
    elif choice == '2':
        handle_display_ranking()
    elif choice == '3':
        handle_quit()
    else:
        print("Option invalide. Veuillez choisir 1, 2 ou 3.")


def main_menu():
    """Affiche le menu principal et gère les options."""
    while True:
        display_main_menu()
        choice = input("Sélectionnez une option : ")
        process_menu_choice(choice)


if __name__ == "__main__":
    main_menu()