#!/usr/bin/env bash
# Helper to run a short demo session (not recorded automatically).
# Use with asciinema: asciinema rec demo.cast -- command

set -euo pipefail

echo "Starting short GearIQ demo script"
echo "Show backend health and an example search against local backend"

echo "=== /health ==="
curl -sS http://127.0.0.1:8000/health || true
echo

echo "=== /v1/search?q=MIPS bike helmet&budget=150 ==="
curl -sS "http://127.0.0.1:8000/v1/search?q=MIPS%20bike%20helmet&budget=150" | python -m json.tool || true

echo
echo "Demo complete. To record this session, run:"
echo "  asciinema rec demo.cast ./scripts/record_demo.sh"
