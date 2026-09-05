#!/usr/bin/env python3
"""
Telugu Sgr A* Explainer — Upgraded Video Pipeline
Voice: te-IN-MohanNeural (edge-tts, free)
Music: 6-layer synthesized space ambient
Visuals: PIL cinematic space with Telugu typography
"""
import asyncio, edge_tts, subprocess, numpy as np, wave, os, math, json, sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
FPS = 30
OUT = "/home/user/out"
os.makedirs(OUT, exist_ok=True)

# ===== 27 TELUGU NARRATION BLOCKS (verbatim transcript) =====
NARRATIONS = [
    "మన మిల్కీ వే గలాక్సీకి సరిగ్గా మధ్యలో ఒక వింతైన ప్రదేశం ఉంది. అక్కడికి చేరుకోగానే నక్షత్రాల సాధారణ దారి పూర్తిగా అంతమైపోతుంది. కనిపించని ఒక రహస్య ఆబ్జెక్ట్ చుట్టూ ఎన్నో పెద్ద పెద్ద స్టార్స్ తిరుగుతూ ఉంటాయి.",
    "వాటిలో S2 అనే ఒక స్టార్ ప్రతి 16 ఏళ్లకు ఒకసారి ఆ కనిపించని ఆబ్జెక్ట్ దగ్గరికి వస్తుంది.",
    "అది దగ్గరికి వెళ్ళే కొద్దీ దాని స్పీడ్ సెకనుకు వేల కిలోమీటర్ల వరకు పెరిగిపోతుంది. ఏదో అదృశ్య శక్తి ఆ స్టార్‌ను ఒక తాటితో కట్టి తన చుట్టూ తిప్పుకున్నట్లుగా అనిపిస్తుంది.",
    "ఆ చీకటి ప్రదేశంలో మన సూర్యుడి కంటే దాదాపు 40 లక్షల రెట్లు ఎక్కువ బరువు ఉన్న మాస్ దాగి ఉంది.",
    "కానీ అక్కడ ఎలాంటి పెద్ద స్టార్ కనిపించదు, కనీసం గ్రహం కానీ, మెరిసే ఆబ్జెక్ట్ కానీ ఉండదు. కేవలం ఖాళీ ప్రదేశం... దాని చుట్టూ వేగంగా తిరుగుతున్న స్టార్స్ మాత్రమే కనిపిస్తాయి.",
    "దశాబ్దాలుగా దీనికి ఒకటే సమాధానం ఉంటుంది, సైంటిస్టులు దాన్నే చెబుతున్నారు. అదేంటంటే—మన గలాక్సీ గుండెల్లో ఒక సూపర్ మ్యాసివ్ బ్లాక్ హోల్ కూర్చునుంది. దానికి సెజిటేరియస్ ఏ స్టార్ (Sagittarius A*) అని పేరు పెట్టారు.",
    "ఆ తర్వాత 2022 లో ప్రపంచం మొత్తం ఆ బ్లాక్ హోల్ ఫేమస్ ఆరెంజ్ రింగ్‌ను చూసింది. దాంతో ఈ మిస్టరీకి ఎండ్ కార్డ్ పడిందని అందరూ అనుకున్నారు.",
    "కానీ ఆ ఫోటోలో మనం చూసింది బ్లాక్ హోల్ కాదు. దాని చుట్టూ తిరుగుతున్న వేడి గ్యాస్ లైట్‌ను, మధ్యలో ఉన్న ఒక డార్క్ షాడోను మాత్రమే మనం చూశాం. ఆ చీకటి వెనుక అసలు ఏముందనేది ఇప్పటికీ మన కళ్ళకు కనిపించని రహస్యంగా ఉండిపోయింది.",
    "ఆ తర్వాత 2026 ఫిబ్రవరిలో ఒక సైంటిస్టుల టీం సరికొత్త మోడల్‌ను తెరపైకి తెచ్చింది.",
    "వాళ్ళ ప్రకారం మన గలాక్సీ సెంటర్‌లో ఉన్నది బ్లాక్ హోల్ కాదు. అది డార్క్ మేటర్‌తో నిండిన ఒక అత్యంత దట్టమైన ఇన్విజిబుల్ కోర్.",
    "అది కూడా చుట్టుపక్కల ఉన్న స్టార్స్‌ను దాదాపుగా బ్లాక్ హోల్ లాగే తిప్పుతోంది. అంటే దశాబ్దాలుగా గలాక్సీ సెంటర్‌లో ఉన్న ఆబ్జెక్ట్‌కు మనం తప్పు పేరు పెట్టామా?",
    "2022 లో మనం చూసిన ఆ ఫోటో ఒక బ్లాక్ హోల్‌ది కాదా? దానిలాగే కనిపించే వేరేదైనా కాస్మిక్ మాన్‌స్టర్‌దా?",
    "ఒకవేళ మన గలాక్సీ గుండెల్లో ఉన్నది బ్లాక్ హోల్ కాకుండా డార్క్ మేటర్ కోర్ అయితే, ఈ యూనివర్స్ గురించి మనకున్న అవగాహన ఇంకా సంపూర్ణంగానే ఉన్నట్లా?",
    "వెల్, ఇక అసలు కథలోకి వెళితే... 1846వ సంవత్సరం, ఫ్రాన్స్‌లోని ఒక అబ్జర్వేటరీ అది. అర్బన్ లెవేరియర్ అనే ఆస్ట్రానమర్ తన టేబుల్ ముందు కూర్చుని గంటల తరబడి పేపర్లపై లెక్కలు వేస్తున్నాడు.",
    "అతని కళ్ళ ముందు ఒక వింతైన పజిల్ ఉంది. ఆ కాలం వరకు మన సోలార్ సిస్టమ్‌లో చిట్ట చివరి గ్రహం యురేనస్ అని అందరూ నమ్మేవారు.",
    "కానీ యురేనస్ కదలికల్లో ఏదో తేడా కనిపించింది. అది తన ఆర్బిట్‌లో సరిగ్గా తిరగడం లేదు. అప్పుడప్పుడు కొంచెం ముందుకు వెళ్ళడం, మళ్ళీ వెనకబడడం జరుగుతోంది.",
    "ఏదో అదృశ్య శక్తి దాన్ని లాగుతున్నట్లుగా అనిపించింది. ప్రపంచవ్యాప్తంగా ఉన్న సైంటిస్టులంతా ఆశ్చర్యపోయారు. అక్కడ గ్రావిటీ నియమాలు పని చేయవేమో అని అందరూ అనుకున్నారు.",
    "కానీ లెవేరియర్ మాత్రం కాస్త భిన్నంగా ఆలోచించాడు. యురేనస్‌ను ఏదో ఒక వస్తువు లాగుతుందని అతను అనుకున్నాడు. ఇప్పటివరకు ఎవరూ చూడని ఒక కొత్త గ్రహం అక్కడ ఉండి ఉంటుందని అతను నమ్మాడు.",
    "టెలిస్కోప్ వాడకుండా కేవలం పేపర్ మ్యాథ్స్ ఆధారంగా ఆ కనిపించని గ్రహం ఆకాశంలో సరిగ్గా ఎక్కడ ఉంటుందో లెక్కగట్టి చెప్పాడు.",
    "సడన్‌గా చాలా నెమ్మదిగా తిరుగుతున్నాయి. చాలా థియరీలు ఈ విషయాన్ని సరిగ్గా వివరించలేకపోయాయి. కానీ ఈ డార్క్ మేటర్ ఐడియా మాత్రం దానికి స్పష్టమైన కారణాన్ని చూపించింది.",
    "ఇక జేమ్స్ వెబ్ టెలిస్కోప్ (JWST) అయితే మరింత ఆశ్చర్యకరమైన విషయాలను బయట పెట్టింది. యూనివర్స్ పుట్టిన తొలినాళ్ళలో ఏర్పడిన అత్యంత భారీ వస్తువులని అది రికార్డ్ చేసింది.",
    "అయితే నేను ఇక్కడ ఒక విషయం స్పష్టంగా చెప్పాలి—ఇవన్నీ కూడా ఇంకా పూర్తిగా ప్రూవ్ కాలేదు. ఆ సైంటిస్టులు కూడా ఇదే విషయాన్ని చెబుతున్నారు.",
    "ఇప్పటికీ చాలా మంది అది బ్లాక్ హోల్ అనే నమ్ముతున్నారు. ఈ డార్క్ మేటర్ అనే కొత్త వాదనను అప్పుడే తప్పు పట్టలేమని కూడా అంటున్నారు. అంటే ఈ రెండిటిలో ఏది నిజం అనేది ఇంకా ఎవరికీ ఖచ్చితంగా తెలియదు.",
    "ఇక మన గలాక్సీ మధ్యలో దాగి ఉన్న ఆ అదృశ్య రాక్షసుడు—అంటే బ్లాక్ హోల్, అలాగే టోటల్ యూనివర్స్‌లో 85% నిండి ఉన్న ఆ డార్క్ మేటర్... ఇన్నాళ్లూ మనం ఈ రెండిటినీ రెండు వేరు వేరు మిస్టరీలుగా భావించాం.",
    "కానీ ఈ కథ చెబుతున్న దాన్ని బట్టి ఈ రెండు మిస్టరీలు నిజానికి ఒకటే. ఆ రెండిటికీ ఒకటే సమాధానం.",
    "ఒకవేళ ఇదే నిజమైతే, సమస్తాన్ని మింగేసే బ్లాక్ హోల్ ఎప్పటికీ ఉనికిలోనే లేనట్లు! లేక దానికి బదులుగా మన గలాక్సీకి సరిగ్గా మధ్యలో, విశ్వంలోకెల్లా అత్యంత రహస్యమైన డార్క్ మేటర్ ఎప్పటి నుంచో నిశ్శబ్దంగా కూర్చునే ఉంది.",
    "వీడియో నచ్చితే లైక్ చేయండి, షేర్ చేయండి. ఇప్పటి వరకు మన ఛానల్‌ని సబ్స్క్రైబ్ చేయనట్లయితే ఇప్పుడే సబ్స్క్రైబ్ చేసుకొని పక్కనే ఉన్న బెల్ ఐకాన్‌పై క్లిక్ చేయండి. నెక్స్ట్ వీడియోలో మళ్ళీ కలుద్దాం. థాంక్స్ ఫర్ వాచింగ్!",
]

