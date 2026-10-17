#!/usr/bin/env python3
"""Build every script view from script.full.tsv (the single source; edit only that file).

Writes, in projects/kavach-railway-reality/:
  script.md         phone-readable shooting script: section, Telugu VO, English, visual, on-screen text, sound
  bunty_blocks.md   paste-ready ElevenLabs blocks (Telugu only), 4,000-4,500 characters, split at section ends
  script.tsv        te<TAB>en, one spoken line per row, `---` between blocks (align_script.py / estimate_vo.py)
and lints the Telugu text for the Bunty format (CLAUDE.md, PLAYBOOK §4, §4b): Telugu script only, no ! quotes dashes
brackets or stage directions, at most one `...` per sentence, no banned newspaper connectors or ban-list words.
"""
import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
TARGET, CAP = (4000, 4500), 5000
TITLE = "The Kavach Railway Reality"
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from estimate_vo import line_seconds  # noqa: E402  (one timing model for every tool)
BANNED = ["ఈ నేపథ్యంలో", "ఈ క్రమంలో", "అనంతరం", "తద్వారా", "కావున", "సదరు", "పేర్కొన్నారు", "వెల్లడించారు",
          "చండాల", "కటిక చీకటి", "నువ్వు"]


LETTERS = {"ఏ", "బి", "బీ", "సి", "సీ", "డి", "డీ", "ఈ", "ఎఫ్", "జి", "జీ", "హెచ్", "ఐ", "జె", "కె", "కే", "ఎల్", "ఎం", "ఎన్",
           "ఓ", "పి", "పీ", "క్యూ", "ఆర్", "ఎస్", "టి", "టీ", "యు", "యూ", "వి", "వీ", "వై", "జెడ్", "ఎక్స్"}
SUFFIXES = {"కి", "కు", "లో", "లోనే", "లోకి", "లోంచి", "ని", "ను", "తో", "గా", "నే", "లు", "ల", "ది", "కే"}
QWORDS = ("తెలుసా", "ఏంటి", "ఎవరు", "ఏముంటుంది", "ఎందుకు", "ఏమిటి", "ఎలా", "వచ్చిందా", "చేశారా", "కదా", "ఏమనుకుంటాం")
TAGS = {"[serious]", "[tense]", "[menacing]", "[slowly]", "[softly]", "[sighs]", "[dramatic pause]", "[intense]", "[curious]",
        "[confident]", "[warmly]", "[shocked]", "[hopeful]", "[sad]", "[empathetic]", "[grave]", "[urgent]", "[firm]",
        "[emphatic]", "[gently]", "[inspired]", "[whispers]"}


def lint(row):
    """Bunty format (CLAUDE.md, PLAYBOOK §4, §4b; owner 2026-10-09): Telugu script only; `?` on real questions; acronyms
    written as one word as Telugu media spell them (ఈడీ, ఓటీపీ: spaced letters are misread, e.g. ఈ = 'this');
    case endings joined to the noun (ఫ్యామిలీకి, not ఫ్యామిలీ కి); no ! quotes dashes brackets; ban list."""
    te, errs = row["te"], []
    bad = re.findall(r"[^\u0C00-\u0C7F\s,.?\u200c\u200d]", te)
    if bad:
        errs.append(f"non-Telugu characters {sorted(set(bad))}")
    toks = re.findall(r"[^\s,.?]+", te)
    for a, b in zip(toks, toks[1:]):
        if a in LETTERS and b in LETTERS:
            errs.append(f"spaced acronym '{a} {b}': write it as one word (ఈడీ, ఓటీపీ, సీబీఐ)")
            break
    for m in re.finditer(r"(?<=[\u0C00-\u0C7F]) ([\u0C00-\u0C7F]+)(?=[\s,.?]|$)", te):
        if m.group(1) in SUFFIXES:
            errs.append(f"detached case ending ' {m.group(1)}': join it to the word before")
            break
    for sent in re.split(r"(?<=[.?])\s+", te):
        words = re.findall(r"[^\s,.?]+", sent)
        if sent.rstrip().endswith(".") and not sent.rstrip().endswith("...") and words and words[-1] in QWORDS:
            errs.append(f"question ends with a full stop: '{sent.strip()[-30:]}'")
    for s in re.split(r"(?<=\.)\s", te):
        if s.count("...") > 1:
            errs.append("more than one ... in a sentence")
    errs += [f"banned word {w}" for w in BANNED if w in te]
    tag = row.get("emotion", "").strip()
    if tag and tag not in TAGS:
        errs.append(f"unknown emotion tag {tag}")
    return errs


