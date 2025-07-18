from collections import defaultdict
import json

def lire_dataset(fichier):
    mots = []
    with open(fichier, 'r', encoding='utf-8', errors='ignore') as f:
        for ligne in f:
            mdp = ligne.strip()
            if mdp: 
                mots.append(mdp)
    return mots

def construire_matrice_transition(mots):
    transitions = defaultdict(lambda: defaultdict(int))

    for mot in mots:
        for i in range(len(mot) - 1):
            c1 = mot[i]
            c2 = mot[i+1]
            transitions[c1][c2] += 1


    matrice = {}
    for c1, suivant_dict in transitions.items():
        total = sum(suivant_dict.values())
        matrice[c1] = {}
        for c2, count in suivant_dict.items():
            matrice[c1][c2] = count / total
    return matrice

def sauvegarder_matrice(matrice, fichier_json):
    with open(fichier_json, 'w', encoding='utf-8') as f:
        json.dump(matrice, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    dataset = "leaksmdp.txt"  
    mots_de_passe = lire_dataset(dataset)
    matrice_transition = construire_matrice_transition(mots_de_passe)
    sauvegarder_matrice(matrice_transition, "matrice_transition.json")
    print("Matrice de transition générée et sauvegardée dans 'matrice_transition.json'")
