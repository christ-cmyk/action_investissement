# Optimisation de Portefeuille d'Actions

Ce projet implémente différentes stratégies pour optimiser un portefeuille d'investissement avec un budget limité de 500 000 F CFA. L'objectif est de maximiser le profit après 2 ans en sélectionnant judicieusement les actions à acheter.

## Structure du Projet

```
action_investissement/
├── data/                   # Dossier contenant les jeux de données d'actions
├── results/                # Dossier contenant les résultats des exécutions
├── src/                    # Code source du projet
│   ├── brute_force.py      # Implémentation de la solution par force brute
│   ├── optimisation.py     # Implémentation de la solution optimisée
│   ├── utils.py            # Fonctions utilitaires (lecture/écriture de fichiers)
│   └── main.py             # Point d'entrée principal
├── requirements.txt        # Dépendances du projet
└── README.md               # Ce fichier
```

## Installation

1. Assurez-vous d'avoir Python 3.8 ou supérieur installé
2. Clonez ce dépôt
3. Installez les dépendances :

```bash
pip install -r requirements.txt
```

## Utilisation

### Générer un jeu de données de test

```bash
python -c "from src.utils import generate_test_data; generate_test_data(n_actions=20, output_file='data/test_dataset.csv')"
```

### Exécuter l'optimisation

Pour exécuter les deux algorithmes (force brute et optimisé) :

```bash
python src/main.py data/test_dataset.csv
```

Options disponibles :
- `--budget` : Définir un budget personnalisé (par défaut: 500000)
- `--algo` : Choisir l'algorithme à exécuter (`brute`, `optimized` ou `all` par défaut)
- `--output-dir` : Définir le répertoire de sortie (par défaut: `results`)

Exemple avec options :

```bash
python src/main.py data/test_dataset.csv --budget 300000 --algo optimized --output-dir my_results
```

### Format des fichiers d'entrée

Le fichier d'entrée doit être un CSV sans en-tête avec les colonnes suivantes :
1. Identifiant de l'action (chaîne)
2. Coût de l'action en F CFA (nombre)
3. Pourcentage de profit après 2 ans (nombre)

Exemple :
```
Share-PLLK,1994,0.12
Share-ECAQ,3166,0.08
Share-IXCI,2632,0.15
```

## Algorithmes Implémentés

### 1. Force Brute (`brute_force.py`)
- Explore toutes les combinaisons possibles d'actions
- Garantit de trouver la solution optimale
- Complexité exponentielle : O(2^n) où n est le nombre d'actions
- Ne convient que pour un petit nombre d'actions (n < 25)

### 2. Algorithme Optimisé (`optimisation.py`)
- Utilise une approche gloutonne avec un filtre de profit minimum
- Beaucoup plus rapide que la force brute
- Ne garantit pas toujours la solution optimale mais donne de bons résultats en pratique
- Complexité : O(n log n) pour le tri + O(n) pour la sélection

## Résultats

Les résultats sont sauvegardés dans le dossier `results/` (ou le dossier spécifié) avec les formats suivants :
- `brute_<dataset>_result.txt` : Résultats de l'algorithme de force brute
- `optimized_<dataset>_result.txt` : Résultats de l'algorithme optimisé

Chaque fichier contient :
- La liste des actions sélectionnées avec leur coût et profit
- Le coût total de l'investissement
- Le profit total après 2 ans
- Le nombre d'actions sélectionnées

## Auteur

[Votre nom]

## Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.