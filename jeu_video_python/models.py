from datetime import datetime

class Attack:
    """Modèle simple pour une attaque."""
    def __init__(self, name: str, base_damage: int, modifier: float = 1.0):
        self.name = name
        self.base_damage = base_damage
        self.modifier = modifier 

    def to_dict(self):
        """Retourne les attributs pour le stockage (optionnel) ou la création."""
        return {
            "name": self.name,
            "base_damage": self.base_damage,
            "modifier": self.modifier
        }

class Character:
    """Modèle pour les personnages jouables et les monstres."""
    def __init__(self, name: str, attack: int, defense: int, hp: int, 
                 is_player_char: bool = True, attacks: list = None):
        self.name = name
        self.attack = attack 
        self.defense = defense
        self.max_hp = hp
        self.current_hp = hp
        self.is_player_char = is_player_char
        
        # S'assure que 'attacks' contient des objets Attack, même s'ils viennent d'un dict MongoDB
        self.attacks = []
        if attacks is not None:
            for atk_data in attacks:
                if isinstance(atk_data, Attack):
                    self.attacks.append(atk_data)
                elif isinstance(atk_data, dict):
                    # Crée un objet Attack à partir du dictionnaire MongoDB
                    self.attacks.append(Attack(
                        name=atk_data.get("name"),
                        base_damage=atk_data.get("base_damage"),
                        modifier=atk_data.get("modifier")
                    ))


    def to_dict(self):
        """Retourne les attributs pour l'insertion dans MongoDB."""
        return {
            "name": self.name,
            "attack": self.attack,
            "defense": self.defense,
            "hp": self.max_hp,
            "type": "Player" if self.is_player_char else "Monster",
            "attacks": [atk.to_dict() for atk in self.attacks if isinstance(atk, Attack)]
        }

    def __str__(self):
        """Représentation textuelle de l'entité."""
        return f"{self.name} - ATK: {self.attack} - DEF: {self.defense} - PV: {self.current_hp}/{self.max_hp}"

class Score:
    """Modèle pour l'enregistrement des scores."""
    def __init__(self, username: str, waves_survived: int):
        self.username = username
        self.waves_survived = waves_survived

    def to_dict(self):
        """Retourne les attributs pour l'insertion dans MongoDB."""
        return {
            "username": self.username,
            "score": self.waves_survived,
            "timestamp": datetime.now()
        }