#!/usr/bin/env python3
"""Write every scene in scenes.py to video/cantpay/<id>/ (index.html, params.js, img/ copies of its props or plates)
and its sound-effect track to assets/scenes/<id>.sfx.wav. Times become relative to the scene's start.
  python3 build/make_scenes.py [id ...]        (shoots missing props first: build/props_lib.py)
Then render with build/render_scenes.sh."""
import json, re, shutil, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import props_lib                         # noqa: E402

P = Path(__file__).resolve().parents[1]
ROOT = P.parents[1]
OUT = ROOT / "video/cantpay"
SFX = P / "assets/scenes"
DRAWN = {"path", "split", "bill", "coins", "card", "pos", "phone", "calendar", "meter", "toggle", "net", "scale", "bars", "arrow", "loop", "box",
         "contact", "house", "slider", "seesaw", "calc", "ring", "strike", "cross"}


def put(path, text):
    if not path.exists() or path.read_text() != text:
        path.write_text(text)


def rel_item(it, t0, dur):
    r = lambda t: round(min(dur, max(0.0, t - t0)), 2)
    o = {(k[:-1] if k.endswith("_") else k): v for k, v in it.items() if not k.startswith("_")}   # in_ / from_ (Python keywords)
    for k in ("at", "hlAt", "onAt", "bandAt", "bandShatterAt", "exit", "until"):
        if k in o:
            o[k] = r(o[k])
    if "moves" in o:
        o["moves"] = [dict(m, at=r(m["at"])) for m in o["moves"]]
    for k in ("needle", "tilt", "spin", "knob"):
        if k in o:
            o[k] = [[0, v[1]] if i == 0 else [r(v[0]), *v[1:]] for i, v in enumerate(o[k])]
    if "grow" in o:
        o["grow"] = [r(t) for t in o["grow"]]
    if "steps" in o:
        o["steps"] = [[r(a), *rest] for a, *rest in o["steps"]]
    return o


def page_sfx(items):
    cues = []
    for it in items:
        how = it.get("in") or ("draw" if it["kind"] in DRAWN else "pop")
        snd = {"draw": "scribble", "pop": "pop", "stamp": "thud", "slide": "whoosh", "drop": "rip", "fade": None}[how]
        if it["kind"] in ("coins",):
            snd = "clink"
        if it["kind"] in ("cross", "strike"):
            snd = "scribble"
        if snd:
            cues.append([it["at"], snd])
        cues += [[m["at"], "whoosh"] for m in it.get("moves", [])]
        cues += [[t, "pop"] for t in it.get("grow", [])]
    cues += [[t, "whoosh"] for t in sorted({it["exit"] for it in items if it.get("exit") is not None})]
    cues.sort()
    out = []
    for c in cues:
        if out and (c[0] - out[-1][0] < 0.12 or (c[1] == out[-1][1] and c[0] - out[-1][0] < 0.25)):
            continue
        out.append(c)
    return out


def page_cam(items, dur, push=0.06):
    """Slow push toward each page's content (from its first item to its page turn); reset during the turn."""
    turns = sorted({it["exit"] for it in items if it.get("exit") is not None and it["exit"] < dur - 0.3}) + [dur]
    keys, t_prev = [[0, 1.0, 0, 0, 0]], 0.0
    for turn in turns:
        its = [it for it in items if (it.get("exit") if it.get("exit") is not None and it["exit"] < dur - 0.3 else dur) == turn]
        if not its:
            continue
        t0 = max(t_prev, min(it["at"] for it in its) - 0.2)
        cx = sum(it.get("x", 960) + it.get("w", 0) / 2 * (it["kind"] == "photo") for it in its) / len(its)
        cy = sum(it.get("y", 540) + it.get("h", 0) / 2 * (it["kind"] == "photo") for it in its) / len(its)
        keys.append([round(t0, 2), 1.0, 0, 0, 0.01])
        keys.append([round(t0 + 0.02, 2), round(1 + push, 3), round(-(cx - 960) * push, 1), round(-(cy - 540) * push, 1), round(max(0.6, turn - t0 - 0.05), 2)])
        t_prev = turn + 0.36
    return keys