# Per-block voice settings: (rate, pitch) for te-IN-MohanNeural
VSETTINGS = [
    ("+5%","+8Hz"), ("-3%","+5Hz"), ("+8%","+12Hz"), ("-8%","-6Hz"),
    ("-5%","+3Hz"), ("+3%","+6Hz"), ("+10%","+15Hz"), ("-5%","+5Hz"),
    ("-3%","+8Hz"), ("-8%","-5Hz"), ("-5%","+5Hz"), ("+12%","+12Hz"),
    ("-7%","-8Hz"), ("+5%","+5Hz"), ("-5%","+3Hz"), ("-8%","-5Hz"),
    ("-10%","-8Hz"), ("-5%","+5Hz"), ("+8%","+10Hz"), ("-5%","-5Hz"),
    ("+5%","+8Hz"), ("-8%","+5Hz"), ("-7%","-5Hz"), ("-10%","-8Hz"),
    ("-5%","+5Hz"), ("+10%","+12Hz"), ("-10%","-10Hz"),
]

TITLES = [
    "గలాక్సీ రహస్యం", "S2 స్టార్", "అదృశ్య శక్తి", "40 లక్షల సూర్యులు",
    "ఖాళీ ప్రదేశం", "Sagittarius A*", "2022 - ఆరెంజ్ రింగ్", "నిజం ఏమిటి?",
    "కొత్త సిద్ధాంతం 2026", "డార్క్ మేటర్ కోర్", "బ్లాక్ హోల్ లాంటిదే", "తప్పు పేరా?",
    "మనకు ఏం కనిపించింది?", "1846 - లెవేరియర్", "యురేనస్ పజిల్", "ఆర్బిట్ తేడా",
    "అదృశ్య గ్రావిటీ", "వేరే గ్రహం ఉందా?", "పేపర్ మ్యాథ్స్", "రొటేషన్ కర్వ్స్",
    "JWST రహస్యాలు", "ఇంకా ప్రూవ్ కాలేదు", "ఇంకా డిబేట్", "రెండూ వేరు మిస్టరీలు",
    "ఒకే సమాధానం!", "అద్భుతమైన ముగింపు", "మళ్ళీ కలుద్దాం!",
]

