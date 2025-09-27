import os
from mistralai import Mistral
from .prompts import SYSTEM, USER_TMPL

MODEL = os.getenv("MISTRAL_MODEL", "mistral-large-latest")

_client = None

def _get_client():
    global _client
    if _client is None:
        key = os.getenv("MISTRAL_API_KEY")
        if not key:
            return None
        _client = Mistral(api_key=key)
    return _client


def summarize(front_rows, off_rows, targets):
    client = _get_client()
    if client is None:
        return "(LLM disabled: set MISTRAL_API_KEY to enable commentary)"

    def _fmt(rows):
        # keep a short subset to fit token budget
        lines = []
        for r in rows[:8]:
            lines.append(
                f"- {r['name']}: MW={r['props']['MW']:.1f}, logP={r['props']['logP']:.2f}, TPSA={r['props']['TPSA']:.1f}, RB={r['props']['RB']}, QED={r['props']['QED']:.2f}"
            )
        return "\n".join(lines) if lines else "(none)"

    user = USER_TMPL.format(
        logP=targets["logP"],
        TPSA=targets["TPSA"],
        front=_fmt(front_rows),
        off=_fmt(off_rows),
    )

    resp = client.chat.complete(
        model=MODEL,
        messages=[{"role":"system","content":SYSTEM},{"role":"user","content":user}],
        temperature=0.3,
    )
    return resp.choices[0].message.content
