"""Phase 0: Opus 5.5 feasibility checks (HANDOFF §9).

1. Structured output via output_config.format (no forced tool_choice), Pydantic-validated.
2. Prompt caching on a large source bundle placed in `system` with a 1h TTL:
   A) write, B) same effort / different question -> read expected,
   C) different effort -> does the system-tier cache survive? This decides
   whether synthesis (xhigh), verify (max) and script (high) can share one prefix.
3. Image QA on a rendered snapshot PNG.

Writes <out>/opus_spike.md (phone-readable report) and <out>/cost.json.

Usage: python -m pipeline.spike.opus_spike --image path/to/frame.png --out spike-out
"""

import argparse
import base64
import json
import random
import time
import uuid
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from pipeline import config
from pipeline.cost import CostTracker
from pipeline.llm import LLM, cached_block, untrusted

# --- 1. structured output ---------------------------------------------------

SAMPLE_TRANSCRIPT = """[00:41] The display on this phone is the brightest I've measured this year,
easily readable in direct sunlight. [03:12] Battery got me through a full day,
about six and a half hours of screen-on time. [05:58] My one real complaint:
it gets noticeably warm during long gaming sessions, and frame rates drop
after about twenty minutes. [07:42] Software is clean, but the update policy
is only three years, which is short for this price."""


class Claim(BaseModel):
    model_config = ConfigDict(extra="forbid")
    category: Literal["display", "camera", "battery", "performance", "software", "build", "value"]
    aspect: str
    sentiment: int = Field(ge=-2, le=2)
    quote: str
    locator: str = Field(description="Timestamp like 05:58 where the claim is made")


class Extraction(BaseModel):
    model_config = ConfigDict(extra="forbid")
    claims: list[Claim]


def test_structured(llm: LLM) -> dict:
    t0 = time.time()
    r = llm.call(
        "claim_extraction",
        stage="spike_structured",
        system="Extract every review claim from the source. Use only facts in the source. "
        "Quote the reviewer's own words.",
        messages=[{"role": "user", "content": untrusted("Sample Reviewer (video)", SAMPLE_TRANSCRIPT)}],
        schema=Extraction,
        max_tokens=8000,
    )
    claims = r.parsed.claims
    return {
        "ok": len(claims) >= 3 and all(c.locator for c in claims),
        "seconds": round(time.time() - t0, 1),
        "claims": [c.model_dump() for c in claims],
        "usage": r.usage,
    }


# --- 2. caching ---------------------------------------------------------------

def synthetic_bundle(target_tokens: int) -> str:
    """A deterministic fake source bundle (~4 chars/token). Seeded: byte-identical every run."""
    rng = random.Random(42)
    cats = ["display", "camera", "battery", "performance", "software", "build", "value"]
    adjs = ["excellent", "solid", "disappointing", "class-leading", "average", "inconsistent", "impressive"]
    parts, chars, n = [], 0, 0
    while chars < target_tokens * 4:
        n += 1
        lines = [f"## Source {n}: Sample Reviewer {n} (video)"]
        for minute in range(0, 12):
            c, a = rng.choice(cats), rng.choice(adjs)
            lines.append(f"[{minute:02d}:{rng.randint(0, 59):02d}] The {c} is {a}; "
                         f"in my testing over {rng.randint(2, 14)} days it scored {rng.randint(50, 98)} on our rubric.")
        block = untrusted(f"source-{n}", "\n".join(lines))
        parts.append(block)
        chars += len(block)
    return "\n\n".join(parts)


SYNTH_SYSTEM = ("You analyse phone reviews. Use only the sources provided below; never use your own "
                "memory for phone facts. Answer in at most two sentences.")


def test_caching(llm: LLM, bundle_tokens: int) -> dict:
    # Per-run nonce at the front of the prefix, so a re-run within the 1h TTL
    # still starts with a cache write instead of reading the previous run's entry.
    bundle = synthetic_bundle(bundle_tokens)
    system = [{"type": "text", "text": f"Run {uuid.uuid4()}\n{SYNTH_SYSTEM}"}, cached_block(bundle)]
    measured = llm.client.messages.count_tokens(
        model=config.models()["model"], system=system, messages=[{"role": "user", "content": "x"}]
    ).input_tokens

    def ask(label: str, task: str, question: str) -> dict:
        t0 = time.time()
        r = llm.call(task, stage=f"spike_cache_{label}", system=system,
                     messages=[{"role": "user", "content": question}], max_tokens=4000)
        u = r.usage
        return {"label": label, "effort": config.task(task)["effort"], "seconds": round(time.time() - t0, 1),
                "input": u.input_tokens, "cache_read": u.cache_read_tokens,
                "cache_write": u.cache_write_5m_tokens + u.cache_write_1h_tokens,
                "output": u.output_tokens, "usd": u.usd}

    # metadata=medium, script=high: two different efforts from config.
    a = ask("A_write", "metadata", "How many sources mention battery?")
    b = ask("B_same_effort", "metadata", "Which category appears most often?")
    c = ask("C_other_effort", "script", "Which category appears least often?")
    return {
        "bundle_tokens": measured,
        "calls": [a, b, c],
        "hit_same_effort": b["cache_read"] > 0.9 * a["cache_write"] > 0,
        "hit_across_effort": c["cache_read"] > 0.9 * a["cache_write"] > 0,
    }


