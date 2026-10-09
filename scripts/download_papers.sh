#!/usr/bin/env bash
# Download the papers from docs/notes/milestone-1-reading-guide.md into papers/.
# papers/ is gitignored: the PDFs belong to their authors, so we link rather than redistribute.
#
# Run with:  bash scripts/download_papers.sh

set -uo pipefail
cd "$(dirname "$0")/.."
mkdir -p papers/later
failed=0

download() {  # download <arxiv id> <output path>
  local id="$1" out="$2"
  if [[ -s "$out" ]]; then
    echo "skip  $out (already downloaded)"
    return
  fi
  if ! curl -sSfL -A "constraintbench-replication paper downloader" -o "$out" "https://arxiv.org/pdf/$id" \
     || [[ "$(head -c 4 "$out")" != "%PDF" ]]; then
    rm -f "$out"
    echo "FAIL  $id -> $out" >&2
    failed=$((failed + 1))
    return
  fi
  echo "ok    $out"
}

# Milestone 1, in reading order
download 2602.22465 papers/00_ConstraintBench_2602.22465.pdf
download 2608.00991 papers/01_SCHEDBench_2608.00991.pdf
download 2510.07043 papers/02_COMPASS_2510.07043.pdf
download 2402.01622 papers/03_TravelPlanner_2402.01622.pdf
download 2402.01817 papers/04_LLM-Modulo_2402.01817.pdf
download 2310.01798 papers/05_LLMs-Cannot-Self-Correct-Yet_2310.01798.pdf
download 2411.00640 papers/06_Adding-Error-Bars-to-Evals_2411.00640.pdf

# Later milestones
download 2405.17743 papers/later/ORLM-IndustryOR_2405.17743.pdf
download 2402.10172 papers/later/OptiMUS_2402.10172.pdf
download 2505.11792 papers/later/Solver-Informed-RL_2505.11792.pdf
download 2501.12948 papers/later/DeepSeek-R1_2501.12948.pdf
download 2508.15204 papers/later/R-ConstraintBench_2508.15204.pdf

exit "$failed"
