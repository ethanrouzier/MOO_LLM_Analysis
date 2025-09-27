#!/usr/bin/env bash
set -euo pipefail
source .venv/bin/activate || true
export $(grep -v '^#' .env | xargs) 2>/dev/null || true
python -m flask --app app.main run --debug --port=${PORT:-5001}
