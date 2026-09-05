#!/usr/bin/env python3
"""Upgraded video pipeline: dramatic narrations, AndrewNeural voice with per-block
rate/pitch variation, synthesized space-ambient background music, PIL-only visuals."""
import os, math, asyncio, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, BD = 1280, 720, 15, 10
FR = FPS * BD
BG = (8, 6, 18)
CR = (245, 238, 220)
OR = (204, 102, 34)
OR2 = (230, 140, 60)
GO = (210, 170, 80)
PU = (110, 55, 195)
GR = (80, 70, 100)
OUT = '/home/user/vid'


def gf(sz, bold=False):
    for p in [
        f'/usr/share/fonts/truetype/dejavu/DejaVuSans{"-Bold" if bold else ""}.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
    ]:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, sz)
            except Exception:
                pass
    return ImageFont.load_default()


_BASE = None


def base():
    global _BASE
    if _BASE is None:
        _BASE = Image.new('RGB', (W, H), BG)
        rng = np.random.default_rng(42)
        xs = rng.integers(0, W, 700)
        ys = rng.integers(0, H, 700)
        br = rng.uniform(0.3, 1.0, 700)
        for x, y, b in zip(xs, ys, br):
            c = int(b * 255)
            _BASE.putpixel((x, y), (c, c, c))
    return _BASE.copy()


