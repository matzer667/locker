import json
from collections import defaultdict

def charger_matrice(fichier):
    """Charge une matrice de transition depuis un fichier JSON."""
    with open(fichier, 'r', encoding='utf-8') as f:
        return json.load(f)

def fusionner_matrices(matrice1, matrice2, poids1=0.5, poids2=0.5):
    matrice_fusionnee = defaultdict(dict)
    
  
    tous_caracteres_source = set(matrice1.keys()) | set(matrice2.keys())
    
    for char_source in tous_caracteres_source:
       
        destinations1 = matrice1.get(char_source, {})
        destinations2 = matrice2.get(char_source, {})
        
        toutes_destinations = set(destinations1.keys()) | set(destinations2.keys())
        
        for char_dest in toutes_destinations:
            prob1 = destinations1.get(char_dest, 0.0)
            prob2 = destinations2.get(char_dest, 0.0)
            
           
            prob_fusionnee = (prob1 * poids1) + (prob2 * poids2)
            
            if prob_fusionnee > 0:
                matrice_fusionnee[char_source][char_dest] = prob_fusionnee
    
   
    for char_source in matrice_fusionnee:
        total = sum(matrice_fusionnee[char_source].values())
        if total > 0:
            for char_dest in matrice_fusionnee[char_source]:
                matrice_fusionnee[char_source][char_dest] /= total
    
    return dict(matrice_fusionnee)

def sauvegarder_matrice(matrice, fichier):
    
    with open(fichier, 'w', encoding='utf-8') as f:
        json.dump(matrice, f, ensure_ascii=False, indent=2)

def main():
    print("Fusion des matrices de transition...")
    
    
    print("Chargement de matrice_transition.json...")
    matrice1 = charger_matrice('matrice_transition.json')
    
    print("Chargement de matrice_transition_2.json...")
    matrice2 = charger_matrice('matrice_transition_2.json')
    
    print(f"Matrice 1: {len(matrice1)} caractères sources")
    print(f"Matrice 2: {len(matrice2)} caractères sources")
    
    
    print("Fusion des matrices...")
    matrice_fusionnee = fusionner_matrices(matrice1, matrice2, 0.5, 0.5)
    
    print(f"Matrice fusionnée: {len(matrice_fusionnee)} caractères sources")
    
    
    fichier_sortie = 'matrice_transition_fusionnee.json'
    print(f"Sauvegarde dans {fichier_sortie}...")
    sauvegarder_matrice(matrice_fusionnee, fichier_sortie)
    
    print("Fusion terminée avec succès!")
    
    
    total_transitions = sum(len(destinations) for destinations in matrice_fusionnee.values())
    print(f"Total des transitions: {total_transitions}")

if __name__ == "__main__":
    main()