EN_QWORDS = ("right", "how", "why", "what", "who", "which")
# Acronyms the voice should say as a word (PLAYBOOK §4a-4); every other capital acronym must be hyphenated (R-D-S-O).
EN_WORD_ACRONYMS = {"ISRO", "OK", "I"}


def lint_en(row):
    """English VO (owner 2026-10-11 and 2026-10-15, PLAYBOOK §4a-2, §4a-4): no ! double quotes or brackets; `—` allowed
    for mid-thought pivots, but no spaced hyphen or `--`; `?` on real questions; numbers and amounts as words (no digits
    or ₹); at most one `...` per sentence; acronyms said letter by letter are written with hyphens for Akash (R-D-S-O,
    R-F-I-D), so a bare capital acronym fails; no lecture openers. The VO text sits in row["te"] after main() swaps
    the columns."""
    t, errs = row["te"], []
    bad = re.findall(r"[!\"“”‘’–\[\]()₹0-9#&;/]", t)
    if bad:
        errs.append(f"characters not allowed in English VO {sorted(set(bad))}")
    if re.search(r"\s-\s|--", t):
        errs.append("spaced hyphen in English VO: use — for a pivot")
    for tok in re.findall(r"\b[A-Z]{2,}\b", t):
        if tok not in EN_WORD_ACRONYMS:
            errs.append(f"bare acronym {tok}: write it for the voice (e.g. {'-'.join(tok)})")
    for opener in ("now let us", "let us understand", "in this video we", "first, one thing must be clear",
                   "welcome to be practical", "today we'll", "today we will", "it has been observed"):
        if opener in t.lower():
            errs.append(f"lecture opener '{opener}' (PLAYBOOK §4a-4, §4a-5; the channel is named only in the outro)")
    for sent in re.split(r"(?<=[.?])\s+", t):
        w = re.findall(r"[A-Za-z']+", sent.lower())
        if sent.rstrip().endswith(".") and not sent.rstrip().endswith("...") and w and (w[0] in EN_QWORDS[1:] or w[-1] == "right"):
            errs.append(f"question ends with a full stop: '{sent.strip()[-30:]}'")
        if sent.count("...") > 1:
            errs.append("more than one ... in a sentence")
    tag = row.get("emotion", "").strip()
    if tag and tag not in TAGS:
        errs.append(f"unknown emotion tag {tag}")
    return errs


def short_runs(rows):
    """PLAYBOOK §4a-4: never 3+ very short sentences (< 6 words) in a row: Akash drops pitch at every full stop."""
    out, run = [], []
    for r in rows:
        for sent in re.split(r"(?<=[.?])\s+", r["te"].strip()):
            if not sent:
                continue
            if len(re.findall(r"[A-Za-z0-9'-]+", sent)) < 6:
                run.append(r["id"])
                if len(run) == 3:
                    out.append((r["id"], f"three very short sentences in a row ({', '.join(dict.fromkeys(run))}): join or vary them"))
            else:
                run = []
    return out


def spoken(r, tags=True):
    tag = r.get("emotion", "").strip()
    return f"{tag} {r['te']}" if tags and tag else r["te"]


