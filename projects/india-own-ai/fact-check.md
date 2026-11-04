# Fact-check: Can India Build Its Own ChatGPT? (narration v2)

Independent full pass, 2026-11-03, on `vo.txt` v2 (84 lines, commit 42c0b00, after audience review v1). No draft
`claims.csv` existed, so every claim was checked. Rows where `research.md` gave a primary URL and quote were
spot-opened. Our own measurements were re-run, and the method was checked against the tokenizer files on Hugging Face.

**Result: 83 claims. 76 confirmed, 7 `claim` (the VO attributes them), 0 disputed.** `scripts/claims_check.py`
passes **only if the 16 line changes below are made**: each changed line has a row in `claims.csv` whose claim starts
`Replacement for L…` and whose note says `REPLACES`. If a line stays as it is, that row must go back to `wrong`.

## Required script changes (current line → replacement)

1. **L9** (wrong: ChatGPT already had a free tier. What became free for a year was the paid Go plan. TechCrunch, Business Today; A11)
   - Now: Now think back to last November. Chat G.P.T. became free in India for a whole year. Maybe you signed up too. OpenAI says India is now one of its biggest markets.
   - New: Now think back to last November. Chat G.P.T.'s paid plan, called Go, became free in India for a whole year. Maybe you signed up too. OpenAI says India is now one of its biggest markets.

