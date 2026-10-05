# Denominators by topic (v2)

Generated 2026-10-05. Each OUTLET counts once per scope, even if it published several reviews in that scope (only The Guardian has two documents in one scope: Pro and Pro XL).

**How to read:** `addressed` is the denominator. praised / criticised / mixed / neutral are disjoint and add up to it. `mixed` = the outlet both praised and criticised that point; `neutral` = mentioned it without a verdict (spec, description, or could not test).

Scope sizes (max possible denominator): base 10 outlets, Pro+Pro XL 15 outlets, Fold 9 outlets.

**Method and limits:** each document's re-fetched text (2026-10-05) was keyword-searched for the topic and the passages were read and labelled by hand; verified claims from the research JSON were used where they exist. 'Not addressed' means no passage was found: it is a lower bound on coverage, not proof the outlet ignored the topic. Labels are editorial judgements; the evidence excerpt for every label is in `denominators.json`.

## Display brightness / quality

_Quality/brightness only; refresh-rate and PWM are separate topics. Fold: displays excluding the crease._

**Base Pixel 11: 7 of 10 outlets addressed it** (mixed 1, praised 6)
- praised: Android Headlines, Engadget, GSMArena, PCMag, The Guardian, Tom's Guide
- mixed: Android Authority

**Pixel 11 Pro + Pro XL: 14 of 15 outlets addressed it** (praised 12, mixed 1, neutral 1)
- praised: Android Authority, Android Central, Android Headlines, Digital Trends, GSMArena, Gizmodo, Stuff, Tech Advisor, TechRadar, The Guardian, Tom's Guide, Trusted Reviews
- mixed: Android Police
- neutral: Engadget

**Pixel 11 Pro Fold: 8 of 9 outlets addressed it** (neutral 1, praised 6, mixed 1)
- praised: Android Central, Droid Life, Engadget, Tech Advisor, TechRadar, Tom's Guide
- mixed: BGR
- neutral: 9to5Google

## Base model: 60Hz default / no LTPO

_C = flags the 60Hz default or the lack of LTPO as a drawback._

**Base Pixel 11: 7 of 10 outlets addressed it** (criticised 3, neutral 4)
- criticised: 9to5Google, Android Authority, GSMArena
- neutral: Android Headlines, CNET, Engadget, PCMag

## PWM dimming

_No outlet praised PWM; every mention is a criticism._

**Base Pixel 11: 0 of 10 outlets addressed it** ()

**Pixel 11 Pro + Pro XL: 3 of 15 outlets addressed it** (criticised 3)
- criticised: Android Central, Android Headlines, Tech Advisor

**Pixel 11 Pro Fold: 1 of 9 outlets addressed it** (criticised 1)
- criticised: Android Central

## Everyday smoothness

_giz: latency in UI/agentic tasks; tapro: freezes and forced reboot (bugs)._

**Base Pixel 11: 10 of 10 outlets addressed it** (neutral 2, criticised 1, praised 7)
- praised: Android Central, Android Headlines, CNET, Engadget, GSMArena, PCMag, The Guardian
- criticised: Android Authority
- neutral: 9to5Google, Tom's Guide

**Pixel 11 Pro + Pro XL: 13 of 15 outlets addressed it** (praised 11, mixed 2)
- praised: Android Authority, Android Headlines, Android Police, Digital Trends, Engadget, GSMArena, Stuff, TechCrunch, TechRadar, The Guardian, Trusted Reviews
- mixed: Gizmodo, Tech Advisor

**Pixel 11 Pro Fold: 6 of 9 outlets addressed it** (praised 6)
- praised: 9to5Google, BGR, Engadget, Tech Advisor, TechRadar, Tom's Guide

## GPU / gaming

**Base Pixel 11: 8 of 10 outlets addressed it** (criticised 5, mixed 3)
- criticised: Android Authority, Android Central, Android Headlines, CNET, PCMag
- mixed: GSMArena, The Guardian, Tom's Guide

**Pixel 11 Pro + Pro XL: 13 of 15 outlets addressed it** (mixed 5, criticised 7, praised 1)
- praised: TechRadar
- criticised: Android Central, Android Headlines, Digital Trends, Gizmodo, Stuff, Tom's Guide, Trusted Reviews
- mixed: Android Authority, Android Police, GSMArena, Tech Advisor, The Guardian