def blocks_of(rows):
    """Fewest blocks that respect the 5,000 cap, sized near 4,250; cut at section ends near the ideal points."""
    import math
    total = sum(len(spoken(r)) + 1 for r in rows)
    k = max(math.ceil(total / CAP), round(total / 4250), 1)
    ideal = [total * j / k for j in range(1, k)]
    pos, cuts = 0, []  # cumulative size after each line
    ends = []
    for i, r in enumerate(rows):
        pos += len(spoken(r)) + 1
        ends.append((i, pos, i + 1 < len(rows) and rows[i + 1]["section"] != r["section"]))
    for t in ideal:
        # prefer a section end within 450 chars of the ideal point, else the nearest line end
        sec = [e for e in ends if e[2] and abs(e[1] - t) <= 450]
        best = min(sec or ends, key=lambda e: abs(e[1] - t))
        cuts.append(best[0])
    out, start = [], 0
    for c in cuts:
        out.append(rows[start:c + 1]); start = c + 1
    out.append(rows[start:])
    return out


def block_text(block, tags=True):
    """Lines joined with spaces; a blank line between sections gives Bunty a natural paragraph pause. With tags, each
    line's emotion cue (an ElevenLabs v4 audio tag in square brackets) goes in front of it."""
    paras, cur, sec = [], [], None
    for r in block:
        if sec is not None and r["section"] != sec:
            paras.append(" ".join(cur)); cur = []
        cur.append(spoken(r, tags)); sec = r["section"]
    paras.append(" ".join(cur))
    return "\n\n".join(paras)


def chars(block):
    return len(block_text(block))


def secs(block):
    return sum(line_seconds(r["te"]) for r in block)


def mmss(s):
    return f"{int(s // 60)}:{int(s % 60):02d}"


