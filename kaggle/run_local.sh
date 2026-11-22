#!/bin/bash
# Resumable judged run outside Kaggle (any Linux machine, CPU or GPU).
# Usage: bash run_local.sh [workdir]. Re-invokes the script until it finishes; state lives in <workdir>/diagrag_out/checkpoint.pkl.
# The 14 Nov 2026 CPU judged run used:
#   RERANKER=cross-encoder/ms-marco-MiniLM-L-6-v2 CE_MAXLEN=256 N_BASE_ESCI=2400 N_PRDC=528 N_HARD=50 MAX_ATT=2500 N_HARM=20 TIME_BUDGET=1480
HERE="$(cd "$(dirname "$0")" && pwd)"; WORK="${1:-$PWD/diagrag_work}"; mkdir -p "$WORK"
export DIAGRAG_WORK="$WORK" TIME_BUDGET="${TIME_BUDGET:-0}"
for i in $(seq 1 40); do
  python -u "$HERE/diagrag_core28.py" 2>&1 | tee "$WORK/run_$i.log"
  grep -q "done. outputs in" "$WORK/run_$i.log" && { echo "finished: $WORK/diagrag_out/VERDICT.json"; exit 0; }
  grep -q "TIME_BUDGET reached" "$WORK/run_$i.log" || { echo "stopped with an error, see $WORK/run_$i.log"; exit 1; }
done
