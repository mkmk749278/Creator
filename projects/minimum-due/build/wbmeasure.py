"""Measure whiteboard text with the same pen-font data the engine uses (video/lib/whiteboard/wb-fonts.js)."""
import json
from pathlib import Path
_src = (Path(__file__).resolve().parents[3] / "video/lib/whiteboard/wb-fonts.js").read_text()
FONTS = json.loads(_src[_src.index("=") + 1:].strip().rstrip(";"))


def width(text, size, font="tech"):
    F = FONTS[font]; k = size / F["cap"]
    return sum((F["glyphs"].get(ch) or F["glyphs"]["?"])["w"] for ch in text) * k
