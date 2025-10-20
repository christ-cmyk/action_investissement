import pandas as pd

def clean_value(value):
    """Nettoie une valeur en supprimant les symboles et en convertissant en float."""
    if isinstance(value, str):
        # Supprime les espaces, symboles % et convertit les virgules en points
        value = value.strip().replace('%', '').replace(',', '.')
        # Si la chaîne est vide après nettoyage, retourne 0
        if not value:
            return 0.0
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

def read_actions_csv(file_path):
    """
    Lit un fichier CSV contenant les données des actions.
    Supporte plusieurs formats :
    - Format 1: id;cost;profit_pct
    - Format 2: id,cost,profit_pct
    
    Args:
        file_path (str): Chemin vers le fichier CSV
        
    Returns:
        list: Liste de dictionnaires représentant les actions
    """
    try:
        # Essaye d'abord avec le point-virgule comme séparateur
        df = pd.read_csv(file_path, sep=';', header=None, 
                        names=['id', 'cost', 'profit_pct'],
                        decimal=',',
                        encoding='utf-8')
        
        # Si le fichier n'a qu'une seule colonne, essayer avec la virgule
        if len(df.columns) == 1:
            df = pd.read_csv(file_path, sep=',', header=None,
                           names=['id', 'cost', 'profit_pct'],
                           decimal='.',
                           encoding='utf-8')
        
        # Nettoyage des données
        df['id'] = df['id'].astype(str).str.strip()
        df['cost'] = df['cost'].apply(clean_value)
        df['profit_pct'] = df['profit_pct'].apply(clean_value)
        
        # Supprimer les lignes où le coût ou le profit est négatif ou nul
        df = df[(df['cost'] > 0) & (df['profit_pct'] > 0)]
        
        return df.to_dict('records')
        
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {file_path}: {str(e)}")
        return []

def save_results(selected_actions, total_cost, total_profit, output_file):
    """
    Sauvegarde les résultats dans un fichier texte.
    
    Args:
        selected_actions (list): Liste des actions sélectionnées
        total_cost (float): Coût total de l'investissement
        total_profit (float): Profit total attendu
        output_file (str): Chemin du fichier de sortie
    """
    with open(output_file, 'w') as f:
        if not selected_actions:
            f.write("Aucune action sélectionnée dans la limite du budget.\n")
            return
            
        f.write("=== Actions sélectionnées ===\n")
        for action in selected_actions:
            f.write(f"{action['id']} - Coût: {action['cost']:.2f}€ - Profit: {action['profit_pct']:.2f}%\n")
        
        f.write("\n=== Résumé ===\n")
        f.write(f"Coût total: {total_cost:,.2f}€\n")
        f.write(f"Profit total après 2 ans: {total_profit:,.2f}€\n")
        f.write(f"Nombre d'actions sélectionnées: {len(selected_actions)}\n")

def generate_test_data(n_actions=20, max_cost=1000, max_profit=20, output_file='test_dataset.csv'):
    """
    Génère un jeu de données de test aléatoire.
    
    Args:
        n_actions (int): Nombre d'actions à générer
        max_cost (int): Coût maximum d'une action
        max_profit (int): Profit maximum en pourcentage
        output_file (str): Fichier de sortie
    """
    import random
    
    actions = []
    for i in range(n_actions):
        actions.append({
            'id': f'Share-{random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")}{random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")}{random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")}',
            'cost': round(random.uniform(10, max_cost), 2),
            'profit_pct': round(random.uniform(0.1, max_profit), 2)
        })
    
    df = pd.DataFrame(actions)
    df.to_csv(output_file, index=False, header=False)
    print(f"Fichier de test généré: {output_file}")