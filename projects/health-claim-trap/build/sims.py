#!/usr/bin/env python3
"""SIMULATION stills (no real hospital, insurer or TPA): HTML -> 3840x2160 PNG with headless Chromium.
Each frame lays a paper or screen on a dark desk; assemble.py moves it (Ken Burns, push into the focus box).
Writes assets/sim/<id>.png and <id>.json (focus box as fractions, for the push-in)."""
import json, subprocess
from pathlib import Path

P = Path(__file__).resolve().parents[1]
OUT = P / "assets/sim"; OUT.mkdir(parents=True, exist_ok=True)
FONT = (P.parents[1] / "node_modules/@fontsource/inter/files").as_uri()

BASE = f"""<style>
@font-face {{ font-family: I; font-weight: 400; src: url('{FONT}/inter-latin-400-normal.woff2'); }}
@font-face {{ font-family: I; font-weight: 600; src: url('{FONT}/inter-latin-600-normal.woff2'); }}
@font-face {{ font-family: I; font-weight: 800; src: url('{FONT}/inter-latin-800-normal.woff2'); }}
@font-face {{ font-family: I; font-weight: 400; src: url('{FONT}/inter-latin-ext-400-normal.woff2'); unicode-range: U+0100-02FF, U+20A0-20CF; }}
@font-face {{ font-family: I; font-weight: 800; src: url('{FONT}/inter-latin-ext-800-normal.woff2'); unicode-range: U+0100-02FF, U+20A0-20CF; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ width: 1920px; height: 1080px; overflow: hidden; font-family: I, Arial, sans-serif;
  background: radial-gradient(ellipse at 50% 35%, #2b3448, #0b1020 75%); }}
.paper {{ position: absolute; background: #f4f1ea; color: #1f2937; border-radius: 6px; box-shadow: 0 40px 90px rgba(0,0,0,.7); font-size: 22px; line-height: 1.45; }}
.hd {{ background: #e7e2d6; padding: 20px 34px; border-bottom: 3px solid #cbc3b1; }}
.co {{ font-weight: 800; font-size: 26px; color: #1e3a5f; letter-spacing: .04em; }}
.sub {{ font-weight: 600; font-size: 16px; color: #6b7280; letter-spacing: .08em; text-transform: uppercase; margin-top: 4px; }}
.bd {{ padding: 24px 34px; }}
.t {{ font-weight: 800; font-size: 24px; letter-spacing: .06em; text-transform: uppercase; margin-bottom: 14px; }}
.row {{ display: flex; justify-content: space-between; border-bottom: 1px solid #d6d0c2; padding: 7px 0; }}
.row b {{ font-weight: 800; }}
.sim {{ position: absolute; font-weight: 800; letter-spacing: .3em; color: rgba(15,23,42,.16); transform: rotate(-22deg); font-size: 30px; }}
.hl {{ background: rgba(255,214,0,.55); border-radius: 4px; padding: 0 4px; }}
.box {{ display: inline-block; width: 26px; height: 26px; border: 3px solid #374151; border-radius: 4px; vertical-align: -5px; margin-right: 12px; text-align: center; font-weight: 800; line-height: 20px; }}
.hand {{ font-family: 'Segoe Script', cursive; font-style: italic; color: #1d3c8f; font-size: 30px; }}
</style>"""

