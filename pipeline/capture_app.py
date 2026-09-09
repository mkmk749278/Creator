#!/usr/bin/env python3
"""Capture real Lumin app footage (screenshots + screen recording) for social reels.

Runs the LOCAL web build under the real ``https://app.luminapp.org`` origin via
Playwright request interception, so Firebase accepts the origin as authorized.

Prerequisites -- see ``lumin-app/docs/AI_AGENT_APP_ACCESS.md``:
  * a local ``flutter build web`` of a SCRATCH copy patched with LUMIN_E2E
    (that patch is never committed to lumin-app, and is not committed here either)
  * sign-in only with a REGISTERED TEST NUMBER

Why coordinates: Flutter web renders to a canvas. There is no DOM to query, so
every interaction is a click at a point. Those points drift with any layout
change, which is why this script screenshots after every single step -- the
screenshots are the only feedback a canvas app gives, and they are also the
raw material the reels are cut from.
"""
from __future__ import annotations

import argparse
import os
import re
import io
import pathlib
import sys
import time

from PIL import Image, ImageChops, ImageStat
from playwright.sync_api import sync_playwright

BUILD_WEB = pathlib.Path(os.environ.get("LUMIN_BUILD_WEB", "/home/user/work/lumin-scratch/build/web"))
ORIGIN = "https://app.luminapp.org"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

# Viewport matches a tall modern phone; the reels are 1080x1920 (9:16) and this
# is 430x930 (~9:19.5), so the capture is cropped rather than stretched later.
VW, VH = 430, 930

MIME = {
    ".html": "text/html", ".js": "text/javascript", ".mjs": "text/javascript",
    ".json": "application/json", ".css": "text/css", ".png": "image/png",
    ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".svg": "image/svg+xml",
    ".wasm": "application/wasm", ".ttf": "font/ttf", ".otf": "font/otf",
    ".woff": "font/woff", ".woff2": "font/woff2", ".ico": "image/x-icon",
    ".map": "application/json", ".bin": "application/octet-stream",
    ".symbols": "application/octet-stream",
}


# Flutter fetches CanvasKit from a VERSION-HASHED gstatic path:
#   /flutter-canvaskit/<engine-hash>/chromium/canvaskit.js
# The local build ships the same files unhashed under build/web/canvaskit/, so
# the hash segment has to be dropped -- stripping only the literal prefix leaves
# "<hash>/chromium/canvaskit.js", every request 404s, and the app renders a bare
# background with no error a screenshot can show.
_CANVASKIT_RE = re.compile(r"^/flutter-canvaskit/[0-9a-f]+/")


def _serve(root: pathlib.Path, canvaskit: bool = False):
    """Return a Playwright route handler serving `root` from disk."""

    def handler(route, request):
        path = request.url.split("?")[0].split("#")[0]
        for pre in (ORIGIN, "https://www.gstatic.com"):
            if path.startswith(pre):
                path = path[len(pre):]
                break
        if canvaskit:
            path = _CANVASKIT_RE.sub("/", path)
        rel = path.lstrip("/") or "index.html"
        f = root / rel
        if f.is_dir():
            f = f / "index.html"
        if not f.exists():
            # Flutter asks for a few optional files; a clean 404 is correct.
            return route.fulfill(status=404, body="")
        body = f.read_bytes()
        return route.fulfill(
            status=200,
            body=body,
            headers={
                "content-type": MIME.get(f.suffix, "application/octet-stream"),
                "cache-control": "no-store",
                "access-control-allow-origin": "*",
            },
        )

    return handler



