# Film 01 · UPI Payment Failed, But Money Deducted. Where Did It Go?

First film of the 180-second roadmap (`config/roadmap-180s.yaml` #01; rules PLAYBOOK §4a-9). English VO (`lang.txt`),
389 words, about 2:35 at 150 words a minute (VO v4: built on the three app statuses, success, failed and processing, owner 2026-10-20; written to the narration blueprint, PLAYBOOK §4a-10). Genre: tech explainer, dark blueprint look (`blueprint` in `config/brand.yaml`).

**Mechanism (corrected from the roadmap note):** the roadmap called this an "asynchronous rollback vs CBS deadlock in a
distributed two-phase commit". The sources show something simpler and more accurate: UPI runs a **debit leg, then a
credit leg**, each with a 15-second response limit. When the credit reply doesn't come back, NPCI marks the payment
**deemed (credit timeout)**, then checks with the payee's bank, which either credits the payee or returns the money,
and the payer's bank reverses the debit. The RBI's 2019 TAT rule sets the deadline (T+5 for a shop, T+1 for a person,
₹100 a day after that, paid without a complaint). Claims and sources: `claims.csv` (gate passes).

Files: `vo.txt` (recording text) · `script.tsv` (one line per row, for `scripts/align_script.py`) · `hud.md` (Block 1) ·
`screenplay.md` (Block 3) · `claims.csv`.

Next: owner records the VO → align → final fact-check pass on changed lines → sourcing (counter footage, RBI and NPCI
pages, rack references) → Blender hero shots + HyperFrames scenes → review → render → YouTube package.
