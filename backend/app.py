from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import generateur 

app = Flask(__name__)
CORS(app)

matrice = None

def charger_matrice():
    global matrice
    try:
        matrice = generateur.charger_matrice("../data_markov/matrice_transition.json")
        print("✅ Matrice chargée")
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

@app.route("/")
def accueil():
    return send_from_directory("../frontend", "index.html")

@app.route("/frontend/<path:filename>")
def servir_frontend(filename):
    return send_from_directory("../frontend", filename)

@app.route("/generermdp", methods=["POST"])
def generer_mdp():
    if not matrice:
        return jsonify({"error": "Matrice non chargée"}), 500
    
    try:
        data = request.get_json() or {}
        longueur = data.get("longueur", 12)
        
        if longueur < 4 or longueur > 50:
            return jsonify({"error": "Longueur entre 4 et 50"}), 400
            
        mot_de_passe = generateur.generer_mot_de_passe(matrice, longueur)
        
        return jsonify({
            "mot_de_passe": mot_de_passe,
            "longueur": len(mot_de_passe)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("🚀 Démarrage...")
    if charger_matrice():
        print("✅ Serveur prêt sur:")
        print("   🌐 Frontend: http://localhost:5001")
        print("   🔌 API: http://localhost:5001/generermdp")
        app.run(debug=True, port=5001)
    else:
        print("❌ Impossible de démarrer")


