"""
Implémentation de la solution par force brute pour le problème du sac à dos d'investissement.
Cette solution explore toutes les combinaisons possibles d'actions pour trouver la meilleure solution.
"""
import itertools

def brute_force_selection(actions, max_budget=500000):
    """
    Trouve la combinaison optimale d'actions en utilisant la force brute.
    
    Args:
        actions (list): Liste des actions disponibles
        max_budget (float): Budget maximum en F CFA (500 000 par défaut)
        
    Returns:
        tuple: (liste des actions sélectionnées, coût total, profit total)
    """
    best_combination = []
    best_profit = 0
    best_cost = 0
    
    # Générer toutes les combinaisons possibles de différentes tailles
    for r in range(1, len(actions) + 1):
        for combination in itertools.combinations(actions, r):
            total_cost = sum(action['cost'] for action in combination)
            
            # Vérifier si la combinaison est dans le budget
            if total_cost <= max_budget:
                total_profit = sum(action['cost'] * (action['profit_pct'] / 100) for action in combination)
                
                # Mettre à jour la meilleure solution si nécessaire
                if total_profit > best_profit:
                    best_profit = total_profit
                    best_combination = list(combination)
                    best_cost = total_cost
    
    return best_combination, best_cost, best_profit

def main():
    """Fonction principale pour tester l'algorithme de force brute."""
    import sys
    from utils import read_actions_csv, save_results
    
    if len(sys.argv) != 2:
        print("Usage: python brute_force.py <fichier_actions.csv>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = f"results/brute_force_{input_file.split('/')[-1].replace('.csv', '')}_result.txt"
    
    try:
        # Lire les actions depuis le fichier
        actions = read_actions_csv(input_file)
        
        # Exécuter l'algorithme
        print(f"Recherche de la meilleure combinaison parmi {len(actions)} actions...")
        selected_actions, total_cost, total_profit = brute_force_selection(actions)
        
        # Sauvegarder les résultats
        save_results(selected_actions, total_cost, total_profit, output_file)
        print(f"Résultats sauvegardés dans {output_file}")
        
    except FileNotFoundError:
        print(f"Erreur: Le fichier {input_file} n'a pas été trouvé.")
        sys.exit(1)
    except Exception as e:
        print(f"Une erreur s'est produite: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()