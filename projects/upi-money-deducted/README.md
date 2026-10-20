# Film 01 · UPI Payment Failed, But Money Deducted. Where Did It Go?

First film of the 180-second roadmap (`config/roadmap-180s.yaml` #01; rules PLAYBOOK §4a-9). English VO (`lang.txt`),
about 690 words, about 4:40 at 150 words a minute: VO v16, cleared after nine independent audience reviews
(`review_audience_v1.md` … `v9.md`, PLAYBOOK §4a-11). Genre: tech explainer, dark blueprint look (`blueprint` in `config/brand.yaml`).

**Mechanism (v5, owner 2026-10-20: "no technical depth, nothing cleared from the user's point of view"):** the
film answers the stuck viewer's three questions. *Where is my money?* UPI runs on two layers: messages in real time
(15-second replies), money between banks later, in 10 settlement batches a day through accounts at the RBI. On a credit
timeout NPCI marks the payment deemed approved and settles it, so the money moves to the shop's bank. *When does it
come back?* The next day the shop's bank files TCC (credited: the shop has it even if the speaker was silent) or RET
(return: your bank credits you); RBI deadline T+1 person / T+5 shop, then ₹100 a day automatically. *What do I do?*
Don't pay again while it says processing, ask the shop to check its bank statement, complain in UPI Help then the bank.
Claims and sources: `claims.csv` (19 confirmed, gate passes).

Files: `vo.txt` (recording text) · `script.tsv` (one line per row, for `scripts/align_script.py`) · `hud.md` (Block 1) ·
`screenplay.md` (Block 3) · `claims.csv`.

Next: owner records the VO → align → final fact-check pass on changed lines → sourcing (counter footage, RBI and NPCI
pages, rack references) → Blender hero shots + HyperFrames scenes → review → render → YouTube package.