**Pixel 11 Pro Fold: 8 of 9 outlets addressed it** (criticised 5, mixed 2, praised 1)
- praised: TechRadar
- criticised: 9to5Google, Android Authority, Android Central, BGR, Tech Advisor
- mixed: Engadget, Tom's Guide

## Heat / thermals

_P = runs cool / cooler than before. aapro C refers to heat during Extreme Charging, not workload heat. BGR (Fold review) also says the 11 Pro XL "got hot under heavy loads"; that is a remark in a Fold review and is not counted in the Pro scope._

**Base Pixel 11: 4 of 10 outlets addressed it** (criticised 2, praised 1, mixed 1)
- praised: Android Headlines
- criticised: Android Authority, Android Central
- mixed: GSMArena

**Pixel 11 Pro + Pro XL: 7 of 15 outlets addressed it** (criticised 2, praised 4, mixed 1)
- praised: Android Headlines, Android Police, Digital Trends, Trusted Reviews
- criticised: Android Authority, Gizmodo
- mixed: GSMArena

**Pixel 11 Pro Fold: 2 of 9 outlets addressed it** (praised 2)
- praised: 9to5Google, BGR

## Genshin Impact

_Software timing matters: giz (Aug 19) got Google statement that a fix was coming; GSMArena (XL updated Sep 5, base Sep 15) and Android Authority Fold (Sep 11) report it fixed after updates._

**Base Pixel 11: 2 of 10 outlets addressed it** (criticised 1, praised 1)
- praised: GSMArena
- criticised: Android Headlines

**Pixel 11 Pro + Pro XL: 4 of 15 outlets addressed it** (criticised 3, mixed 1)
- criticised: Android Headlines, Gizmodo, Tech Advisor
- mixed: GSMArena

**Pixel 11 Pro Fold: 1 of 9 outlets addressed it** (mixed 1)
- mixed: Android Authority

## Camera stills quality

**Base Pixel 11: 8 of 10 outlets addressed it** (praised 5, mixed 3)
- praised: Android Authority, Android Central, CNET, Engadget, The Guardian
- mixed: Android Headlines, GSMArena, Tom's Guide

**Pixel 11 Pro + Pro XL: 15 of 15 outlets addressed it** (praised 15)
- praised: Android Authority, Android Central, Android Headlines, Android Police, Digital Trends, Engadget, GSMArena, Gizmodo, Stuff, Tech Advisor, TechCrunch, TechRadar, The Guardian, Tom's Guide, Trusted Reviews

## Base model 5x telephoto

**Base Pixel 11: 9 of 10 outlets addressed it** (neutral 4, criticised 1, praised 3, mixed 1)
- praised: CNET, Engadget, The Guardian
- criticised: Android Headlines
- mixed: GSMArena
- neutral: Android Authority, Android Central, PCMag, Tom's Guide

## Night Sight speed (Pro)

_tgpro: faster but "isn't actually instant" (two seconds). Nobody criticised the speed._

**Pixel 11 Pro + Pro XL: 11 of 15 outlets addressed it** (praised 11)
- praised: Android Authority, Android Central, Android Headlines, Digital Trends, Engadget, Gizmodo, Stuff, TechCrunch, The Guardian, Tom's Guide, Trusted Reviews

## 120x Pro Zoom

**Pixel 11 Pro + Pro XL: 13 of 15 outlets addressed it** (criticised 8, mixed 4, praised 1)
- praised: Tom's Guide
- criticised: Android Authority, Android Headlines, Digital Trends, Engadget, Gizmodo, Stuff, TechCrunch, Trusted Reviews
- mixed: Android Central, Tech Advisor, TechRadar, The Guardian

## Magic Capture

**Base Pixel 11: 10 of 10 outlets addressed it** (praised 5, criticised 1, neutral 3, mixed 1)
- praised: 9to5Google, Android Authority, Android Central, Android Headlines, Tom's Guide
- criticised: CNET
- mixed: PCMag
- neutral: Engadget, GSMArena, The Guardian

