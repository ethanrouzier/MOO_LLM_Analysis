from typing import List, Dict, Any

# Objectifs par défaut: maximiser QED, rapprocher logP et TPSA de cibles, minimiser MW et RB
DEFAULT_TARGETS = {"logP": 2.5, "TPSA": 75.0}

# On convertit en coûts à minimiser
# -QED -> 1-QED ; logP/TPSA -> distance à la cible ; MW et RB bruts (avec normalisation douce)

def make_objectives(p: Dict[str, float], targets=DEFAULT_TARGETS) -> List[float]:
    return [
        1.0 - float(p["QED"]),
        abs(float(p["logP"]) - targets["logP"]) / 3.0,   # ~0..1
        abs(float(p["TPSA"]) - targets["TPSA"]) / 150.0, # ~0..1
        float(p["MW"]) / 600.0,                            # scale MW
        float(p["RB"]) / 12.0,                             # scale RB
    ]

def is_dominated(a: List[float], b: List[float]) -> bool:
    return all(bi <= ai for ai, bi in zip(a, b)) and any(bi < ai for ai, bi in zip(a, b))

def pareto_front(objs: List[List[float]]):
    front_idx = []
    for i, ai in enumerate(objs):
        dominated = False
        for j, bj in enumerate(objs):
            if i == j:
                continue
            if is_dominated(ai, bj):
                dominated = True
                break
        if not dominated:
            front_idx.append(i)
    return front_idx