2. **L17** (the government's own release of 30 Jan 2025, PIB 2097709, says he "expressed hope that the Indian AI model is likely to be ready within 6 months". "At maximum 10 months" came later, on 4 Feb (ANI); A21, A22)
   - Now: Three days later, in Delhi, India's I.T. minister, Ashwini Vaishnaw, makes a promise. India will build its own A.I. model, and reports say he gave it about ten months.
   - New: Three days later, in Delhi, India's I.T. minister, Ashwini Vaishnaw, makes a promise. India will build its own A.I. model... and he hopes it will be ready within six months.

3. **L26** (GPT-3 is not ChatGPT. The GPT-3 paper documents Common Crawl, and no source says ChatGPT's own model was trained on it; A27)
   - Now: A lot of A.I. learns from the internet. One of the biggest free copies of the web is called Common Crawl. Many A.I. models learned from it, including an early Chat G.P.T.
   - New: A lot of A.I. learns from the internet. One of the biggest free copies of the web is called Common Crawl. Many A.I. models learned from it, including an early model from the makers of the Chat G.P.T. you use.

4. **L27** (honesty: we did not count two billion pages. Common Crawl counts the languages with its own detector, CLD2, and we did the maths; A29)
   - Now: So we took its latest copy, from October twenty twenty-six — more than two billion web pages — and we counted the languages for you.
   - New: So we took its latest copy, from October twenty twenty-six — more than two billion web pages — and checked its own count of languages.

5. **L37** (no source says AI Kosh is free. Its datasets are Open, meaning downloadable by registered users, or Restricted, meaning they need the owner's approval. The live page shows 16,140+ datasets today. Over 14,000 was the July figure; A39)
   - Now: And India has started. The government has a free online shelf for Indian builders, called A.I. Kosh. It now holds more than fourteen thousand collections of data.
   - New: And India has started. The government runs an online shelf of data for Indian builders, called A.I. Kosh. It now holds more than sixteen thousand collections of data.

6. **L48** (PIB, 30 Jan 2025: a facility "of about 18,693" GPUs, "beginning with … roughly 10000 GPUs". So the pool did not yet "have" them, and 18,693 rounds to nineteen thousand; A47)
   - Now: In January twenty twenty-five, that pool had about eighteen thousand chips. By June twenty twenty-six, more than forty-five thousand.
   - New: In January twenty twenty-five, India lined up more than eighteen thousand chips for that pool. By June twenty twenty-six, more than forty-five thousand.

7. **L49** (there is no official count newer than "45,000+ as of June 2026". A February claim of 38,000 plus 20,000 would make the ratio six, so "today" is not supported; A50)
   - Now: That's a big jump, right? But by the end of twenty twenty-four, one American company, Meta, said it would have around three hundred and fifty thousand of these chips. Almost eight times your country's whole shared pool today.
   - New: That's a big jump, right? But by the end of twenty twenty-four, one American company, Meta, said it would have around three hundred and fifty thousand of these chips. Almost eight times your country's whole shared pool this June.

8. **L51** (Meta's latest guidance, 21 Oct 2026, is $135–145 billion. At ₹94.91 a dollar (ECB, 2 Nov 2026) that is ₹12.8–13.8 lakh crore. "More than ten" is true but far too low; A52)
   - Now: This year alone, Meta told its investors it would spend more than ten lakh crore rupees on buildings and machines, much of it for A.I.
   - New: This year alone, Meta told its investors it would spend around thirteen lakh crore rupees on buildings and machines, much of it for A.I.

9. **L52** (₹12.8–13.8 lakh crore ÷ ₹10,371.92 crore = 124–133 times; A53)
   - Now: So India's whole mission... ten thousand crore, over five years. Meta alone... ten lakh crore, in one single year. That's not double. That's about a hundred times more.
   - New: So India's whole mission... ten thousand crore, over five years. Meta alone... thirteen lakh crore, in one single year. That's not double. That's more than a hundred times as much.

10. **L61** (Sarvam unveiling both models at the summit is confirmed by TechCrunch and Inc42. Only one minor outlet says Pratyush Kumar presented them, and the Forbes India caption in `research.md` could not be found. Keep his name only if the launch footage the film uses shows him presenting; A62)
    - Now: Sarvam's co-founder, Pratyush Kumar, walks on stage with two new models. The bigger one has a hundred and five billion parameters. Think of them as tiny dials the machine tunes while it reads.
    - New: There, Sarvam shows India two new models. The bigger one has a hundred and five billion parameters. Think of them as tiny dials the machine tunes while it reads.

11. **L64** (follows change 2. Six months hoped, ten at the most, about twelve and a half taken; A21, A22, A67)
    - Now: The minister had said about ten months. It took about a year. A little late, you could say... but delivered.
    - New: The minister had hoped for six months, and later said ten at the most. It took about a year. Late, you could say... but delivered.

12. **L68** (`token_test.py` runs 13 languages: English plus 10 Indian, Chinese and French; A71)
    - Now: And this isn't one lucky sentence. We ran the same test on more than a thousand sentences, each one in twelve languages.
    - New: And this isn't one lucky sentence. We ran the same test on more than a thousand sentences, each one in thirteen languages.

13. **L70** (overstated. Sarvam's chopper is still 1.2–1.6 times English, and Telugu is 1.45. It is also not new: Sarvam's own 2024 model, Sarvam-1, already read Telugu at 1.15. Our vocabulary check shows Sarvam's chopper keeps 91.3% of Google's Gemma 3 vocabulary, with about 22,800 pieces swapped for Indian scripts: Telugu pieces go from 1,764 to 4,284 and Odia from 100 to 3,428. So the true reason is that an Indian team added the missing pieces; A73)
    - Now: Now a machine reads your language almost as cheaply as English. Because this time... it was built by people who speak it.
    - New: So for your language, the gap shrinks, a lot. Because this time... an Indian team put the missing pieces in.

14. **L73** (outdated. 671 billion is DeepSeek-V3 from December 2024. DeepSeek-V4-Pro, released April 2026, has 1.6 trillion parameters in total, which is 15.2 times Sarvam's 105 billion; A76)
    - Now: DeepSeek's big model has six hundred and seventy-one billion of those dials in total. More than six times Sarvam's.
    - New: DeepSeek's newest big model has one point six trillion of those dials in total. About fifteen times Sarvam's.

15. **L76** (wrong. The twenty proposals picked from 506 applications include Sarvam's 30B and 105B and BharatGen. PIB factsheet of 13 Aug 2026, and the minister's reply of July 2026; A78)
    - Now: What's next? The IndiaAI Mission has picked twenty more Indian proposals to build models. And BharatGen's mandate is to keep scaling, all the way up to a trillion dials.
    - New: What's next? The IndiaAI Mission has now picked twenty Indian proposals to build models, Sarvam and BharatGen among them. And BharatGen's mandate is to keep scaling, all the way up to a trillion dials.

16. **L79** ("the giants" is too broad. Google's Gemma 3 chopper, which is the same as Gemini 2.0's, reads Tamil in exactly the same 39,830 pieces as Sarvam and Bengali in 32,836 against Sarvam's 32,840. Against the two choppers the film actually shows, Sarvam is cheaper in all four languages; A80)
    - Now: But today, there's an Indian machine that reads Telugu, Tamil, Bengali and Odia more cheaply than the giants do.
    - New: But today, there's an Indian machine that reads your Telugu, Tamil, Bengali or Odia more cheaply than Chat G.P.T. and DeepSeek do.

**Blocks to record again (Akash):** whichever blocks hold L9, L17, L26, L27, L37, L48, L49, L51, L52, L61, L64, L68,
L70, L73, L76 and L79. With all 16 replacements applied to a scratch copy of `vo.txt`,
`scripts/spoken_english_check.py` passes (2,020 words, about 808 s at 150 wpm). The real `vo.txt` was not edited.

## Required on-screen fixes (picture, not VO)

- **Library tower:** 923,409,281 ÷ 400,109 = **2,308** English pages per Telugu page, not the 2,313 in `research.md`
  and `treatment.md`, which came from the rounded percentages. Tag it `OCT 2026`, because the ratio moves between crawls (1,645–2,647).
- **Common Crawl tag:** `COMMON CRAWL'S OWN COUNT (CLD2) · CC-MAIN-2026-43`, not `OUR COUNT`. English is 42.56%; never show 43.
- **Hundred-times stack:** ₹13 lakh crore against ₹10,372 crore is about **124–133 bricks**, not 100. Tag
  `META 2026 CAPEX GUIDE $135–145 BN [META, 21 OCT 2026] · ₹94.91/$ (2 NOV 2026)`.
- **Nvidia:** `$592.7 BN ≈ ₹51 LAKH CRORE [REUTERS · ₹86.31/$ ECB, 27 JAN 2025]`. Budget: `₹50.65 LAKH CRORE [BUDGET 2025-26]`.
- **DeepSeek cost:** `DEEPSEEK'S OWN FIGURE · FINAL TRAINING RUN · AT $2 PER GPU-HOUR`.
- **Meters:** `DEEPSEEK CHOPPER (V3–V4.1)`, `CHATGPT CHOPPER (o200k)`, `SARVAM CHOPPER (105B)`; test tag
  `OUR TEST · FLORES-200 · 1,012 SENTENCES × 13 LANGUAGES`. Show the split ఊ as one letter cut into two pieces (2 bytes + 1 byte).
- **GPU pool:** `18,693 LINED UP · JAN 2025 → 45,000+ · JUNE 2026 [PIB]`.
- `treatment.md` still says "about ten months" (angle B), "a hundred times" (logline) and "₹10 lakh crore as a wall".
  Fix these to match the VO.

## Rows marked `claim` (the VO already attributes each one)

- A08: the film's rule, *a machine speaks best in the language of the people who built it* (L6, L77). It is our framing; see the optional wording below.
- A12: *OpenAI says* India is one of its biggest markets (L9). Altman said second-largest user base.
- A15: *DeepSeek says* the final training run cost about $5.5 million (L14). This is DeepSeek-V3 at an assumed $2 per GPU-hour, excluding research.
- A55: *DeepSeek says* about two thousand chips (L54). The paper says 2,048 H800s.
- A60: *critics ask* (L58). Our paraphrase of the doubt. The documented critic, Deedy Das, called it "a 24B Mistral small post trained on Indic data".
- A74: *Sarvam says* its models help run Aadhaar services (L71). UIDAI–Sarvam deal of March 2025, one year and extendable; the extension was not found.
- A77: *Sarvam says it plainly* (L74). The exact sentence is "The newest models from other labs are trained with significantly larger clusters and budgets."

## Our measurements (re-run and method check)

- `tools/token_test.py` and `tools/token_example.py` were re-run on the scratchpad files. Their outputs are **identical** to
  `research/token_test_flores200.json` and `research/token_example.txt`.
- **The tokenizer files are the right ones.** Sarvam 30B and 105B ship the same `tokenizer.json`, and both repos have LFS
  sha256 `a574ceaa…`, matching ours. BharatGen Param2 is `3451f6a1…` (matches), and DeepSeek-V3's git blob is `51083c60…` (matches).
- **o200k_base is ChatGPT's chopper.** OpenAI's own tiktoken (main branch) maps gpt-4o, gpt-4.1, o1, o3, o4-mini and
  every `gpt-5` model to `o200k_base`. `o200k_harmony` gives the same counts.
- **DeepSeek's chopper has not changed.** V3.1, R1-0528, V3.2, V4-Pro and V4.1-Flash give identical counts (25 / 8 / 7, and all
  1,012 FLORES sentences), so "on DeepSeek" holds for DeepSeek's current models.
- **The translation is fair.** Five other natural Telugu wordings, such as గ్రామంలో, నా ఊరిలో, ఊర్లో, వాన and కురుస్తుందా, give 14–15 /
  11–12 / 23–27 pieces on o200k / Sarvam / DeepSeek. Chinese gives 7 on DeepSeek in all three wordings. The used sentence
  is everyday Telugu (మా ఊరు = my village), but the owner should still confirm it as a Telugu reader.
- **New tool:** `tools/token_factcheck.py` produces `research/token_factcheck.txt`. It covers DeepSeek versions, earlier choppers
  (Sarvam-1, Param-1, Krutrim-1, Gemma 3), the Sarvam–Gemma vocabulary overlap, the alternative translations, and the
  byte splits. Download commands are in its docstring.
- **Common Crawl was re-checked:** `languages.csv`, CC-MAIN-2026-43, is the latest crawl (2.16 billion pages, crawled 5–18 Oct). Its
  figures are English 42.5647%, Telugu 0.0184%, all Indian codes 0.570% (0.574% with every South Asian code), and 2,308 English pages per Telugu page.
- **Rupees:** the ECB rate was ₹86.31 a dollar on 27 Jan 2025 and ₹94.91 on 2 Nov 2026. Nvidia's loss is ₹51.2 lakh crore against a Union Budget
  of ₹50.65 lakh crore. Meta's guidance is ₹12.8–13.8 lakh crore, which is 124–133 times ₹10,371.92 crore.

## Optional suggestions (not wrong, just tighter or richer)

- L6 / L77: our test has a counterexample, because Google's chopper reads Hindi, Tamil and Bengali as cheaply as Sarvam's.
  The line works as the narrator's rule. A softer version: *A machine speaks best in the languages its makers care about.*
- L12: "why India doesn't have its own yet". The film later shows India's own model, so consider *To see why India is so far behind, you have to go back to one Monday.*
- L28: *English? More than forty-two out of every hundred pages.* (42.56%.)
- L30: *At the last census, Telugu was the mother tongue of around eight crore people.* Census 2011 is the latest. Hindi's 52.8 crore is the Hindi language group; Hindi as a mother tongue alone is 32.2 crore.
- L49, for clarity: *But in twenty twenty-four, one American company, Meta, said that by the end of that year it would have…*
- L58: *And critics point out it's a French model with Indian training on top. So how Indian is it?* This keeps L59's "Fair question".
- A signature beat, sourced by A73, after L69: *And here's what we found. Sarvam's chopper started from Google's... then swapped
  about twenty-three thousand foreign pieces for Indian ones.* It credits Sarvam's work. It is our own finding, which Sarvam
  does not state, so it is the owner's call.
- If the January 2025 story should keep 671 billion: *The DeepSeek model from that Monday had six hundred and seventy-one
  billion of those dials. Its newest has one point six trillion.*
- L81 names Sarvam's Indus app, which TechCrunch on 20 Feb 2026 called "available in beta". That conflicts with the treatment's no-promotion line, so it is the owner's call; check the app is open to all before upload.
- The cut Stanford line (v1 L24) was imprecise. If it comes back, use the AI Index 2026, section 7.4: *Stanford University's A.I. report puts India first in the world for A.I. skills on LinkedIn profiles — almost three times the world average.*
- L84, "I read every one", is the owner's own promise. It was not checked.

## Re-check before upload

- The rupee rate. If it falls below about ₹92 a dollar, L51 and L52 should say *around twelve lakh crore*. Meta's next guidance is due late January 2027.
- L10 "about now" holds for a November 2026 release. After that, change it to *has already run out*.
- New DeepSeek or OpenAI models. Re-run section 1 of `token_factcheck.py`, and check `tiktoken/model.py`.
- A new official IndiaAI GPU count (L48, L49), the live AI Kosh count (L37), and Indus availability (L81).
- L18 "just before minute ten" must match the final cut.

## Sources I could not open (worked around)

- reuters.com was blocked. I used the Reuters text via ThePrint and Malay Mail, plus AFP via The Manila Times.
- Deccan Herald and Business Standard returned 403. I cited them as reported, and used other reports.
- pib.gov.in returned 403 to WebFetch. I fetched it with curl, and read 2097709 through the PSA copy.
- openai.com returned 403. I used OpenAI's tiktoken repository instead.
- federalregister.gov redirected. I used its API instead.
- The UIDAI PDF reset the connection. I used Inc42 (18 Mar 2025) instead.
- index.commoncrawl.org reset the connection. I used commoncrawl.org/latest-crawl instead.
- google/gemma-3-27b-it is gated. I used the unsloth copy, which has the same 33,384,568-byte size.
- The Forbes India caption could not be found.
- The GitHub API is not enabled for openai/tiktoken. Raw file access worked.
