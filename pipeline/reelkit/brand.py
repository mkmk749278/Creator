"""Lumin brand constants for social video.

Colours are the app's OWN tokens, copied from lumin-app/lib/shared/tokens.dart
rather than eyedropped from a screenshot -- a reel that sits next to a real app
screenshot in the same frame has to match it exactly, and an eyedropped value
drifts the moment the app retints anything.

If lumin-app/lib/shared/tokens.dart changes, change these with it.
Verified against that file 2026-09-08.
"""
from __future__ import annotations

import pathlib

# --- Canvas ---------------------------------------------------------------
# Instagram Reels / TikTok / YT Shorts all take 1080x1920 @ 30fps.
W, H, FPS = 1080, 1920, 30

# Instagram overlays its own UI on top of a reel. Keeping anything that must be
# read inside these bounds is the difference between a caption people can read
# and one hidden under the username and the audio ticker.
SAFE_TOP = 220
SAFE_BOTTOM = 1560          # below this the IG action rail / caption sits
SAFE_X = 72

# --- Palette (lumin-app/lib/shared/tokens.dart) ---------------------------
BG_DEEP = (0x0A, 0x0E, 0x1A)
BG_CARD = (0x0F, 0x17, 0x29)
BG_ELEVATED = (0x13, 0x1C, 0x32)
ACCENT = (0x7B, 0xD3, 0xF7)
ACCENT_MUTED = (0x4A, 0x8D, 0xAA)
TEXT_PRIMARY = (0xF8, 0xFA, 0xFC)
TEXT_SECONDARY = (0x94, 0xA3, 0xB8)
TEXT_MUTED = (0x64, 0x74, 0x8B)
SUCCESS = (0x4A, 0xDE, 0x80)
WARN = (0xF5, 0x9E, 0x0B)
LOSS = (0xF8, 0x71, 0x71)

# --- Type -----------------------------------------------------------------
_ROOT = pathlib.Path(__file__).resolve().parents[2]
FONTS = _ROOT / "assets" / "fonts"
DISPLAY = str(FONTS / "Montserrat-800.ttf")     # hooks, big statements
DISPLAY_HEAVY = str(FONTS / "Montserrat-900.ttf")
BODY_BOLD = str(FONTS / "Inter-700.ttf")
BODY = str(FONTS / "Inter-500.ttf")
BODY_SEMI = str(FONTS / "Inter-600.ttf")

CHARACTER_DIR = _ROOT / "assets" / "character"
CAPTURE_DIR = _ROOT / "capture" / "app"

# --- Voice ----------------------------------------------------------------
# Ava: "Expressive, Caring, Pleasant, Friendly" -- the closest free neural voice
# to the character's register. Slightly fast, because a reel that dawdles loses
# the viewer before the second line.
VOICE = "en-US-AvaNeural"
VOICE_RATE = "+10%"
VOICE_PITCH = "+0Hz"
