class Combattant:

    def __init__(self, data):
        self.id = data.get("_id")
        self.nom = data.get("Nom", "Inconnu")
        stats = data.get("Statistiques", {})
        self.attaque = stats.get("Attaque", 10)
        self.defense = stats.get("Défense", 10)
        self.vie_max = stats.get("Vie", 100)
        self.vie_actuelle = self.vie_max

    def attaquer(self, cible):
        degats_bruts = self.attaque
        degats_reels = cible.recevoir_degats(degats_bruts)
        return degats_reels

    def recevoir_degats(self, degats_bruts):
        degats_reels = max(0, degats_bruts - self.defense)
        self.vie_actuelle -= degats_reels
        return degats_reels
    
    def est_vivant(self):
        return self.vie_actuelle > 0
    
    def __str__(self):
        return f"{self.nom} - {self.attaque} ATK - {self.defense} DEF - {self.vie_actuelle}/{self.vie_max} PV"
    

class Personnage(Combattant):
    
    def __init__(self, data):
        super().__init__(data) 
        self.description = data.get("Description", "")
        self.specialite = data.get("Spécialité", "")
    
    def __str__(self):
        base_str = super().__str__()
        return f"{base_str} - Spécialité: {self.specialite}"
    

class Monstre(Combattant):

    def __init__(self, data):
        super().__init__(data)
        self.role = data.get("Rôle", "")
        self.faction = data.get("Faction", "")

    def __str__(self):
        base_str = super().__str__()
        return f"{base_str} ({self.role}) - Faction: {self.faction}"