**Pixel 11 Pro + Pro XL: 14 of 15 outlets addressed it** (neutral 4, praised 7, mixed 2, criticised 1)
- praised: Android Central, Digital Trends, Tech Advisor, TechCrunch, TechRadar, The Guardian, Tom's Guide
- criticised: Trusted Reviews
- mixed: Gizmodo, Stuff
- neutral: Android Authority, Android Headlines, Engadget, GSMArena

**Pixel 11 Pro Fold: 6 of 9 outlets addressed it** (praised 4, criticised 1, neutral 1)
- praised: Android Central, Engadget, TechRadar, Tom's Guide
- criticised: BGR
- neutral: Tech Advisor

## Camera Looks

**Base Pixel 11: 5 of 10 outlets addressed it** (mixed 1, neutral 2, praised 2)
- praised: The Guardian, Tom's Guide
- mixed: 9to5Google
- neutral: Android Authority, Engadget

**Pixel 11 Pro + Pro XL: 11 of 15 outlets addressed it** (praised 7, criticised 3, neutral 1)
- praised: Android Authority, Digital Trends, Gizmodo, Stuff, TechRadar, The Guardian, Trusted Reviews
- criticised: Android Police, Engadget, Tech Advisor
- neutral: TechCrunch

**Pixel 11 Pro Fold: 2 of 9 outlets addressed it** (praised 2)
- praised: Engadget, Tech Advisor

## Video quality

_Few outlets judged video at all; fta C = missing Log/APV/8K/4K120 (F059)._

**Base Pixel 11: 2 of 10 outlets addressed it** (neutral 1, praised 1)
- praised: The Guardian
- neutral: CNET

**Pixel 11 Pro + Pro XL: 6 of 15 outlets addressed it** (neutral 1, mixed 1, praised 3, criticised 1)
- praised: GSMArena, Tech Advisor, The Guardian
- criticised: Trusted Reviews
- mixed: Digital Trends
- neutral: Android Authority

**Pixel 11 Pro Fold: 1 of 9 outlets addressed it** (criticised 1)
- criticised: Tech Advisor

## Battery endurance

_See test_conditions.md: these verdicts rest on very different tests and usage patterns._

**Base Pixel 11: 10 of 10 outlets addressed it** (praised 9, criticised 1)
- praised: 9to5Google, Android Authority, Android Central, Android Headlines, CNET, Engadget, GSMArena, PCMag, The Guardian
- criticised: Tom's Guide

**Pixel 11 Pro + Pro XL: 14 of 15 outlets addressed it** (praised 9, criticised 4, mixed 1)
- praised: Android Authority, Android Headlines, Android Police, Engadget, GSMArena, Gizmodo, TechRadar, The Guardian, Trusted Reviews
- criticised: Android Central, Digital Trends, Tech Advisor, Tom's Guide
- mixed: Stuff

**Pixel 11 Pro Fold: 9 of 9 outlets addressed it** (criticised 7, mixed 1, praised 1)
- praised: TechRadar
- criticised: 9to5Google, Android Central, BGR, Droid Life, Engadget, Tech Advisor, Tom's Guide
- mixed: Android Authority

## Wired charging speed

**Base Pixel 11: 8 of 10 outlets addressed it** (criticised 3, neutral 4, mixed 1)
- criticised: 9to5Google, Android Authority, Tom's Guide
- mixed: GSMArena
- neutral: Android Headlines, CNET, PCMag, The Guardian

**Pixel 11 Pro + Pro XL: 12 of 15 outlets addressed it** (criticised 6, mixed 3, neutral 2, praised 1)
- praised: GSMArena
- criticised: Android Authority, Android Central, Android Police, Tech Advisor, Tom's Guide, Trusted Reviews
- mixed: Android Headlines, Stuff, TechRadar
- neutral: Digital Trends, The Guardian

**Pixel 11 Pro Fold: 7 of 9 outlets addressed it** (criticised 5, neutral 2)
- criticised: 9to5Google, Android Authority, Android Central, BGR, Tom's Guide
- neutral: Engadget, Tech Advisor

## Wireless charging / Pixelsnap

_pcm11 states the base model does "up to 15W wireless", which conflicts with Google spec (25W Qi2.2) and other reviews._

**Base Pixel 11: 9 of 10 outlets addressed it** (praised 6, neutral 3)
- praised: 9to5Google, Android Authority, Android Central, Android Headlines, CNET, Tom's Guide
- neutral: GSMArena, PCMag, The Guardian

