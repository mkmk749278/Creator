#!/usr/bin/env python3
"""Film 01 assembly: the shot list, overlays, telemetry HUD and captions -> five HyperFrames parts in video/upi01/p1..p5.

Times are seconds on the paced VO (voice/upi01_v16_edit.wav; sentence cues in align_sent/slots_edit.csv). Each shot
shows exactly what the VO says at that second (screenplay.md plan v2). Base media come from assets/ (Blender renders,
stock B-roll, the soundbox stills); everything drawn on top is HTML animated by video/upi01/_shared/upi.js.
Usage: python3 projects/upi-money-deducted/build/make_film.py   (then npm run vendor; render each part)
"""
import csv, html, json, re, shutil, subprocess
from pathlib import Path

P = Path(__file__).resolve().parents[1]; ROOT = P.parents[1]; A = P / "assets"; R = A / "renders"
OUTV = ROOT / "video/upi01"; END = 258.0
PARTS = [0.0, 47.2, 101.0, 147.0, 200.8, END]
esc = html.escape

# ---------- media (logical name -> file); stock picks are filled from qa/broll after sourcing ----------
BROLL = json.loads((P / "build/broll_picks.json").read_text()) if (P / "build/broll_picks.json").exists() else {}


def media(name):
    if name in BROLL:
        return A / "broll_soft" / BROLL[name]["soft"] if BROLL[name].get("use_soft") else A / "broll" / BROLL[name]["file"]
    for ext in (".mp4", ".png", ".jpg"):
        f = R / f"{name}{ext}"
        if f.exists():
            return f
    return R / "BG_soft.png"   # fallback backdrop, so a missing render never breaks the build


SHOTS, OV = [], []


def shot(t0, t1, src, move="push", tag="ILLUSTRATION", media_start=0.0, flick=None, src_b=None, warm=False, dim=False, origin=None):
    if not media_start and src in BROLL:
        media_start = BROLL[src].get("ms", 0.0)
    SHOTS.append(dict(t0=t0, t1=t1, src=src, move=move, tag=tag, ms=media_start, flick=flick, src_b=src_b, warm=warm, dim=dim, origin=origin))


def el(html_s, at, to=None):
    OV.append(dict(h=html_s, at=at, to=to))


def attrs(at, to, fx, d=None, extra=""):   # film times are written as F<seconds>; emit() converts them to part time
    s = f'data-at="F{at}" data-fx="{fx}"' + (f' data-to="F{to}"' if to is not None else "") + (f' data-d="{d}"' if d else "")
    return s + extra


def chip(text, at, to, x, y, col="amber", size="", fx="pop", icon=""):
    ic = f'<span class="ico">{icon}</span>' if icon else ""
    el(f'<div class="chip {size} c-{col}" style="left:{x}px;top:{y}px" {attrs(at, to, fx)}>{ic}{esc(text)}</div>', at, to)


def lbl(text, at, to, x, y, col="ink", fx="left"):
    el(f'<div class="lbl c-{col}" style="left:{x}px;top:{y}px" {attrs(at, to, fx)}>{esc(text)}</div>', at, to)


def cite(text, at, to):
    el(f'<div class="cite" {attrs(at, to, "fade")}>{esc(text)}</div>', at, to)


# ---------- phone screens (generic UPI app; no real brand) ----------
SB = '<div class="sbar"><span>9:41</span><span>5G ▮▮▮ 78%</span></div>'


def scr(body, at, to, cls="light", fx="cut"):
    return f'<div class="scr {cls}" {attrs(at, to, fx)}>{SB}{body}</div>'


def head(t="Pay"):
    return f'<div class="app-h"><span class="dot"></span>{t}</div>'


PAYEE = '<div class="payee"><div class="av">S</div><div class="nm">Sharma Kirana Store</div><div class="sub">UPI ID: sharmakirana@okbank</div></div>'


def sms(at, to, body, cls="", frm="YOUR BANK · SMS", when="now"):
    return f'<div class="notif {cls}" {attrs(at, to, "down")}><div class="from"><span>{frm}</span><span>{when}</span></div>{body}</div>'


def tap(t, x, y):
    return f'<div class="tap" style="left:{x}px;top:{y}px" {attrs(t, None, "tap")}></div>'


def phone(at, to, x, y, inner, rot=0, fx="up"):
    el(f'<div class="phone" data-rot="{rot}" style="left:{x}px;top:{y}px;transform:rotate({rot}deg) scale(.86)" {attrs(at, to, fx, 0.6)}>'
       f'<div class="scrn"><div class="cam"></div>{inner}<div class="glare"></div></div></div>', at, to)


# =====================================================================================================
# THE CUT (film seconds). VO cues in comments.
# =====================================================================================================
# ---- HOOK
shot(0.0, 4.4, "K_kirana", "slow", "PHOTO · IDEALIST JACK / FLICKR · PUBLIC DOMAIN", warm=True)           # "Your bank S.M.S. says ₹840 — debited."
phone(0.0, 7.0, 1240, 60, '<div class="wall"></div><div class="clock">9:41</div>'
      + sms(0.35, None, '<b>₹840.00 debited</b> from A/c XX4521 to Sharma Kirana Store. UPI Ref 4271 8830 1265.')
      + scr(head("Paying") + PAYEE + '<div class="amt">₹840</div><div class="stat"><div class="spin"></div><div class="t" style="color:#b7791f">Payment processing</div>'
            '<div class="s">Waiting for confirmation from the bank</div></div>', 4.45, None)
      + scr(head("Paying") + PAYEE + '<div class="amt">₹840</div><div class="stat"><div class="spin"></div><div class="t" style="color:#b7791f">Payment processing</div>'
            '<div class="s">Waiting for confirmation from the bank</div></div>'
            + sms(4.5, None, '<b>₹840.00 debited</b> from A/c XX4521 to Sharma Kirana Store.', ""), 4.45, None), rot=-4)
