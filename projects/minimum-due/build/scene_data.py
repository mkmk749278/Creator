#!/usr/bin/env python3
"""Data for the refined animation scenes (s01 phone payment, s02 timeline, s03 allocation).

Every number comes from tools/mad_math.py (the checked calculation behind claims MD-049 etc.), every cue time from the
VO alignment: a cue is (line, phrase) and lands where that phrase starts inside the line, by character position
(speech in these lines runs at an even pace; good to about ±0.3 s). Writes video/minimumdue/<id>/data.js with times
relative to the scene start, plus images the scenes use (blurred desk backdrop, purchase thumbnails).

Usage: python3 projects/minimum-due/build/scene_data.py
"""
import json, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
P = HERE.parent
ROOT = P.parents[1]
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(P / "tools"))
import mad_math as mm   # noqa: E402
from review_shots import vo_lines   # noqa: E402

LINES = {k: (s, e, t) for k, s, e, t in vo_lines()}
A = P / "assets"


def cue(key, phrase=None, frac=None):
    """Film time where `phrase` starts in VO line `key` (or a fraction through the line)."""
    s, e, t = LINES[key]
    if phrase is None:
        return s + (e - s) * (frac or 0.0)
    i = t.find(phrase)
    if i < 0:
        sys.exit(f"phrase not in {key}: {phrase!r}")
    return s + (e - s) * i / len(t)


def numbers():
    i1 = mm.month_one(1500)
    per = [dict(date=d.isoformat(), amount=a, days=(mm.DUE - d).days, interest=round(mm.interest(a, (mm.DUE - d).days), 2))
           for d, a in mm.SPENDS]
    resid_days = (mm.S2 - mm.DUE).days + 1
    snaps, months, share = mm.mad_only(snapshots=range(1, 241))
    return dict(
        total=mm.TOTAL, mad=1500, rate_month=3.75, rate_year=45, gst_rate=18,
        interest=round(i1, 2), gst=round(i1 * mm.GST, 2), charges=round(i1 * (1 + mm.GST), 2),
        new_balance=round(mm.TOTAL - 1500 + i1 * (1 + mm.GST), 2),
        per_purchase=per, residual=dict(amount=mm.TOTAL - 1500, days=resid_days,
                                        interest=round(mm.interest(mm.TOTAL - 1500, resid_days), 2)),
        # [payments made, paid so far, still pending after the next statement]; 0 = the first bill, 1 = after the ₹1,500
        series=[[0, 0, mm.TOTAL], [1, 1500, round(mm.TOTAL - 1500 + i1 * (1 + mm.GST), 2)]]
               + [[n, round(p, 2), round(o, 2)] for n, (p, o) in sorted(snaps.items())],
        months_to_clear=months, year1_interest_share=round(share, 4),
    )