**Pixel 11 Pro + Pro XL: 11 of 15 outlets addressed it** (praised 7, neutral 4)
- praised: Android Authority, Android Headlines, Gizmodo, Stuff, Tech Advisor, TechRadar, Trusted Reviews
- neutral: Android Police, Digital Trends, The Guardian, Tom's Guide

**Pixel 11 Pro Fold: 6 of 9 outlets addressed it** (praised 6)
- praised: 9to5Google, Android Central, BGR, Engadget, Tech Advisor, Tom's Guide

## Rambler dictation

**Base Pixel 11: 8 of 10 outlets addressed it** (mixed 1, praised 6, neutral 1)
- praised: Android Authority, Android Central, CNET, Engadget, The Guardian, Tom's Guide
- mixed: 9to5Google
- neutral: PCMag

**Pixel 11 Pro + Pro XL: 13 of 15 outlets addressed it** (praised 11, mixed 1, criticised 1)
- praised: Android Authority, Android Central, Digital Trends, Engadget, Gizmodo, Tech Advisor, TechCrunch, TechRadar, The Guardian, Tom's Guide, Trusted Reviews
- criticised: Stuff
- mixed: Android Police

**Pixel 11 Pro Fold: 3 of 9 outlets addressed it** (praised 3)
- praised: Engadget, Tech Advisor, Tom's Guide

## Proactive Assistance

_trxl and tapro could not test it in the UK (N)._

**Base Pixel 11: 7 of 10 outlets addressed it** (criticised 2, praised 3, neutral 1, mixed 1)
- praised: Android Central, Engadget, Tom's Guide
- criticised: Android Authority, GSMArena
- mixed: The Guardian
- neutral: PCMag

**Pixel 11 Pro + Pro XL: 11 of 15 outlets addressed it** (criticised 6, mixed 2, praised 1, neutral 2)
- praised: Gizmodo
- criticised: Android Authority, Android Central, Android Police, Stuff, TechCrunch, TechRadar
- mixed: Android Headlines, The Guardian
- neutral: Tech Advisor, Trusted Reviews

**Pixel 11 Pro Fold: 1 of 9 outlets addressed it** (criticised 1)
- criticised: Android Central

## Gemini features US-only / region-locked

_C = flags region limits as a drawback. All three are UK-based reviewers._

**Base Pixel 11: 1 of 10 outlets addressed it** (neutral 1)
- neutral: The Guardian

**Pixel 11 Pro + Pro XL: 3 of 15 outlets addressed it** (criticised 3)
- criticised: Stuff, Tech Advisor, Trusted Reviews

## HiLight

_Per Google spec the base Pixel 11 has no HiLight. aa11 says you "won't miss it"; ac11 lists "No HiLight" as a con; ah11 describes a HiLight LED on the base model and calls it useless (conflicts with spec)._

**Base Pixel 11: 4 of 10 outlets addressed it** (neutral 2, criticised 2)
- criticised: Android Central, Android Headlines
- neutral: Android Authority, CNET

**Pixel 11 Pro + Pro XL: 15 of 15 outlets addressed it** (criticised 13, mixed 1, praised 1)
- praised: Digital Trends
- criticised: Android Authority, Android Central, Android Police, Engadget, GSMArena, Gizmodo, Stuff, Tech Advisor, TechCrunch, TechRadar, The Guardian, Tom's Guide, Trusted Reviews
- mixed: Android Headlines

**Pixel 11 Pro Fold: 6 of 9 outlets addressed it** (criticised 6)
- criticised: 9to5Google, Android Central, BGR, Engadget, Tech Advisor, TechRadar

## Price rise

_M = notes the rise but also a mitigating factor (doubled base storage, or undercuts rivals). tgpro text says both "$100 more" and "$200 price hike" (internal inconsistency)._

**Base Pixel 11: 7 of 10 outlets addressed it** (criticised 4, mixed 1, neutral 2)
- criticised: Android Authority, Android Central, Engadget, Tom's Guide
- mixed: GSMArena
- neutral: PCMag, The Guardian

