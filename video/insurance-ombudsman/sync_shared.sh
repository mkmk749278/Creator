#!/usr/bin/env bash
# Copy the shared kit into each session-C scene (HyperFrames serves one folder; no ../ paths at render time).
set -euo pipefail
cd "$(dirname "$0")"
for d in C1_filing_stepper C2_offices_board C3_document_slots C4_binding_award C5_proof_magnifier; do
  mkdir -p "$d/shared"; cp _shared/io.css _shared/io.js "$d/shared/"
done
