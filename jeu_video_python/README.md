# RPG Warhammer — MongoDB Edition

RPG Warhammer est un jeu de combat tactique de commande développé en Python. Le joueur constitue une équipe de personnages, affronte des vagues successives de monstres et peut enregistrer son score dans une base MongoDB.

---

## Prérequis

Avant d'utiliser le jeu, assurez-vous d'avoir installé :

* Python
* MongoDB

---

## Installation

1. Clonez ou téléchargez le projet.
2. Installez les dépendances nécessaires :

   ```bash
   pip install pymongo
   ```
3. Configurez la base de données :

    ```bash
   python db_init.py
   ```
---

## Lancement du jeu

Pour démarrer la partie :

```bash
python main.py
```

---

## Fonctionnement du jeu

### 1. Menu principal

Au lancement, le jeu propose trois options :

1. Lancer un nouveau combat
2. Afficher le classement (Top 3)
3. Quitter

### 2. Création de l'équipe

* Le joueur saisit un pseudo.
* Il sélectionne ensuite trois personnages stockés en base pour constituer son équipe.
* Le choix des personnages influence directement les chances de survie.

### 3. Système de combat (mode survie)

* Le jeu fonctionne sous forme de vagues successives.
* À chaque nouvelle vague, un monstre aléatoire est généré.
* Les combats sont automatiques et se déroulent tour par tour.
* Les points de vie des personnages sont entièrement restaurés entre les vagues.

### 4. Mécanique "Quitte ou Double"

Après chaque victoire, le joueur doit choisir :

**Continuer**

* Le joueur affronte la vague suivante avec l'état actuel de son équipe.
* Si l'équipe est vaincue, aucun score n'est sauvegardé.

**Se retirer**

* Le joueur met fin immédiatement à la partie.
* Le nombre de vagues franchies est enregistré dans la collection `scores`.

Important : pour enregistrer un score, le joueur doit explicitement choisir de se retirer. Une défaite entraîne la perte du score.

---

## Structure du projet

```
main.py       - Point d'entrée du jeu et gestion du menu
game.py       - Logique des combats, gestion des vagues et déroulement des tours
utils.py      - Fonctions utilitaires (connexion MongoDB, affichage, calculs, etc.)
models.py     - Classes métiers (Personnage, Monstre, etc.)
```

---

## Technologies utilisées

* Python
* MongoDB (NoSQL)
* PyMongo