# ---------------------------------------------------------------------------
# Self-locating helpers.
#
# The documented tap coordinates in lumin-app/docs/AI_AGENT_APP_ACCESS.md are a
# snapshot and they HAD drifted by the time this ran -- the onboarding became a
# 3-page carousel and boot took longer than the documented 20s, so every early
# tap landed on a blank frame and was silently lost. A canvas app gives no error
# for a tap that hits nothing, so blind coordinates fail invisibly.
#
# These helpers locate things by what is actually on screen instead:
#   * boot is detected by the frame gaining detail, not by a fixed sleep
#   * the primary CTA is found by its brand accent colour (#7BD3F7), which is
#     layout-independent and survives a redesign that moves the button
# ---------------------------------------------------------------------------
ACCENT = (0x7B, 0xD3, 0xF7)


def _frame(page) -> "Image.Image":
    return Image.open(io.BytesIO(page.screenshot())).convert("RGB")


def _detail(img) -> float:
    """Rough busy-ness of a frame. A booting Flutter app paints a flat
    background colour, so near-zero means 'nothing rendered yet'."""
    return ImageStat.Stat(img.convert("L")).stddev[0]


def wait_boot(page, timeout: float = 90.0, thresh: float = 4.0) -> bool:
    """Block until the Flutter engine has actually painted something."""
    t0 = time.time()
    while time.time() - t0 < timeout:
        if _detail(_frame(page)) > thresh:
            print(f"  booted after {time.time() - t0:.0f}s")
            time.sleep(2.0)
            return True
        time.sleep(2.0)
    print(f"  WARNING: still blank after {timeout:.0f}s")
    return False