chip("₹840 debited", 0.4, 4.4, 140, 510, "red", "xl", "pop")
shot(4.4, 7.0, "K_paytm", "left", "PHOTO · SASHA INDIA / FLICKR · CC BY-SA 2.0", warm=True)           # "Your U.P.I. app says — processing."
chip("Processing", 4.6, 7.0, 360, 430, "amber", "", "pop", "⧗")
shot(7.0, 9.75, "SB_phonepe", "in", "DEVICE IMAGE · PHONEPE", warm=True)                          # "And the shop's soundbox? Silent."
chip("Silent", 8.7, 9.75, 1180, 330, "slate", "sm", "pop", "🔇")
shot(9.75, 11.85, "K_shopkeeper", "in", "PHOTO · THE_STEVE_COX / FLICKR · CC BY 2.0", warm=True, origin="68% 36%")            # "The shopkeeper is looking at you."
chip("Not received", 10.1, 11.85, 140, 820, "red", "sm", "left")
# "Don't pay again. Your money is not lost."
shot(11.85, 15.0, "kirana_soft3", "slow", "SIMULATED SCREEN", warm=True)
phone(11.85, 15.0, 725, 60, scr(head("Pay again?") + PAYEE + '<div class="amt">₹840</div>'
      + '<div class="btn">PAY ₹840</div>' , 11.85, None), fx="up")
el('<div class="ring" style="left:870px;top:820px;width:180px;height:180px" ' + attrs(12.0, 15.0, "pop") + "></div>", 12.0, 15.0)
chip("Don't pay again", 12.0, 15.0, 90, 300, "red", "sm", "pop", "✋")
chip("Not lost", 13.3, 15.0, 1340, 380, "green", "", "pop")
# "In a few minutes, you'll know exactly where it is, when it comes back, and the one mistake that makes people pay twice."
shot(15.0, 18.4, "street_soft", "right", "ILLUSTRATIVE FOOTAGE")
chip("₹840 → ?", 15.1, 17.0, 640, 400, "amber", "xl", "pop")
chip("Where?", 17.0, 18.4, 420, 400, "cyan", "xl", "pop")
chip("When?", 17.8, 18.4, 1000, 400, "cyan", "xl", "pop")
shot(18.4, 22.0, "kirana_soft", "out", "SIMULATED SCREEN", warm=True, media_start=3.0)
chip("Paying twice", 18.9, 22.0, 160, 400, "red", "xl", "pop", "✕")
phone(18.6, 22.0, 1240, 60, '<div class="wall"></div>' + sms(18.7, None, '<b>₹840.00 debited</b> · Sharma Kirana Store', "", when="2 min")
      + sms(19.6, None, '<b>₹840.00 debited</b> · Sharma Kirana Store', "n2"), rot=3, fx="rise")
# ---- FLOW
shot(22.0, 24.55, "hands_soft", "push", "SIMULATED SCREEN")                         # "Here's what happens after you type your pin."
pin_dots = '<div class="dots">' + "".join(f'<i style="position:relative"><span style="position:absolute;inset:-3px;border-radius:50%;background:#12161c" {attrs(22.45 + 0.24 * k, None, "pop", 0.15)}></span></i>' for k in range(6)) + "</div>"
keys = '<div class="keys">' + "".join(f"<span>{k}</span>" for k in "123456789") + "<span>⌫</span><span>0</span><span>✓</span></div>"
phone(22.0, 24.55, 725, 60, scr('<div class="pin" style="text-align:center"><div style="font:700 26px Inter;margin-top:30px">ENTER UPI PIN</div>' + pin_dots + "</div>" + keys, 22.0, None))
for k, (x, y) in enumerate([(110, 640), (330, 750), (220, 860), (110, 750), (330, 640), (220, 970)]):
    el(f'<div class="tap" style="left:{725 + 16 + x}px;top:{60 + 16 + y}px" {attrs(22.45 + 0.24 * k, None, "tap")}></div>', 22.45 + 0.24 * k)
