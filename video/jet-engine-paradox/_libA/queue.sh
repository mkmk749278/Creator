#!/usr/bin/env bash
# wait for the running render to finish, then render the rest in order
cd "$(dirname "$0")"
while ! grep -q "A6_spin_bus done" render_status.txt 2>/dev/null; do sleep 15; done
bash ./render.sh A5_thermal_reveal A8_verdict_blade A4_combustor_flow A3_blade_rise A1_title_blade A2_engine_dive
