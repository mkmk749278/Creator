# The Pharmacy of the World's Missing Powder (working title)

"India's Missing Pieces" episode 4, picked by the owner on 2026-10-28 from the slate in
`docs/research/reports/India content edge 2026-10-21.md`; it answers the rare-earth film's closing bridge ("India is
called the pharmacy of the world... but a big share of the ingredients in your medicines comes from China. Why?").
English VO (`lang.txt`), Akash; target about 11–12 minutes, set by the story.

**Genre and look:** business + science (PLAYBOOK §5.3), "clean room" palette: pharmaceutical white and steel on deep teal;
mould green = penicillin, amber = China's supply, saffron-white = Indian-made, red stamp = a stopped plant. Signature
device: the CAPSULE GAUGE. Full plan: `treatment.md`.

Files: `treatment.md` (angle, shape, package) · `research.md` (writer's leads) · `research/search_terms.md`
(autocomplete, main phrase) · `vo.txt` / `script.tsv` (narration v5, 1,802 words, about 11 minutes) · `vo_blocks.md`
(Akash blocks) · `claims.csv` + `fact-check.md` (independent check: 67 confirmed, 4 attributed) ·
`review_audience_v1.md`, `review_audience_v2.md`.

Checks: `.venv/bin/python scripts/spoken_english_check.py projects/pharma-apis/vo.txt --min-words 1300 --max-words 2000`
and `python3 scripts/claims_check.py projects/pharma-apis/claims.csv`.

Status: narration v5 ready to record (both gates pass). Next: owner records the blocks → `align_script.py` → recheck
the "minute eight" open loop → sourcing → thumbnails (3+ curiosity concepts through `thumb_feed.py` + click panel) →
scenes → review → render.
**Time-sensitive, recheck before upload:** the minimum import price (to about 29 January 2027), the two DGTR
anti-dumping cases opened in September 2026, and whether any bulk drug park has started.
