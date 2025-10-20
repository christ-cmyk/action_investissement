# Optimisation de Portefeuille d'Actions

Ce projet implémente différentes stratégies pour optimiser un portefeuille d'investissement avec un budget limité de 500 000 F CFA. L'objectif est de maximiser le profit après 2 ans en sélectionnant judicieusement les actions à acheter.

## Structure du Projet

```
action_investissement/
├── data/                   # Dossier contenant les jeux de données d'actions
├── results/                # Dossier contenant les résultats des exécutions
├── src/                    # Code source du projet
│   ├── __init__.py         # Fichier d'initialisation du package
│   ├── brute_force.py      # Implémentation de la solution par force brute
│   ├── optimisation.py     # Implémentation de la solution optimisée
│   ├── menu.py             # Interface utilisateur en mode console
│   ├── utils.py            # Fonctions utilitaires (lecture/écriture de fichiers)
│   └── main.py             # Point d'entrée principal
├── requirements.txt        # Dépendances du projet
└── README.md               # Ce fichier
```

## Installation

1. Assurez-vous d'avoir Python 3.8 ou supérieur installé
2. Clonez ce dépôt
3. Créez et activez un environnement virtuel (recommandé) :
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Sur Windows
   source venv/bin/activate   # Sur macOS/Linux
   ```
4. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

### Mode Ligne de Commande

Pour exécuter avec des paramètres spécifiques :

```bash
python src/main.py data/test_dataset.csv
```

Options disponibles :
- `--budget` : Définir un budget personnalisé (par défaut: 500000)
- `--algo` : Choisir l'algorithme à exécuter (`brute`, `optimized` ou `all` par défaut)
- `--output-dir` : Définir le répertoire de sortie (par défaut: `results`)

### Mode Interactif (Recommandé)

Lancez simplement :
```bash
python src/main.py
```

Le menu interactif vous permettra de :
1. Choisir entre l'algorithme de force brute, optimisé ou les deux
2. Sélectionner le fichier de données à analyser
3. Voir les résultats détaillés
4. Changer de fichier de données
5. Quitter l'application

### Format des fichiers d'entrée

Le fichier d'entrée doit être un CSV avec les colonnes suivantes :
- Séparateur : point-virgule (;) ou virgule (,)
- Pas d'en-tête requis
- Colonnes :
  1. Identifiant de l'action (chaîne)
  2. Coût de l'action en F CFA (nombre)
  3. Pourcentage de profit après 2 ans (nombre ou pourcentage avec %)

Exemple :
```
Action-1;20000;5%
Action-2;30000;10
Action-3;50000;15.5
```

## Algorithmes Implémentés

### 1. Force Brute (`brute_force.py`)
- Explore toutes les combinaisons possibles d'actions
- Garantit de trouver la solution optimale
- Complexité exponentielle : O(2^n)
- Recommandé pour n < 20 actions

### 2. Algorithme Optimisé (`optimisation.py`)
- Approche gloutonne avec tri par ratio profit/coût
- Solution quasi-optimale en temps raisonnable
- Complexité : O(n log n)
- Fonctionne bien même avec un grand nombre d'actions

## Résultats

Les résultats sont sauvegardés dans le dossier `results/` avec les formats suivants :
- `brute_<dataset>_result.txt` : Résultats de la force brute
- `optimized_<dataset>_result.txt` : Résultats de l'algorithme optimisé

Chaque rapport inclut :
- Liste des actions sélectionnées avec coût et profit
- Coût total et profit total
- Temps d'exécution
- Nombre d'actions sélectionnées

## Auteur

Christophe M.

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
