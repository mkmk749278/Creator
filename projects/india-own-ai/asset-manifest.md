# Asset manifest (draft, 2026-11-03)

## Owner's footage (Drive `footage/` folder 1t9l77-LXeoyMrn7IayenyrEzFXYAcIQH, fetched 2026-11-03)
Contact sheet: `qa/owner_footage_sheet.jpg`. Third-party clips: short credited excerpts only (PLAYBOOK §8.6);
every use gets a `media_manifest.csv` row with the source, the timecode used and the on-screen credit.

| File | Source | Use | Beat |
|---|---|---|---|
| 03_J0Cin9zOSSM.mp4 | Digit, "Inside the Yotta NM1 data center" (YouTube J0Cin9zOSSM) | ★ real Indian AI data hall | shared pool (block 5), "trained in India on shared chips" (block 7) |
| 04_oG_whhbr0sg.mp4 | moneycontrol, "PM Modi Uses AI Tool Bhashini" (oG_whhbr0sg) | ★ Bhashini live Hindi→Tamil; Bhasha Daan | "page by page, voice by voice" (block 4) |
| 05_u8uJ6tqYt4I.mp4 | Agriculture INDIA, Kisan e-Mitra chatbot (u8uJ6tqYt4I) | ★ farmer + Indian-language chatbot; Hindi/English/Marathi | ending ("ask in your own language"), village texture |
| 02_tiaX1Ja3C5g.mp4 | NVIDIA, "Quick Tour of NVIDIA DGX H100" (vertical 608×1080) | H100 / DGX macro | "a chip like this one" (block 4); frame on a blurred plate |
| 01_ytvy1JruLlY.mp4 | Business Standard, IT firms payouts (ytvy1JruLlY) | Infosys/Wipro campuses (avoid its stock-market and AI-art shots) | "Indian engineers write software…" (block 2) |
| 01_Ap3ek027Feo.mp4 | Bright Way By Monu Sharma, Tata fab Dholera (Ap3ek027Feo) | 3 s glimpse | "If you watched our chip film" (block 4) |
| pexels_server_rack_5028622.mp4 | Pexels (licence: free use) | rack cutaway | reading room |
| pexels_semiconductor_6754830.mp4 | Pexels | chip board macro | reading room |
| pexels_corporate_tech_856662.mp4, pexels_power_grid_4035765.mp4 | Pexels | generic, likely unused | — |
| 02_a3TmvqHJB5A.mp4 | Bloomberg Tech (a3TmvqHJB5A) | **broken: 1 s** | re-fetch if wanted |

Labels: the Kisan e-Mitra and Bhashini clips are real government tools, shown as themselves; nothing here is
"ILLUSTRATIVE". No stock clip used more than twice.

## Pexels batches (2026-11-03)
- `assets/pexels_termux/` (24 clips, owner's Termux run of `scripts/termux_pexels_to_drive.sh`; Drive
  `Creator/English/india-own-ai/footage/pexels/`) and `assets/pexels_ag/` (36 clips + `pexels_list.csv` with creator
  names, Antigravity; Drive shared `footage/india-own-ai-pexels/`). Verdicts and picks: `qa/pexels/verdicts.md`;
  sheets `qa/pexels/termux_*.jpg`, `qa/pexels/ag_*.jpg`. Lesson: IDs from an AI-written list were wrong for 9 of 24;
  check every clip by picture.
