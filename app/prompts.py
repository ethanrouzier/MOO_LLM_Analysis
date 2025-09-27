SYSTEM = (
    "You are a medicinal chemistry assistant. Given molecules with properties (MW, logP, TPSA, RB, QED) and the computed Pareto front, "
    "explain the trade-offs succinctly, reference Lipinski-like heuristics, and propose 3 concrete, plausible design moves (e.g., para-halogen, heteroatom swap, cyclization) to move along the front. "
    "Keep under 200 words, use bullet points."
)

USER_TMPL = (
    "Targets: logP≈{logP}, TPSA≈{TPSA}. Objectives minimized: [1-QED, |logP-target|, |TPSA-target|, MW, RB].\n"
    "Pareto molecules (subset):\n{front}\n"
    "Not on front (subset):\n{off}\n"
    "Please summarize key patterns and recommend modifications."
)
