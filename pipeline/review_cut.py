"""Automated pre-render review of a documentary cut (PLAYBOOK §14, §22.6).

Contact sheets of the cut (scripts/contact_sheet.py) plus the EDL or script text go to Opus with the
pre-render checklist; it returns every issue with timecode, rule and fix. Writes review.md (phone-readable),
review.json and cost.json next to the sheets. Effort comes from config/models.yaml `tasks.cut_review`.

  python -m pipeline.review_cut --sheets runs/<slug>/qa --edl projects/<slug>/edl.md --out runs/<slug>/qa
"""

import argparse
import base64
import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from pipeline.llm import LLM, untrusted

CHECKLIST = """Pre-render checklist (Be Practical with Kishore documentaries):
1. At least 85% of the runtime is moving footage or animation; no unmoving still or flat frame over 1.5 s;
   no shot over 4 s except LIVE clips and animated explainer scenes.
2. No slide-deck look: no full-screen text boxes, bullet lists, cards, question-mark graphics, flat colour or plain
   gradient backgrounds. Text covers at most 15% of the frame (2-4-word lower-thirds, dates, numbers, timers, credits).
3. Every shot matches the words spoken at that moment (use the EDL/script text): no generic B-roll for a specific claim.
4. The subject's face and name appear within the first 20 s.
5. Every frame's on-screen data (numbers, monitors, headlines, dates) agrees with the narration.
6. Stock or stand-in footage that could pass for the real event carries an "ILLUSTRATIVE FOOTAGE" label; stock never
   has a CCTV or archival look; authentic footage carries a source credit.
7. No stock clip appears more than twice.
8. Science is shown with animation, labelled ILLUSTRATION / ILLUSTRATIVE CURVE / HYPOTHESIS; no still anatomy plates.
9. Logo sting when the channel is named, a small logo bug on other shots, the end card last.
10. No near-black, blank, broken or half-loaded frames; text is readable on a phone; nothing is cropped badly
    (cut-off faces, headless torsos)."""

SYSTEM = (
    "You are the final reviewer for a documentary YouTube channel. You look at timecoded contact sheets of a cut "
    "and report every problem a viewer or the channel owner would notice, against the checklist. Be exact: cite the "
    "timecode printed on the tile, the checklist rule number, what is wrong and the concrete fix. Report only what "
    "the frames show; if a rule cannot be judged from stills (e.g. audio), say so in `not_checkable`.\n\n" + CHECKLIST
)


class Issue(BaseModel):
    model_config = ConfigDict(extra="forbid")
    timecode: str = Field(description="as printed on the tile, e.g. 01:42.00")
    rule: int = Field(description="checklist rule number")
    severity: Literal["blocker", "major", "minor"]
    problem: str
    fix: str


class Review(BaseModel):
    model_config = ConfigDict(extra="forbid")
    passed: bool = Field(description="true only when there are no blocker or major issues")
    summary: str
    issues: list[Issue]
    not_checkable: list[str]


def review(llm: LLM, sheets: list[Path], edl_text: str | None) -> Review:
    content: list[dict] = []
    for s in sheets:
        content.append({"type": "text", "text": f"Contact sheet {s.name}:"})
        content.append({"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                                    "data": base64.standard_b64encode(s.read_bytes()).decode()}})
    if edl_text:
        content.append({"type": "text", "text": untrusted("edl_or_script", edl_text)})
    content.append({"type": "text", "text": "Review the cut against the checklist. List every issue."})
    res = llm.call("cut_review", system=SYSTEM, messages=[{"role": "user", "content": content}], schema=Review,
                   stage="cut_review")
    return res.parsed


def to_markdown(r: Review) -> str:
    lines = [f"# Cut review: {'PASS' if r.passed else 'FIX BEFORE RENDER'}", "", r.summary, ""]
    if r.issues:
        lines += ["| Time | Rule | Severity | Problem | Fix |", "|---|---|---|---|---|"]
        order = {"blocker": 0, "major": 1, "minor": 2}
        for i in sorted(r.issues, key=lambda i: (order[i.severity], i.timecode)):
            lines.append(f"| {i.timecode} | {i.rule} | {i.severity} | {i.problem} | {i.fix} |")
    if r.not_checkable:
        lines += ["", "Not checkable from stills: " + "; ".join(r.not_checkable)]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sheets", type=Path, required=True, help="folder with sheet-NN.jpg")
    ap.add_argument("--edl", type=Path, help="EDL or script text the shots must match")
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    sheets = sorted(a.sheets.glob("sheet-*.jpg"))
    if not sheets:
        raise SystemExit(f"no sheet-*.jpg in {a.sheets} (run scripts/contact_sheet.py first)")
    llm = LLM()
    r = review(llm, sheets, a.edl.read_text() if a.edl else None)
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / "review.json").write_text(json.dumps(r.model_dump(), indent=2))
    (a.out / "review.md").write_text(to_markdown(r))
    llm.costs.write(a.out / "cost.json")
    print(to_markdown(r))
    raise SystemExit(0 if r.passed else 1)


if __name__ == "__main__":
    main()
