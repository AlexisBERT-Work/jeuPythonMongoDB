# game.py

import random
from models import Character, Attack
from utils import get_random_monster, save_score, display_ranking


def calculate_damage(attacker: Character, defender: Character, attack_choice: Attack = None) -> int:
    """
    Calcule les dégâts infligés en tenant compte de l'ATK de l'attaquant,
    de la DEF du défenseur et du modificateur de l'attaque choisie.
    Dégâts = (ATK * Modificateur) - Défense (minimum 1 dégât)
    """
    modifier = attack_choice.modifier if attack_choice else 1.0
    raw_damage = attacker.attack * modifier
    damage = int(raw_damage) - defender.defense
    return max(1, damage)


def display_attack_options(character: Character):
    """Affiche les options d'attaque disponibles pour un personnage."""
    print("Options d'Attaque :")
    for i, atk in enumerate(character.attacks):
        print(f"[{i + 1}] {atk.name:<20} (Modificateur ATK: x{atk.modifier:.1f})")


def get_player_attack_choice(character: Character) -> Attack:
    """Demande au joueur de choisir une attaque et retourne l'attaque sélectionnée."""
    selected_attack = None
    
    while selected_attack is None:
        try:
            choice = int(input(f"Choisissez une action (1-{len(character.attacks)}) pour {character.name} : ")) - 1
            
            if 0 <= choice < len(character.attacks):
                selected_attack = character.attacks[choice]
            else:
                print("Choix hors limites. Veuillez saisir un numéro valide.")
        except ValueError:
            print("Entrée invalide. Veuillez saisir un nombre.")
    
    return selected_attack


def execute_player_attack(character: Character, monster: Character, attack: Attack) -> int:
    """Exécute l'attaque du personnage sur le monstre et retourne les dégâts infligés."""
    damage = calculate_damage(character, monster, attack)
    monster.current_hp -= damage
    
    print(f"  {character.name} utilise {attack.name} ! Le monstre {monster.name} subit {damage} dégâts.")
    
    return damage


def is_monster_defeated(monster: Character) -> bool:
    """Vérifie si le monstre est vaincu et met à jour ses PV."""
    if monster.current_hp <= 0:
        monster.current_hp = 0
        return True
    return False


def handle_player_turn(team: list[Character], monster: Character) -> bool:
    """
    Gère le tour où le joueur choisit une attaque pour chaque personnage
    encore vivant. Retourne True si le monstre est vaincu.
    """
    print("\n--- Phase d'Action de l'Équipe ---")
    
    for char in team:
        if char.current_hp <= 0:
            continue
        
        print(f"\nC'est le tour de {char.name} (PV: {char.current_hp}/{char.max_hp}) :")
        
        display_attack_options(char)
        selected_attack = get_player_attack_choice(char)
        execute_player_attack(char, monster, selected_attack)
        
        if is_monster_defeated(monster):
            return True
    
    return False


def get_living_team_members(team: list[Character]) -> list[Character]:
    """Retourne la liste des personnages encore en vie dans l'équipe."""
    return [char for char in team if char.current_hp > 0]


def select_random_target(team: list[Character]) -> Character:
    """Sélectionne aléatoirement un personnage vivant dans l'équipe."""
    living_members = get_living_team_members(team)
    return random.choice(living_members) if living_members else None


def execute_monster_attack(monster: Character, target: Character):
    """Exécute l'attaque du monstre sur la cible."""
    monster_attack = monster.attacks[0] if monster.attacks else None
    damage = calculate_damage(monster, target, monster_attack)
    target.current_hp -= damage
    
    print(f"  {monster.name} attaque {target.name} et lui inflige {damage} dégâts.")


def display_target_status(target: Character):
    """Affiche l'état du personnage après avoir subi une attaque."""
    if target.current_hp <= 0:
        target.current_hp = 0
        print(f"  {target.name} a été vaincu !")
    else:
        print(f"  {target.name} : PV restants {target.current_hp}/{target.max_hp}")


def handle_monster_attack(team: list[Character], monster: Character):
    """Gère l'attaque du monstre sur un personnage aléatoire de l'équipe."""
    print("\n--- Phase d'Attaque du Monstre ---")
    
    target = select_random_target(team)
    
    if not target:
        return
    
    execute_monster_attack(monster, target)
    display_target_status(target)


def is_team_defeated(team: list[Character]) -> bool:
    """Vérifie si tous les personnages de l'équipe sont vaincus."""
    return all(char.current_hp <= 0 for char in team)


def display_wave_header(wave_number: int, monster: Character):
    """Affiche l'en-tête d'information pour une nouvelle vague."""
    print("\n" + "="*50)
    print(f"   VAGUE {wave_number} : Un {monster.name} apparaît !")
    print(f"   [Monstre] ATK: {monster.attack} | DEF: {monster.defense} | PV: {monster.current_hp}")
    print("="*50)


def display_game_start(username: str):
    """Affiche le message de début de partie."""
    print("\n" + "#"*40)
    print(f"  {username} entre dans l'Arène avec son équipe !")
    print("#"*40)


def display_wave_victory(monster_name: str):
    """Affiche le message de victoire d'une vague."""
    print(f"\nVICTOIRE ! Le {monster_name} est vaincu.")


def display_game_over(final_score: int):
    """Affiche le message de fin de partie."""
    print("\n" + "="*50)
    print("DÉFAITE ! L'équipe est vaincue.")
    print(f"   Votre score final est de : {final_score} vagues.")
    print("="*50)


def process_wave_combat(team: list[Character], monster: Character) -> bool:
    """
    Gère le combat tour par tour pour une vague.
    Retourne True si l'équipe est vaincue, False sinon.
    """
    while monster.current_hp > 0 and not is_team_defeated(team):
        monster_defeated = handle_player_turn(team, monster)
        
        if monster_defeated:
            display_wave_victory(monster.name)
            return False
        
        handle_monster_attack(team, monster)
        
        if is_team_defeated(team):
            return True
    
    return False


def start_combat(username: str, team: list[Character]):
    """
    Lance la boucle de combat infinie jusqu'à la défaite.
    """
    waves_survived = 0
    is_game_over = False
    
    display_game_start(username)
    
    while not is_game_over:
        waves_survived += 1
        
        monster = get_random_monster()
        if not monster:
            print("Erreur : Impossible de charger un monstre.")
            break
        
        display_wave_header(waves_survived, monster)
        
        is_game_over = process_wave_combat(team, monster)
    
    final_score = waves_survived - 1
    display_game_over(final_score)
    
    save_score(username, final_score)
    display_ranking()