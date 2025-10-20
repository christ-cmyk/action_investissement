"""
Algorithme optimisé pour sélectionner les actions les plus rentables
en maximisant le bénéfice total sous contrainte de budget.

Utilise une approche gloutonne basée sur le ratio profit/coût.
"""

def optimized_selection(actions, max_budget):
    """
    Sélectionne les actions pour maximiser le profit avec un budget donné.
    
    Args:
        actions: Liste des dictionnaires contenant 'id', 'cost' et 'profit_pct'
        max_budget: Budget maximum en FCFA
        
    Returns:
        tuple: (actions sélectionnées, coût total, profit total)
    """
    if not actions:
        return [], 0, 0
    
    # Étape 1 : Prétraitement et calcul des ratios
    processed_actions = []
    for action in actions:
        try:
            cost = float(action['cost'])
            profit_pct = float(action['profit_pct'])
            
            # On ne garde que les actions avec coût et profit positifs
            if cost > 0 and profit_pct > 0:
                profit = cost * (profit_pct / 100)
                ratio = profit / cost  # Ratio profit/coût pour le tri
                
                processed_actions.append({
                    'id': action.get('id', 'unknown'),
                    'cost': cost,
                    'profit_pct': profit_pct,
                    'profit': profit,
                    'ratio': ratio
                })
        except (ValueError, KeyError) as e:
            print(f"Avertissement: action ignorée - {e}")
            continue
    
    if not processed_actions:
        return [], 0, 0
    
    # Étape 2 : Tri par ratio décroissant
    processed_actions.sort(key=lambda x: x['ratio'], reverse=True)
    
    # Étape 3 : Sélection gloutonne
    selected_actions = []
    total_cost = 0
    total_profit = 0
    
    for action in processed_actions:
        if total_cost + action['cost'] <= max_budget:
            selected_actions.append({
                'id': action['id'],
                'cost': action['cost'],
                'profit_pct': action['profit_pct'],
                'profit': action['profit']
            })
            total_cost += action['cost']
            total_profit += action['profit']
    
    return selected_actions, total_cost, total_profit
