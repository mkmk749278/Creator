#!/usr/bin/env python3
"""Generate a VO take with ElevenLabs from the session (owner, 2026-11-03: "Eleven labs api is available in environment
secrets. Use that Akash, and that settings").

Voice and settings come from config/voice.yaml (the owner's app settings, screenshot 2026-11-03). One request per block;
the request text is saved beside the take (`.txt`) so `align_script.py` and `vo_take_check.py` time the exact words read.

usage: python3 scripts/eleven_tts.py --text-file block.txt --out projects/<slug>/voice/xx_b01.mp3 [--voice akash]
       python3 scripts/eleven_tts.py --blocks projects/<slug>/vo_blocks.md --prefix aig --outdir projects/<slug>/voice
needs: ELEVENLABS_API_KEY in the environment. Prints characters used. Never prints the key.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
API = "https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format={fmt}"


def load_voice(name):
    cfg = yaml.safe_load(open(ROOT / "config" / "voice.yaml"))
    v = cfg["voices"][name]
    return v


def tts(text, v, out, prev_text=None, next_text=None):
    body = {"text": text, "model_id": v["model_id"], "voice_settings": v["settings"]}
    if v.get("language_code"):
        body["language_code"] = v["language_code"]
    if prev_text:
        body["previous_text"] = prev_text
    if next_text:
        body["next_text"] = next_text
    req = urllib.request.Request(API.format(voice=v["voice_id"], fmt=v["output_format"]),
                                 data=json.dumps(body).encode(), method="POST",
                                 headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"],
                                          "Content-Type": "application/json", "Accept": "audio/mpeg"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                data = r.read()
                cost = r.headers.get("character-cost") or r.headers.get("x-character-count")
            break
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="ignore")[:400]
            if e.code in (429, 500, 502, 503) and attempt < 2:
                time.sleep(4 * (attempt + 1)); continue
            sys.exit(f"ElevenLabs error {e.code}: {msg}")
    out = Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    out.with_suffix(".txt").write_text(text, encoding="utf-8")
    print(f"{out}  {len(data)/1024:.0f} KB  chars={cost or len(text)}")


def blocks_from_md(path):
    """The fenced code blocks of vo_blocks.md, in order (the recording blocks)."""
    return [b.strip("\n") for b in re.findall(r"```(?:text)?\n(.*?)```", open(path, encoding="utf-8").read(), re.S)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", default="akash")
    ap.add_argument("--text-file")
    ap.add_argument("--out")
    ap.add_argument("--blocks", help="vo_blocks.md: generate every block")
    ap.add_argument("--only", help="comma list of block numbers to (re)generate, e.g. 3,7")
    ap.add_argument("--prefix")
    ap.add_argument("--outdir")
    a = ap.parse_args()
    v = load_voice(a.voice)
    if a.text_file:
        tts(open(a.text_file, encoding="utf-8").read().strip(), v, a.out)
        return
    blocks = blocks_from_md(a.blocks)
    only = {int(x) for x in a.only.split(",")} if a.only else None
    for i, b in enumerate(blocks, 1):
        if only and i not in only:
            continue
        # previous/next text keeps the read continuous across block seams (ElevenLabs request stitching)
        tts(b, v, Path(a.outdir) / f"{a.prefix}_b{i:02d}.mp3",
            prev_text=blocks[i - 2][-600:] if i > 1 else None, next_text=blocks[i][:300] if i < len(blocks) else None)


if __name__ == "__main__":
    main()
