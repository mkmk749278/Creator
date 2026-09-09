"""Kinetic captions driven by real word timings.

edge-tts returns a WordBoundary event per word (offset + duration in 100ns
ticks) when constructed with boundary="WordBoundary". That is what lets the
caption highlight land exactly on the syllable instead of being guessed from an
average words-per-second -- guessed timing drifts within about six seconds and
reads as broken.

Captions are grouped into short chunks rather than shown a word at a time: a
single word gives the reader no phrase to parse, and the whole sentence at once
gives them no focus. Three-to-four words is the shape that tests best.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from PIL import Image, ImageDraw

from . import brand, draw, motion


@dataclass
class Word:
    text: str
    start: float
    dur: float
    ends_sentence: bool = False
    ends_clause: bool = False

    @property
    def end(self) -> float:
        return self.start + self.dur


def mark_punctuation(words: list["Word"], narration: str, *,
                     lookahead: int = 4) -> list["Word"]:
    """Flag which words end a sentence or a clause.

    edge-tts strips punctuation from WordBoundary events, so a chunker that
    only counts words will happily put the end of one sentence and the start of
    the next on the same caption line -- "wish you luck Lumin" and "futures
    pairs Fifteen AI" both appeared on screen before this existed. Reading the
    punctuation back off the original narration is the only place that
    information survives.

    Matching is positional and best-effort, and the resync is BOUNDED -- which
    this function claimed to be and was not until 2026-09-09.

    The old inner loop scanned forward to the end of the token list looking for
    a match, so one word edge-tts tokenised differently did not cost that word's
    marks: it consumed every remaining token and silently dropped the marks for
    the WHOLE REST OF THE SCRIPT. The docstring said the opposite.

    The word that triggered it was **a hyphenated compound**. `trade-only` comes
    back from edge-tts as one word; the tokeniser split it into `trade-` and
    `only,`; nothing ever matched `tradeonly`; and from that point on no caption
    in the reel could break on a full stop -- so `06_three_checks` rendered
    "rejected Two Is there" and "tell And with your" across three sentences.
    Reels 01-03 were clean only because their narration happens to say "trade
    only" without the hyphen, which is exactly how a bug like this waits.

    Two fixes, because either alone leaves the trap armed:

      * `-` joins the word class, so a hyphenated compound tokenises the way the
        speech engine says it;
      * the forward scan is capped at `lookahead` tokens, so ANY future
        tokenisation surprise costs one word's marks instead of a whole reel's.

    Unmatched words are counted and reported. A silent desync is worse than a
    loud one: the captions still render, they just quietly stop breaking where
    the sentences do, and nothing on screen says so.
    """
    toks = re.findall(r"[A-Za-z0-9'\u2019-]+[^A-Za-z0-9'\u2019]*", narration)
    j, missed = 0, 0
    for w in words:
        target = re.sub(r"[^a-z0-9]", "", w.text.lower())
        hit = False
        for k in range(j, min(len(toks), j + lookahead + 1)):
            tok = toks[k]
            core = re.sub(r"[^a-z0-9]", "", tok.lower())
            if core == target or not core:
                trail = tok[len(re.match(r"[A-Za-z0-9\u2019'-]*", tok).group(0)):]
                w.ends_sentence = bool(re.search(r"[.!?]", trail))
                w.ends_clause = bool(re.search(r"[,;:\u2014]", trail))
                j = k + 1
                hit = True
                break
        if not hit:
            missed += 1
            j += 1
    if missed:
        print(f"  ! captions: {missed}/{len(words)} word(s) did not match the "
              f"script's tokens -- their sentence breaks are lost. Check for a "
              f"character the tokeniser and edge-tts disagree about.")
    return words


@dataclass
class Chunk:
    words: list[Word] = field(default_factory=list)

    @property
    def start(self) -> float:
        return self.words[0].start

    @property
    def end(self) -> float:
        return self.words[-1].end


def group(words: list[Word], *, max_words: int = 4, max_chars: int = 26,
          max_gap: float = 0.55) -> list[Chunk]:
    """Chunk words into caption lines.

    Breaks on, in priority order: the end of a sentence, a long pause, a clause
    break when the line is already long, then the word/character caps. A caption
    that straddles a full stop reads as two half-thoughts and is the single most
    common way an auto-captioned reel looks machine-made.
    """
    chunks: list[Chunk] = []
    cur = Chunk()
    for w in words:
        if cur.words:
            prev = cur.words[-1]
            would = len(" ".join(x.text for x in cur.words + [w]))
            gap = w.start - prev.end
            hard = prev.ends_sentence or gap > max_gap
            soft = (len(cur.words) >= max_words or would > max_chars
                    or (prev.ends_clause and len(cur.words) >= 2))
            if hard or soft:
                chunks.append(cur)
                cur = Chunk()
        cur.words.append(w)
    if cur.words:
        chunks.append(cur)

    # Pull a one-word orphan back onto the previous line when they belong to the
    # same sentence. "instead" alone under "Lumin does the work" is technically
    # correct chunking and reads as a stutter.
    merged: list[Chunk] = []
    for c in chunks:
        if (merged and len(c.words) == 1 and not merged[-1].words[-1].ends_sentence
                and len(" ".join(w.text for w in merged[-1].words + c.words)) <= max_chars + 8):
            merged[-1].words.extend(c.words)
        else:
            merged.append(c)
    return merged


def render(t: float, chunks: list[Chunk], *, size=(brand.W, brand.H),
           baseline: int = 1330, font_size: int = 74,
           active=brand.ACCENT, idle=brand.TEXT_PRIMARY) -> Image.Image | None:
    """Render the caption layer for time `t`, or None when nothing is spoken."""
    chunk = next((c for c in chunks if c.start - 0.12 <= t <= c.end + 0.34), None)
    if chunk is None:
        return None

    f = draw.font(brand.DISPLAY, font_size)
    words = chunk.words
    gap = f.getlength(" ")
    widths = [f.getlength(w.text) for w in words]
    total = sum(widths) + gap * (len(words) - 1)

    # Shrink a long chunk rather than letting it touch the frame edge.
    max_w = size[0] - brand.SAFE_X * 2 - 48
    if total > max_w:
        f = draw.font(brand.DISPLAY, max(36, int(font_size * max_w / total)))
        gap = f.getlength(" ")
        widths = [f.getlength(w.text) for w in words]
        total = sum(widths) + gap * (len(words) - 1)

    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    # Whole-chunk entrance: rise and fade over 180ms.
    intro = motion.ease_out_cubic(min(1.0, max(0.0, (t - chunk.start + 0.12) / 0.18)))
    dy = int((1 - intro) * 26)
    alpha = int(255 * intro)

    asc = f.getbbox("Ag")
    height = asc[3] - asc[1]
    x = (size[0] - total) / 2
    y = baseline + dy

    pad_x, pad_y = 34, 22
    plate = draw.rounded_rect(
        (int(total + pad_x * 2), int(height + pad_y * 2 + 14)), 26,
        (7, 11, 22, int(150 * intro)))
    layer.alpha_composite(plate, (int(x - pad_x), int(y - pad_y - 6)))

    for w, wd in zip(words, widths):
        spoken = w.start <= t <= w.end + 0.10
        colour = active if spoken else idle
        # A small pop on the spoken word draws the eye without moving the line.
        pop = motion.ease_out_back(min(1.0, max(0.0, (t - w.start) / 0.13))) if spoken else 1.0
        off = int((pop - 1.0) * 9)
        d.text((x, y - asc[1] - off), w.text, font=f, fill=colour + (alpha,))
        x += wd + gap

    return layer
