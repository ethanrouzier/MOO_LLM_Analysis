# Pareto Mini‑MOO (RDKit + Mistral)

**But**: Démo de décision multi‑critères pour chimie médicinale: calcul de propriétés (RDKit), front de Pareto (QED↑, logP≈cible, TPSA≈cible, MW↓, RB↓), et **commentaire IA** (Mistral) qui explique les compromis.

## 🚀 Installation rapide

### Prérequis
- Python 3.8+
- pip ou conda

### Installation
```bash
# Cloner le repository
git clone https://github.com/ethanrouzier/MOO_LLM_Analysis.git
cd MOO_LLM_Analysis

# Créer un environnement virtuel
python -m venv .venv

# Activer l'environnement virtuel
source .venv/bin/activate  # Sur Windows: .venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Si RDKit pose problème, utiliser conda:
# conda install -c conda-forge rdkit
```

### Configuration (optionnel)
```bash
# Copier le fichier de configuration
cp .env.example .env

# Éditer .env pour ajouter votre clé API Mistral (optionnel)
# Obtenez votre clé sur: https://console.mistral.ai/

# Charger les variables d'environnement
export $(grep -v '^#' .env | xargs)
```

## 🎯 Lancer l'application

### Option 1: Script automatique
```bash
./run.sh
```

### Option 2: Flask directement
```bash
python -m flask --app app.main run --debug --port=5001
```

### Option 3: Python module
```bash
python -m app.main
```

L'application sera disponible sur: **http://127.0.0.1:5001**

## 📊 Utilisation

### Interface web
1. **Page d'accueil** (`/`): Interface pour uploader un CSV ou utiliser le dataset de démo
2. **Dataset de démo** (`/demo`): Utilise automatiquement `data/demo_mols.csv`
3. **Upload CSV**: Format requis avec colonnes `name,smiles`
4. **Réglages cibles**: logP et TPSA pour l'optimisation
5. **Résultats**: 
   - Tableau avec front de Pareto mis en évidence
   - Commentaire LLM explicatif des compromis
   - Export JSON des résultats

### Format CSV attendu
```csv
name,smiles
mol1,CC(=O)O
mol2,C1=CC=CC=C1
mol3,CCN(CC)CC
```

## 🧬 Modèle d'objectifs

Le système minimise le vecteur multi-objectifs:
`[1-QED, |logP-cible|, |TPSA-cible|, MW, RB]` 

- **QED** (Drug-likeness): maximisé
- **logP**: proche de la cible
- **TPSA**: proche de la cible  
- **MW** (Molecular Weight): minimisé
- **RB** (Rotatable Bonds): minimisé

Les échelles sont normalisées pour permettre la comparaison. La **Pareto-optimalité** ne nécessite pas de pondération.

## 🔧 Technologies utilisées

- **Flask**: Framework web
- **RDKit**: Calcul des propriétés moléculaires
- **Mistral AI**: Commentaires explicatifs
- **Pandas**: Manipulation des données
- **NumPy**: Calculs numériques

## 🚀 Idées d'évolutions

- [ ] Ajouter des objectifs supplémentaires (alerts PAINS, HBD/HBA, cLogS)
- [ ] Filtre Lipinski/Veber en soft constraints
- [ ] Visualisation 2D (PCA) avec colorisation par appartenance au front
- [ ] Proposer des **mutations chimiques** concrètes (LLM) à partir d'un noyau commun
- [ ] Interface de comparaison de plusieurs datasets
- [ ] Export des résultats en formats multiples (CSV, SDF, etc.)

## 📝 Licence

MIT License - Voir le fichier LICENSE pour plus de détails.
