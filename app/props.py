from rdkit import Chem
from rdkit.Chem import Descriptors, Crippen, QED, Lipinski, rdMolDescriptors

PROP_KEYS = ["MW","logP","TPSA","HBD","HBA","RB","QED"]

def mol_from_smiles(smiles: str):
    m = Chem.MolFromSmiles(smiles)
    if m is None:
        return None
    Chem.SanitizeMol(m)
    return m

def compute_props(smiles: str):
    m = mol_from_smiles(smiles)
    if m is None:
        return None
    return {
        "MW": Descriptors.MolWt(m),
        "logP": Crippen.MolLogP(m),
        "TPSA": rdMolDescriptors.CalcTPSA(m),
        "HBD": Lipinski.NumHDonors(m),
        "HBA": Lipinski.NumHAcceptors(m),
        "RB": Lipinski.NumRotatableBonds(m),
        "QED": QED.qed(m),
    }
