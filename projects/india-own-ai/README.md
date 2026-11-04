# Can India Build Its Own ChatGPT? (working title)

"India's Missing Pieces" episode 5, picked by the owner on 2026-11-03 ("Sovereign AI"); it answers the pharma film's
closing bridge. English VO (`lang.txt`), Akash on Eleven v4 through the API (`config/voice.yaml`,
`scripts/eleven_tts.py`; owner's settings 2026-11-03); about 12 minutes, set by the story.

**Genre and look:** tech + business (PLAYBOOK §5.3), "the reading room": library amber and paper against the cold
blue-black of a data hall. Colour = meaning: paper amber = words, chip green = compute, saffron = Indian-built,
grey-blue = built abroad, red cut = a letter split in half. Signature device: the PIECE METER (top left, one glowing
tile per token, tokenizer named). Media stack: real summit/lab/data-hall footage and press photos, document push-ins
(PIB, DeepSeek paper, Federal Register, model cards), HyperFrames for the meter, library stack and money wall; macro of
Indian scripts in print. Full plan: `treatment.md`.

**Original research:** `tools/token_test.py` (FLORES-200, 1,012 sentences × 12 languages × 6 tokenizers →
`research/token_test_flores200.json`), `tools/token_example.py` (the village question → `research/token_example.txt`),
Common Crawl CC-MAIN-2026-43 language count (`research.md`).

Files: `treatment.md` · `research.md` (writer's leads) · `research/search_terms.md` · `vo.txt` (narration) ·
`claims.csv` + `fact-check.md` (independent check) · `review_audience_vN.md`.

Checks: `python3 scripts/spoken_english_check.py projects/india-own-ai/vo.txt --min-words 1300 --max-words 2100` and
`python3 scripts/claims_check.py projects/india-own-ai/claims.csv`.

Rebuild the token test: download the tokenizer files and FLORES-200 (see `research.md`), then
`python3 projects/india-own-ai/tools/token_test.py <dir> out.json`.

Music and SFX: open sources first (Pixabay API, Freesound CC0), ElevenLabs sound effects only where nothing fits
(owner, 2026-11-03).
