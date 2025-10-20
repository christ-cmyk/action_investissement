"""
Programme principal pour l'optimisation de portefeuille d'actions.
Permet de comparer différentes méthodes d'optimisation.
"""
import sys
import time
import argparse
from pathlib import Path
from typing import Tuple, List, Dict, Any

def parse_arguments():
    """Parse les arguments en ligne de commande."""
    parser = argparse.ArgumentParser(description='Optimisation de portefeuille d\'actions')
    parser.add_argument('input_file', type=str, help='Chemin vers le fichier CSV des actions')
    parser.add_argument('--budget', type=float, default=500000.0,
                      help='Budget maximum en F CFA (défaut: 500000)')
    parser.add_argument('--algo', type=str, choices=['all', 'brute', 'optimized'], default='all',
                      help='Algorithme à utiliser: all, brute (force brute), ou optimized (défaut: all)')
    parser.add_argument('--output-dir', type=str, default='results',
                      help='Répertoire de sortie pour les résultats (défaut: results/)')
    return parser.parse_args()

def run_algorithm(algorithm_name: str, actions: List[Dict[str, Any]], max_budget: float) -> Tuple[float, float, float]:
    """
    Exécute l'algorithme spécifié et mesure son temps d'exécution.
    
    Args:
        algorithm_name: Nom de l'algorithme ('brute' ou 'optimized')
        actions: Liste des actions disponibles
        max_budget: Budget maximum
        
    Returns:
        Tuple (temps d'exécution, coût total, profit total)
    """
    start_time = time.time()
    
    if algorithm_name == 'brute':
        from brute_force import brute_force_selection as algorithm
    else:  # optimized
        from optimisation import optimized_selection as algorithm
    
    selected_actions, total_cost, total_profit = algorithm(actions, max_budget)
    execution_time = time.time() - start_time
    
    return execution_time, total_cost, total_profit, selected_actions

def main():
    """Fonction principale du programme."""
    args = parse_arguments()
    
    # Créer le répertoire de sortie si nécessaire
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    
    # Lire les actions depuis le fichier
    try:
        from utils import read_actions_csv, save_results
        actions = read_actions_csv(args.input_file)
        print(f"{len(actions)} actions chargées depuis {args.input_file}")
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier: {e}")
        return
    
    # Déterminer quels algorithmes exécuter
    algorithms = []
    if args.algo in ['all', 'brute']:
        algorithms.append('brute')
    if args.algo in ['all', 'optimized']:
        algorithms.append('optimized')
    
    # Exécuter les algorithmes demandés
    results = {}
    for algo in algorithms:
        print(f"\nExécution de l'algorithme: {algo}...")
        try:
            time_taken, cost, profit, selected_actions = run_algorithm(algo, actions, args.budget)
            results[algo] = {
                'time': time_taken,
                'cost': cost,
                'profit': profit,
                'actions': selected_actions
            }
            print(f"  Temps d'exécution: {time_taken:.4f} secondes")
            print(f"  Coût total: {cost:,.2f} F CFA")
            print(f"  Profit total: {profit:,.2f} F CFA")
            
            # Sauvegarder les résultats
            output_file = f"{args.output_dir}/{algo}_{Path(args.input_file).stem}_result.txt"
            save_results(selected_actions, cost, profit, output_file)
            print(f"  Résultats sauvegardés dans {output_file}")
            
        except Exception as e:
            print(f"  Erreur lors de l'exécution de l'algorithme {algo}: {e}")
    
    # Afficher une comparaison si plusieurs algorithmes ont été exécutés
    if len(results) > 1:
        print("\n=== Comparaison des algorithmes ===")
        print(f"{'Algorithme':<12} {'Temps (s)':<12} {'Coût (FCFA)':<15} {'Profit (FCFA)':<15} {'Nb actions':<12}")
        print("-" * 60)
        for algo, res in results.items():
            print(f"{algo:<12} {res['time']:<12.4f} {res['cost']:<15,.2f} {res['profit']:<15,.2f} {len(res['actions']):<12}")

if __name__ == "__main__":
    main()