# Visual type per block: 0=galaxy 1=orbit 2=bh 3=dm 4=solar 5=curve 6=jwst 7=end
VIS_TYPE = [0,1,1,0,0,2,2,2,3,3,3,3,3,4,4,4,4,4,4,5,6,3,3,7,7,7,7]


def star_field(d, rng, count=700):
    for _ in range(count):
        x, y = rng.randint(0, W), rng.randint(0, H)
        r = rng.choice([1,1,1,2,2,3])
        b = rng.randint(100, 255)
        col = (b, b, min(255, b+30))
        d.ellipse([x-r, y-r, x+r, y+r], fill=col)


def glow_circle(d, cx, cy, rmax, color_fn):
    for r in range(rmax, 0, -2):
        col = color_fn(r, rmax)
        d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=col)


def make_visual(bi, font_lg, font_sm, font_def):
    img = Image.new('RGB', (W, H), (0, 0, 10))
    d = ImageDraw.Draw(img)
    rng = np.random.RandomState(bi * 137 + 7)
    star_field(d, rng)
    cx, cy = W // 2, H // 2
    vt = VIS_TYPE[bi] if bi < len(VIS_TYPE) else 7

    if vt == 0:  # Galaxy center
        for r in range(120, 0, -3):
            ratio = (120 - r) / 120
            rc = int(255 * min(1.0, ratio * 3))
            gc = int(200 * max(0, ratio * 2 - 0.5))
            d.ellipse([cx-r, cy-r//2, cx+r, cy+r//2], fill=(rc, gc, 0))
        # Spiral arms
        for arm in range(3):
            for s in range(60):
                angle = arm * 2.094 + s * 0.15
                dist = 60 + s * 4
                sx = int(cx + dist * math.cos(angle))
                sy = int(cy + dist * math.sin(angle) * 0.45)
                br = max(0, 150 - s * 2)
                d.ellipse([sx-2, sy-2, sx+2, sy+2], fill=(br, br//2, 0))

    elif vt == 1:  # S2 orbit
        glow_circle(d, cx, cy, 35, lambda r, rm: (int(255*(rm-r)/rm), int(200*(rm-r)/rm), 0))
        d.ellipse([cx-200, cy-90, cx+200, cy+90], outline=(80, 160, 255, 255), width=2)
        # Orbit trail
        for s in range(20):
            angle = bi * 0.7 + s * 0.08
            sx = int(cx + 180 * math.cos(angle))
            sy = int(cy + 75 * math.sin(angle))
            br = int(80 + s * 8)
            d.ellipse([sx-2, sy-2, sx+2, sy+2], fill=(br, br, min(255, br+50)))
        # S2 star
        angle = bi * 0.7 + 20 * 0.08
        sx = int(cx + 180 * math.cos(angle))
        sy = int(cy + 75 * math.sin(angle))
        d.ellipse([sx-8, sy-8, sx+8, sy+8], fill=(255, 255, 200))
        # Speed label
        d.text((cx-80, cy+110), "7,650 km/s", fill=(100, 200, 255), font=font_def)

    elif vt == 2:  # Black hole / EHT
        for r in range(160, 0, -2):
            ratio = r / 160
            rc = int(255 * min(1, (1-ratio)*3))
            gc = int(150 * max(0, (1-ratio)*2 - 0.3))
            d.ellipse([cx-r, cy-r//2, cx+r, cy+r//2], fill=(rc, gc, 0))
        d.ellipse([cx-50, cy-30, cx+50, cy+30], fill=(0, 0, 5))
        d.text((cx-80, cy+90), "Sagittarius A*", fill=(255, 150, 50), font=font_def)

    elif vt == 3:  # Dark matter core
        glow_circle(d, cx, cy, 110, lambda r, rm: (
            int(80*(1-r/rm)), int(10*(1-r/rm)), int(200*(1-r/rm)+30)))
        for _ in range(15):
            px = rng.randint(cx-80, cx+80)
            py = rng.randint(cy-80, cy+80)
            d.ellipse([px-3, py-3, px+3, py+3], fill=(180, 80, 255))
        d.text((cx-40, cy+120), "Dark Matter?", fill=(180, 100, 255), font=font_def)

    elif vt == 4:  # Solar system / Le Verrier
        sun_r = 45
        glow_circle(d, 120, cy, sun_r, lambda r, rm: (255, int(220*(rm-r)/rm), 0))
        orbits = [(150, 80, (100, 180, 255)), (230, 110, (100, 220, 150)),
                  (310, 135, (200, 100, 80)), (380, 155, (150, 100, 255))]
        for orbit_a, orbit_b, col in orbits:
            d.ellipse([120-orbit_a, cy-orbit_b, 120+orbit_a, cy+orbit_b],
                     outline=(50, 50, 80), width=1)
            angle = bi * 0.4 + orbit_a * 0.01
            px = int(120 + orbit_a * math.cos(angle))
            py = int(cy + orbit_b * math.sin(angle))
            r = 8 if orbit_a < 200 else 14
            d.ellipse([px-r, py-r, px+r, py+r], fill=col)
        # Neptune hidden planet hint
        if bi >= 17:
            d.text((cx+50, cy-50), "???", fill=(100, 150, 255), font=font_def)

    elif vt == 5:  # Rotation curve
        # Graph area
        gx, gy, gw, gh = 150, 80, W-250, H-200
        d.rectangle([gx, gy, gx+gw, gy+gh], outline=(60, 60, 90))
        # Expected (Keplerian decline)
        pts_exp = [(gx + i*10, int(gy + gh - gh * 0.8 / (1 + (i*0.08)**0.5)))
                   for i in range(gw//10)]
        d.line(pts_exp, fill=(220, 80, 80), width=2)
        # Observed (flat)
        flat_y = gy + gh - int(gh * 0.55)
        d.line([(gx, flat_y), (gx+gw, flat_y)], fill=(80, 220, 80), width=3)
        d.text((gx+5, gy+5), "Velocity (km/s)", fill=(180, 180, 180), font=font_def)
        d.text((gx+gw-80, gy+gh+5), "Distance", fill=(180, 180, 180), font=font_def)
        d.text((gx+gw//2-60, flat_y-25), "Observed", fill=(80, 220, 80), font=font_def)
        d.text((gx+20, pts_exp[-1][1]-25), "Expected", fill=(220, 80, 80), font=font_def)

    elif vt == 6:  # JWST galaxies
        for _ in range(40):
            gx = rng.randint(30, W-30)
            gy = rng.randint(30, H-180)
            gs = rng.randint(6, 30)
            hue = [(255, 150, 100), (100, 150, 255), (255, 240, 100), (200, 100, 255)][rng.randint(0,4)]
            d.ellipse([gx-gs, gy-gs//2, gx+gs, gy+gs//2], fill=hue)
            d.ellipse([gx-gs+1, gy-gs//2+1, gx+gs-1, gy+gs//2-1], outline=(255,255,255))
        d.text((cx-100, 30), "James Webb Space Telescope", fill=(100, 200, 255), font=font_def)

    else:  # Conclusion / end
        # BH on left
        glow_circle(d, 320, cy, 90, lambda r, rm: (int(255*(rm-r)/rm), int(130*(rm-r)/rm), 0))
        d.ellipse([270, cy-28, 370, cy+28], fill=(0, 0, 10))
        # DM on right
        glow_circle(d, W-320, cy, 90, lambda r, rm: (
            int(80*(1-r/rm)), 0, int(200*(1-r/rm)+30)))
        # Equal sign
        d.rectangle([cx-50, cy-12, cx+50, cy-4], fill=(255, 200, 0))
        d.rectangle([cx-50, cy+4, cx+50, cy+12], fill=(255, 200, 0))
        d.text((310, cy+100), "Black Hole", fill=(255, 150, 50), font=font_def)
        d.text((W-360, cy+100), "Dark Matter", fill=(160, 80, 255), font=font_def)

    # === Gradient bottom bar for text ===
    for row in range(H-130, H):
        alpha = (row - (H-130)) / 130
        r0 = int(0 * (1 - alpha) + 0)
        g0 = int(0 * (1 - alpha) + 0)
        b0 = int(10 * (1 - alpha) + 25 * alpha)
        d.line([(0, row), (W, row)], fill=(r0, g0, b0))

    # === Telugu title (top glow) ===
    title = TITLES[bi] if bi < len(TITLES) else ""
    if font_lg and title:
        try:
            for ox, oy in [(-3,0),(3,0),(0,-3),(0,3),(-2,-2),(2,-2),(-2,2),(2,2)]:
                d.text((40+ox, 22+oy), title, fill=(80, 40, 0), font=font_lg)
            d.text((40, 22), title, fill=(255, 220, 70), font=font_lg)
        except Exception:
            d.text((40, 22), title, fill=(255, 220, 70), font=font_def)

    # === Telugu subtitle (bottom) ===
    narr = NARRATIONS[bi]
    words = narr.split()
    line1 = " ".join(words[:12])
    line2 = " ".join(words[12:24]) if len(words) > 12 else ""
    if font_sm:
        try:
            for ox, oy in [(-1,0),(1,0),(0,-1),(0,1)]:
                d.text((30+ox, H-115+oy), line1, fill=(0,0,0), font=font_sm)
                if line2:
                    d.text((30+ox, H-75+oy), line2, fill=(0,0,0), font=font_sm)
            d.text((30, H-115), line1, fill=(255, 255, 255), font=font_sm)
            if line2:
                d.text((30, H-75), line2, fill=(240, 240, 240), font=font_sm)
        except Exception:
            d.text((30, H-115), line1[:80], fill=(255, 255, 255), font=font_def)

    # === Progress dot row ===
    for pi in range(len(NARRATIONS)):
        px = 60 + pi * ((W - 120) // (len(NARRATIONS) - 1))
        col = (255, 200, 0) if pi == bi else (50, 50, 70)
        d.ellipse([px-4, H-18, px+4, H-10], fill=col)

    return img


def make_music(dur=680, sr=44100):
    print("Synthesizing music...")
    t = np.linspace(0, dur, dur * sr, endpoint=False)
    s = (0.22 * np.sin(2*np.pi*27.5*t)
       + 0.18 * np.sin(2*np.pi*55.0*t)
       + 0.11 * np.sin(2*np.pi*82.5*t + np.sin(2*np.pi*0.05*t)*0.9)
       + 0.08 * np.sin(2*np.pi*110.0*t)
       + 0.05 * np.sin(2*np.pi*165.0*t + np.sin(2*np.pi*0.07*t)*0.6)
       + 0.03 * np.sin(2*np.pi*440.0*t) * np.abs(np.sin(2*np.pi*0.09*t))
       + 0.015 * np.random.RandomState(42).randn(dur*sr) * 0.5)
    s *= (0.60 + 0.40 * np.sin(2*np.pi*0.025*t))
    fade = sr * 6
    s[:fade] *= np.linspace(0, 1, fade)
    s[-fade:] *= np.linspace(1, 0, fade)
    s = np.clip(s, -1, 1)
    with wave.open(f"{OUT}/music.wav", 'w') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr)
        wf.writeframes((s * 32767).astype(np.int16).tobytes())
    print(f"Music: {OUT}/music.wav ({dur}s)")


async def gen_audio():
    for i, (narr, (rate, pitch)) in enumerate(zip(NARRATIONS, VSETTINGS)):
        p = f"{OUT}/audio_{i:02d}.mp3"
        if os.path.exists(p) and os.path.getsize(p) > 1000:
            print(f"Audio {i:02d}: cached")
            continue
        try:
            await edge_tts.Communicate(narr, voice="te-IN-MohanNeural",
                                       rate=rate, pitch=pitch).save(p)
            sz = os.path.getsize(p)
            print(f"Audio {i:02d}: {sz//1024}KB")
        except Exception as e:
            print(f"Audio {i:02d}: ERROR {e}")


def get_dur(path):
    r = subprocess.run(['ffprobe','-v','quiet','-show_entries','format=duration',
                       '-of','json', path], capture_output=True, text=True)
    try:
        return float(json.loads(r.stdout)['format']['duration'])
    except Exception:
        return 20.0


def main():
    # --- Font setup ---
    font_lg = font_sm = None
    font_def = ImageFont.load_default()

    font_candidates = [
        '/usr/share/fonts/truetype/noto/NotoSansTelugu-Regular.ttf',
        '/usr/share/fonts/noto/NotoSansTelugu-Regular.ttf',
        '/usr/share/fonts/opentype/noto/NotoSansTelugu-Regular.ttf',
        '/tmp/NotoSansTelugu.ttf',
    ]

    installed = False
    for c in font_candidates:
        if os.path.exists(c):
            font_lg = ImageFont.truetype(c, 46)
            font_sm = ImageFont.truetype(c, 30)
            print(f"Font found: {c}")
            installed = True
            break

    if not installed:
        print("Installing fonts-noto-extra...")
        subprocess.run(['apt-get','install','-y','-q','fonts-noto-extra'],
                      capture_output=True)
        for c in font_candidates:
            if os.path.exists(c):
                font_lg = ImageFont.truetype(c, 46)
                font_sm = ImageFont.truetype(c, 30)
                print(f"Font installed: {c}")
                break

    if not font_lg:
        print("Downloading Noto Sans Telugu from GitHub...")
        url = "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansTelugu/NotoSansTelugu-Regular.ttf"
        subprocess.run(['curl','-sL', url, '-o', '/tmp/NotoSansTelugu.ttf'])
        if os.path.exists('/tmp/NotoSansTelugu.ttf') and os.path.getsize('/tmp/NotoSansTelugu.ttf') > 10000:
            font_lg = ImageFont.truetype('/tmp/NotoSansTelugu.ttf', 46)
            font_sm = ImageFont.truetype('/tmp/NotoSansTelugu.ttf', 30)
            print("Font downloaded OK")
        else:
            print("WARNING: No Telugu font - text will be boxes")

    # --- Music ---
    if not os.path.exists(f"{OUT}/music.wav"):
        make_music()

    # --- Audio ---
    print("\n=== Generating audio (te-IN-MohanNeural) ===")
    asyncio.run(gen_audio())

    # --- Visuals + encode ---
    print("\n=== Generating visuals and encoding segments ===")
    segments = []
    total_dur = 0
    music_offset = 0

    for i, narr in enumerate(NARRATIONS):
        audio_p = f"{OUT}/audio_{i:02d}.mp3"
        if not os.path.exists(audio_p):
            print(f"Seg {i:02d}: no audio, skipping")
            continue

        dur = get_dur(audio_p)
        total_dur += dur

        # Generate visual frame
        img = make_visual(i, font_lg, font_sm, font_def)
        img_p = f"{OUT}/frame_{i:02d}.jpg"
        img.save(img_p, quality=92)

        # Mix: narration + music segment
        mix_p = f"{OUT}/mix_{i:02d}.aac"
        subprocess.run([
            'ffmpeg', '-y',
            '-ss', str(music_offset), '-i', f"{OUT}/music.wav",
            '-i', audio_p,
            '-filter_complex',
            '[0:a]volume=0.13[m];[1:a]volume=1.0[v];[m][v]amix=inputs=2:duration=shortest[out]',
            '-map','[out]','-t', str(dur), '-c:a','aac','-b:a','192k', mix_p
        ], capture_output=True)
        music_offset += dur

        # Encode segment (stillimage mode for speed)
        seg_p = f"{OUT}/seg_{i:02d}.mp4"
        subprocess.run([
            'ffmpeg', '-y',
            '-loop', '1', '-i', img_p,
            '-i', mix_p,
            '-c:v', 'libx264', '-preset', 'ultrafast', '-tune', 'stillimage',
            '-crf', '26', '-pix_fmt', 'yuv420p',
            '-c:a', 'copy', '-shortest', '-t', str(dur+0.1),
            seg_p
        ], capture_output=True)

        if os.path.exists(seg_p):
            sz = os.path.getsize(seg_p) // 1024
            print(f"Seg {i:02d}: {dur:.1f}s → {sz}KB")
            segments.append(seg_p)
        else:
            print(f"Seg {i:02d}: encoding failed")

    # --- Concatenate ---
    if not segments:
        print("ERROR: no segments produced")
        sys.exit(1)

    list_p = f"{OUT}/concat.txt"
    with open(list_p, 'w') as f:
        for s in segments:
            f.write(f"file '{s}'\n")

    final = f"{OUT}/final_te.mp4"
    r = subprocess.run([
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', list_p,
        '-c', 'copy', final
    ], capture_output=True)

    if os.path.exists(final):
        sz = os.path.getsize(final)
        print(f"\n=== DONE: {final}")
        print(f"    Size: {sz//1024//1024}MB, Duration: {total_dur:.1f}s ({total_dur/60:.1f}min)")
        print(f"    Segments: {len(segments)}/27")
        return final
    else:
        print("CONCAT FAILED:", r.stderr.decode()[-500:])
        sys.exit(1)


if __name__ == '__main__':
    main()
