# Treatment: Can India Build Its Own ChatGPT?

*India's Missing Pieces, episode 5 (after chips, rare earth magnets, jet engine, pharma). English, Akash (Eleven v4).
About 11 minutes, set by the story. Draft 1, 2026-11-03 (★ = chosen). Topic picked by the owner on 2026-11-03
("Sovereign AI"), and promised by the pharma film's last line: "India writes software for the whole world. So why is
India's own A.I. still so far behind?"*

**Logline.** Ask an A.I. "Will it rain in my village tomorrow?" In English it reads 8 pieces. In Telugu, DeepSeek's
machine reads 25, and cuts Telugu letters in half to do it; in Chinese, 7. A machine speaks best in the language of the
people who built it. So India set out to build its own, and in February 2026 a Bengaluru team showed one, trained from
zero on shared Indian chips. Its chopper reads the same Telugu question in 11. **But can India keep up with rivals
spending a hundred times more?**

**Tension:** pride (we write the world's software) against dependence (every chatbot we use was built abroad, reads our
languages at a markup, and runs on chips we can't make or freely buy), resolved as a live bet, not a verdict.

**Our own research is the spine.** We measured it ourselves: 1,012 sentences of the FLORES-200 benchmark, the same
sentences in 12 languages, through six real tokenizers (`tools/token_test.py`, `research/token_test_flores200.json`),
and the language mix of the October 2026 Common Crawl (`research.md`). Nobody else on YouTube can show this, and it
turns "sovereign AI", an abstract word, into a meter the viewer can see.

## Angles considered
| | Angle | Verdict |
|---|---|---|
| ★ A | **The language tax.** One village question, chopped into pieces; the chopper learns from a library that is 0.02% Telugu; India builds its own library, rents a reading room, and its own machine reads Telugu at under half DeepSeek's count. | Best: an original measurement, a felt mechanism, Telugu/Tamil/Odia viewers see their own script on screen, and a proud but honest payoff |
| B | **The ten-month promise.** 30 Jan 2025 the minister says India will have its own model "within six months" (PIB), later "ten at the most"; 18 Feb 2026 Sarvam 105B. Did India deliver? | A good spine for chapter 5, not a film: the answer is "yes, a bit late", so no tension left |
| C | **DeepSeek on a budget.** How a Chinese lab did it with ~2,000 restricted chips. | Foreign hero; becomes the hope beat in chapter 4 ("you need the cleverest engineers, not the biggest room") |
| D | **Why is ChatGPT free in India?** The free Go year from 4 Nov 2025 runs out from this month. | Strong news hook and a lived-memory anchor, but a business story; it becomes the 0:30 anchor and the plant for the ending |

**Why ours is different** from the summit news clips (launch, no mechanism), the "Sarvam vs ChatGPT" demo videos
(features, no why) and the "India's AI mission explained" exam-prep videos (lists of schemes): we make the viewer **see**
the machine reading their language, show **why** it does (the library), what India can't control (the chips), and end
on the same meter, now Indian.

## Cold opens considered
1. ★ **The chopping test (0:00–0:25).** A phone, a village question typed in English: eight glowing pieces drop into a
   meter. The same question in Telugu: twenty-five pieces, two of them a single letter cut in half. Chinese: seven.
   "A machine speaks best in the language of the people who built it." Then the title question at ~0:22.
2. The DeepSeek day, 27 Jan 2025: Nvidia loses about $593 billion in a day, about India's whole Union Budget for the
   year. Spectacular, but foreign and a stock-market scene; it moves to ~0:50 as the "why now".
3. Bharat Mandapam, 18 Feb 2026: the launch on stage. Ends the story before it starts; kept for chapter 5.

## Shape (chapter names = search phrases)
0:00 **Can India build its own ChatGPT?** (chopping test; free year anchor; DeepSeek day; the ten-month promise; open
loop: "just before minute ten, the same test on an Indian machine") → 1:50 **How ChatGPT actually works** (the child who
read a library; three ingredients: library, reading room, teachers) → 3:05 **Why AI is weak in Indian languages** (the
library count: 2,300 English pages for each Telugu page; why the chopper splits letters; AI Kosh) → 4:50 **India's GPU
problem** (one chip, lakhs of rupees; India makes none; the January 2025 US rule; the shared pool 18,693 → 45,000+;
Meta's 350,000; ₹10,000 crore vs ~₹13 lakh crore; DeepSeek's 2,048 cut-down chips) → 7:05 **What India built: Sarvam
and BharatGen** (April 2025 pick; the French-base criticism; Bharat Mandapam 2026; the meter again; Odia; Aadhaar,
Maharashtra) → 9:30 **Has India caught up?** (671B vs 105B; Sarvam's own admission; the trillion-dial mandate; 20 more
teams; the lesson; what it means for you) → outro: bridge to NavIC, pinned-comment challenge.

**Feelings:** start: a small sting of injustice (my language costs more?); low point at ~6:10: the hundred-times money
gap in silence; end: sober pride, a Telugu question lighting up eleven pieces on an Indian machine, and a challenge the
viewer can try tonight.

## Art direction (fresh for this film)
**"The reading room."** Warm library amber and paper against the cold blue-black of a data hall. Colour = meaning:
**paper amber** = words, the library; **chip green** = compute, the reading room; **saffron** = Indian-built;
**foreign grey-blue** = machines built abroad; **red cut** = a letter split in half. Signature device: the **PIECE METER**,
a small counter in the top left that drops one glowing tile for every token, the language name beside it, with the
tokenizer named ("DEEPSEEK CHOPPER"). Texture: macro of Telugu, Tamil and Odia print (newspaper, palm-leaf, school
slate), server-hall footage, GPU macro, document push-ins (PIB factsheet, the DeepSeek paper, the US Federal Register
rule, Sarvam's model card).

## Signature moments
1. **The letter cut in half** (~0:10): the Telugu tile for ఊ splits down the middle into two dead grey shards (real
   byte pieces from the DeepSeek tokenizer, `research/token_example.txt`). The image the film is remembered by.
2. **The library to scale** (~3:40): a single Telugu page on a desk; the camera pulls back as 2,308 English pages stack
   beside it into a tower, counted live (to scale; "COMMON CRAWL'S OWN COUNT, OCT 2026").
3. **The meter again** (~9:35): the same village question, three machines side by side: 25, 15, 11. Then the Odia bar
   collapses from 5.5× to 1.4×. Silence, then a single saffron chime.
4. Supporting: the hundred-times stack (₹10,000 crore as one brick, about ₹13 lakh crore as a wall of 124–133 bricks), animated, never written.

## Sound
Room tone of a library (page turns, a clock), cooling-fan roar of a data hall, a soft tile "tick" for each token (the
meter's own sound, pitched lower for broken pieces), a warm sitar-and-synth pad that only resolves in chapter 5;
silence before the hundred-times reveal and before the meter returns. Open sources first (Pixabay, Freesound CC0),
ElevenLabs sound effects only where nothing fits (owner, 2026-11-03).

## Package (brief)
- **Main search phrase:** `india own ai model` / `indian chatgpt` (autocomplete, `research/search_terms.md`).
- **Title ★:** `Can India Build Its Own ChatGPT? | Be Practical With Kishore` (alt: `India's Own ChatGPT: Why
  Telugu Costs 3× More | …`; `Why Every AI Charges Extra for Indian Languages | …`).
- **Thumbnail concepts** (each through `thumb_feed.py` + an independent click panel):
  ★ T1 **"8 vs 25"**: a phone screen, the same question in English and Telugu, the Telugu one bursting into many glowing
  tiles; one Telugu letter cracked in half. Text: `SAME QUESTION?` T2 **"CUT IN HALF"**: a giant Telugu letter ఊ split
  down the middle like broken glass, a chip glowing behind it. Text: `WHY?` T3 **"MADE IN INDIA?"**: a GPU with a
  saffron tricolour glow and a padlock. (T3 risks implying India makes GPUs; keep only with a clear question mark.)
- **For:** Indian viewers 18–40 who use ChatGPT/Gemini, watch Think School, Mohak Mangal and our chip and pharma films;
  South Indian viewers see their own script.

## Hard lines in this film
No product promotion: Sarvam, BharatGen, OpenAI and DeepSeek are named for what documents say they did; "try more
than one, in your own language" is the only advice. Benchmarks are the companies' own claims and are said as claims.
Our token test is ours: method on screen, numbers exactly as measured, the example sentence shown as an example and
the averages as averages. No stock talk (Nvidia's loss is a news event, not advice). Real people (Vaishnaw, Raghavan,
Kumar, Ramakrishnan) only from real photos or footage with licences; no generated faces or voices. Never cynical about
India: the gap is named plainly, the builders get their due.