# --- 3. image QA ----------------------------------------------------------------

class Issue(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["text_overflow", "overlap", "unreadable_on_phone", "wrong_colour", "clipping", "other"]
    where: str
    detail: str


class FrameQA(BaseModel):
    model_config = ConfigDict(extra="forbid")
    verdict: Literal["PASS", "FAIL"]
    issues: list[Issue]
    notes: str


def test_image(llm: LLM, image: Path) -> dict:
    t0 = time.time()
    data = base64.standard_b64encode(image.read_bytes()).decode()
    r = llm.call(
        "visual_qa",
        stage="spike_image",
        system="You are the visual QA reviewer for a premium dark-themed YouTube video. Brand colours: "
        "background #07090d, ink #f4f6fb, accent #5ee1c2, warn #ffb35c, bad #ff6b7a. Check for text "
        "overflow, overlapping elements, clipping, wrong colours, and text too small to read when the "
        "video is watched on a phone. FAIL only for real defects.",
        messages=[{"role": "user", "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": data}},
            {"type": "text", "text": "Review this rendered frame."},
        ]}],
        schema=FrameQA,
        max_tokens=8000,
    )
    return {"seconds": round(time.time() - t0, 1), "qa": r.parsed.model_dump(), "usage": r.usage}


# --- report ---------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", type=Path, required=True)
    ap.add_argument("--out", type=Path, default=Path("spike-out"))
    ap.add_argument("--bundle-tokens", type=int, default=150_000,
                    help="Size of the synthetic cached bundle. 900000 approximates a full 1M call.")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    costs = CostTracker()
    llm = LLM(costs)
    results: dict = {}
    errors: dict = {}
    for name, fn in [("structured", lambda: test_structured(llm)),
                     ("caching", lambda: test_caching(llm, args.bundle_tokens)),
                     ("image", lambda: test_image(llm, args.image))]:
        try:
            results[name] = fn()
        except Exception as e:  # report every test, even if one fails
            errors[name] = f"{type(e).__name__}: {e}"

    costs.write(args.out / "cost.json")
    (args.out / "opus_spike.json").write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")

    md = ["# Opus 5.5 spike", "", f"Model: `{config.models()['model']}` · total cost **${costs.total_usd}**", ""]
    if s := results.get("structured"):
        md += ["## 1. Structured output (no forced tool_choice)",
               f"- {'✅' if s['ok'] else '❌'} {len(s['claims'])} claims, schema-valid, {s['seconds']}s, ${s['usage'].usd}"]
        md += [f"  - `{c['category']}` {c['sentiment']:+d} @ {c['locator']}: {c['aspect']}" for c in s["claims"]]
        md.append("")
    if c := results.get("caching"):
        md += ["## 2. Prompt caching (bundle in `system`, 1h TTL)",
               f"Bundle: {c['bundle_tokens']:,} tokens", "",
               "| call | effort | cache write | cache read | uncached in | out | $ | s |", "|---|---|---|---|---|---|---|---|"]
        md += [f"| {x['label']} | {x['effort']} | {x['cache_write']:,} | {x['cache_read']:,} | {x['input']:,} | "
               f"{x['output']:,} | {x['usd']} | {x['seconds']} |" for x in c["calls"]]
        md += ["", f"- Cache hit, same effort: {'✅' if c['hit_same_effort'] else '❌'}",
               f"- Cache hit across effort change: {'✅' if c['hit_across_effort'] else '❌ (stages with different effort cannot share one cached prefix)'}", ""]
    if i := results.get("image"):
        md += ["## 3. Image QA on a rendered frame",
               f"- Verdict: **{i['qa']['verdict']}**, {len(i['qa']['issues'])} issue(s), {i['seconds']}s, ${i['usage'].usd}"]
        md += [f"  - {x['kind']} @ {x['where']}: {x['detail']}" for x in i["qa"]["issues"]]
        md += [f"- Notes: {i['qa']['notes']}", ""]
    for name, err in errors.items():
        md += [f"## ❌ {name} failed", f"`{err}`", ""]
    (args.out / "opus_spike.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