def vis(bi, t):
    img = base()
    d = ImageDraw.Draw(img)
    cx, cy = W // 2, H // 2

    if bi in (0, 3, 6):  # galaxy
        for i in range(160):
            th = i / 160 * 4 * math.pi + t * 0.5
            r = i / 160 * 290
            x = cx + int(r * math.cos(th))
            y = cy + int(r * math.sin(th) * 0.4)
            if 0 <= x < W and 0 <= y < H:
                d.ellipse([x-1, y-1, x+1, y+1], fill=(*GO, int(i / 160 * 90)))
        for r, a in [(88, 35), (54, 88), (27, 158), (12, 228)]:
            d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(*OR, a))
        d.ellipse([cx-6, cy-6, cx+6, cy+6], fill=BG)

    elif bi in (1, 2, 18):  # S2 orbit
        A, B = 280, 160
        E = t * 2 * math.pi
        pts = [(cx + int(A * math.cos(th) - 60), cy + int(B * math.sin(th)))
               for th in np.linspace(0, 2 * math.pi, 200)]
        d.polygon(pts, outline=(*OR, 65))
        for j in range(16):
            ta = E - j * 0.05
            px = cx + int(A * math.cos(ta) - 60)
            py = cy + int(B * math.sin(ta))
            if 0 <= px < W and 0 <= py < H:
                d.ellipse([px-2, py-2, px+2, py+2], fill=(*OR2, int(j / 16 * 165)))
        sx = cx + int(A * math.cos(E) - 60)
        sy = cy + int(B * math.sin(E))
        d.ellipse([sx-8, sy-8, sx+8, sy+8], fill=(255, 255, 255))
        d.ellipse([cx-12, cy-12, cx+12, cy+12], fill=(*OR, 192))
        d.text((sx+12, sy-8), 'S2', font=gf(24), fill=CR)
        d.text((cx+8, cy+36), 'Sgr A*', font=gf(22), fill=(*OR, 185))

    elif bi in (4, 5):  # event horizon
        for r in range(195, 28, -15):
            d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=(*OR, int((1 - r/195) * 112)), width=1)
        d.ellipse([cx-80, cy-80, cx+80, cy+80], outline=(*OR2, 188), width=3)
        d.ellipse([cx-48, cy-48, cx+48, cy+48], fill=BG)
        d.ellipse([cx-8, cy-8, cx+8, cy+8], fill=OR)
        d.text((cx+90, cy-18), 'event horizon', font=gf(19), fill=(*OR, 188))

    elif bi in (7, 8, 9, 10):  # EHT ring
        rng = np.random.default_rng(7)
        for _ in range(1400):
            ang = rng.uniform(0, 2 * math.pi)
            R = 160 + rng.normal(0, 21)
            x = cx + int(R * math.cos(ang))
            y = cy + int(R * math.sin(ang) * 0.85)
            if 0 <= x < W and 0 <= y < H:
                bm = 0.5 + 0.5 * math.sin(ang + math.pi * 1.3)
                d.ellipse([x-2, y-2, x+2, y+2], fill=(*OR, int(bm * 172)))
        d.ellipse([cx-110, cy-110, cx+110, cy+110], fill=BG)
        d.text((W//2, H-55), 'Event Horizon Telescope · 2022 · Sgr A*',
               font=gf(19), fill=(*CR, 162), anchor='mm')

    elif bi in (11, 12, 13, 19):  # dark matter core
        for r in range(198, 6, -11):
            d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(*PU, int((1 - r/198) * 93)))
        rc = int(70 + 5 * (0.5 + 0.5 * math.sin(t * math.pi * 1.5)))
        d.ellipse([cx-rc, cy-rc, cx+rc, cy+rc], fill=(142, 58, 220))
        for fi in range(14):
            fa = fi * 2 * math.pi / 14 + t * 0.8
            px = cx + int(200 * math.cos(fa))
            py = cy + int(200 * math.sin(fa))
            if 0 <= px < W and 0 <= py < H:
                d.ellipse([px-3, py-3, px+3, py+3], fill=(255, 255, 255))
        d.text((cx, cy), '4M x Sun', font=gf(28, True), fill=(255, 255, 255), anchor='mm')
        d.text((cx, H-55), 'STABLE · NON-SINGULAR · DARK MATTER CORE',
               font=gf(17), fill=(*OR, 192), anchor='mm')

    elif bi in (14, 15, 16, 17):  # Le Verrier solar system
        d.ellipse([cx-27, cy-27, cx+27, cy+27], fill=GO)
        for r_, sp, sz, col in [(80, 2.2, 5, CR), (150, 0.7, 8, (150, 200, 255)), (240, 0.4, 9, (100, 150, 200))]:
            d.ellipse([cx-r_, cy-r_, cx+r_, cy+r_], outline=(*col, 54), width=1)
            a = t * sp * math.pi * 2
            px, py = cx + int(r_ * math.cos(a)), cy + int(r_ * math.sin(a))
            d.ellipse([px-sz, py-sz, px+sz, py+sz], fill=col)
        if bi >= 16:
            a = t * 0.4 * math.pi * 2
            nx = cx + int(240 * math.cos(a))
            ny = cy + int(240 * math.sin(a))
            d.ellipse([nx-14, ny-14, nx+14, ny+14], fill=(80, 120, 200))
            d.text((nx+20, ny-10), 'Neptune\n1846', font=gf(17), fill=(*OR, 192))

    elif bi in (20, 21, 22, 23, 24, 25):  # rotation curve
        ox, oy, pw, ph = 100, 580, 1080, 440
        d.line([(ox, oy), (ox+pw, oy)], fill=CR, width=2)
        d.line([(ox, oy), (ox, oy-ph)], fill=CR, width=2)
        n = int(200 * min(1, t * 1.2)) if bi < 25 else 200
        kp = [(ox + int(i/200*pw), oy - int(0.5/math.sqrt(max(0.01, i/200)) * 0.7 * ph))
              for i in range(1, 201)]
        d.line(kp[:n], fill=(*GR, 142), width=2)
        op = [(ox + int(i/200*pw), oy - int(0.42 * ph)) for i in range(n)]
        d.line(op, fill=OR, width=3)
        if bi == 25:
            fp = [(ox + int(i/200*pw), oy - int((0.40 + 0.06*math.exp(-i/200*5)) * ph))
                  for i in range(200)]
            d.line(fp, fill=(118, 78, 218), width=3)
            d.text((ox+20, oy - int(0.57*ph)), 'Fermionic DM model', font=gf(17), fill=(118, 78, 218))
        d.text((ox+20, oy - int(0.30*ph)), 'Observed (flat)', font=gf(17), fill=OR)
        d.text((ox+20, oy - int(0.66*ph)), 'Keplerian (expected)', font=gf(17), fill=(*GR, 152))
        d.text((W//2, H-35), 'GALACTIC ROTATION CURVE', font=gf(17), fill=(*CR, 152), anchor='mm')

    elif bi in (26, 27, 28):  # JWST early universe
        pulse = 0.5 + 0.5 * math.sin(t * math.pi * 2)
        for sx, sy in [(320, 250), (820, 180), (460, 520), (900, 480), (200, 420), (640, 340)]:
            for rr, aa in [(42, 20), (25, 62), (12, 142)]:
                r2 = int(rr * (1 + 0.15 * pulse))
                d.ellipse([sx-r2, sy-r2, sx+r2, sy+r2], fill=(*GO, aa))
        d.text((W//2, 50), '380 Myr post Big Bang', font=gf(20), fill=(*OR, 195), anchor='mm')
        d.text((W//2, H-50), 'JWST · Early Universe Galaxy Seeds · z > 10',
               font=gf(19), fill=(*CR, 162), anchor='mm')

    elif bi in (29, 30, 31, 32, 33):  # comparison
        for r in range(118, 8, -10):
            d.ellipse([320-r, H//2-r, 320+r, H//2+r], fill=(*OR, int((1-r/118)*152)))
        d.ellipse([320-29, H//2-29, 320+29, H//2+29], fill=BG)
        pulse = 0.5 + 0.5 * math.sin(t * math.pi * 1.5)
        for r in range(118, 8, -10):
            rc = int(r * (1 + 0.04 * pulse))
            d.ellipse([960-rc, H//2-rc, 960+rc, H//2+rc], fill=(*PU, int((1-r/118)*132)))
        d.line([(W//2, 80), (W//2, H-80)], fill=(*GR, 142), width=2)
        f1 = gf(20, True)
        d.text((320, 95), 'BLACK HOLE', font=f1, fill=OR, anchor='mm')
        d.text((960, 95), 'DARK MATTER CORE', font=f1, fill=(148, 98, 238), anchor='mm')
        f2 = gf(16)
        for i, lbl in enumerate(['Singularity', 'Event horizon', 'Infinite density', 'Halo-separate']):
            d.text((320, 390 + i*48), f'• {lbl}', font=f2, fill=(*CR, 192), anchor='mm')
        for i, lbl in enumerate(['Stable sphere', 'No event horizon', 'Finite density', 'Continuous halo']):
            d.text((960, 390 + i*48), f'• {lbl}', font=f2, fill=(*CR, 192), anchor='mm')

    else:  # conclusion (bi 34, 35)
        for r in range(248, 8, -12):
            frac = 1 - r/248
            c1 = int(60 + frac * 100)
            d.ellipse([cx-r, cy-r, cx+r, cy+r],
                      fill=(c1, int(c1*0.3), int(80 + c1*0.5), int(frac*74)))
        rc = int(62 + 4 * (0.5 + 0.5 * math.sin(t * math.pi * 1.2)))
        d.ellipse([cx-rc, cy-rc, cx+rc, cy+rc], fill=(142, 58, 220))
        d.text((cx, cy), '4M x Sun', font=gf(28, True), fill=(255, 255, 255), anchor='mm')
        if bi == 35:
            d.text((cx, cy-192), '"Invisible mass speaks through visible orbits"',
                   font=gf(19), fill=CR, anchor='mm')
            d.text((cx, cy+192), '— Le Verrier, applied to the cosmos',
                   font=gf(17), fill=(*OR, 192), anchor='mm')
        else:
            d.text((cx, H-58), 'CORE AND HALO — ONE CONTINUOUS STRUCTURE',
                   font=gf(17), fill=(*OR, 178), anchor='mm')
    return img


def mk(bi, fi, narr):
    t = fi / FR
    img = vis(bi, t)
    d = ImageDraw.Draw(img)
    # Progress dots
    rng = np.random.default_rng(42)
    pos = [(int(20 + rng.integers(0, 40)), int(20 + (i*19) % (H-40))) for i in range(36)]
    for di in range(min(bi+1, 36)):
        px, py = pos[di]
        d.ellipse([px-4, py-4, px+4, py+4], fill=OR)
    # Subtitle
    words = narr.split()
    n = max(1, int(len(words) * min(1, t * 1.3)))
    show = ' '.join(words[:n])
    bar = Image.new('RGBA', (W, 90), (0, 0, 0, 194))
    img.paste(bar, (0, H-90), bar)
    d2 = ImageDraw.Draw(img)
    f = gf(31)
    d2.text((W//2+1, H-65+1), show, font=f, fill=(0, 0, 0, 172), anchor='mm')
    d2.text((W//2, H-65), show, font=f, fill=CR, anchor='mm')
    return img


NARRATIONS = [
    "Right now, at our galaxy's core, something invisible whips stars at 8,000 km per second. That is Earth to Moon each second. Four million suns of gravity. Nobody knows what it is.",
    "Meet S2: sixteen-year orbit. At closest pass — eight thousand kilometers per second. Three percent of light speed. Pulled by four million solar masses. And completely invisible.",
    "The fastest human spacecraft hits 690 km per second. S2 is twelve times faster. Whatever commands that gravity at our galactic center staggers imagination — and cannot be seen.",
    "No star. No cluster. No glow. Pure invisible gravity — four million solar masses compressed into a space too small to see. Something extraordinary is there. We just cannot look at it.",
    "Physics has a name for this. Compress mass below a critical threshold and collapse becomes total — a singularity, infinite density, zero volume — with a boundary of absolute no return.",
    "That boundary is the event horizon. Cross it and you are gone — not trapped, gone. Even light cannot escape. The laws of physics as we understand them break down completely beyond it.",
    "For decades this was settled: a supermassive black hole named Sagittarius A-star at our galactic center. Orbits match. Math works. Case closed. Or — was it? What if not?",
    "April 2022. A planet-sized telescope network stares at the galactic center. Humanity erupts. We photographed a black hole. But here is what those headlines actually left out.",
    "That image does not show a black hole. It shows superheated gas swirling near something massive. Any compact massive object casts that same shadow. No singularity required.",
    "A shadow proves something massive exists — not what that something actually is. The image is real. Extraordinary. But the interpretation of what made it remains wide open.",
    "The most studied object in astrophysics. The most photographed galactic region. And the fundamental question — what exactly is Sagittarius A-star — remains unanswered.",
    "February 2026. Crespi, Arguelles, and collaborators publish a paper that reopens everything at the highest scientific levels. Sagittarius A-star may not be a black hole at all.",
    "Ultra-dense fermionic dark matter — packed so tightly it mimics black hole gravity exactly. Four million solar masses. No event horizon. No singularity. Stable. Finite. Real.",
    "Fermions obey one iron quantum rule: no two can share the same state. Pack them tight and quantum mechanics itself pushes back. Degeneracy pressure. Collapse halted permanently.",
    "To understand how invisible mass is detected through visible motion — travel to 1846. Astronomers face a crisis. Uranus does not follow its predicted orbit. Something unseen pulls it.",
    "Le Verrier does not build a telescope. He calculates — on paper alone — exactly where an eighth planet must be to explain the wobble. Then tells the observatories where to look.",
    "They look. Neptune is exactly there — found by pure mathematics before any telescope ever saw it. Science proved invisible mass through visible orbits. It did not need to see Neptune.",
    "The S-stars orbiting Sagittarius A-star are our Neptune story. Their paths reveal four million solar masses — but not the form that mass takes. We see the fingerprint. Not the hand.",
    "S2 tracked for thirty years with breathtaking precision. The ellipse — exact. The sixteen-year period — exact. Four million solar masses implied with certainty. What creates it — open.",
    "The dark matter core reproduces Sagittarius A-star's gravitational signature exactly. Same mass, volume, orbital dynamics — indistinguishable from outside. No singularity anywhere inside.",
    "Zoom out. Way out. Into the spiral arms — where something has puzzled astronomers for ninety years and reveals a profound gap in our understanding of the cosmos. Something is missing.",
    "Newtonian mechanics says outer stars should slow down — like outer planets, Pluto crawling while Mercury sprints. Kepler's third law. Every solar system obeys. Every galaxy should too.",
    "Galaxies don't obey. Stars at galactic edges orbit just as fast as inner ones. Flat rotation curves. Measured in hundreds of galaxies. One of astronomy's most enduring mysteries.",
    "Standard answer: an invisible dark matter halo scaffolds the entire galaxy at every radius, keeping outer stars fast. Elegant theory. Explains the data well. Never directly observed.",
    "In 2022, ESA's Gaia mission mapped outer Milky Way stellar velocities with remarkable precision — and found something unexpected: a subtle Keplerian decline at extreme galactic radii.",
    "Standard halo models struggled with Gaia's decline. The fermionic dark matter core model fits both inner S-star orbits and the outer Gaia rotation profile from one continuous distribution.",
    "The James Webb Space Telescope finds galaxies — massive, fully formed — just hundreds of millions of years after the Big Bang. Far too early. Far too large. They should not yet exist.",
    "Growing a supermassive black hole that fast demands continuous feeding at the absolute physical maximum. One pause and you miss the window forever. The math barely closes. Barely.",
    "Fermionic dark matter cores can collapse quickly in the early universe — seeding massive structures without slow accretion. This could explain what JWST keeps showing us should not exist.",
    "Intellectual honesty demands a pause. The dark matter core is not proven. Most astrophysicists still regard Sagittarius A-star as a genuine black hole. This is live frontier science.",
    "Current observations — stellar orbits, gas dynamics, shadow imagery — fit both models at today's resolution. The evidence does not break the tie. We need sharper instruments and tests.",
    "Next-generation Event Horizon Telescope baselines will probe the photon ring structure at far higher resolution. GRAVITY tracks S-star orbits deeper into the relativistic regime.",
    "The decisive test: a true black hole gives a sharp photon ring at one precise angular size. A dark matter core gives a subtly broader ring at a different size. Observable. Coming soon.",
    "For decades, dark matter and supermassive black holes were separate mysteries. This model asks: what if the dark thing at the center and the dark thing in the halo are the same thing?",
    "If the dark matter core holds, the singularity thought to lurk four million suns deep at our galaxy's heart may simply not exist. No infinite density. No breakdown of physics equations.",
    "The universe has fooled careful observers before. Invisible mass speaks through visible orbits — and science listens. We know its mass and gravity. What it actually is — that is the invitation.",
]

# Per-block voice settings: (rate, pitch) tuned for emotional variety
VSETTINGS = [
    ("+10%", "+12Hz"), ("-3%", "+5Hz"), ("-3%", "+3Hz"), ("-8%", "-6Hz"),
    ("+5%", "+8Hz"), ("0%", "+5Hz"), ("-8%", "-10Hz"), ("+18%", "+15Hz"),
    ("-5%", "+3Hz"), ("-10%", "-5Hz"), ("-12%", "-8Hz"), ("-5%", "+8Hz"),
    ("-7%", "+5Hz"), ("-4%", "+5Hz"), ("-7%", "-5Hz"), ("-10%", "-8Hz"),
    ("+12%", "+12Hz"), ("-5%", "+5Hz"), ("-8%", "+5Hz"), ("-5%", "+8Hz"),
    ("-7%", "-5Hz"), ("-5%", "-5Hz"), ("+5%", "+5Hz"), ("-8%", "-8Hz"),
    ("-10%", "-5Hz"), ("-5%", "+8Hz"), ("+10%", "+12Hz"), ("-5%", "+5Hz"),
    ("-5%", "+8Hz"), ("-10%", "-5Hz"), ("-8%", "-5Hz"), ("-5%", "+5Hz"),
    ("+8%", "+10Hz"), ("-8%", "-5Hz"), ("-10%", "-8Hz"), ("-10%", "-10Hz"),
]


async def gen_audio():
    import edge_tts
    os.makedirs(f"{OUT}/audio", exist_ok=True)
    for i, (narr, (rate, pitch)) in enumerate(zip(NARRATIONS, VSETTINGS)):
        p = f"{OUT}/audio/b{i:02d}.mp3"
        if os.path.exists(p):
            print(f"  aud {i:02d} ok")
            continue
        print(f"  aud {i:02d}...", flush=True)
        await edge_tts.Communicate(narr, voice="en-US-AndrewNeural",
                                   rate=rate, pitch=pitch).save(p)


def make_music(dur=375, sr=44100):
    p = f"{OUT}/music.wav"
    if os.path.exists(p):
        return p
    print("  synthesizing music...", flush=True)
    t = np.linspace(0, dur, dur * sr, endpoint=False)
    # Layered space ambient drone
    s = (0.20 * np.sin(2*np.pi*55*t)
         + 0.13 * np.sin(2*np.pi*82.5*t)
         + 0.09 * np.sin(2*np.pi*110*t + np.sin(2*np.pi*0.1*t)*0.5)
         + 0.07 * np.sin(2*np.pi*27.5*t)
         + 0.05 * np.sin(2*np.pi*165*t + np.sin(2*np.pi*0.07*t)*0.3))
    s *= (0.7 + 0.3 * np.sin(2*np.pi*0.04*t))
    fin = min(sr*6, len(s)//4)
    s[:fin] *= np.linspace(0, 1, fin)
    s[-fin:] *= np.linspace(1, 0, fin)
    s = np.clip(s, -0.95, 0.95)
    import wave as wv
    with wv.open(p, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes((s * 32767).astype(np.int16).tobytes())
    print("  music done")
    return p


def mix_audio(bi, music):
    out = f"{OUT}/mixed/b{bi:02d}.aac"
    os.makedirs(f"{OUT}/mixed", exist_ok=True)
    if os.path.exists(out):
        return out
    subprocess.run([
        'ffmpeg', '-y', '-loglevel', 'error',
        '-i', f"{OUT}/audio/b{bi:02d}.mp3",
        '-i', music,
        '-filter_complex', '[0:a]volume=1.0[v];[1:a]volume=0.11[m];[v][m]amix=inputs=2:duration=first',
        '-c:a', 'aac', '-b:a', '128k', out
    ], check=True)
    return out


def build_seg(bi, music):
    seg = f"{OUT}/segs/s{bi:02d}.mp4"
    if os.path.exists(seg):
        print(f"  seg {bi:02d} ok")
        return seg
    fd = f"{OUT}/frames/b{bi:02d}"
    os.makedirs(fd, exist_ok=True)
    narr = NARRATIONS[bi]
    print(f"  frames {bi:02d}...", flush=True)
    for fi in range(FR):
        fp = f"{fd}/f{fi:04d}.jpg"
        if not os.path.exists(fp):
            mk(bi, fi, narr).save(fp, 'JPEG', quality=85)
    audio = mix_audio(bi, music)
    print(f"  encode {bi:02d}...", flush=True)
    subprocess.run([
        'ffmpeg', '-y', '-loglevel', 'error',
        '-framerate', str(FPS), '-i', f"{fd}/f%04d.jpg",
        '-i', audio,
        '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '28',
        '-c:a', 'aac', '-b:a', '128k',
        '-pix_fmt', 'yuv420p', '-t', str(BD), seg
    ], check=True)
    print(f"  seg {bi:02d} done")
    return seg


def main():
    os.makedirs(f"{OUT}/segs", exist_ok=True)
    print("=== Phase 1: Audio ===", flush=True)
    asyncio.run(gen_audio())

    print("=== Phase 2: Background Music ===", flush=True)
    music = make_music()

    print("=== Phase 3: Video Segments ===", flush=True)
    for bi in range(36):
        build_seg(bi, music)

    print("=== Phase 4: Concat ===", flush=True)
    cl = f"{OUT}/concat.txt"
    with open(cl, 'w') as f:
        for bi in range(36):
            f.write(f"file '{OUT}/segs/s{bi:02d}.mp4'\n")
    final = f"{OUT}/out/final_v2.mp4"
    os.makedirs(f"{OUT}/out", exist_ok=True)
    subprocess.run([
        'ffmpeg', '-y', '-loglevel', 'error',
        '-f', 'concat', '-safe', '0', '-i', cl,
        '-c', 'copy', final
    ], check=True)
    print(f"DONE: {final} ({os.path.getsize(final) // 1024 // 1024} MB)")


if __name__ == '__main__':
    main()
