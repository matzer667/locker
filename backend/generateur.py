import random
import json
from zxcvbn import zxcvbn

def charger_matrice(fichier_json):
    with open(fichier_json, 'r', encoding='utf-8') as f:
        return json.load(f)

def tirage_pondere_inverse(suivant_probs):
    epsilon = 1e-6
    poids = {k: 1/(v + epsilon) for k, v in suivant_probs.items()}
    total_poids = sum(poids.values())

    r = random.uniform(0, total_poids)
    cumul = 0
    for lettre, p in poids.items():
        cumul += p
        if r <= cumul:
            return lettre

    return random.choice(list(suivant_probs.keys()))

def generer_mot_de_passe(matrice, longueur):
    lettres = list(matrice.keys())
    curr_char = random.choice(lettres)
    mot = curr_char

    for _ in range(longueur -1):
        if curr_char not in matrice or not matrice[curr_char]:
            curr_char = random.choice(lettres)
            mot += curr_char
            continue

        suivant_probs = matrice[curr_char]
        lettre_suivante = tirage_pondere_inverse(suivant_probs)
        mot += lettre_suivante
        curr_char = lettre_suivante

    return mot

if __name__ == "__main__":
    matrice = charger_matrice("data_markov/matrice_transition.json")
    mot_genere = generer_mot_de_passe(matrice, longueur=4)
    print("Mot de passe généré :", mot_genere)
    resultat = zxcvbn(mot_genere)
    print("Score (0-4) :", resultat['score'])
    print("Temps estimé pour le cracker :", resultat['crack_times_display']['offline_fast_hashing_1e10_per_second'])
    