def find_accent_button(page, min_w_frac: float = 0.30, min_h_px: int = 18):
    """Locate the primary CTA by its accent FILL; return viewport (x, y) or None.

    Must match a filled block, not a border. The sign-in screen stacks a filled
    "Send via SMS" button directly above an OUTLINED "Send via Telegram" one,
    and an outline's horizontal edge is also a full-width run of accent pixels
    -- an earlier version matched that edge and clicked the 5px gap between the
    two buttons, so the code was never sent and every later step ran against a
    screen that had not moved. Requiring vertical thickness separates a filled
    button from a 1px stroke; taking the largest block by area rather than the
    first one found keeps it stable when several accents are on screen.
    """
    img = _frame(page)
    w, h = img.size
    px = img.load()
    step = max(1, w // 240)

    def is_accent(x, y):
        r, g, b = px[x, y]
        return (abs(r - ACCENT[0]) < 26 and abs(g - ACCENT[1]) < 26
                and abs(b - ACCENT[2]) < 26)

    # Widest accent run per sampled row.
    rows = {}
    for y in range(0, h, step):
        run_start, best_run = None, None
        for x in range(0, w, step):
            if is_accent(x, y):
                if run_start is None:
                    run_start = x
            elif run_start is not None:
                if best_run is None or (x - run_start) > (best_run[1] - best_run[0]):
                    best_run = (run_start, x)
                run_start = None
        if run_start is not None and (best_run is None or (w - run_start) > (best_run[1] - best_run[0])):
            best_run = (run_start, w)
        if best_run and (best_run[1] - best_run[0]) >= w * min_w_frac:
            rows[y] = best_run

    # Group vertically-adjacent rows whose runs overlap into blocks.
    blocks, cur = [], None
    for y in sorted(rows):
        x0, x1 = rows[y]
        if cur and y - cur["y1"] <= step * 2 and min(x1, cur["x1"]) - max(x0, cur["x0"]) > 0:
            cur["y1"] = y
            cur["x0"] = min(cur["x0"], x0)
            cur["x1"] = max(cur["x1"], x1)
        else:
            if cur:
                blocks.append(cur)
            cur = {"y0": y, "y1": y, "x0": x0, "x1": x1}
    if cur:
        blocks.append(cur)

    solid = [b for b in blocks if (b["y1"] - b["y0"]) >= min_h_px]
    if not solid:
        return None
    b = max(solid, key=lambda b: (b["x1"] - b["x0"]) * (b["y1"] - b["y0"]))
    cx = (b["x0"] + b["x1"]) / 2
    cy = (b["y0"] + b["y1"]) / 2
    return int(cx * VW / w), int(cy * VH / h)


def tap_until_change(page, x, y, label="", timeout=8.0, settle=1.0):
    """Tap and wait for the frame to actually change; report if it did not."""
    before = _frame(page)
    page.mouse.click(x, y)
    if label:
        print(f"  tap {label} ({x},{y})")
    t0 = time.time()
    while time.time() - t0 < timeout:
        time.sleep(0.6)
        cur = _frame(page)
        if ImageChops.difference(before, cur).convert("L").getbbox() is not None:
            diff = ImageStat.Stat(ImageChops.difference(before, cur).convert("L")).mean[0]
            if diff > 1.2:
                time.sleep(settle)
                return True
    print(f"  (no visible change after {label or 'tap'})")
    return False


class Shot:
    """Screenshot counter that names files in capture order."""

    def __init__(self, page, outdir: pathlib.Path):
        self.page, self.dir, self.n = page, outdir, 0
        outdir.mkdir(parents=True, exist_ok=True)

    def __call__(self, label: str, wait: float = 0.0):
        if wait:
            time.sleep(wait)
        self.n += 1
        p = self.dir / f"{self.n:02d}_{label}.png"
        self.page.screenshot(path=str(p))
        print(f"  shot {p.name}")
        return p


def tap(page, x: int, y: int, label: str = "", settle: float = 1.2):
    page.mouse.click(x, y)
    if label:
        print(f"  tap {label} ({x},{y})")
    time.sleep(settle)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="/home/user/Creator/capture/app")
    # Deliberately NOT defaulted. The registered test numbers and their codes
    # live in lumin-app/docs/AI_AGENT_APP_ACCESS.md, and one copy of a
    # credential-shaped string is easier to keep correct than two.
    ap.add_argument("--phone",
                    help="registered Firebase TEST number only, digits without "
                         "the country code (see lumin-app AI_AGENT_APP_ACCESS.md)")
    ap.add_argument("--code", help="the test number's fixed verification code")
    ap.add_argument("--country", default="",
                    help="country name to pick; empty keeps the default (+1)")
    ap.add_argument("--no-signin", action="store_true",
                    help="stop at the sign-in screen; no production side effects")
    ap.add_argument("--boot-wait", type=float, default=90.0,
                    help="max seconds to wait for the Flutter engine to paint")
    ap.add_argument("--consent-x", type=int, default=52)
    ap.add_argument("--consent-ys", type=int, nargs="*", default=[161, 257, 373])
    args = ap.parse_args()

    # Required only for a real sign-in -- a --no-signin dry run touches nothing
    # in production and should not need a credential to run.
    if not args.no_signin and not (args.phone and args.code):
        ap.error("--phone and --code are required unless --no-signin is given")

    if not BUILD_WEB.exists():
        print(f"missing web build at {BUILD_WEB}", file=sys.stderr)
        return 2

    out = pathlib.Path(args.out)
    shots = out / "shots"
    video = out / "video"
    video.mkdir(parents=True, exist_ok=True)

    # The agent proxy's port changes mid-session; read it live, never hardcode.
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    launch = dict(
        executable_path=CHROME,
        headless=True,
        args=[
            # Chrome's post-quantum ClientHello is reset by the MITM proxy.
            "--disable-features=PostQuantumKyber,X25519Kyber768,"
            "EncryptedClientHello,TLS13EarlyData",
            "--ssl-version-max=tls1.2",
            "--ignore-certificate-errors",
            "--autoplay-policy=no-user-gesture-required",
        ],
    )
    if proxy:
        # Never bypass 127.0.0.1 -- the proxy itself listens there.
        launch["proxy"] = {"server": proxy}
        print(f"proxy: {proxy}")

    with sync_playwright() as pw:
        browser = pw.chromium.launch(**launch)
        ctx = browser.new_context(
            viewport={"width": VW, "height": VH},
            device_scale_factor=3,          # crisp enough to upscale into 1080-wide
            is_mobile=True,
            has_touch=True,
            user_agent=("Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                        "Version/17.0 Mobile/15E148 Safari/604.1"),
            record_video_dir=str(video),
            record_video_size={"width": VW, "height": VH},
            ignore_https_errors=True,
        )
        page = ctx.new_page()
        page.route(f"{ORIGIN}/**", _serve(BUILD_WEB))
        canvaskit = BUILD_WEB / "canvaskit"
        if canvaskit.exists():
            page.route("https://www.gstatic.com/flutter-canvaskit/**",
                       _serve(canvaskit, canvaskit=True))
        page.on("console", lambda m: m.type == "error" and print(f"  js-error: {m.text[:160]}"))

        shot = Shot(page, shots)
        print(f"goto {ORIGIN}")
        page.goto(ORIGIN, wait_until="domcontentloaded", timeout=120_000)
        wait_boot(page, timeout=args.boot_wait)
        shot("boot")

        # --- Onboarding carousel + consent -------------------------------
        # Paged by the accent CTA rather than fixed coordinates. On the consent
        # screen the CTA is disabled (not accent) until all three boxes are
        # ticked, so "no accent button found" is how we detect we are there.
        for i in range(8):
            btn = find_accent_button(page)
            if btn is None:
                print("  no accent CTA -> consent screen (disabled continue)")
                break
            tap_until_change(page, *btn, label=f"CTA step {i+1}", settle=1.4)
            shot(f"onboard_{i+1}")
        else:
            print("  onboarding did not end after 8 CTA taps")

        shot("consent")
        for i, y in enumerate(args.consent_ys, 1):
            tap_until_change(page, args.consent_x, y, f"consent box {i}",
                             timeout=4.0, settle=0.4)
        shot("consent_checked")
        btn = find_accent_button(page)
        if btn:
            tap_until_change(page, *btn, "consent continue", timeout=12.0, settle=2.5)
        shot("after_consent")

        if args.no_signin:
            print("--no-signin set: stopping before sign-in")
        else:
            # --- Sign-in (REGISTERED TEST NUMBER ONLY) --------------------
            if args.country:
                tap_until_change(page, 79, 225, "country picker", settle=1.5)
                shot("country_picker")
                page.mouse.click(215, 327)
                page.keyboard.type(args.country, delay=60)
                time.sleep(1.4)
                shot("country_typed")
                tap_until_change(page, 215, 386, "first country result", settle=1.5)
                shot("country_chosen")
            else:
                print("  keeping the default country code (test number is +1)")

            page.mouse.click(265, 225)
            page.keyboard.type(args.phone, delay=80)
            time.sleep(0.8)
            shot("phone_typed")
            btn = find_accent_button(page)
            if btn:
                tap_until_change(page, *btn, "send via sms", timeout=20.0, settle=4.0)
            shot("code_screen")

            # The code field does not autofocus -- tap it before typing.
            page.mouse.click(215, 251)
            time.sleep(0.4)
            page.keyboard.type(args.code, delay=90)
            time.sleep(0.8)
            shot("code_typed")
            btn = find_accent_button(page)
            if btn:
                tap_until_change(page, *btn, "verify", timeout=30.0, settle=8.0)
            shot("after_verify")

            # --- The tabs: this is the footage the reels are cut from -----
            for label, x in (("pulse", 43), ("signals", 129), ("charts", 215),
                             ("trade", 301), ("menu", 387)):
                tap_until_change(page, x, 890, f"tab {label}", timeout=10.0, settle=3.0)
                shot(f"tab_{label}")
                page.mouse.move(215, 600)
                page.mouse.wheel(0, 300)
                time.sleep(2.0)
                shot(f"tab_{label}_scrolled")
                page.mouse.wheel(0, -300)
                time.sleep(1.5)

        ctx.close()
        browser.close()

    vids = sorted(video.glob("*.webm"))
    print(f"\ncaptured {shot.n} screenshots -> {shots}")
    for v in vids:
        print(f"video -> {v} ({v.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
