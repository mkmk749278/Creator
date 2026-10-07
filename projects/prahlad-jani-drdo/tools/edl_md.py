"""Render edl.csv as edl.md (phone-readable table with programme timecodes)."""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
from assemble import load_edl  # noqa: E402
MOTION = {"none": "as shot", "push": "push 1.00→1.04", "zoom_in": "zoom 1.00→1.15", "zoom_out": "zoom 1.15→1.00", "pan_lr": "pan L→R", "pan_rl": "pan R→L"}
NAMES = {"B1": "Block 1: the 3-day rule and the DRDO challenge", "B2": "Block 2: inside the sealed room",
         "B3": "Block 3: the ultrasound shock"}


def tc(t):
    return f"{int(t // 60):02d}:{t % 60:05.2f}"


rows, _ = load_edl()
t, block, out = 0.0, None, []
out.append("# Step 2: scene and timeline map (EDL)\n")
out.append("Generated from `edl.csv` by `tools/edl_md.py`; edit the CSV, not this file. **Prog** = final video time; "
           "**VO** = time in `voiceover.mp3`. Every shot gets grain + vignette (Layer 2); `+hud` adds the medical HUD.\n")
for r in rows:
    d = r["dur"]
    if r["type"] == "LIVE":
        out.append(f"\n> **🎬 LIVE CLIP {tc(t)} ({d:.1f} s)**: VO stops at {r['vo_at']} s; `{r['asset']}` plays "
                   f"{r['src_in']:.1f}–{r['src_in'] + d:.1f} s **with its own audio**, then the VO continues. "
                   f"{('Caption: ' + r['subtitle'] + '. ') if r.get('subtitle') else ''}{r['note']}\n")
    elif r["type"] == "VO_PAUSE":
        out.append(f"\n> **⏸ LIVE AUDIO PAUSE {tc(t)} ({d:.1f} s)**: VO stops at {r['vo_at']} s"
                   + (f", skips {r['vo_skip']} s of VO" if float(r['vo_skip'] or 0) else "")
                   + f". Picture: `{r['asset']}` ({MOTION[r['motion']]}). Audio: {r['sfx']}. {r['note']}\n")
    else:
        if r["block"] != block:
            block = r["block"]
            out.append(f"\n## {NAMES[block]}\n\n| # | Prog | VO | Dur | Layer 1 asset (fallback) | Motion | Layer 3 text | SFX / note |\n"
                       "|---|---|---|---|---|---|---|---|")
        txt = f"{r['text']} ({r['text_pos']})" if r["text"] else ""
        extra = " · ".join(x for x in (r["sfx"], r["note"]) if x)
        hud = " +hud" if "hud" in r["overlay"] else ""
        out.append(f"| {r['id']} | {tc(t)} | {float(r['vo_in']):.2f} | {d:.2f} | `{r['asset']}` (`{r['fallback']}`) | "
                   f"{MOTION[r['motion']]}{hud} | {txt} | {extra} |")
    t += d
out.append(f"\n**Programme length: {tc(t)}** ({sum(r['type'] == 'SHOT' for r in rows)} shots, "
           f"{sum(r['type'] == 'LIVE' for r in rows)} live clips, {sum(r['type'] == 'VO_PAUSE' for r in rows)} VO pauses).\n")
out.append("""
## Audio cue sheet
| Element | Level | Notes |
|---|---|---|
| Voiceover (`voiceover.mp3`) | lead, normalised with the mix to −14 LUFS / −1 dBTP | Removes the duplicate line at VO 221.40–223.40 |
| BGM (`bgm_dark.mp3`) | −20 dB, side-chain ducked (ratio 6, release 400 ms) | Swells up in each pause |
| SFX | −8 dB, 3 s max with 0.3 s fade | Placed from the `sfx` column (`file@seconds-into-shot`) |
| Pause audio | 0 dB | Real recordings only. Pause 3 must be the real Dr. Shah clip; if none exists, use monitor beeps |
""")
(HERE / "edl.md").write_text("\n".join(out), encoding="utf-8")
print("wrote edl.md")