**Pixel 11 Pro + Pro XL: 13 of 15 outlets addressed it** (criticised 12, mixed 1)
- criticised: Android Authority, Android Central, Android Police, Engadget, Gizmodo, Stuff, Tech Advisor, TechCrunch, TechRadar, The Guardian, Tom's Guide, Trusted Reviews
- mixed: Android Headlines

**Pixel 11 Pro Fold: 3 of 9 outlets addressed it** (mixed 3)
- mixed: Android Central, TechRadar, Tom's Guide

## 12GB base RAM (Pro)

_Review-unit RAM differs: giz tested 16GB units; dtpro a 12GB unit; engpro says the RAM cut is not yet an issue._

**Pixel 11 Pro + Pro XL: 15 of 15 outlets addressed it** (criticised 10, neutral 4, mixed 1)
- criticised: Android Authority, Android Central, Android Headlines, Android Police, Gizmodo, Tech Advisor, TechRadar, The Guardian, Tom's Guide, Trusted Reviews
- mixed: Engadget
- neutral: Digital Trends, GSMArena, Stuff, TechCrunch

## "Pixel 10 owners shouldn't upgrade"

**Base Pixel 11: 4 of 10 outlets addressed it** (agree 4)
- agree: 9to5Google, Android Authority, Engadget, Tom's Guide

**Pixel 11 Pro + Pro XL: 7 of 15 outlets addressed it** (agree 7)
- agree: Android Authority, Gizmodo, TechCrunch, TechRadar, The Guardian, Tom's Guide, Trusted Reviews

**Pixel 11 Pro Fold: 4 of 9 outlets addressed it** (disagree 1, neutral 1, agree 2)
- agree: Tech Advisor, TechRadar
- disagree: Android Central
- neutral: BGR

## "Base Pixel 11 is the value pick"

_faa recommends the Pixel 11 Pro XL (not the base model) over the Fold. tg11 says a discounted Pixel 10 is the smarter buy._

**Base Pixel 11: 7 of 10 outlets addressed it** (agree 5, neutral 2)
- agree: Android Authority, Android Headlines, CNET, PCMag, The Guardian
- neutral: Android Central, Tom's Guide

**Pixel 11 Pro + Pro XL: 1 of 15 outlets addressed it** (agree 1)
- agree: Android Authority

**Pixel 11 Pro Fold: 1 of 9 outlets addressed it** (neutral 1)
- neutral: Android Authority

## Fold: IP68

**Pixel 11 Pro Fold: 9 of 9 outlets addressed it** (praised 8, neutral 1)
- praised: 9to5Google, Android Authority, Android Central, BGR, Engadget, Tech Advisor, TechRadar, Tom's Guide
- neutral: Droid Life

## Fold: crease

_fta: improved vs Pixel 10 Pro Fold but worse than every other foldable tested this year._

**Pixel 11 Pro Fold: 7 of 9 outlets addressed it** (mixed 2, criticised 4, praised 1)
- praised: Droid Life
- criticised: Android Authority, BGR, Tech Advisor, Tom's Guide
- mixed: 9to5Google, TechRadar

## Fold: battery

**Pixel 11 Pro Fold: 9 of 9 outlets addressed it** (criticised 7, mixed 1, praised 1)
- praised: TechRadar
- criticised: 9to5Google, Android Central, BGR, Droid Life, Engadget, Tech Advisor, Tom's Guide
- mixed: Android Authority

## Fold: camera

**Pixel 11 Pro Fold: 9 of 9 outlets addressed it** (praised 2, criticised 2, mixed 5)
- praised: 9to5Google, BGR
- criticised: Android Authority, Droid Life
- mixed: Android Central, Engadget, Tech Advisor, TechRadar, Tom's Guide

## Fold: GPU / performance

**Pixel 11 Pro Fold: 8 of 9 outlets addressed it** (mixed 4, criticised 3, praised 1)
- praised: TechRadar
- criticised: Android Authority, Android Central, Tech Advisor
- mixed: 9to5Google, BGR, Engadget, Tom's Guide

## Fold: multitasking

**Pixel 11 Pro Fold: 9 of 9 outlets addressed it** (praised 6, mixed 1, criticised 2)
- praised: 9to5Google, Android Central, BGR, Engadget, TechRadar, Tom's Guide
- criticised: Droid Life, Tech Advisor
- mixed: Android Authority

