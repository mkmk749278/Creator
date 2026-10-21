# India Has the Rare Earths. China Has the Magnets. Why?

"India's Missing Pieces" episode 2 (owner, 2026-10-21: back to documentaries; topic research in
`docs/research/reports/India content edge 2026-10-21.md`). English VO (`lang.txt`), Akash; about 1,660 words, about
10–11 minutes. The film answers the viewer's questions in order: what the magnet is and why motors need it; why
separating seventeen near-identical rare earths takes hundreds of tanks; how China came to hold every link of the chain;
what kept India's monazite locked away (thorium, the Atomic Energy Act, one state company, small demand, raw exports to
Japan); the April 2025 licence shock (Bajaj Chetak output about halved); India's answer (Vizag magnet plant, ₹7,280 crore
scheme, 20 bids, rare earth corridors) and the dates to watch (China's hold ends 10 November 2026 on paper, while the US–China truce now runs to 10 January 2027;
scheme winners).

**Genre and look:** tech + business, dark blueprint palette (amber = China's control, cyan = magnetism / India's
build-out, green = a link India owns, red = a stopped line). Signature device: the six-link CHAIN BAR. Plan:
`screenplay.md`.

Files: `vo.txt` (recording text, one beat per line) · `script.tsv` (same lines, for `scripts/align_script.py`) ·
`research.md` (writer's leads) · `claims.csv` + `fact-check.md` (independent check) · `screenplay.md` ·
`youtube/thumbnail_a.jpg`, `thumbnail_b.jpg` (drafts; build: `youtube/thumb/`).

Checks: `python3 scripts/spoken_english_check.py projects/rare-earth-magnets/vo.txt --min-words 1300 --max-words 1800`
and `python3 scripts/claims_check.py projects/rare-earth-magnets/claims.csv`.

Thumbnail rebuild (from the repo root, with `python3 -m http.server 8765` running):
`node projects/rare-earth-magnets/youtube/thumb/shoot.mjs http://localhost:8765/projects/rare-earth-magnets/youtube/thumb/magnet_render.html projects/rare-earth-magnets/youtube/thumb/magnet.png 1400 1050 png`
then the same with `thumb_a.html` / `thumb_b.html` → `youtube/thumbnail_a.jpg` / `thumbnail_b.jpg` (1280 720).
The magnet is a Three.js render of a generic nickel-plated block magnet (illustration); the sand is Pixabay 1208503
(Pixabay Content License, milivigerova).

Next: owner records the VO → `align_script.py` → re-check the open-loop minute → sourcing → 3D hero shots + HyperFrames
scenes → review → render → YouTube package. **Re-check before upload:** whether China extended the 10 November hold, and
whether the scheme winners were announced (both lines are time-sensitive).
