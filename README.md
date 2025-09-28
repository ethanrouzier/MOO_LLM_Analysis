# Pareto Multi-Objective Optimization for Drug Discovery

A web application for multi-objective optimization in medicinal chemistry using RDKit for molecular property calculations and Mistral AI for explanatory analysis.

## Installation

### Prerequisites
- Python 3.8+
- pip or conda

### Setup
```bash
# Clone the repository
git clone https://github.com/ethanrouzier/MOO_LLM_Analysis.git
cd MOO_LLM_Analysis

# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# If RDKit installation fails, use conda:
# conda install -c conda-forge rdkit
```

### Configuration (Optional)
```bash
# Copy configuration file
cp .env.example .env

# Edit .env to add your Mistral API key (optional)
# Get your key at: https://console.mistral.ai/

# Load environment variables
export $(grep -v '^#' .env | xargs)
```

## Running the Application

### Option 1: Automated script
```bash
./run.sh
```

### Option 2: Flask directly
```bash
python -m flask --app app.main run --debug --port=5001
```

### Option 3: Python module
```bash
python -m app.main
```

The application will be available at: **http://127.0.0.1:5001**

## Usage

### Web Interface
1. **Home page** (`/`): Upload CSV or use demo dataset
2. **Demo** (`/demo`): Uses `data/demo_mols.csv` automatically
3. **CSV Upload**: Required format with `name,smiles` columns
4. **Target settings**: logP and TPSA for optimization
5. **Results**: 
   - Table with Pareto front highlighted
   - LLM explanatory comments
   - JSON export

### Expected CSV Format
```csv
name,smiles
mol1,CC(=O)O
mol2,C1=CC=CC=C1
mol3,CCN(CC)CC
```

## Multi-Objective Model

The system minimizes the multi-objective vector:
`[1-QED, |logP-target|, |TPSA-target|, MW, RB]` 

- **QED** (Drug-likeness): maximized
- **logP**: close to target
- **TPSA**: close to target  
- **MW** (Molecular Weight): minimized
- **RB** (Rotatable Bonds): minimized

Scales are normalized for comparison. **Pareto-optimality** requires no weighting.