shot(24.55, 29.55, "B09")                                                             # "First, your bank takes the money out..."
lbl("Step 1 · Debit", 25.0, 29.4, 120, 740, "cyan")
shot(29.55, 35.6, "S10_board", "in")                                                  # "Then N.P.C.I. steps in. It's not your app..."
for k, (c, g) in enumerate([("#3b5bdb", "₹"), ("#2f9e44", "P"), ("#e8590c", "U"), ("#7048e8", "B"), ("#0c8599", "A"), ("#c2255c", "W")]):
    x0, y0 = 160 + (k % 3) * 150, 260 + (k // 3) * 150
    el(f'<div class="app" style="left:{x0}px;top:{y0}px;background:{c}" {attrs(31.8 + 0.12 * k, 35.6, "pop")}>{g}</div>', 31.8 + 0.12 * k, 35.6)
el(f'<div class="arrow" style="left:640px;top:410px;width:300px" {attrs(32.9, 35.6, "grow", 0.6)}></div>', 32.9, 35.6)
chip("System behind all apps", 33.2, 35.6, 120, 600, "cyan", "sm", "up")
cite("[WORLD BANK | UPI CASE STUDY 2021]", 29.7, 35.6)
shot(35.6, 40.3, "B11")                                                               # "It calls the shop's bank and says, please add..."
chip("Please add ₹840", 37.4, 40.3, 1150, 250, "cyan", "sm", "pop", "☎")
shot(40.3, 42.9, "B12part")
chip("Like a phone call", 40.6, 44.0, 120, 740, "cyan", "sm", "up", "☎")                                                           # "...a phone call. And like every phone call in India..."
shot(42.9, 47.2, "B12_last", "slow")                                                  # "...three things can happen." (lamps light in 2D)
for k, (x, y, col, word) in enumerate([(360, 715, "green", "Success"), (960, 733, "red", "Failed"), (1650, 751, "amber", "Processing")]):
    el(f'<div class="glow g-{col}" style="left:{x - 70}px;top:{y - 70}px" {attrs(44.0 + 0.8 * k, 47.2, "fade", 0.2)}></div>', 44.0 + 0.8 * k, 47.2)
    lbl(word, 44.1 + 0.8 * k, 47.2, x - 80, y + 70, col, "up")
# ---- SUCCESS / FAILED
shot(47.2, 48.1, "L_calling", "in")                                                  # "One, the shop's bank picks up..."
shot(48.1, 53.0, "L_success", "in", origin="80% 45%")                                 # "...done, the shop got it — that's success."
el(f'<div class="flash" style="background:rgba(63,185,80,.35);z-index:16" {attrs(48.1, None, "flash")}></div>', 48.1)
chip("1", 47.3, 53.0, 120, 340, "green", "xl", "pop")
chip("Success", 51.6, 53.0, 260, 266, "green", "", "pop", "✓")
shot(53.0, 54.2, "L_calling", "out")                                                 # "Two, the shop's bank picks up and says, sorry..."
shot(54.2, 60.7, "L_failed", "in", origin="70% 50%")                                  # "...we can't take this... that's failed."
el(f'<div class="flash" style="background:rgba(248,81,73,.35);z-index:16" {attrs(54.2, None, "flash")}></div>', 54.2)
chip("2", 53.1, 60.7, 120, 340, "red", "xl", "pop")
chip("Failed", 59.0, 60.7, 260, 266, "red", "", "pop", "✕")
shot(60.7, 68.3, "L_failed", "zoomhome", origin="14% 25%")                          # "Failed sounds scary... comes back on its own."
chip("Clear answer", 62.0, 64.0, 120, 340, "red", "sm", "pop")
chip("Comes back by itself", 64.4, 68.3, 120, 340, "green", "sm", "pop", "↩")
cite("[NPCI UPI CIRCULAR | 2026]", 64.4, 68.3)
shot(68.3, 73.6, "kirana_soft2", "push", "SIMULATED SCREEN", warm=True, media_start=2.5)   # "So if it says failed, you can pay again."
phone(68.3, 73.6, 1240, 60, scr(head("Payment") + PAYEE + '<div class="stat"><div class="ic" style="background:#d63a3a">✕</div><div class="t" style="color:#c92a2a">Payment failed</div>'
      '<div class="s">Money, if debited, will come back to your account</div></div><div class="btn">TRY AGAIN</div>', 68.3, None)
      + tap(70.6, 235, 870), rot=-3)
chip("You can pay again", 69.2, 73.6, 160, 420, "green", "", "pop", "✓")
chip("Simple?", 71.9, 73.6, 160, 560, "ink", "sm", "pop")
# ---- PROCESSING
shot(73.6, 76.3, "L_calling", "slow")                                                # "Three. The troublemaker. N.P.C.I. calls..."
shot(76.3, 82.5, "L_drop", "none", media_start=0.0)                                   # "...the line goes quiet. Hello?... Hello?... Call dropped." (motion test)
chip("3", 73.8, 82.5, 120, 340, "amber", "xl", "pop")
chip("Hello?", 79.6, 81.5, 1250, 300, "ink", "sm", "pop")
chip("Hello?", 80.6, 81.5, 1350, 400, "ink", "sm", "pop")
cite("[NPCI UPI CIRCULAR | 2026]", 76.0, 82.5)
shot(82.5, 87.2, "S18_slot840", "in", flick=0.42, src_b="S18_slot0")                  # "Did the shop's bank add the money...? Nobody knows yet."
chip("Shop's balance: ₹0 or ₹840?", 82.7, 87.2, 760, 760, "amber", "sm", "pop")
chip("Nobody knows yet", 85.9, 87.2, 120, 740, "amber", "sm", "up")
shot(87.2, 90.8, "hands_soft", "slow", "SIMULATED SCREEN", media_start=2.0)          # "That's the processing you see — some apps call it pending."
phone(87.2, 90.8, 1240, 60, scr(head("Payment") + PAYEE + '<div class="amt">₹840</div><div class="stat"><div class="spin"></div><div class="t" style="color:#b7791f">Pending</div>'
      '<div class="s">We are checking with the bank</div></div>', 87.2, None), rot=-3)
chip("Pending = Processing", 88.6, 90.8, 140, 440, "amber", "", "pop")
cite("[NPCI | UPI HELP GUIDELINES]", 88.6, 90.8)
# ---- AT THE COUNTER
shot(90.8, 97.6, "K_store", "push", "PHOTO · NAMAN BHAGAT / WIKIMEDIA · CC BY-SA 4.0", warm=True)             # "So right there at the counter, don't pay again. Ask... bank S.M.S..."
chip("Don't pay again", 91.3, 93.6, 120, 390, "red", "", "pop", "✋")
chip("Check bank S.M.S.", 93.7, 97.6, 120, 390, "cyan", "", "pop")
chip("Not the soundbox", 95.4, 97.6, 120, 580, "slate", "sm", "pop")
phone(93.7, 97.6, 1290, 80, '<div class="wall"></div>' + sms(93.9, None, "<b>Checking…</b> Shop's bank S.M.S. inbox", frm="SHOP'S PHONE"), rot=3)
shot(97.6, 101.0, "kirana_soft3", "push", "SIMULATED SCREEN", warm=True, media_start=2.0)   # "And take a screenshot of your payment..."
phone(97.6, 101.0, 1240, 60, scr(head("Payment") + PAYEE + '<div class="amt">₹840</div><div class="stat"><div class="spin"></div><div class="t" style="color:#b7791f">Payment processing</div>'
      '<div class="s">UPI Ref 4271 8830 1265</div></div>', 97.6, None)
      + f'<div class="flash" {attrs(98.4, None, "flash")}></div><div class="thumb" {attrs(98.6, None, "pop")}><div style="font:800 34px Inter;text-align:center;margin-top:70px">₹840</div><div style="font:700 15px Inter;color:#b7791f;text-align:center;margin-top:8px">Processing</div><div style="font:500 11px Inter;text-align:center;margin-top:10px;opacity:.6">Ref 4271 8830 1265</div></div>', rot=-3)
chip("Screenshot = proof", 98.8, 101.0, 140, 440, "cyan", "", "pop", "📸")
# "Bank says received? Then the shop got your money... Nothing yet? Then it's still processing."
shot(101.0, 107.4, "BG_soft", "slow", "SIMULATED SCREEN")
phone(101.0, 107.4, 560, 60, '<div class="wall"></div>' + sms(101.2, None, '<b>₹840.00 received</b> in A/c XX7790 from customer. UPI Ref 4271 8830 1265.', frm="SHOP'S BANK · SMS"), rot=-2)
phone(104.7, 107.4, 1120, 60, '<div class="wall"></div><div class="clock" style="font-size:70px;top:430px">No new S.M.S.</div>', rot=2)
chip("Received", 102.4, 107.4, 620, 820, "green", "sm", "pop", "✓")
chip("Nothing yet", 105.8, 107.4, 1210, 820, "amber", "sm", "pop", "⧗")
# "Show them your screenshot and say — it's stuck, not lost. If it reaches you... If not, it comes back to me."
shot(107.4, 111.4, "kirana_soft", "push", "SIMULATED SCREEN", warm=True, media_start=9.0)
shot(111.4, 116.6, "kirana_soft2", "slow", "SIMULATED SCREEN", warm=True, media_start=7.0)
phone(107.4, 111.4, 1240, 60, scr(head("Payment") + PAYEE + '<div class="amt">₹840</div><div class="stat"><div class="spin"></div><div class="t" style="color:#b7791f">Processing</div>'
      '<div class="s">Screenshot saved · UPI Ref 4271 8830 1265</div></div>', 107.4, None), rot=-3)
chip("Tell the shopkeeper", 107.6, 116.6, 120, 340, "ink", "sm", "pop", "💬")
chip("Stuck, not lost", 109.6, 111.3, 120, 490, "amber", "", "pop")
chip("Reaches you → S.M.S.", 111.4, 116.6, 420, 420, "green", "xl", "pop")
chip("If not → back to me", 113.7, 116.6, 420, 620, "cyan", "xl", "pop", "↩")
# ---- WHERE IS IT
shot(116.6, 119.5, "S24_where", "in")                                                 # "So where is your money right now?" (music silent 1.5 s before)
chip("Where is ₹840?", 116.9, 119.5, 120, 340, "amber", "", "pop")
shot(119.5, 124.6, "S25a_hold", "in")                                                 # "...N.P.C.I. doesn't cancel the payment — it puts it on hold."
chip("Not cancelled", 120.6, 124.6, 120, 340, "ink", "sm", "pop")
chip("On hold", 123.2, 124.6, 1250, 330, "amber", "", "pop", "⏸")
cite("[NPCI UPI CIRCULAR | 2026]", 119.7, 131.4)
shot(124.6, 129.6, "S25b_hold", "right")                                              # "...stuck between your bank and the shop's bank."
lbl("Your bank", 125.4, 129.6, 120, 740, "slate")
lbl("Shop's bank", 126.6, 129.6, 1440, 740, "slate")
chip("Between banks", 127.6, 129.6, 760, 250, "amber", "sm", "pop")
shot(129.6, 131.4, "S24_where", "zoomhome", origin="66% 62%")                                                 # "Not lost — just waiting."
chip("Not lost · just waiting", 129.7, 131.4, 120, 740, "green", "sm", "up")
# ---- THE ANSWER
shot(131.4, 138.8, "BG_soft", "slow")                                                # "Now the shop's bank has to answer one simple question..."
el(f'<div class="ledger" style="left:360px;top:240px;width:1200px" {attrs(131.6, 141.4, "up", 0.5)}><div class="lh">SHOP&#39;S BANK · LEDGER</div>'
   f'<div class="lr"><span>Customer payment</span><b>₹840</b><i {attrs(131.6, 138.95, "cut")} data-cut>?</i></div><div class="lr dim2"><span>Milk booth</span><b>₹56</b><i>✓</i></div>'
   f'<div class="lr dim2"><span>Electricity</span><b>₹1,240</b><i>✓</i></div></div>', 131.6, 141.4)
el(f'<div class="ledger" style="left:360px;top:240px;width:1200px" {attrs(143.1, 147.0, "cut")}><div class="lh">SHOP&#39;S BANK · LEDGER</div>'
   f'<div class="lr"><span>Customer payment</span><b>₹840</b><i {attrs(143.1, 143.25, "cut")} data-cut>?</i></div><div class="lr dim2"><span>Milk booth</span><b>₹56</b><i>✓</i></div>'
   f'<div class="lr dim2"><span>Electricity</span><b>₹1,240</b><i>✓</i></div></div>', 143.1, 147.0)
chip("In the shop's account?", 133.2, 138.8, 360, 600, "ink", "sm", "pop")
chip("Only two answers", 137.4, 138.8, 360, 720, "amber", "sm", "pop")
cite("[NPCI | UPI OC 213]", 131.6, 147.0)
shot(138.8, 141.4, "BG_soft", "in")                                                  # "Yes? Then the shop has your money..."
el(f'<div class="stampmark c-green" style="left:1270px;top:330px" {attrs(138.95, 141.4, "stamp", 0.18)}>YES</div>', 138.95, 141.4)
chip("Into shop's account", 139.7, 141.4, 360, 820, "green", "sm", "pop", "→")
shot(141.4, 143.1, "BG_soft", "in")                                                  # "...even though the soundbox stayed silent."
phone(141.4, 143.1, 1240, 60, '<div class="wall"></div>' + sms(141.5, None, '<b>₹840.00 received</b> in A/c XX7790. UPI Ref 4271 8830 1265.', frm="SHOP'S BANK · SMS", when="next day"), rot=-2)
chip("Soundbox stayed silent", 141.6, 143.1, 120, 420, "slate", "sm", "pop", "🔇")
shot(143.1, 147.0, "BG_soft", "out")                                                  # "No? Then it comes back to your bank, and into your account."
el(f'<div class="stampmark c-red" style="left:1300px;top:330px" {attrs(143.25, 147.0, "stamp", 0.18)}>NO</div>', 143.25, 147.0)
chip("Back to your account", 144.2, 147.0, 360, 820, "green", "sm", "pop", "↩")
# ---- THE DEADLINE (2D calendar over the blurred room)
DAYS = ["WED", "THU", "FRI", "SAT", "SUN", "MON", "TUE", "WED"]   # T+4 is a Sunday: "Sundays included" is true on screen


def calendar(at, to, x, y, labels=True):
    cells = "".join(f'<div class="d{" sun" if w == "SUN" else ""}"><div class="w">{w}</div><div class="n">{15 + i}</div>'
                    f'<div class="t">{"TODAY" if i == 0 else f"T+{i}"}</div></div>' for i, w in enumerate(DAYS))
    el(f'<div class="cal" style="left:{x}px;top:{y}px" {attrs(at, to, "up", 0.5)}>{cells}</div>', at, to)


shot(147.0, 152.6, "BG_soft", "slow")                                                 # "How long can this take? If the money didn't reach them..."
calendar(147.3, 152.6, 128, 360)
calendar(156.6, 171.0, 128, 360)
chip("How long?", 147.2, 152.6, 900, 200, "ink", "", "pop")
el(f'<div class="mark amber" style="left:120px;top:352px;width:212px;height:226px" {attrs(148.8, 152.6, "pop")}></div>', 148.8, 152.6)
chip("Failed or processing", 151.0, 152.6, 120, 660, "amber", "sm", "up")
shot(152.6, 156.6, "rbi_table", "in", "R.B.I. CIRCULAR · 2019")                      # "...the bank must return it, and the R.B.I. has set a deadline."
cite("[RBI CIRCULAR | SEP 2019]", 152.7, 171.0)
shot(156.6, 159.6, "BG_soft", "slow")                                                 # "Paid a person? Back by the next day."
el(f'<div class="mark" style="left:330px;top:352px;width:212px;height:226px" {attrs(157.8, 171.0, "pop")}></div>', 157.8, 171.0)
el(f'<div class="rowlbl c-green" style="left:128px;top:630px" {attrs(156.8, 171.0, "left")}>👤 Person → next day · T+1</div>', 156.8, 171.0)
shot(159.6, 168.0, "BG_soft", "in")                                                   # "Paid a shop or a business? Within five days — ... Sundays included..."
el(f'<div class="rowlbl c-amber" style="left:128px;top:720px" {attrs(159.7, 171.0, "left")}>🏪 Shop → five days · T+5</div>', 159.7, 171.0)
el(f'<div class="bar5" style="left:338px;top:588px;width:1036px" {attrs(161.4, 171.0, "grow", 2.0)}></div>', 161.4, 171.0)
el(f'<div class="mark amber" style="left:1170px;top:352px;width:212px;height:226px" {attrs(163.4, 171.0, "pop")}></div>', 163.4, 171.0)
chip("Sundays count", 164.2, 168.0, 1000, 180, "orange", "sm", "pop")
shot(168.0, 171.0, "BG_soft", "out")                                                  # "Person, one day. Shop, five days."
chip("Person · 1 day", 168.1, 171.0, 1180, 640, "green", "sm", "pop")
chip("Shop · 5 days", 169.5, 171.0, 1180, 760, "amber", "sm", "pop")
# "And if the bank takes longer, it has to pay you ₹100 for every extra day. You don't even have to complain..."
shot(171.0, 177.9, "BG_soft", "slow")
el(f'<div class="acct" style="left:128px;top:560px" {attrs(171.2, 183.2, "up")}><div class="k">YOUR ACCOUNT · BANK PAYS</div>'
   f'<div class="v" style="position:relative;height:92px"><span style="position:absolute" {attrs(171.2, 175.3, "cut")} data-cut>+₹0</span><span style="position:absolute" {attrs(175.3, 177.4, "pop", 0.2)} data-cut>+₹100</span><span style="position:absolute" {attrs(177.4, 183.2, "pop", 0.2)}>+₹200</span></div><div class="s">₹100 for every extra day</div></div>', 171.2, 183.2)
calendar(171.2, 183.2, 128, 250)
el(f'<div class="mark amber" style="left:1170px;top:242px;width:212px;height:226px" {attrs(171.4, 183.2, "cut")}></div>', 171.4, 183.2)
for k, (t, x) in enumerate([(175.3, 0), (177.4, 0)]):
    el(f'<div class="coin" style="left:{720 + k * 150}px;top:660px" {attrs(t, 183.2, "fall")}>₹100</div>', t, 183.2)
lbl("T+6 · late", 174.4, 183.2, 1388, 476, "red")
el(f'<div class="mark amber" style="left:1380px;top:242px;width:212px;height:226px;border-color:var(--red)" {attrs(175.3, 183.2, "pop")}></div>', 175.3, 183.2)
el(f'<div class="mark amber" style="left:1590px;top:242px;width:212px;height:226px;border-color:var(--red)" {attrs(177.4, 183.2, "pop")}></div>', 177.4, 183.2)
shot(177.9, 183.2, "BG_soft", "in")
chip("No complaint needed", 178.1, 183.2, 1000, 120, "green", "sm", "pop")
chip("R.B.I. rule", 181.8, 183.2, 1000, 680, "cyan", "sm", "pop")
# ---- SUMMARY
shot(183.2, 187.9, "S35a_lamps", "in")                                                # "Quick summary... Success — the shop got it."
chip("Shop got it", 185.8, 187.9, 120, 740, "green", "", "up", "✓")
shot(187.9, 192.9, "S35b_lamps", "in")                                                # "Failed — it didn't go through... you can pay again."
chip("Pay again", 188.1, 192.9, 120, 740, "green", "", "up", "↻")
shot(192.9, 195.1, "S35c_lamps", "in")                                                # "Processing — don't pay again."
chip("Don't pay", 193.0, 195.1, 120, 740, "amber", "", "up", "✋")
shot(195.1, 200.8, "BG_soft", "slow")                                                 # "If it never reaches the shop... one day for a person, five days for a shop."
calendar(195.1, 200.8, 128, 250)
el(f'<div class="mark" style="left:330px;top:242px;width:212px;height:226px" {attrs(195.4, 200.8, "pop")}></div>', 195.4, 200.8)
el(f'<div class="mark amber" style="left:1170px;top:242px;width:212px;height:226px" {attrs(196.6, 200.8, "pop")}></div>', 196.6, 200.8)
el(f'<div class="rowlbl c-green" style="left:128px;top:540px" {attrs(195.3, 200.8, "left")}>👤 Person → 1 day</div>', 195.3, 200.8)
el(f'<div class="rowlbl c-amber" style="left:128px;top:630px" {attrs(196.5, 200.8, "left")}>🏪 Shop → 5 days</div>', 196.5, 200.8)
chip("One rule →", 197.6, 200.8, 1380, 740, "cyan", "sm", "left")
# ---- THE ONE RULE
shot(200.8, 205.5, "S36_rule", "in")                                                  # "My one rule: never pay again while it says processing."
chip("One rule", 201.2, 205.5, 120, 340, "amber", "", "pop")
chip("Processing → don't pay", 202.6, 205.5, 120, 520, "amber", "sm", "pop")
shot(205.5, 209.9, "hands_soft", "push", "SIMULATED SCREEN", media_start=4.0)        # "Because if that first payment turns out to be a yes..."
phone(205.5, 209.9, 1240, 60, '<div class="wall"></div>' + sms(206.0, None, '<b>₹840.00 debited</b> · Sharma Kirana Store', "", when="10:02")
      + sms(207.4, None, '<b>₹840.00 debited</b> · Sharma Kirana Store', "n2", when="10:03"), rot=-3)
chip("First one: yes", 206.6, 209.9, 140, 440, "green", "sm", "pop")
shot(209.9, 214.2, "S37b_twice", "in")                                                # "...congrats, you just paid ₹840... twice."
chip("Paid twice", 212.4, 214.2, 120, 340, "red", "xl", "pop")
# ---- UPI HELP
shot(214.2, 220.9, "hands_soft", "slow", "SIMULATED SCREEN", media_start=1.0)        # "Don't want to wait? Open your app... U.P.I. Help."
hist = ('<div class="list">' + "".join(f'<div class="it"><span class="ic"></span>{n}<span class="r">{a}</span></div>' for n, a in [("Mobile recharge", "₹299"), ("Sharma Kirana Store", "₹840"), ("Milk booth", "₹56"), ("Electricity bill", "₹1,240")]) + "</div>")
phone(214.2, 226.0, 725, 60, scr(head("History") + hist, 214.2, 217.6)
      + tap(217.3, 230, 370)
      + scr(head("Payment details") + PAYEE + '<div class="amt" style="font-size:72px">₹840</div><div style="text-align:center;color:#b7791f;font:800 28px Inter">Pending</div><div class="help">UPI Help · Raise a complaint</div>', 217.6, 220.9)
      + tap(220.0, 210, 760)
      + scr(head("UPI Help") + '<div style="font:600 24px Inter;opacity:.7;margin:10px 0 18px">What went wrong?</div>'
            + "".join(f'<div class="opt{" hl" if o == "Duplicate payment" else ""}">{o}</div>' for o in ["Money debited, not received", "Payment pending for long", "Duplicate payment", "Other issue"]), 220.9, None))
cite("[NPCI | UPI HELP GUIDELINES]", 215.5, 226.0)
chip("← Tap U.P.I. Help", 219.2, 220.9, 1220, 560, "cyan", "sm", "left")
chip("← Duplicate payment", 222.6, 226.0, 1220, 560, "amber", "sm", "left")
shot(220.9, 226.0, "kirana_soft", "push", "SIMULATED SCREEN", warm=True, media_start=6.0)
chip("Raise it now", 221.0, 226.0, 150, 420, "cyan", "sm", "pop")
# ---- ESCALATE (ladder)
shot(226.0, 232.1, "kirana_soft2", "slow", "ILLUSTRATIVE FOOTAGE", media_start=8.0)                                                 # "Still not solved? Complain to your bank. Bank not fixing it? ... R.B.I."
for k, (t, txt) in enumerate([(226.0, "U.P.I. Help"), (227.2, "Your bank"), (230.0, f'<span {attrs(230.0, 234.2, "cut")} data-cut>R.B.I.</span><span style="position:absolute;left:108px" {attrs(234.2, 238.2, "pop")} class="c-cyan">R.B.I. Ombudsman</span>')]):
    el(f'<div class="step" style="left:{140 + k * 560}px;top:{640 - k * 170}px" {attrs(t, 238.2, "up")}><span class="no">{k + 1}</span>{txt}</div>', t, 238.2)
    if k:
        el(f'<div class="arrow" style="left:{140 + k * 560 - 100}px;top:{715 - k * 170 + 85}px;width:90px;transform:rotate(-30deg)" {attrs(t - 0.2, 238.2, "grow", 0.3)}></div>', t - 0.2, 238.2)
cite("[RBI CIRCULAR | SEP 2019]", 230.0, 238.2)
shot(232.1, 238.2, "kirana_soft3", "in", "ILLUSTRATIVE FOOTAGE", media_start=12.0)                                                   # "The office has a strange name — the R.B.I. Ombudsman. Remember it."
chip("Remember it", 235.5, 238.2, 1340, 560, "amber", "sm", "pop")
# ---- SHARE + BRIDGE
shot(238.2, 242.7, "street_soft", "slow", "SIMULATED SCREEN", media_start=3.0)       # "Send this to that one friend who always pays twice..."
phone(238.2, 242.7, 725, 60, '<div class="wall"></div>' + f'<div class="share" {attrs(238.2, None, "cut")}><div class="ttl">Share to</div><div class="ppl">'
      + "".join(f'<div class="{"hl" if n == "Pays Twice" else ""}"><i></i>{n}</div>' for n in ["Amma", "Ravi", "Office group", "Pays Twice", "Sneha", "Arjun", "Family", "More"]) + "</div></div>")
chip("You know one", 240.0, 242.7, 150, 420, "amber", "sm", "pop", "😄")
shot(242.7, 251.7, "L_success", "zoomboard", origin="50% 26%")                             # "Next video: what really happens in those few seconds after you hit pay..."
chip("Next: when it works", 243.4, 251.7, 120, 740, "cyan", "sm", "up")
shot(251.7, END, "B43_end", "slow", "")
el('<div class="endcard" ' + attrs(251.9, None, "fade", 0.8) + '><img class="logo" src="media/logo_square.png" alt=""/><div class="ch">Be Practical<br/>with Kishore</div>'
   '<div class="sub">SUBSCRIBE</div><div class="tile"><img src="media/B43_end.png" alt=""/><div class="nx">NEXT VIDEO</div>'
   '<div class="tt">The 3 seconds after you hit pay</div></div></div>', 251.9)

# ---------- telemetry HUD: two persistent lines + pop rows (values only when the VO says them) ----------
HUD = {  # field -> [(t, text, colour)]
    "STATUS": [(0.0, "—", "slate"), (4.5, "PROCESSING", "amber"), (24.6, "DEBIT ✓", "cyan"), (36.0, "CALLING…", "cyan"),
               (48.1, "SUCCESS ✓", "green"), (54.0, "CALLING…", "cyan"), (54.2, "FAILED ✕", "red"), (73.8, "CALLING…", "cyan"),
               (81.7, "PROCESSING", "amber"), (138.9, "ANSWER: YES", "green"), (143.25, "ANSWER: NO", "red"), (147.0, "PROCESSING", "amber"),
               (185.7, "SUCCESS ✓", "green"), (188.0, "FAILED ✕", "red"), (193.0, "PROCESSING", "amber"),
               (195.1, "RECAP", "ink"), (200.8, "ONE RULE", "amber"), (214.2, "TIPS", "cyan")],
    "MONEY AT": [(0.0, "?", "slate"), (24.6, "YOUR BANK", "ink"), (26.0, "LEFT YOUR A/C", "amber"), (36.0, "ON THE CALL", "cyan"),
                 (50.4, "SHOP", "green"), (54.0, "ON THE CALL", "cyan"), (62.0, "COMING BACK", "red"), (67.1, "YOUR A/C", "green"),
                 (75.5, "ON THE CALL", "cyan"), (82.2, "?", "amber"), (123.3, "BETWEEN BANKS", "amber"), (140.8, "SHOP", "green"),
                 (145.0, "YOUR A/C", "green"), (147.0, "BETWEEN BANKS", "amber"), (183.2, "—", "slate")],
}
POPS = [  # (at, to, key, value, colour, illustrative)
    (0.6, 11.8, "BALANCE", "₹5,240 → ₹4,400", "amber", True), (26.0, 29.5, "BALANCE", "₹4,400", "amber", True),
    (37.4, 40.3, "LEG TIMER", "0.0 → 3.0 s", "cyan", True), (67.2, 73.5, "BALANCE", "₹5,240", "green", True),
    (76.0, 82.4, "LEG TIMER", "15.0 s · TIMEOUT", "red", False), (147.2, 171.0, "DAY", "T+0 → T+5", "amber", False),
    (171.2, 183.2, "BANK OWES", "₹100 / DAY", "red", False), (210.6, 214.2, "BALANCE", "₹3,560", "red", True),
]
HUD_OFF = 238.2   # "HUD collapses" for the share and the bridge

# ---------- captions from the sentence cues (numbers as digits, bold) ----------
NUMS = [("eight hundred and forty rupees", "₹840"), ("one hundred rupees", "₹100"), ("five normal days", "5 normal days"),
        ("five working days", "5 working days"), ("five days", "5 days"), ("one day", "1 day")]


def capify(s):
    for a, b in NUMS:
        s = s.replace(a, b)
    s = esc(s)
    return re.sub(r"(₹\d[\d,]*|\b\d+ (?:normal |working )?days?\b)", r"<b>\1</b>", s)


def captions():
    m = [l.rstrip("\n").split("\t") for l in open(P / "align_sent/sentence_line_map.tsv")]
    rows = list(csv.DictReader(open(P / "align_sent/slots_edit.csv")))
    out = []
    for (_, text), r in zip(m, rows):
        a, b = float(r["speech_start"]), float(r["speech_end"])
        parts, cur = [], ""
        for w in re.split(r"(?<=[,—?])\s+|\s+(?=—)", text):
            if cur and len(cur) + len(w) > 46:
                parts.append(cur); cur = w
            else:
                cur = (cur + " " + w).strip()
        parts.append(cur)
        tot = sum(len(p) for p in parts); t = a
        for n, p in enumerate(parts):   # chunks hand over exactly; only a sentence's last chunk lingers
            d = (b - a) * len(p) / tot
            out.append((round(t, 2), round(t + d + (0.12 if n == len(parts) - 1 else 0.0), 2), capify(p))); t += d
    return out


# ---------- emit parts ----------
def r3(x):
    return round(x, 3)


def emit():
    caps = captions()
    copied = {}
    for k in range(len(PARTS) - 1):
        t0, t1 = PARTS[k], PARTS[k + 1]; D = r3(t1 - t0); pid = f"p{k + 1}"; d = OUTV / pid
        shutil.rmtree(d / "media", ignore_errors=True); (d / "media").mkdir(parents=True, exist_ok=True)
        shutil.copytree(OUTV / "_shared", d / "shared", dirs_exist_ok=True)
        shutil.copy(ROOT / "assets/brand/logo_square.png", d / "media/logo_square.png")
        (d / "vendor/fonts").mkdir(parents=True, exist_ok=True)   # self-vendored (scripts/vendor-assets.mjs aborts on an unrelated project)
        shutil.copy(ROOT / "node_modules/gsap/dist/gsap.min.js", d / "vendor/gsap.min.js")
        for f in ["inter/files/inter-latin-600-normal.woff2", "inter/files/inter-latin-800-normal.woff2", "inter/files/inter-latin-ext-600-normal.woff2",
                  "inter/files/inter-latin-ext-800-normal.woff2", "jetbrains-mono/files/jetbrains-mono-latin-700-normal.woff2",
                  "jetbrains-mono/files/jetbrains-mono-latin-800-normal.woff2"]:
            shutil.copy(ROOT / "node_modules/@fontsource" / f, d / "vendor/fonts" / Path(f).name)
        if (R / "B43_end.png").exists():
            shutil.copy(R / "B43_end.png", d / "media/B43_end.png")
        loc = lambda x: r3(x - t0)
        H = []
        for i, s in enumerate(x for x in SHOTS if t0 - 1e-6 <= x["t0"] < t1 - 1e-6):
            st, du = loc(s["t0"]), r3(s["t1"] - s["t0"]); src = media(s["src"])
            fn = f"media/{src.name}"; shutil.copy(src, d / fn) if not (d / fn).exists() else None
            cls = "shot" + (" warm" if s["warm"] else "")
            tag = f'<div class="tag">{esc(s["tag"])}</div>' if s["tag"] else ""
            if src.suffix == ".mp4":
                H.append(f'      <div id="{pid}-s{i}" class="{cls}" data-vs="{st}" data-vd="{du}" style="visibility:hidden"><video id="{pid}-v{i}" class="m" src="{fn}" muted playsinline '
                         f'data-move="{s["move"]}" data-start="{st}" data-duration="{du}" data-media-start="{s["ms"]}" data-track-index="2" data-volume="0"></video></div>')
                H.append(f'      <div class="vover {"warm" if s["warm"] else ""}" data-vs="{st}" data-vd="{du}" style="visibility:hidden">{tag}</div>')
            else:
                b = ""
                if s["src_b"]:
                    sb = media(s["src_b"]); shutil.copy(sb, d / f"media/{sb.name}")
                    b = f'<img class="m b" src="media/{sb.name}" alt="" data-move="{s["move"]}" />'
                flick = f' data-flick="{s["flick"]}"' if s["flick"] else ""
                H.append(f'      <div id="{pid}-s{i}" class="{cls}" data-start="{st}" data-duration="{du}" data-track-index="1"{flick}>'
                         f'<img class="m a" src="{fn}" alt="" data-move="{s["move"]}"{f' data-origin="{s["origin"]}"' if s["origin"] else ""} />{b}{"<div class=dim></div>" if s["dim"] else ""}{tag}</div>')
        O = []
        for o in OV:
            a, b = o["at"], o["to"] if o["to"] is not None else END
            if b <= t0 or a >= t1:
                continue
            h = re.sub(r'(data-(?:at|to)=")F([\d.]+)"', lambda mm: f'{mm.group(1)}{min(D, max(0.0, loc(float(mm.group(2)))))}"', o["h"])
            h = re.sub(r'(data-count="[\d.]+,[\d.]+,)F([\d.]+)', lambda mm: f'{mm.group(1)}{loc(float(mm.group(2)))}', h)
            O.append("      " + h)
        hud = hud_html(t0, t1)
        cap = "\n".join(f'      <div class="cap" data-at="{max(0.0, loc(a))}" data-to="{min(D, loc(b))}" data-fx="fade" data-d="0.12">{c}</div>'
                        for a, b, c in caps if b > t0 and a < t1)
        (d / "index.html").write_text(PAGE.format(pid=pid, D=D, shots="\n".join(H), ov="\n".join(O), hud=hud, cap=cap))
        print(f"{pid}: {t0:.1f}-{t1:.1f} ({D:.1f}s) {sum(1 for x in SHOTS if t0 - 1e-6 <= x['t0'] < t1 - 1e-6)} shots, {len(O)} overlays")


def hud_html(t0, t1):
    D = t1 - t0; loc = lambda x: r3(x - t0)
    rows = []
    for key, seq in HUD.items():
        vals = []
        for i, (t, txt, col) in enumerate(seq):
            nt = seq[i + 1][0] if i + 1 < len(seq) else END
            a, b = max(t, t0), min(nt, t1, HUD_OFF)
            if b <= a:
                continue
            vals.append(f'<span class="v c-{col}" data-at="{loc(a)}" data-to="{loc(b)}" data-fx="{"cut" if a == t0 else "up"}" data-d="0.25" data-cut>{esc(txt)}</span>')
        rows.append(f'<div class="row"><span class="k">{key}</span><span class="vals">{"".join(vals)}</span></div>')
    pops = []
    for (a, b, key, val, col, ill) in POPS:
        if b <= t0 or a >= t1:
            continue
        A_, B_ = loc(max(a, t0)), loc(min(b, t1))
        slot = sum(1 for p in POPS if p[0] < a and p[1] > a) * 52
        pops.append(f'<div class="pop" style="top:{slot}px;border-left-color:var(--{col})" data-at="{A_}" data-to="{B_}" data-fx="left">'
                    f'<span class="k">{key}</span><span class="v c-{col}">{esc(val)}</span></div>')
        if ill:
            pops.append(f'<div class="illus" style="top:{slot + 52}px" data-at="{A_}" data-to="{B_}" data-fx="fade">ILLUSTRATIVE</div>')
    vis = f'data-at="0" data-to="{min(D, loc(HUD_OFF))}" data-fx="cut" data-cut' if t0 < HUD_OFF else 'style="display:none"'
    return f'<div class="hud" {vis}><div class="panel">{"".join(rows)}</div><div class="pops" style="position:relative">{"".join(pops)}</div></div>'


PAGE = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>UPI money deducted: {pid}</title>
    <script src="vendor/gsap.min.js"></script>
    <link rel="stylesheet" href="shared/upi.css" />
    <script src="shared/upi.js"></script>
    <style>
      @font-face {{ font-family: "Inter"; font-weight: 600; src: url("vendor/fonts/inter-latin-600-normal.woff2") format("woff2"); }}
      @font-face {{ font-family: "Inter"; font-weight: 800; src: url("vendor/fonts/inter-latin-800-normal.woff2") format("woff2"); }}
      @font-face {{ font-family: "Inter"; font-weight: 800; src: url("vendor/fonts/inter-latin-ext-800-normal.woff2") format("woff2"); unicode-range: U+20B9, U+0100-024F; }}
      @font-face {{ font-family: "Inter"; font-weight: 600; src: url("vendor/fonts/inter-latin-ext-600-normal.woff2") format("woff2"); unicode-range: U+20B9, U+0100-024F; }}
      @font-face {{ font-family: "JetBrains Mono"; font-weight: 700; src: url("vendor/fonts/jetbrains-mono-latin-700-normal.woff2") format("woff2"); }}
      @font-face {{ font-family: "JetBrains Mono"; font-weight: 800; src: url("vendor/fonts/jetbrains-mono-latin-800-normal.woff2") format("woff2"); }}
    </style>
  </head>
  <body>
    <!-- Generated by projects/upi-money-deducted/build/make_film.py. Edit that, not this file. -->
    <div id="root" data-composition-id="{pid}" data-start="0" data-width="1920" data-height="1080" data-duration="{D}">
{shots}
      <div class="grade" style="z-index:15"></div>
{ov}
      {hud}
{cap}
      <img class="bug" src="media/logo_square.png" alt="Be Practical with Kishore" />
      <canvas id="grain" width="500" height="290"></canvas>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      UPI_animate(tl, {D});
      window.__timelines["{pid}"] = tl;
    </script>
  </body>
</html>
"""

if __name__ == "__main__":
    emit()
