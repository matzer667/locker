const API_URL = 'http://localhost:5001/generermdp';
let currentPassword = '';

async function generatePassword() {
    console.log(' Fonction generatePassword appelée');
    
    try {
        const length = parseInt(document.getElementById('length').value);
        console.log(' Longueur demandée:', length);
        
        if (length < 4 || length > 50) {
            alert('La longueur doit être entre 4 et 50 caractères');
            return;
        }

        const btn = document.getElementById('generateBtn');
        btn.disabled = true;
        btn.textContent = ' Génération...';
        console.log(' Bouton désactivé');

        console.log(' Appel API vers:', API_URL);
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ longueur: length })
        });

        console.log(' Réponse reçue, status:', response.status);

        if (!response.ok) {
            throw new Error('Erreur serveur: ' + response.status);
        }

        const data = await response.json();
        console.log(' Données reçues:', data);
        
        currentPassword = data.mot_de_passe;
        console.log(' Mot de passe généré:', currentPassword);

        const display = document.getElementById('passwordDisplay');
        display.textContent = currentPassword;
        display.classList.remove('empty');
        console.log(' Mot de passe affiché');

        document.getElementById('copyBtn').disabled = false;

    } catch (error) {
        console.error(' Erreur:', error);
        alert('Erreur: ' + error.message);
    } finally {
        const btn = document.getElementById('generateBtn');
        btn.disabled = false;
        btn.textContent = ' Générer un Mot de Passe';
        console.log(' Bouton réactivé');
    }
}

function copyPassword() {
    console.log(' Fonction copyPassword appelée');
    
    if (!currentPassword) {
        console.log(' Aucun mot de passe à copier');
        return;
    }

    navigator.clipboard.writeText(currentPassword).then(() => {
        console.log(' Mot de passe copié');
        const btn = document.getElementById('copyBtn');
        const originalText = btn.textContent;
        btn.textContent = ' Copié !';
        
        setTimeout(() => {
            btn.textContent = originalText;
        }, 2000);
    }).catch((error) => {
        console.error(' Erreur copie:', error);
        alert('Impossible de copier');
    });
}

document.addEventListener('DOMContentLoaded', function() {
    console.log(' DOM chargé, initialisation...');
    
    const generateBtn = document.getElementById('generateBtn');
    const copyBtn = document.getElementById('copyBtn');
    
    if (generateBtn) {
        generateBtn.addEventListener('click', generatePassword);
        console.log(' Event listener ajouté au bouton générer');
    } else {
        console.error(' Bouton generateBtn non trouvé');
    }
    
    if (copyBtn) {
        copyBtn.addEventListener('click', copyPassword);
        console.log(' Event listener ajouté au bouton copier');
    } else {
        console.error(' Bouton copyBtn non trouvé');
    }
    
    console.log(' Génération d\'un mot de passe initial...');
    generatePassword();
});