def build(sid, d):
    t0, dur = d["start"], round(d["end"] - d["start"], 2)
    f = OUT / sid; (f / "img").mkdir(parents=True, exist_ok=True)
    r = lambda t: round(min(dur, max(0.0, t - t0)), 2)
    if d["kind"] == "page":
        items = [rel_item(it, t0, dur) for it in d["items"]]
        first = min(it["at"] for it in items)   # never open on an empty page: the opening items are there from the cut
        for it in items:
            if it["at"] - first < 0.5 and first < 1.2:
                it["at"] = 0.0
                if it["kind"] == "photo":
                    it["opaque"] = True
        for it in items:
            if it.get("float") and "until" not in it:
                it["until"] = it.get("exit", dur)
        imgs = {it["src"][4:-4] for it in items if it["kind"] == "photo"}
        scene = dict(duration=dur, tag=d.get("tag", ""), kicker=d.get("kicker", ""), items=items,
                     sfx=page_sfx(items) + [[r(t), s] for t, s in d.get("sfx", [])], cam=d.get("cam") or page_cam(items, dur))
        tpl = ROOT / "video/lib/doodle/scene.html"
    else:
        layers = [dict(L, src=f"img/{L['src']}.png", at=r(L.get("at", t0)), **({"out": r(L["out"])} if "out" in L else {})) for L in d["layers"]]
        imgs = {L["src"] for L in d["layers"]}
        scene = dict(duration=dur, tag=d.get("tag", ""), kicker=d.get("kicker", ""), layers=layers,
                     cam=[[r(k[0]), *k[1:]] for k in d.get("cam", [])], shake=[[r(t), dd, a] for t, dd, a in d.get("shake", [])],
                     lower=[dict(x, at=r(x["at"]), **({"out": r(x["out"])} if x.get("out") is not None else {})) for x in d.get("lower", [])],
                     chips=[dict(x, at=r(x["at"]), **({"out": r(x["out"])} if x.get("out") is not None else {})) for x in d.get("chips", [])],
                     sfx=sorted([r(t), s] for t, s in d.get("sfx", [])))
        tpl = ROOT / "video/lib/plates/scene.html"
    for name in imgs:   # copy (not link: renders must not depend on the cache path)
        src, dst = props_lib.OUT / f"{name}.png", f / "img" / f"{name}.png"
        if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
            shutil.copy2(src, dst)
    html = re.sub(r'data-duration="[\d.]+"', f'data-duration="{dur}"', tpl.read_text())
    put(f / "index.html", html)
    put(f / "params.js", f"// Generated by projects/cant-pay-minimum/build/make_scenes.py from build/scenes.py ({t0:.2f}–{d['end']:.2f} s of the film)\n"
                         "window.SCENE = " + json.dumps(scene, ensure_ascii=False, indent=1) + ";\n")
    put(f / ".gitignore", "vendor/\nimg/\nrender.mp4\nrender.log\nsnapshots/\n")
    SFX.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, str(ROOT / "video/lib/doodle/make_sfx.py"), str(f / "params.js"), str(SFX / f"{sid}.sfx.wav")], check=True, capture_output=True)
    print(sid, d["kind"], dur, "s", len(scene.get("items", scene.get("layers", []))), "items", len(scene["sfx"]), "sounds")


if __name__ == "__main__":
    props_lib.shoot()                    # before scenes.py reads prop sizes and anchors
    from scenes import SCENES
    for sid, d in SCENES.items():
        if len(sys.argv) > 1 and sid not in sys.argv[1:]:
            continue
        build(sid, d)
    subprocess.run(["node", str(ROOT / "scripts/vendor-assets.mjs")], check=True, capture_output=True)