SIMS = {
    "bill": ("""<div class="paper" style="left:560px; top:60px; width:800px; height:960px">
      <div class="hd"><div class="co">SAMPLE CITY HOSPITAL</div><div class="sub">Final bill · In-patient · Discharge</div></div>
      <div class="bd"><div class="t">Bill summary</div>
      <div class="row"><span>Room charges (3 days)</span><b>₹24,000</b></div>
      <div class="row"><span>Surgeon and doctor fees</span><b>₹1,20,000</b></div>
      <div class="row"><span>Nursing</span><b>₹15,000</b></div>
      <div class="row"><span>Operation theatre</span><b>₹95,000</b></div>
      <div class="row"><span>Medicines and consumables</span><b>₹1,21,000</b></div>
      <div class="row"><span>Implants</span><b>₹50,000</b></div>
      <div class="row"><span>Tests</span><b>₹25,000</b></div>
      <div class="row" style="border:0; margin-top:18px; font-size:34px"><span><b>Total</b></span><b id="f" class="hl">₹4,50,000</b></div>
      <div style="margin-top:30px; color:#6b7280; font-size:18px">Discharge time: 9:00 PM</div></div>
      <div class="sim" style="left:240px; top:520px">SIMULATION</div></div>""", "f"),
    "notes": ("""<div class="paper" style="left:520px; top:60px; width:880px; height:960px">
      <div class="hd"><div class="co">SAMPLE CITY HOSPITAL</div><div class="sub">Indoor case record · Admission notes</div></div>
      <div class="bd"><div class="row"><span>Complaint</span><b>Fall at home, right leg pain</b></div>
      <div class="row"><span>Diagnosis</span><b>Fracture, right tibia</b></div>
      <div class="row"><span>Plan</span><b>Surgery, plate fixation</b></div>
      <div style="margin-top:30px; font-weight:800">History</div>
      <div class="hand" style="margin-top:10px">Fall from stairs. No loss of consciousness.</div>
      <div class="hand" id="f" style="margin-top:14px"><span class="hl">Patient has mild blood pressure.</span></div>
      <div class="hand" style="margin-top:14px">Vitals stable. Fit for surgery.</div></div>
      <div class="sim" style="left:260px; top:600px">SIMULATION</div></div>""", "f"),
    "proposal": ("""<div class="paper" style="left:520px; top:60px; width:880px; height:960px">
      <div class="hd"><div class="co">SAMPLE HEALTH INSURANCE CO. LTD.</div><div class="sub">Proposal form · 2020 · Health questions</div></div>
      <div class="bd"><div class="t">Do you have, or have you had:</div>
      <div class="row"><span>Diabetes</span><span><span class="box"></span>Yes <span class="box">✓</span>No</span></div>
      <div class="row" id="f"><span class="hl">High blood pressure</span><span><span class="box"></span>Yes <span class="box">✓</span>No</span></div>
      <div class="row"><span>Thyroid disorder</span><span><span class="box"></span>Yes <span class="box">✓</span>No</span></div>
      <div class="row"><span>Heart disease</span><span><span class="box"></span>Yes <span class="box">✓</span>No</span></div>
      <div class="row"><span>Tobacco use</span><span><span class="box"></span>Yes <span class="box">✓</span>No</span></div>
      <div style="margin-top:40px; color:#6b7280">I declare that the answers above are true and complete.</div>
      <div class="hand" style="margin-top:20px">R. K****</div></div>
      <div class="sim" style="left:260px; top:640px">SIMULATION</div></div>""", "f"),
    "proposal_declared": ("""<div class="paper" style="left:520px; top:60px; width:880px; height:960px">
      <div class="hd"><div class="co">SAMPLE HEALTH INSURANCE CO. LTD.</div><div class="sub">Proposal form · Health questions</div></div>
      <div class="bd"><div class="t">Do you have, or have you had:</div>
      <div class="row"><span>Diabetes</span><span><span class="box"></span>Yes <span class="box">✓</span>No</span></div>
      <div class="row" id="f"><span class="hl">High blood pressure (on medicine)</span><span><span class="box">✓</span>Yes <span class="box"></span>No</span></div>
      <div class="row"><span class="hl">Tobacco use (occasional)</span><span><span class="box">✓</span>Yes <span class="box"></span>No</span></div>
      <div class="row"><span>Thyroid disorder</span><span><span class="box"></span>Yes <span class="box">✓</span>No</span></div>
      <div class="row"><span>Heart disease</span><span><span class="box"></span>Yes <span class="box">✓</span>No</span></div>
      <div style="margin-top:40px; color:#6b7280">I declare that the answers above are true and complete.</div>
      <div style="margin-top:40px; display:inline-block; padding:10px 22px; border:6px solid #0284c7; color:#0284c7; font-weight:800; font-size:44px; transform:rotate(-6deg); border-radius:10px">DECLARED</div></div>
      <div class="sim" style="left:260px; top:640px">SIMULATION</div></div>""", "f"),
    "email": ("""<div class="paper" style="left:380px; top:90px; width:1160px; height:900px; background:#fff; border-radius:16px">
      <div class="hd" style="background:#eef2f7"><div class="co" style="color:#0f172a">New message</div></div>
      <div class="bd" style="font-size:24px">
      <div class="row"><span>To</span><b>Grievance Redressal Officer, Sample Health Insurance Co.</b></div>
      <div class="row"><span>Subject</span><b>Grievance: reimbursement claim rejected</b></div>
      <div style="margin-top:24px">Dear Sir or Madam,</div>
      <div style="margin-top:12px">Policy number: <b>XXXX-2020-XXXX</b> · Claim number: <b>CL-2026-XXXX</b> · Amount: <b>₹4,50,000</b></div>
      <div style="margin-top:12px">My claim was rejected for non-disclosure. My policy has run continuously since 2020.</div>
      <div id="f" style="margin-top:12px"><span class="hl">Under the IRDAI moratorium rule, after sixty months of continuous cover a claim cannot be contested on grounds of non-disclosure, except for established fraud.</span></div>
      <div style="margin-top:12px">Please review and settle my claim.</div></div>
      <div class="sim" style="left:380px; top:560px">SIMULATION</div></div>""", "f"),
    "claim_form": ("""<div class="paper" style="left:610px; top:40px; width:700px; height:1000px; background:#fff; border-radius:40px; border:16px solid #0d0f14">
      <div class="hd" style="background:#0f172a; color:#fff; border:0; border-radius:20px 20px 0 0"><div class="co" style="color:#38bdf8">Reimbursement claim</div><div class="sub" style="color:#94a3b8">Sample Health Insurance · app</div></div>
      <div class="bd" style="font-size:22px">
      <div class="row"><span>Date of discharge</span><b>Night of day 3</b></div>
      <div class="row" id="f"><span class="hl">File within</span><b class="hl">15 to 30 days (see policy)</b></div>
      <div class="row"><span>Discharge summary</span><b>✓ uploaded</b></div>
      <div class="row"><span>Final bill with break up</span><b>✓ uploaded</b></div>
      <div class="row"><span>Reports and pharmacy bills</span><b>✓ uploaded</b></div>
      <div class="row"><span>Cashless denial letter</span><b>✓ uploaded</b></div>
      <div style="margin-top:40px; background:#0284c7; color:#fff; text-align:center; padding:20px; border-radius:16px; font-weight:800">Submit claim</div></div>
      <div class="sim" style="left:150px; top:560px">SIMULATION</div></div>""", "f"),
    "letter_note": ("""<div class="paper" style="left:560px; top:60px; width:800px; height:960px">
      <div class="hd"><div class="co">SAMPLE HEALTH INSURANCE CO. LTD.</div><div class="sub">Third Party Administrator: Sample Health TPA</div></div>
      <div class="bd"><div class="t">Cashless authorisation: decision</div>
      <div class="row"><span>Amount requested</span><b>₹4,50,000</b></div>
      <div class="row"><span>Decision</span><b style="color:#b91c1c">Cashless denied</b></div>
      <div style="margin-top:14px; font-weight:600">Reason: non-disclosure of pre-existing disease (hypertension) at proposal stage.</div>
      <div id="f" style="margin-top:22px; font-size:26px"><span class="hl">You may submit the claim for reimbursement as per policy terms and conditions.</span></div></div>
      <div class="sim" style="left:240px; top:600px">SIMULATION</div></div>""", "f"),
}

SHOOT = """const { chromium } = require('/opt/node-tools/node_modules/playwright-core');
(async () => { const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
  const p = await (await b.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2 })).newPage();
  for (const [id, file, focus] of JSON.parse(process.argv[2])) {
    await p.goto('file://' + file); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
    const r = await p.evaluate((f) => { const e = document.getElementById(f); if (!e) return null; const b = e.getBoundingClientRect();
      return { x0: b.left / 1920, y0: b.top / 1080, x1: b.right / 1920, y1: b.bottom / 1080 }; }, focus);
    require('fs').writeFileSync(file.replace('.html', '.json'), JSON.stringify(r));
    await p.screenshot({ path: file.replace('.html', '.png') }); console.log(id); }
  await b.close(); })();"""

if __name__ == "__main__":
    jobs = []
    for sid, (html, focus) in SIMS.items():
        f = OUT / f"{sid}.html"; f.write_text("<!doctype html><meta charset='utf-8'>" + BASE + html)
        jobs.append([sid, str(f), focus])
    js = OUT / "_shoot.js"; js.write_text(SHOOT)
    subprocess.run(["node", str(js), json.dumps(jobs)], check=True)
