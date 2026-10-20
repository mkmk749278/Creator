#!/usr/bin/env python3
"""Spoken-English gate for English narration (PLAYBOOK §4a-10).

Measures a VO the way we measured the Indian explainer channels that hold viewers (study 2026-10-20) and fails
when the script drifts toward "read text": long sentences, no questions, no "you", no narrator, fancy words.

usage: python3 scripts/spoken_english_check.py projects/<slug>/vo.txt [--min-words 320 --max-words 390]
       (a script.tsv works too: the `en` column is read)
needs: pip install -e '.[script]'   (wordfreq, for the rare-word check)
"""
import argparse
import csv
import re
import sys

from wordfreq import zipf_frequency

# Words everyday Indian viewers know even though they are rare in global English text.
INDIAN_OK = {"rupee", "rupees", "lakh", "lakhs", "crore", "crores", "kirana", "chai", "salary", "emi", "upi", "qr",
             "debited", "credited", "shopkeeper", "recharge", "aadhaar", "pan", "kyc", "atm", "otp", "metro", "auto",
             "rickshaw", "scooty", "tiffin", "paise", "pin", "app", "apps", "paytm", "phonepe", "gpay", "bhim"}
# Fancy words that make narration sound like a textbook; say the plain word instead.
FANCY = {"utilize": "use", "utilise": "use", "commence": "start", "facilitate": "help", "subsequently": "then",
         "approximately": "about", "numerous": "many", "regarding": "about", "phenomenon": "thing", "conundrum": "puzzle",
         "endeavour": "try", "endeavor": "try", "ascertain": "find out", "terminate": "end", "sufficient": "enough",
         "obtain": "get", "require": "need", "purchase": "buy", "individuals": "people", "prior": "before",
         "however": "but", "therefore": "so", "thus": "so", "hence": "so", "moreover": "also", "furthermore": "also",
         "nevertheless": "still", "whereby": "where", "wherein": "where", "erratically": "strangely",
         "exasperating": "annoying", "initiate": "start", "remitter": "your bank", "beneficiary": "their bank",
         "transaction": "payment", "transactions": "payments", "mechanism": "how it works"}
YOU = {"you", "your", "you're", "you'll", "you've", "yours", "yourself"}
ME = {"i", "me", "my", "i'm", "i'll", "i've", "we", "us", "our", "let's", "we're", "we'll"}
CHECKINS = ("right?", "isn't it?", "no?", "simple, right?", "see,", "you know", "imagine", "tell me")


def sentences(text):
    parts = re.split(r"(?<=[.?!])\s+", text.replace("...", "… "))
    return [p.strip() for p in parts if re.search(r"[A-Za-z]", p)]


def words(s):
    return re.findall(r"[A-Za-z][A-Za-z'\-]*", s)


def load(path):
    if path.endswith(".tsv"):
        with open(path, newline="", encoding="utf-8") as f:
            return " ".join(r.get("en", "") for r in csv.DictReader(f, delimiter="\t"))
    return open(path, encoding="utf-8").read()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--min-words", type=int, default=320)
    ap.add_argument("--max-words", type=int, default=390)
    a = ap.parse_args()
    text = load(a.path)
    sents = sentences(text)
    ws = [w.lower().strip("-") for w in words(text)]
    n = len(ws)
    lens = [len(words(s)) for s in sents]
    fails, notes = [], []

    if not a.min_words <= n <= a.max_words:
        fails.append(f"{n} words, want {a.min_words}-{a.max_words}")
    avg = n / len(sents)
    if not 7.5 <= avg <= 14:
        fails.append(f"average sentence {avg:.1f} words, want 7.5-14 (creators: 11-13)")
    for s, l in zip(sents, lens):
        if l > 25:
            fails.append(f"sentence of {l} words (max 25): {s[:70]}…")
    for i in range(len(lens) - 2):
        if max(lens[i:i + 3]) - min(lens[i:i + 3]) <= 1 and min(lens[i:i + 3]) >= 6:
            notes.append(f"three same-length sentences in a row ({lens[i:i + 3]}): {sents[i][:50]}…")
    q = sum(s.endswith("?") for s in sents)
    if q / len(sents) < 0.10:
        fails.append(f"questions are {100 * q / len(sents):.0f}% of sentences, want >= 10% (creators: 12-22%)")
    you = 100 * sum(w in YOU for w in ws) / n
    if you < 3:
        fails.append(f"'you/your' {you:.1f} per 100 words, want >= 3 (creators: 2-6)")
    me = 100 * sum(w in ME for w in ws) / n
    if me < 1:
        fails.append(f"narrator 'I/me/we/let's' {me:.1f} per 100 words, want >= 1 (creators: 1-5)")
    low = text.lower()
    checks = sum(low.count(c) for c in CHECKINS)
    if checks < 2:
        fails.append(f"{checks} check-ins (right? / see, / imagine / tell me …), want >= 2")
    fancy = sorted({w for w in ws if w in FANCY})
    for w in fancy:
        fails.append(f"fancy word '{w}': say '{FANCY[w]}'")
    content = [w for w in ws if len(w) > 3 and w not in INDIAN_OK and not w.endswith("'s")]
    rare = sorted({w for w in content if zipf_frequency(w, "en") < 3.5})
    rare_pct = 100 * sum(w in rare for w in content) / max(1, len(content))
    if rare_pct > 4:
        fails.append(f"rare words {rare_pct:.1f}% of content words, want <= 4: {', '.join(rare[:12])}")
    elif rare:
        notes.append(f"rare words (explain each once in plain words): {', '.join(rare)}")
    if re.search(r'[0-9₹!"()\[\]]', text):
        fails.append("digits, ₹, !, double quotes or brackets in VO text")
    bare = sorted(set(re.findall(r"\b[A-Z]{2,}\b", text)))
    if bare:
        fails.append(f"bare capital acronyms (hyphenate for Akash): {', '.join(bare)}")

    print(f"{n} words · {len(sents)} sentences · avg {avg:.1f} · questions {100 * q / len(sents):.0f}% · "
          f"you {you:.1f}/100 · I/we {me:.1f}/100 · check-ins {checks} · rare {rare_pct:.1f}% · "
          f"≈{n / 140:.1f} min at 140 wpm")
    for m in notes:
        print("  note:", m)
    for m in fails:
        print("  FAIL:", m)
    print("spoken-English check", "failed" if fails else "passed")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
