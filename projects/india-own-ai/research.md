# Research leads: Can India Build Its Own ChatGPT? (writer's notes, 2026-11-03)

Leads for the fact-check (`/fact-check` writes `claims.csv`). Each row: what the VO says → source → quote or
measurement. **Bold** = our own measurement (re-run the tool to verify; it is the film's original research).

## Our own measurements (re-runnable)

**Token test.** `tools/token_test.py` on FLORES-200 devtest (Meta/NLLB, CC BY-SA 4.0,
`https://dl.fbaipublicfiles.com/nllb/flores200_dataset.tar.gz`), 1,012 sentences, identical meaning in each language.
Tokenizers: OpenAI `o200k_base` (GPT-4o and later; tiktoken) and `cl100k_base` (GPT-4), and the `tokenizer.json` files
on Hugging Face for `sarvamai/sarvam-30b` (same file as `sarvam-105b`, 33,627,251 bytes each),
`bharatgenai/Param2-17B-A2.4B-Thinking`, `deepseek-ai/DeepSeek-V3`, `Qwen/Qwen3-8B`. Totals in
`research/token_test_flores200.json`. Ratio = language tokens ÷ the same tokenizer's English tokens.

| Language | o200k (ChatGPT) | cl100k (GPT-4) | Sarvam | BharatGen | DeepSeek V3 | Qwen3 |
|---|---|---|---|---|---|---|
| English | 26,873 (1.00) | 27,182 | 27,122 | 32,639 | 27,041 | 27,621 |
| Hindi | 1.57 | 4.76 | 1.31 | 1.14 | 2.80 | 4.42 |
| **Telugu** | **1.93** | 8.29 | **1.45** | 1.27 | **3.74** | 6.99 |
| Tamil | 1.98 | 7.64 | 1.47 | 1.29 | 3.07 | 6.11 |
| Kannada | 1.97 | 8.86 | 1.51 | 1.31 | 3.69 | 6.92 |
| Malayalam | 1.96 | 8.94 | 1.63 | 1.35 | 4.42 | 7.23 |
| Bengali | 1.70 | 5.80 | 1.21 | 1.24 | 2.02 | 5.03 |
| Marathi | 1.82 | 5.06 | 1.40 | 1.12 | 3.00 | 4.62 |
| Gujarati | 1.79 | 7.66 | 1.50 | 1.30 | 3.86 | 6.74 |
| **Odia** | **4.98** | 12.40 | **1.43** | **1.28** | **5.55** | 9.70 |
| Punjabi | 2.62 | 7.85 | 1.56 | 1.46 | 4.48 | 7.28 |
| **Chinese** | 1.25 | 1.87 | 1.08 | 1.40 | **0.94** | 1.00 |
| French | 1.37 | 1.61 | 1.41 | 1.71 | 1.55 | 1.58 |

Note for honesty: BharatGen's ratios look lowest partly because its English count is higher (32,639); in absolute
counts Sarvam is lowest for Telugu (39,400 vs BharatGen 41,522, o200k 51,863, DeepSeek 101,201). VO says BharatGen
"does about as well" for Odia (Sarvam 38,802 vs BharatGen 41,937 absolute; 1.43 vs 1.28 ratio): true either way.

**Example sentence** (`tools/token_example.py`, output `research/token_example.txt`): "Will it rain in my village
tomorrow?" / Telugu "రేపు మా ఊరిలో వర్షం పడుతుందా?" (literally "tomorrow, in our village, will rain fall?") /
Chinese "明天我们村会下雨吗？". DeepSeek V3: en 8, te 25, zh 7. o200k: en 8, te 15. Sarvam: en 8, te 11. The DeepSeek
pieces include byte fragments of single Telugu letters (ఊ → two bytes shown as `' �','�'`; ో, ్ similarly): "cuts some
Telugu letters in half" is literal. Translation to be checked by a Telugu reader (the owner).

**Common Crawl language count.** `https://raw.githubusercontent.com/commoncrawl/cc-crawl-statistics/master/plots/languages.csv`,
crawl `CC-MAIN-2026-43` (October 2026): total 2,169,426,757 pages; English 923,409,281 (42.56%); Telugu 400,109
(0.0184%) → 2,308 English pages per Telugu page (fact-check: 923,409,281 ÷ 400,109); Hindi 0.2111%; Tamil 0.0434%; Odia 0.0064%; all Indian languages
(hin tel tam ben mar kan mal guj ori pan urd asm san nep) 0.570% → "less than one page in every hundred". Primary
language as detected by CLD2 (Common Crawl's method). Common Crawl blog lists the October 2026 crawl.

## Sources for the VO

- **Common Crawl in GPT-3:** Brown et al. 2020, "Language Models are Few-Shot Learners", arXiv 2005.14165, Table 2.2:
  Common Crawl (filtered) 60% of the training mix. VO: "The makers of Chat G.P.T. trained an early model on it."
- **ChatGPT Go free year:** OpenAI announcement 28 Oct 2025 (TechCrunch 27 Oct 2025
  `https://techcrunch.com/2025/10/27/openai-offers-free-chatgpt-go-for-one-year-to-all-users-in-india/`; Business
  Today 28 Oct 2025): free for 12 months for users in India who sign up during a promotional period from 4 Nov 2025.
  "One of its biggest markets": OpenAI / Outlook Business ("one of ChatGPT's largest and fastest-growing markets").
- **DeepSeek day, 27 Jan 2025:** Reuters 27 Jan 2025 `https://www.reuters.com/markets/us/nasdaq-futures-tumble-chinas-ai-push-rattles-big-tech-2025-01-27`:
  "Nvidia (NVDA.O) sank 17%, and it erased about $593 billion in stock market value, the deepest ever one-day loss for a
  company on Wall Street"; "DeepSeek's AI Assistant by Monday had overtaken U.S. rival ChatGPT in downloads from
  Apple's (AAPL.O) App Store." Bloomberg: $589 billion. VO: "around five hundred and ninety billion".
- **Rupee conversion (our calculation):** $593 bn × ~₹86.5/$ (RBI reference rate late Jan 2025, to verify) ≈ ₹51.3
  lakh crore → "about fifty lakh crore". **Union Budget 2025-26** total expenditure ₹50,65,345 crore (Budget at a
  Glance, 1 Feb 2025) → "roughly the size of India's whole Union Budget for that year".
- **DeepSeek-V3 paper** arXiv 2412.19437: "DeepSeek-V3 is trained on a cluster equipped with 2048 NVIDIA H800 GPUs";
  "Assuming the rental price of the H800 GPU is $2 per GPU hour, our total training costs amount to only $5.576M. Note
  that the aforementioned costs include only the official training of DeepSeek-V3, excluding the costs associated with
  prior research and ablation experiments"; 671B total parameters, 37B activated. H800 = export-compliant (cut-down
  interconnect) version made for China (Nvidia/Reuters 2023, to cite). R1 (the Jan 2025 app model) is built on V3.
- **"American giants were spending billions":** e.g. Meta 2024 capex ~$39 bn (Meta 10-K 2024), Microsoft ~$80 bn
  planned for FY2025 (Microsoft blog, Jan 2025).
- **Vaishnaw, 30 Jan 2025:** Firstpost / ET CIO 30 Jan 2025: "18,693 graphics processing units (GPUs) have been
  empanelled"; India to build own foundational models; Inc42 / others: "in the next 10 months". PIB release of
  30 Jan 2025 to cite. VO: "reports say he gave it about ten months".
- **Stanford AI Index:** AI Index (2024 and/or 2025, LinkedIn data): India ranks first in relative AI skill penetration
  (to verify the year; if not supported, cut the sentence).
- **Census 2011 mother tongue:** Telugu 81.1 million ("around eight crore"); Hindi 528 million ("more than fifty crore").
- **India's share of the world's people:** UN World Population Prospects 2024: India ~1.46 bn of ~8.2 bn (2025) =
  ~17.8% → "more than one in every six".
- **AI Kosh:** PIB factsheet (2026) `https://www.pib.gov.in/FactsheetDetails.aspx?Id=150860&reg=3&lang=3`: "As of July
  2026, AI Kosh hosts over 14,000 datasets and 331 AI models".
- **GPU price "lakhs of rupees":** H100 list ~$25,000–40,000 (to cite: HF blog "NVIDIA H100 Price in India 2026").
- **Made in Taiwan:** Nvidia designs, TSMC manufactures (Nvidia 10-K: "We utilize foundries, such as TSMC…").
- **US AI Diffusion rule:** BIS interim final rule, published 15 Jan 2025 (Federal Register 90 FR 4544), three tiers;
  India in the middle tier with caps on advanced GPUs; rescinded 13 May 2025 (BIS press release
  `https://media.bis.gov/sites/default/files/documents/05.07 Recission of AI Diffusion Press Release.pdf`). "Its closest
  allies could buy freely" = Tier 1 (18 countries) exempt; "China was blocked" = Tier 3 (arms-embargoed incl. China).
  Biden left office 20 Jan 2025 → "just days before leaving office".
- **IndiaAI compute pool:** 18,693 GPUs (30 Jan 2025, above); "45,000+ GPUs, as of June 2026" (PIB factsheet above);
  government pays part (subsidy up to 40%, IndiaAI compute portal; to cite).
- **IndiaAI Mission outlay:** ₹10,371.92 crore over five years, Cabinet 7 Mar 2024 (PIB).
- **Meta 350,000 H100s:** Mark Zuckerberg, 18 Jan 2024 (Instagram/Threads video; Reuters/The Verge): "by the end of
  this year we're going to have around 350,000 Nvidia H100s". 350,000 ÷ 45,000 = 7.8 → "almost eight times".
- **Meta 2026 capex:** Q4 2025 results (Jan 2026): $115–135 bn; raised to $125–145 bn at Q1 2026 (Fortune 29 Apr 2026).
  ≥ $115 bn × ~₹88/$ ≈ ₹10.1 lakh crore → "more than ten lakh crore". ₹10.1 lakh crore ÷ ₹10,372 crore ≈ 98;
  at $125–145 bn, 106–123 → "about a hundred times". (Exchange rate at publish to verify; "much of it for A.I." per
  Meta's own guidance on AI infrastructure.)
- **Sarvam picked, April 2025:** PIB 26 Apr 2025 (first of the foundation-model proposals; to cite);
  IndiaAI: 4,096 H100 GPUs for six months (subsidy ₹98.68 crore of ₹246.71 crore; secondary: aiwiki/IASGyan) → "about
  four thousand". Founders Vivek Raghavan and Pratyush Kumar (AIM, Forbes India).
- **Sarvam-M on Mistral, May 2025:** Business Standard 19 Feb 2026: "Sarvam-M, the company's earlier model which was
  released in May 2025. It was built on top of Mistral Small, a base model developed by French AI firm Mistral."
  Criticism: Towards AI ("it drew criticism. If the foundation is foreign, how sovereign is the AI, really?").
- **Sarvam 105B launch:** India AI Impact Summit, Bharat Mandapam, 18 Feb 2026 (Business Standard 19 Feb 2026; Forbes
  India photo caption: "Sarvam's Co-Founder Pratyush Kumar at the launch"). Sarvam blog
  `https://www.sarvam.ai/blogs/sarvam-30b-105b`: "trained from scratch … Training was conducted entirely in India on
  compute provided under the IndiaAI mission"; "16T tokens for the 30B and 12T tokens for the 105B"; Apache 2.0;
  open weights on Hugging Face (`sarvamai/sarvam-105b`, created 3 Mar 2026). Quote for the honest gap: "The newest models
  from other labs are trained with significantly larger clusters and budgets."
- **About a year:** 30 Jan 2025 → 18 Feb 2026 = 12.6 months.
- **BharatGen Param2:** BharatGen blog 17 Feb 2026 `https://bharatgen.com/blogs/param2-what-we-built`: "Param2 is a
  mixture-of-experts language model with 17 billion parameters … We built it from scratch … It covers all 22 scheduled
  Indian languages and English"; IIT Bombay-led consortium.
- **Aadhaar:** Forbes India (Feb 2026): Sarvam "detailed major public sector deployments: Powering UIDAI's Aadhaar
  services with multilingual voice interaction and fraud detection" → VO "Sarvam says".
- **Maharashtra:** launched 28 Oct 2026 by CM Devendra Fadnavis, 2,500 state officials (AIM Network, 2 Nov 2026;
  ET on Sarvam's Indus workspace).
- **671B:** DeepSeek-V3 paper; 671 ÷ 105 = 6.4 → "more than six times".
- **Twenty more proposals:** PIB factsheet: "From 506 applications received, the Government has selected 20 indigenous
  foundation model proposals, including 12 Large Multimodal Models and 8 Small Language Models." (Check whether the 20
  include Sarvam; VO says "twenty more Indian proposals" → may need "twenty Indian proposals".)
- **BharatGen trillion:** The Federal (Feb 2026), Prof Ganesh Ramakrishnan: "Our runway is towards one-trillion-parameter
  models. That is the mandate under the IndiaAI Mission."
- **NavIC bridge:** India's regional navigation system (ISRO). The next film checks the phone question.

## Leads not used (and why)
- India "1.6% of global compute" (Epoch AI via OfficeChai): not confirmed in a primary source.
- xAI Colossus 555,000 GPUs: blog figures only.
- Sarvam's Token Factory hosting DeepSeek/GLM models (Sarvam docs): true, but easily misread as a dig at an Indian
  company; not needed.
- IndiaAI GPU price ₹65/hour: sources differ (₹65–100); not needed.
