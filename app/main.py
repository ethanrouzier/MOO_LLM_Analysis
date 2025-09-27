import io
import os
import pandas as pd
from flask import Flask, request, render_template_string, jsonify
from .props import compute_props
from .moo import make_objectives, pareto_front, DEFAULT_TARGETS
from .llm import summarize

app = Flask(__name__)

HTML = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Pareto Mini‑MOO</title>
    <style>
      body{font-family:system-ui,Arial;max-width:1100px;margin:auto;padding:24px}
      .card{border:1px solid #eee;border-radius:12px;padding:16px;margin:16px 0}
      table{width:100%;border-collapse:collapse}
      th,td{border-bottom:1px solid #eee;padding:6px 8px;text-align:left}
      tr.front{background:#f6fff8}
      .muted{color:#666}
      input[type=number]{width:90px}
      pre{background:#f6f8fa;padding:8px;border-radius:8px;white-space:pre-wrap}
    </style>
  </head>
  <body>
    <h1>Pareto Mini‑MOO (RDKit + Mistral)</h1>
    <p class="muted">Upload CSV with columns <code>name,smiles</code> or use the demo dataset.</p>

    <form class="card" action="/analyze" method="post" enctype="multipart/form-data">
      <div>
        <label>CSV file: <input type="file" name="file" accept=".csv"></label>
        <button type="submit">Analyze</button>
        <a href="/demo" style="margin-left:8px">Use demo dataset</a>
      </div>
      <div style="margin-top:8px">
        Targets: logP≈ <input type="number" step="0.1" name="logP" value="2.5"> &nbsp;
        TPSA≈ <input type="number" step="1" name="TPSA" value="75"> &nbsp;
      </div>
    </form>

    {% if results %}
      <div class="card">
        <h3>Results</h3>
        <p>Front size: {{results.front_size}} / {{results.n_total}}</p>
        <table>
          <thead>
            <tr>
              <th>#</th><th>Name</th><th>SMILES</th>
              <th>MW</th><th>logP</th><th>TPSA</th><th>RB</th><th>QED</th><th>Front?</th>
            </tr>
          </thead>
          <tbody>
          {% for row in results.rows %}
            <tr class="{% if row.front %}front{% endif %}">
              <td>{{ loop.index }}</td>
              <td>{{ row.name }}</td>
              <td><code>{{ row.smiles }}</code></td>
              <td>{{ '%.1f'|format(row.props.MW) }}</td>
              <td>{{ '%.2f'|format(row.props.logP) }}</td>
              <td>{{ '%.1f'|format(row.props.TPSA) }}</td>
              <td>{{ row.props.RB }}</td>
              <td>{{ '%.2f'|format(row.props.QED) }}</td>
              <td>{{ 'yes' if row.front else '' }}</td>
            </tr>
          {% endfor %}
          </tbody>
        </table>
      </div>

      <div class="card">
        <h3>LLM commentary</h3>
        <pre>{{ results.commentary }}</pre>
      </div>

      <div class="card">
        <h3>JSON</h3>
        <pre>{{ results.json }}</pre>
      </div>
    {% endif %}
  </body>
</html>
"""

@app.get("/")
def home():
    return render_template_string(HTML)


def _analyze_df(df: pd.DataFrame, targets):
    rows = []
    for _, r in df.iterrows():
        name = str(r.get("name", "mol"))
        smi = str(r.get("smiles", ""))
        if not smi:
            continue
        props = compute_props(smi)
        if props is None:
            continue
        obj = make_objectives(props, targets)
        rows.append({"name": name, "smiles": smi, "props": props, "obj": obj})

    objs = [r["obj"] for r in rows]
    idx_front = pareto_front(objs)
    for i, r in enumerate(rows):
        r["front"] = (i in idx_front)

    # Split for commentary
    front_rows = [rows[i] for i in idx_front]
    off_rows = [r for i, r in enumerate(rows) if i not in idx_front]
    cm = summarize(front_rows, off_rows, targets)

    # Small JSON dump (without objectives)
    jrows = []
    for r in rows:
        jr = {
            "name": r["name"],
            "smiles": r["smiles"],
            "props": r["props"],
            "front": r["front"],
        }
        jrows.append(jr)

    return {
        "front_size": len(idx_front),
        "n_total": len(rows),
        "rows": rows,
        "commentary": cm,
        "json": __import__("json").dumps({"targets": targets, "molecules": jrows}, indent=2),
    }

@app.post("/analyze")
def analyze():
    logP = float(request.form.get("logP", 2.5))
    TPSA = float(request.form.get("TPSA", 75.0))
    targets = {"logP": logP, "TPSA": TPSA}

    if "file" in request.files and request.files["file"].filename:
        f = request.files["file"]
        data = f.read()
        df = pd.read_csv(io.BytesIO(data))
        res = _analyze_df(df, targets)
        return render_template_string(HTML, results=res)
    return jsonify({"error": "Upload a CSV or use /demo"}), 400

@app.get("/demo")
def demo():
    logP = float(request.args.get("logP", 2.5))
    TPSA = float(request.args.get("TPSA", 75.0))
    targets = {"logP": logP, "TPSA": TPSA}
    p = os.path.join(os.path.dirname(__file__), "..", "data", "demo_mols.csv")
    df = pd.read_csv(p)
    res = _analyze_df(df, targets)
    return render_template_string(HTML, results=res)

if __name__ == "__main__":
    app.run(debug=True, port=int(os.getenv("PORT", 5001)))