def main():
    global HERE
    if len(sys.argv) > 1:  # optional: a folder holding its own script.full.tsv (e.g. v2/); outputs go there
        HERE = Path(sys.argv[1]).resolve()
    rows = list(csv.DictReader(open(HERE / "script.full.tsv", encoding="utf-8"), delimiter="\t"))
    # VO language: `lang.txt` = en makes the `en` column the narration and `te` the optional Telugu dub (owner,
    # 2026-10-11: English VO by default). The views then show the VO first and the other language in italics.
    lang = (HERE / "lang.txt").read_text().strip() if (HERE / "lang.txt").exists() else "te"
    if lang == "en":
        for r in rows:
            r["te"], r["en"] = r["en"], r["te"]
    global TITLE
    if (HERE / "title.txt").exists():
        TITLE = (HERE / "title.txt").read_text(encoding="utf-8").strip()
    problems = [(r["id"], e) for r in rows for e in (lint_en(r) if lang == "en" else lint(r))]
    if lang == "en":
        problems += short_runs(rows)
    for pid, e in problems:
        print(f"LINT {pid}: {e}")
    blocks = blocks_of(rows)
    for r_i, b in enumerate(blocks, 1):
        for r in b:
            r["block"] = r_i

    with open(HERE / "script.tsv", "w", encoding="utf-8") as f:
        f.write("te\ten\n")
        for i, b in enumerate(blocks):
            if i:
                f.write("---\n")
            for r in b:
                f.write(f"{r['te']}\t{r['en']}\n")

    total = sum(chars(b) for b in blocks)
    tsecs = sum(secs(b) for b in blocks)
    with open(HERE / "bunty_blocks.md", "w", encoding="utf-8") as f:
        f.write(f"# Bunty blocks: {TITLE}\n\nPaste each block as one ElevenLabs generation (voice Akash, ElevenLabs v4, stability 0.65, similarity 0.85, style 0.15, speaker boost on; "
                "`language_code` = the VO language). The [square-bracket] words are emotion cues (audio tags), not spoken text. Test "
                "block 1 first: if Bunty reads a tag aloud, use `bunty_blocks_clean.md` instead. Listen to every take; if a "
                "block skips, repeats or drifts, regenerate it, and send the files as `voice/block1.mp3`, "
                "`voice/block2.mp3`, ….\n\n")
        for i, b in enumerate(blocks, 1):
            c = chars(b)
            f.write(f"## Block {i} · {c:,} characters · ~{mmss(secs(b))} · lines {b[0]['id']}–{b[-1]['id']}\n\n")
            f.write(block_text(b) + "\n\n")
        f.write(f"Total {total:,} characters, about {mmss(tsecs)} of speech.\n")
    with open(HERE / "bunty_blocks_clean.md", "w", encoding="utf-8") as f:
        f.write(f"# Bunty blocks without emotion tags: {TITLE}\n\nSame text as bunty_blocks.md minus the [tags]: use it if a "
                "take reads a tag aloud or breaks around one.\n\n")
        for i, b in enumerate(blocks, 1):
            f.write(f"## Block {i} · {len(block_text(b, False)):,} characters · lines {b[0]['id']}–{b[-1]['id']}\n\n")
            f.write(block_text(b, False) + "\n\n")

    with open(HERE / "script.md", "w", encoding="utf-8") as f:
        f.write(f"# {TITLE}: shooting script (Be Practical with Kishore)\n\n"
                "Built from `script.full.tsv` by `tools/build_script.py`; edit the TSV, not this file. "
                "Each line: **Telugu VO** (what Bunty says), English meaning, then 🎬 picture, 🔤 on-screen text, "
                "🔊 sound, ⏱ pacing. Tags: SIMULATION / RECONSTRUCTION / ILLUSTRATION mark anything that is not real footage.\n\n"
                f"Estimated length: **{mmss(tsecs)}** of speech ({total:,} characters, {len(blocks)} Bunty blocks), "
                "plus pauses and music beats.\n")
        sec = None
        for r in rows:
            if r["section"] != sec:
                sec = r["section"]
                f.write(f"\n## {sec}\n")
            emo = f" · 🎭 {r['emotion']}" if r.get("emotion") else ""
            f.write(f"\n**{r['id']}** · block {r['block']}{emo}  \n**{r['te']}**  \n_{r['en']}_  \n🎬 {r['visual']}")
            if r["onscreen"]:
                f.write(f"  \n🔤 {r['onscreen']}")
            if r["sound"]:
                f.write(f"  \n🔊 {r['sound']}")
            if r.get("pacing"):
                f.write(f"  \n⏱ {r['pacing']}")
            f.write("\n")

    with open(HERE / "screenplay.md", "w", encoding="utf-8") as f:
        f.write(f"# {TITLE}: screenplay (Be Practical with Kishore)\n\nBuilt from `script.full.tsv` by `tools/build_script.py` "
                "(PLAYBOOK §4a-4). Times are estimates at the voice rate until the VO is recorded and aligned; `align/` then wins.\n\n"
                "| TIME / SCENE | AUDIO VOICEOVER (AKASH) | VISUAL FORENSICS & SOUND DESIGN |\n|---|---|---|\n")
        t0, sec = 0.0, None
        for r in rows:
            d = line_seconds(r["te"])
            scene = f"**{r['section']}**<br>" if r["section"] != sec else ""
            sec = r["section"]
            vis = f"[VISUAL] {r['visual']}"
            if r["onscreen"]:
                vis += f"<br>[TEXT] {r['onscreen']}"
            if r.get("pacing"):
                vis += f"<br>[ACTION] {r['pacing']}"
            if r["sound"]:
                vis += f"<br>[SFX] {r['sound']}"
            if r.get("cite"):
                vis += f"<br>[CITE] {r['cite']}"
            cell = lambda s: s.replace("|", "\\|")
            f.write(f"| {scene}{mmss(t0)}–{mmss(t0 + d)}<br>{r['id']} | {cell(r['te'])} | {cell(vis)} |\n")
            t0 += d

    for i, b in enumerate(blocks, 1):
        c = chars(b)
        flag = "ok" if TARGET[0] <= c <= TARGET[1] else ("OVER CAP" if c > CAP else "outside target")
        print(f"block {i}: {c:,} chars ~{mmss(secs(b))} {b[0]['id']}-{b[-1]['id']} {flag}")
    print(f"total {total:,} chars ~{mmss(tsecs)}; {len(problems)} lint problems")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
