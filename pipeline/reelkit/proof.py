"""Named proof regions -- the machine-readable half of `content/COMPLIANCE.md`.

That file states the channel's one test:

    Every claim in a reel must be pointable at a screen in
    `capture/app/screens/` or a line in the app's own onboarding.

Until now that test was enforced by a human reading a caption. A `talk` scene's
inset makes it enforceable: a script does not write a crop box, it names a
CLAIM, and this table is where a claim is bound to the pixels that evidence it.
So "which screen says that?" has an answer that can be looked up, and a script
naming a claim nobody has evidenced fails at render rather than at review.

Regions are (x0, y0, x1, y1) normalised on the plate, because the captures are
device-resolution-dependent and pixel boxes would silently point somewhere else
after a re-capture on a different handset.

**Re-verify after every re-capture.** `python3 pipeline/check_proofs.py` renders
every entry to `capture/app/proofs/` so the crops can be read rather than
trusted -- a region that has slid half a row off its claim still renders a
perfectly convincing card of the wrong sentence.
"""
from __future__ import annotations

# claim key -> (screen plate, region, default label)
PROOF: dict[str, tuple[str, tuple[float, float, float, float], str]] = {
    # --- onboarding: "Your funds never leave Binance" -----------------------
    "funds_never_leave": ("onboard_funds_safe.png",
                          (0.03, 0.250, 0.97, 0.355), "IN THE APP"),
    "trade_only_key":    ("onboard_funds_safe.png",
                          (0.03, 0.372, 0.97, 0.462), "IN THE APP"),
    "stop_on_every":     ("onboard_funds_safe.png",
                          (0.03, 0.448, 0.97, 0.520), "IN THE APP"),
    "paper_mode":        ("onboard_funds_safe.png",
                          (0.03, 0.512, 0.97, 0.585), "IN THE APP"),

    # --- onboarding: "How it works" ----------------------------------------
    "scans_75_pairs":    ("onboard_how_it_works.png",
                          (0.03, 0.375, 0.97, 0.452), "IN THE APP"),
    "fifteen_analysts":  ("onboard_how_it_works.png",
                          (0.03, 0.458, 0.97, 0.538), "IN THE APP"),
    "sl_tp_on_fill":     ("onboard_how_it_works.png",
                          (0.03, 0.545, 0.97, 0.622), "IN THE APP"),

    # --- the Signals tab ---------------------------------------------------
    # Deliberately cut ABOVE the live "+0.15%" row. The percentage is the app's
    # own unrealised move and is not cherry-picked, but enlarged into an inset
    # under a promotional headline it reads as a result, and COMPLIANCE.md bans
    # a performance figure whatever its provenance.
    "one_signal":        ("signals_list.png",
                          (0.03, 0.272, 0.97, 0.408), "ONE SIGNAL"),
    "every_signal_free": ("signals_list.png",
                          (0.03, 0.090, 0.97, 0.228), "IN THE APP"),

    # --- the Trade tab -----------------------------------------------------
    # ONLY the Live/Paper toggle. The rest of this plate carries an orange
    # "Status unknown -- could not reach engine" banner and a "Details (3 to
    # fix)" warning: correct product behaviour, and an advertisement for a
    # broken app. Never widen this region without looking at what it lets in.
    "live_or_paper":     ("trade_connect.png",
                          (0.03, 0.055, 0.97, 0.115), "IN THE APP"),
}


def resolve(key: str) -> tuple[str, tuple[float, float, float, float], str]:
    if key not in PROOF:
        raise KeyError(
            f"no proof region named {key!r}. A claim with no screen behind it "
            f"does not ship -- see content/COMPLIANCE.md. Known: {sorted(PROOF)}")
    return PROOF[key]
