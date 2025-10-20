import os
import sys
from typing import List, Dict, Any
from pathlib import Path
import time

# Ajouter le répertoire parent au chemin Python
sys.path.append(str(Path(__file__).parent.parent))

from src.utils import read_actions_csv, save_results
from src.brute_force import brute_force_selection
from src.optimisation import optimized_selection

def clear_screen():
    """Efface l'écran de la console."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu() -> int:
    """Affiche le menu principal et retourne le choix de l'utilisateur."""
    clear_screen()
    print("""
    ╔══════════════════════════════════╗
    ║   OPTIMISATEUR DE PORTEFEUILLE   ║
    ╠══════════════════════════════════╣
    ║ 1. Lancer l'algorithme de force brute ║
    ║ 2. Lancer l'algorithme optimisé      ║
    ║ 3. Lancer les deux algorithmes        ║
    ║ 4. Changer le fichier de données      ║
    ║ 5. Quitter                            ║
    ╚══════════════════════════════════╝
    """)
    
    while True:
        try:
            choice = int(input("Votre choix (1-5) : "))
            if 1 <= choice <= 5:
                return choice
            print("Veuillez entrer un nombre entre 1 et 5.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

def select_data_file() -> str:
    """Permet à l'utilisateur de sélectionner un fichier CSV."""
    data_dir = Path("data")
    csv_files = list(data_dir.glob("*.csv"))
    
    if not csv_files:
        print("Aucun fichier CSV trouvé dans le dossier 'data/'")
        return None
    
    print("\nFichiers disponibles :")
    for i, file in enumerate(csv_files, 1):
        print(f"{i}. {file.name}")
    
    while True:
        try:
            choice = int(input(f"\nChoisissez un fichier (1-{len(csv_files)}) : "))
            if 1 <= choice <= len(csv_files):
                return str(csv_files[choice - 1])
            print(f"Veuillez entrer un nombre entre 1 et {len(csv_files)}")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

def run_algorithm(algorithm_name: str, actions: List[Dict[str, Any]], max_budget: float) -> tuple:
    """Exécute l'algorithme spécifié et retourne les résultats."""
    start_time = time.time()
    
    if algorithm_name == 'brute':
        selected_actions, total_cost, total_profit = brute_force_selection(actions, max_budget)
    else:  # optimized
        selected_actions, total_cost, total_profit = optimized_selection(actions, max_budget)
    
    execution_time = time.time() - start_time
    return selected_actions, total_cost, total_profit, execution_time

def display_results(algorithm_name: str, selected_actions: list, 
                   total_cost: float, total_profit: float, 
                   execution_time: float, output_dir: str = "results"):
    """Affiche et sauvegarde les résultats."""
    print(f"\n{'='*50}")
    print(f"Résultats de l'algorithme: {algorithm_name}")
    print(f"Temps d'exécution: {execution_time:.4f} secondes")
    print(f"Coût total: {total_cost:,.2f} F CFA")
    print(f"Profit total: {total_profit:,.2f} F CFA")
    print(f"Nombre d'actions sélectionnées: {len(selected_actions)}")
    print("="*50)
    
    # Sauvegarder les résultats
    output_file = Path(output_dir) / f"{algorithm_name}_{Path(selected_actions[0]['id']).stem}_result.txt"
    save_results(selected_actions, total_cost, total_profit, str(output_file))
    print(f"Résultats sauvegardés dans {output_file}")

def main_menu():
    """Boucle principale du menu."""
    current_file = None
    max_budget = 500000  # Budget par défaut
    
    while True:
        if not current_file:
            current_file = select_data_file()
            if not current_file:
                print("Aucun fichier sélectionné. Le programme va se terminer.")
                return
        
        try:
            actions = read_actions_csv(current_file)
            print(f"\nFichier actuel: {Path(current_file).name}")
            print(f"Nombre d'actions chargées: {len(actions)}")
            
            choice = display_menu()
            
            if choice == 1:  # Force brute
                selected, cost, profit, time_taken = run_algorithm('brute', actions, max_budget)
                display_results('brute_force', selected, cost, profit, time_taken)
            
            elif choice == 2:  # Optimisé
                selected, cost, profit, time_taken = run_algorithm('optimized', actions, max_budget)
                display_results('optimized', selected, cost, profit, time_taken)
            
            elif choice == 3:  # Les deux
                # Force brute
                print("\nLancement de l'algorithme de force brute...")
                selected_brute, cost_brute, profit_brute, time_brute = run_algorithm('brute', actions, max_budget)
                display_results('brute_force', selected_brute, cost_brute, profit_brute, time_brute)
                
                # Optimisé
                print("\nLancement de l'algorithme optimisé...")
                selected_opt, cost_opt, profit_opt, time_opt = run_algorithm('optimized', actions, max_budget)
                display_results('optimized', selected_opt, cost_opt, profit_opt, time_opt)
                
                # Comparaison
                print("\n" + "="*50)
                print("COMPARAISON DES ALGORITHMES")
                print(f"Temps brute force: {time_brute:.4f}s")
                print(f"Temps optimisé: {time_opt:.4f}s")
                if time_opt > 0:  # Éviter la division par zéro
                    print(f"Différence: {time_brute - time_opt:.4f}s (x{time_brute/time_opt:.1f} plus rapide)")
                print("="*50)
            
            elif choice == 4:  # Changer de fichier
                current_file = None
                continue
                
            elif choice == 5:  # Quitter
                print("Merci d'avoir utilisé l'optimiseur de portefeuille !")
                break
                
            input("\nAppuyez sur Entrée pour continuer...")
            
        except Exception as e:
            print(f"\nErreur: {str(e)}")
            input("Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    # Créer le dossier de résultats s'il n'existe pas
    Path("results").mkdir(exist_ok=True)
    main_menu()