SCENES = {
    # 1.02-1.03: the bill, the minimum, paying it; the market clip for "many people think like this" follows
    "s01_pay": dict(start=cue("1.02") - 0.3, end=cue("1.03", "Many people"), cues=dict(
        two=cue("1.02", "It shows"), total=cue("1.02", "Total amount"), minimum=cue("1.02", "Minimum amount"),
        salary=cue("1.03", "Salary"), think=cue("1.03", "So you think"), tap=cue("1.03", "pay only the minimum"),
        latefee=cue("1.03", "No late fee"), cibil=cue("1.03", "CIBIL"))),
    # 1.17-1.32: one continuous timeline (the edit cuts away to the RBI page and the ICICI rate page inside it)
    "s02_timeline": dict(start=cue("1.17") - 0.25, end=cue("1.32", frac=1.0) + 0.1, cues=dict(
        example=cue("1.17"), oct5=cue("1.17", "On October fifth"), phone=cue("1.17", "for a phone"),
        oct12=cue("1.17", "On the twelfth"), oct20=cue("1.17", "On the twentieth"),
        stmt=cue("1.18"), total=cue("1.18", "Total"), due=cue("1.18", "Last date"),
        free40=cue("1.19"), free25=cue("1.19", "The grocery"),
        cond=cue("1.20"), full=cue("1.21"), onerupee=cue("1.21", "Even one rupee"), rbi=cue("1.22"),
        paid=cue("1.23"), minimum=cue("1.23", "fifteen hundred"), whatbank=cue("1.23", "Now let"),
        rule1=cue("1.24"), fromday=cue("1.24", "It starts"),
        i10=cue("1.25"), i15=cue("1.25", "On the fifteen"), i5=cue("1.25", "On the five"),
        rate=cue("1.26", "In banks"), year=cue("1.26", "That is forty"),
        rule2=cue("1.27"), till=cue("1.28"), after=cue("1.28", "Only after"),
        rule3=cue("1.29"), gst=cue("1.29", "On top"),
        stmt2=cue("1.30"), youpaid=cue("1.31"), added=cue("1.31", "The bank added"),
        wentup=cue("1.32"), to30481=cue("1.32", "to thirty thousand, four"), still=cue("1.32", "You paid money"))),
    # 2.02-2.06: where each payment goes, and the balance over the years
    "s03_allocation": dict(start=cue("2.02") - 0.3, end=cue("2.06", frac=1.0) + 0.25, cues=dict(
        rbi=cue("2.02"), down=cue("2.02", "So the loan"), slowly=cue("2.02", "But very"),
        y1=cue("2.03"), hundred=cue("2.03", "out of every"), seventy=cue("2.03", "about seventy"),
        twentysix=cue("2.03", "Only twenty"), start30=cue("2.04"), after1=cue("2.04", "After one year"),
        pending1=cue("2.04", "But about"), y5=cue("2.05"), paid5=cue("2.05", "You have paid"),
        pending5=cue("2.05", "And still"), ten=cue("2.06"))),
}


def frame(src, t, out, vf):
    seek = [] if t is None else ["-ss", str(t)]   # no seek on a still: ffmpeg then writes nothing and still exits 0
    subprocess.run(["ffmpeg", "-v", "error", "-y", *seek, "-i", str(src), "-frames:v", "1", "-vf", vf, "-q:v", "3", str(out)],
                   check=True)
    if not out.exists():
        sys.exit(f"no frame written: {out}")


def images(d):
    """Backdrop and purchase thumbnails (real footage/photos, logged in media_manifest.csv)."""
    img = d / "img"; img.mkdir(exist_ok=True)
    frame(A / "broll/pixabay_202987.mp4", 6, img / "desk.jpg", "scale=1920:1080,boxblur=18:2,eq=brightness=-0.18:saturation=0.8")
    frame(A / "broll/coverr-online-shopping-with-credit-card.mp4", 3, img / "buy_phone.jpg", "scale=480:-2,crop=480:270")
    frame(A / "broll/pixabay_269529.mp4", 4, img / "buy_function.jpg", "scale=480:-2,crop=480:270")
    frame(A / "commons_new/provision_13_provisions-shop-simsa-manali-himachal-ma.jpg", None, img / "buy_grocery.jpg",
          "scale=480:-2,crop=480:270:0:(ih-270)*0.55")


def main():
    nums = numbers()
    for sid, sc in SCENES.items():
        d = ROOT / "video/minimumdue" / sid; d.mkdir(parents=True, exist_ok=True)
        rel = {k: round(v - sc["start"], 2) for k, v in sc["cues"].items()}
        data = dict(id=sid, start=round(sc["start"], 2), duration=round(sc["end"] - sc["start"], 2), cues=rel, n=nums)
        (d / "data.js").write_text(f"// Generated by projects/minimum-due/build/scene_data.py: cues from the VO alignment,\n"
                                   f"// numbers from tools/mad_math.py. Do not edit by hand.\nwindow.DATA = "
                                   + json.dumps(data, ensure_ascii=False, sort_keys=True) + ";\n")
        images(d)
        html = d / "index.html"   # keep the composition's length in step with the VO
        if html.exists():
            h = html.read_text(); h2 = re.sub(r'data-duration="[\d.]+"', f'data-duration="{data["duration"]}"', h, count=1)
            if h2 != h:
                html.write_text(h2)
        print(sid, data["start"], data["duration"], len(rel), "cues")


if __name__ == "__main__":
    main()
