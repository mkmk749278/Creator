# Film 01: every Blender shot, animated on the set from upi_set.py (shots.md, screenplay.md plan v2).
# The ₹840 token's position is the status (review_visual_plan_v1.md): home slot, riding the call, frozen mid-cable,
# or in the shop's slot. Times in the shot specs are seconds from the shot's own start; FPS 24.
# Run: <venv with bpy==5.2.2>/bin/python -I film.py -- <shot> <samples> <outdir> [WxH] [frames]
#   writes <outdir>/f_0001.png ... (stills write f_0001.png only). `frames` = comma list for spot checks.
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from upi_set import *  # noqa: F401,F403  (builds the static set)

args = sys.argv[sys.argv.index("--") + 1:]
SHOT, SAMPLES, OUT = args[0], int(args[1]), args[2].rstrip("/")
RES = tuple(int(v) for v in (args[3] if len(args) > 3 else "1280x720").split("x"))
SPOT = [int(f) for f in args[4].split(",")] if len(args) > 4 else None
FPS = 24


def F(t):
    return 1 + round(t * FPS)


def key_socket(sock, t, value):
    sock.default_value = value; sock.keyframe_insert("default_value", frame=F(t))


def bsdf(m):
    return m.node_tree.nodes["Principled BSDF"]


# ---------- the token's road: home slot -> debit cable -> board -> call cable -> shop slot ----------
def catmull(pts, n_per=24):
    P = [Vector(p) for p in pts]; P = [P[0]] + P + [P[-1]]; out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n_per):
            t = k / n_per; t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    out.append(P[-2]); return out


debit_pts = [(-0.235, -0.02, 0.85), (-0.8, -0.5, 0.3), (-1.6, -0.6, 0.06), (-2.0, -0.55, 0.4), (-1.95, -0.53, 1.0)]
call_pts = [(-0.049, -0.02, 0.85), (0.4, -0.5, 0.35), (1.3, -0.6, 0.06), (1.9, -0.55, 0.3), (1.95, -0.53, 1.2)]
LIFT = Vector((0, -0.09, 0.15))   # the token rides just in front of and above its cable
HOME, SHOP = Vector((-2.255, -0.66, 1.62)), Vector((2.145, -0.66, 1.62))
legs = [  # (name, control points); the token passes their ends in order
    ("out", [HOME, HOME + Vector((0.12, -0.06, -0.28)), Vector(debit_pts[-1]) + LIFT]),
    ("debit", [Vector(p) + LIFT for p in reversed(debit_pts)]),
    ("hop", [Vector(debit_pts[0]) + LIFT, Vector((-0.14, -0.14, 1.06)), Vector(call_pts[0]) + LIFT]),
    ("call", [Vector(p) + LIFT for p in call_pts]),
    ("in", [Vector(call_pts[-1]) + LIFT, SHOP + Vector((-0.12, -0.06, -0.28)), SHOP]),
]
road, marks = [], {"home": 0.0}
for name, pts in legs:
    seg = catmull(pts); road += seg if not road else seg[1:]
    marks[name] = len(road) - 1
L = [0.0]
for a, b in zip(road, road[1:]):
    L.append(L[-1] + (a - b).length)
# resample by length so the Follow Path factor is proportional to distance travelled
N = 600; uni = []; j = 0
for i in range(N + 1):
    s = L[-1] * i / N
    while j < len(L) - 2 and L[j + 1] < s:
        j += 1
    u = (s - L[j]) / max(L[j + 1] - L[j], 1e-9); uni.append(road[j].lerp(road[j + 1], u))
POS = {k: (L[v] / L[-1] if k != "home" else 0.0) for k, v in marks.items()}
POS.update(home=0.0, rack_out=POS["out"], board_in=POS["debit"], board=POS["hop"], shop_rack=POS["call"], shop=1.0)
POS["mid"] = POS["board"] + 0.55 * (POS["shop_rack"] - POS["board"])   # where a dropped call freezes it


def call_frac(r):  # token road position -> fraction along the call cable (for the glow's growing edge)
    return max(0.0, min(1.0, (r - POS["board"]) / (POS["shop_rack"] - POS["board"])))


cu = bpy.data.curves.new("road", "CURVE"); cu.dimensions = "3D"; sp = cu.splines.new("POLY"); sp.points.add(len(uni) - 1)
for p, v in zip(sp.points, uni):
    p.co = (v.x, v.y, v.z, 1.0)
cu.use_path = True; road_ob = bpy.data.objects.new("road", cu); sc.collection.objects.link(road_ob); road_ob.hide_render = True

# ---------- cables: dead base + a glowing overlay whose colour, strength and length are keyed ----------
cable("debit_base", debit_pts, cable_dead); cable("call_base", call_pts, cable_dead)
glow = {}
for nm, pts in (("debit", debit_pts), ("call", call_pts)):
    m = mat(f"glow_{nm}", C["cyan"], 0, 0.35, C["cyan"], 0.0); o = cable(f"glow_{nm}", pts, m, 0.0128)
    o.data.bevel_factor_mapping_start = o.data.bevel_factor_mapping_end = "SPLINE"
    glow[nm] = (o, m)


def glow_key(nm, t, col=None, strength=None, start=None, end=None):
    o, m = glow[nm]; b = bsdf(m)
    if col:
        key_socket(b.inputs["Emission Color"], t, lin(C[col])); key_socket(b.inputs["Base Color"], t, lin(C[col]))
    if strength is not None:
        key_socket(b.inputs["Emission Strength"], t, strength)
    if start is not None:
        o.data.bevel_factor_start = start; o.data.keyframe_insert("bevel_factor_start", frame=F(t))
    if end is not None:
        o.data.bevel_factor_end = end; o.data.keyframe_insert("bevel_factor_end", frame=F(t))


# ---------- the ₹840 token ----------
def make_token(name, at=None):
    piv = bpy.data.objects.new(name, None); sc.collection.objects.link(piv)
    face = mat(f"{name}_face", "#0c1118", 0.6, 0.3); rim = mat(f"{name}_rim", C["amber"], 0.9, 0.25, C["amber"], 3.0)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.11, depth=0.022, vertices=64, location=(0, 0, 0), rotation=(math.radians(90), 0, 0))
    c = bpy.context.object; c.data.materials.append(face); c.parent = piv
    md = c.modifiers.new("bv", "BEVEL"); md.width = 0.006; md.segments = 3
    bpy.ops.mesh.primitive_torus_add(major_radius=0.11, minor_radius=0.012, location=(0, 0, 0), rotation=(math.radians(90), 0, 0))
    r = bpy.context.object; r.data.materials.append(rim); r.parent = piv
    t = label3d("₹840", (0, -0.013, -0.024), 0.068, mat(f"{name}_txt", C["amber"], 0, 0.4, C["amber"], 8.0), RUPEE_FONT); t.parent = piv
    pl = bpy.data.lights.new(f"{name}_glow", "POINT"); pl.energy = 4; pl.color = lin(C["amber"])[:3]
    po = bpy.data.objects.new(f"{name}_glow", pl); po.location = (0, -0.2, 0); po.parent = piv; sc.collection.objects.link(po)
    if at is not None:
        piv.location = at
    else:
        fp = piv.constraints.new("FOLLOW_PATH"); fp.target = road_ob; fp.use_fixed_location = True; fp.name = "road"
    return piv, rim, po


tok, tok_rim, tok_light = make_token("token")


def tok_at(t, where):
    fp = tok.constraints["road"]; fp.offset_factor = POS[where] if isinstance(where, str) else where
    fp.keyframe_insert("offset_factor", frame=F(t))


def tok_glow(t, strength, light=None):
    key_socket(bsdf(tok_rim).inputs["Emission Strength"], t, strength)
    if light is not None:
        tok_light.data.energy = light; tok_light.data.keyframe_insert("energy", frame=F(t))


def tok_pulse(t0, t1, period=1.0, lo=2.5, hi=9.0):
    t, i = t0, 0
    while t <= t1 + 1e-6:
        tok_glow(t, hi if i % 2 == 0 else lo, 9 if i % 2 == 0 else 3); t += period / 2; i += 1


# ---------- switchboard screen, outcome lamps, 15-second dial ----------
STATE_COL = {"idle": "cyan", "success": "green", "failed": "red", "processing": "amber"}
SCREENS = {"calling": ("CALLING...", "cyan"), "connected": ("CONNECTED", "green"), "declined": ("DECLINED", "red"),
           "dropped": ("CALL DROPPED", "amber")}
box("screen", (0.62, 0.03, 0.13), (0.0, 0.155, 1.80), mat("screen_glass", "#05080c", 0.0, 0.12, coat=1.0), 0.006)
screen_txt = {}
for k, (body, col) in SCREENS.items():
    o = label3d(body, (0.0, 0.135, 1.78), 0.06, mat(f"scr_{k}", C[col], 0, 0.4, C[col], 6.0), RUPEE_FONT)
    o.hide_render = True; screen_txt[k] = o


def screen(seq):
    """seq: [(t, key or None)] — shows one screen text at a time."""
    for t, key in seq:
        for k, o in screen_txt.items():
            o.hide_render = (k != key); o.keyframe_insert("hide_render", frame=F(t))


lamp_m = {}
for k, key in enumerate(("success", "failed", "processing")):
    m = mat(f"lamp_{key}", "#1a1d22", 0.0, 0.2, C[STATE_COL[key]], 0.08); lamp_m[key] = m
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.04, location=((-0.42, 0.0, 0.42)[k], 0.16, 1.645))
    bpy.context.object.scale = (1, 0.55, 1); bpy.context.object.data.materials.append(m)


def lamp(key, t, on):
    b = bsdf(lamp_m[key])
    key_socket(b.inputs["Base Color"], t, lin(C[STATE_COL[key]] if on else "#1a1d22"))
    key_socket(b.inputs["Emission Strength"], t, 9.0 if on else 0.08)


def lamp_set(t, on_key=None):
    for k in lamp_m:
        lamp(k, t, k == on_key)


dial_piv = bpy.data.objects.new("dial_pivot", None); sc.collection.objects.link(dial_piv); dial_piv.location = (0.0, 0.094, 2.38)
_hand = box("dial_hand", (0.012, 0.006, 0.15), (0.0, 0.0, 0.065), tick_m, 0); _hand.parent = dial_piv


def dial(t, seconds):  # hand angle as a share of the 15 s limit (on-screen pace is ILLUSTRATIVE)
    dial_piv.rotation_euler = (0, math.radians(360 * seconds / 15.0), 0)
    dial_piv.keyframe_insert("rotation_euler", index=1, frame=F(t))


# shop's account slot glow (lands) and your slot glow (returns)
slot_glow = {}
for nm, x in (("home", HOME.x), ("shop", SHOP.x)):
    m = mat(f"slotglow_{nm}", "#0b0f14", 0.0, 0.4, C["green"], 0.0)
    box(f"slotglow_{nm}", (0.094, 0.004, 0.054), (x, -0.542, 1.62), m, 0); slot_glow[nm] = m


def slot(nm, t, col, strength):
    b = bsdf(slot_glow[nm]); key_socket(b.inputs["Emission Color"], t, lin(C[col])); key_socket(b.inputs["Emission Strength"], t, strength)


# ---------- the shop's ledger and the two rubber stamps (Answer beat) ----------
LEDGER = Vector((1.25, -1.25, 0.0))
QMARK = []   # the "?" on the page; a stamp print replaces it
HOVER = {"yes": (0.07, 0.2, 0.26), "no": (0.25, 0.2, 0.26)}


def build_ledger():
    oak = mat("lectern", "#2b211a", 0.0, 0.45, coat=0.4)
    box("lectern_post", (0.12, 0.12, 0.92), LEDGER + Vector((0, 0.05, 0.46)), oak, 0.01)
    box("lectern_foot", (0.5, 0.4, 0.04), LEDGER + Vector((0, 0.05, 0.02)), oak, 0.01)
    top = bpy.data.objects.new("lectern_top", None); sc.collection.objects.link(top)
    top.location = LEDGER + Vector((0, 0, 0.95)); top.rotation_euler = (math.radians(24), 0, 0)  # far edge up, toward camera
    paper = mat("paper", "#d9d2bf", 0.0, 0.8); nt = paper.node_tree; b = bsdf(paper)
    wv = nt.nodes.new("ShaderNodeTexWave"); wv.wave_type = "BANDS"; wv.bands_direction = "Y"
    wv.inputs["Scale"].default_value = 70; wv.inputs["Distortion"].default_value = 0.0
    tc = nt.nodes.new("ShaderNodeTexCoord"); nt.links.new(tc.outputs["Object"], wv.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB"); ramp.color_ramp.elements[0].position = 0.9
    ramp.color_ramp.elements[0].color = lin("#d9d2bf"); ramp.color_ramp.elements[1].color = lin("#6f8fb0")
    nt.links.new(wv.outputs["Fac"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    cover = mat("ledger_cover", "#3a1e18", 0.0, 0.55, coat=0.3)
    parts = [box("ledger_board", (0.66, 0.46, 0.02), (0, 0, 0.0), cover, 0.006),
             box("pages_l", (0.31, 0.42, 0.03), (-0.163, 0, 0.022), paper, 0.004),
             box("pages_r", (0.31, 0.42, 0.03), (0.163, 0, 0.022), paper, 0.004)]
    ink = mat("ink_amber", C["amber"], 0, 0.5, C["amber"], 1.5); ink_q = mat("ink_q", "#1d2a38", 0, 0.5)
    t1 = label3d("₹840", (-0.16, 0.04, 0.0385), 0.07, ink, RUPEE_FONT); t1.rotation_euler = (0, 0, 0)
    t2 = label3d("?", (0.16, 0.03, 0.0385), 0.13, ink_q, RUPEE_FONT); t2.rotation_euler = (0, 0, 0)
    hd = label3d("PAYMENTS IN", (-0.16, 0.15, 0.0385), 0.03, mat("ink_head", "#2b3a4a", 0, 0.6), RUPEE_FONT); hd.rotation_euler = (0, 0, 0)
    t1.parent = top; t2.parent = top; hd.parent = top; QMARK.append(t2)
    for o in parts + [t1, t2]:
        o.parent = top
    stamps = {}
    for nm, col, x in (("yes", "green", -0.13), ("no", "red", 0.17)):
        piv = bpy.data.objects.new(f"stamp_{nm}", None); sc.collection.objects.link(piv); piv.parent = top
        piv.location = HOVER[nm]
        rub = mat(f"rubber_{nm}", "#141414", 0.0, 0.7)
        base = box(f"stampbase_{nm}", (0.14, 0.09, 0.03), (0, 0, 0), mat(f"stampwood_{nm}", "#5a3d26", 0.0, 0.5, coat=0.3), 0.006)
        pad = box(f"stamppad_{nm}", (0.13, 0.08, 0.008), (0, 0, -0.019), rub, 0.002)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.018, depth=0.09, location=(0, 0, 0.06)); hnd = bpy.context.object
        hnd.data.materials.append(mat(f"handle_{nm}", "#6b4a2f", 0.0, 0.45, coat=0.4))
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.034, location=(0, 0, 0.12)); knob = bpy.context.object
        knob.data.materials.append(mat(f"knob_{nm}", C[col], 0.0, 0.3, C[col], 1.2))
        lab = label3d(nm.upper(), (0, -0.047, -0.004), 0.034, mat(f"stamplab_{nm}", C[col], 0, 0.4, C[col], 3.0), RUPEE_FONT)
        for o in (base, pad, hnd, knob, lab):
            o.parent = piv
        prt = label3d("YES" if nm == "yes" else "NO", (0.16, 0.03, 0.0395), 0.07,
                      mat(f"print_{nm}", C[col], 0, 0.6, C[col], 2.5), RUPEE_FONT)
        prt.rotation_euler = (0, 0, math.radians(-8 if nm == "yes" else 6)); prt.parent = top; prt.hide_render = True
        stamps[nm] = (piv, prt)
    return top, stamps


# ---------- camera rig ----------
cd = bpy.data.cameras.new("cam"); cd.lens = 35; cd.dof.use_dof = True; cd.dof.aperture_fstop = 2.4
cam = bpy.data.objects.new("cam", cd); sc.collection.objects.link(cam); sc.camera = cam
aim = bpy.data.objects.new("cam_aim", None); sc.collection.objects.link(aim)
tr = cam.constraints.new("TRACK_TO"); tr.target = aim; tr.track_axis = "TRACK_NEGATIVE_Z"; tr.up_axis = "UP_Y"


def cam_key(t, loc, look, lens=35, focus=None, shake=0.0):
    cam.location = loc; cam.keyframe_insert("location", frame=F(t))
    aim.location = look; aim.keyframe_insert("location", frame=F(t))
    cd.lens = lens; cd.keyframe_insert("lens", frame=F(t))
    cd.dof.focus_distance = focus if focus else (Vector(loc) - Vector(look)).length
    cd.dof.keyframe_insert("focus_distance", frame=F(t))


def micro_shake(t0, t1, amp=0.006):  # handheld feel on the drop: deterministic small offsets, keyed every 2 frames
    i = 0; t = t0
    while t <= t1:
        ofs = Vector((math.sin(i * 1.7) * amp, 0, math.cos(i * 2.3) * amp))
        cam.delta_location = ofs; cam.keyframe_insert("delta_location", frame=F(t)); t += 2 / FPS; i += 1
    cam.delta_location = (0, 0, 0); cam.keyframe_insert("delta_location", frame=F(t))


def ring_start(t, until_mid_at):  # the call: token rides from the board toward the shop, glow grows behind it
    tok_at(t, "board"); tok_at(until_mid_at, "mid")
    glow_key("call", t, col="cyan", strength=12.0, start=0.0, end=0.0)
    glow_key("call", until_mid_at, end=call_frac(POS["mid"]))


WIDE = ((0.0, -6.6, 1.55), (0.0, 0.0, 1.05))


# ---------- shots (durations from shots.md; t = seconds into the shot) ----------
def shot_B09():   # 0:24.5 "First, your bank takes the money out of your account." (5.0 s)
    D = 5.0; screen([(0, None)]); lamp_set(0); dial(0, 0)
    tok_at(0, "home"); tok_at(0.5, "home"); tok_at(2.6, "rack_out")
    tok_glow(0, 1.5, 2); tok_glow(2.6, 6.0, 6); slot("home", 0, "cyan", 0.0); slot("home", 0.5, "cyan", 0.0)
    slot("home", 0.9, "amber", 4.0); slot("home", 2.8, "amber", 0.0)
    glow_key("debit", 0, col="cyan", strength=0.0, start=0.0, end=1.0)
    cam_key(0, (-1.05, -2.55, 1.62), (-2.15, -0.55, 1.35), 42); cam_key(D, (-1.25, -2.15, 1.45), (-2.1, -0.6, 1.2), 42)
    return D


def shot_B11():   # 0:35.6 "It calls the shop's bank and says, please add this money..." (4.7 s)
    D = 4.7; screen([(0, None), (1.6, "calling")]); lamp_set(0); dial(0, 0); dial(1.6, 0); dial(D, 3.0)
    tok_at(0, "rack_out"); tok_at(1.4, "board_in"); tok_at(1.8, "board")
    tok_glow(0, 6.0, 6)
    glow_key("debit", 0, col="cyan", strength=0.0)
    ring_start(1.8, D)
    cam_key(0, (-1.6, -4.8, 1.3), (-0.9, -0.3, 0.7), 35); cam_key(D, (0.2, -4.6, 1.4), (0.5, -0.3, 0.8), 35)
    return D


def shot_B12():   # 0:40.3 "...a phone call. And like every phone call in India... three things can happen." (6.4 s)
    D = 6.4; screen([(0, "calling")]); lamp_set(0); dial(0, 3.0); dial(D, 6.5)
    tok_at(0, "mid"); glow_key("call", 0, col="cyan", strength=12.0, start=0.0, end=call_frac(POS["mid"]))
    for i, key in enumerate(("success", "failed", "processing")):   # "three things" -> three lamps, one by one
        t = 3.6 + i * 0.8; lamp(key, t - 0.05, False); lamp(key, t, True)
    cam_key(0, (0.55, -1.6, 1.82), (0.0, 0.16, 1.78), 50, 1.8); cam_key(D, (0.35, -1.25, 1.8), (0.0, 0.16, 1.74), 50, 1.45)
    return D


def shot_B13():   # 0:47.2 "One, the shop's bank picks up and says, done, the shop got it — that's success." (5.8 s)
    D = 5.8; screen([(0, "calling"), (0.9, "connected")]); lamp_set(0); lamp_set(0.9, "success"); dial(0, 2.0); dial(0.9, 2.6)
    tok_at(0, "mid"); tok_at(0.9, "mid"); tok_at(3.3, "shop")
    glow_key("call", 0, col="cyan", strength=12.0, start=0.0, end=call_frac(POS["mid"]))
    glow_key("call", 0.85, col="cyan"); glow_key("call", 1.0, col="green", end=1.0)
    slot("shop", 0, "green", 0.0); slot("shop", 3.2, "green", 0.0); slot("shop", 3.4, "green", 8.0); tok_glow(3.3, 3.0, 4)
    cam_key(0, (0.6, -5.4, 1.35), (1.0, -0.3, 0.9), 35); cam_key(D, (1.35, -3.9, 1.45), (1.9, -0.5, 1.25), 38)
    return D


def shot_B14():   # 0:53.0 "Two, the shop's bank picks up and says, sorry, we can't take this... that's failed." (7.7 s)
    D = 7.7; screen([(0, "calling"), (1.0, "declined")]); lamp_set(0); lamp_set(1.0, "failed"); dial(0, 2.0); dial(1.0, 2.7)
    tok_at(0, "mid"); tok_at(1.0, "mid"); tok_at(2.2, POS["mid"] + 0.6 * (POS["shop_rack"] - POS["mid"]))
    tok_at(2.6, POS["mid"] + 0.5 * (POS["shop_rack"] - POS["mid"]))   # bounces off the shop's bank
    glow_key("call", 0, col="cyan", strength=12.0, start=0.0, end=call_frac(POS["mid"]))
    glow_key("call", 0.95, col="cyan", end=call_frac(POS["mid"])); glow_key("call", 1.1, col="red", end=1.0)
    slot("shop", 0, "red", 0.0); slot("shop", 2.1, "red", 0.0); slot("shop", 2.2, "red", 7.0); slot("shop", 3.2, "red", 2.0)
    cam_key(0, (1.9, -4.6, 0.9), (1.35, -0.4, 0.6), 40); cam_key(D, (1.6, -3.7, 0.95), (1.5, -0.45, 0.75), 40)
    return D


def shot_B15():   # 1:00.7 "Failed sounds scary... your money comes back to you on its own." (7.6 s, parcel cam)
    D = 7.6; screen([(0, "declined")]); lamp_set(0, "failed"); dial(0, 2.7)
    back = POS["mid"] + 0.5 * (POS["shop_rack"] - POS["mid"])
    tok_at(0, back); tok_at(1.0, back); tok_at(3.6, "board"); tok_at(4.0, "board_in"); tok_at(6.4, "home")
    glow_key("call", 0, col="red", strength=10.0, start=0.0, end=1.0); glow_key("call", 3.6, strength=10.0); glow_key("call", 5.0, strength=2.0)
    glow_key("debit", 0, col="red", strength=0.0, start=0.0, end=1.0); glow_key("debit", 3.6, strength=0.0); glow_key("debit", 4.0, strength=10.0)
    slot("home", 0, "green", 0.0); slot("home", 6.3, "green", 0.0); slot("home", 6.5, "green", 8.0)
    cam_key(0, (1.6, -3.4, 1.1), (1.1, -0.6, 0.45), 38); cam_key(3.6, (0.2, -3.6, 1.3), (-0.2, -0.3, 0.8), 36)
    cam_key(D, (-1.3, -2.9, 1.55), (-2.1, -0.6, 1.4), 40)
    return D


def shot_B17():   # 1:13.5 "Three. The troublemaker. N.P.C.I. calls... and the line goes quiet... Call dropped." (9.0 s)
    D = 9.0; lamp_set(0); screen([(0, None), (2.4, "calling"), (8.1, "dropped")])
    tok_at(0, "board_in"); tok_at(2.4, "board"); tok_at(5.4, "mid")
    glow_key("call", 0, col="cyan", strength=0.0, start=0.0, end=0.0); glow_key("call", 2.4, strength=12.0, end=0.0)
    glow_key("call", 5.4, end=call_frac(POS["mid"]))
    for t, v in ((5.9, 12.0), (6.3, 2.0), (6.5, 11.0), (6.9, 0.6), (7.2, 9.0), (7.6, 1.0), (8.1, 0.0), (8.5, 0.0), (8.9, 4.0)):
        glow_key("call", t, strength=v)   # "...the line goes quiet. Hello?... Hello?..." flicker, then dead
    glow_key("call", 8.0, col="cyan"); glow_key("call", 8.5, col="amber")
    lamp("processing", 8.05, False); lamp("processing", 8.1, True)
    dial(0, 0); dial(2.4, 0); dial(8.1, 15.0)   # the 15-second limit runs out as the call drops
    tok_glow(0, 6.0, 6); tok_pulse(8.1, D, 0.9)
    cam_key(0, *WIDE, 32); cam_key(5.4, (0.25, -6.1, 1.45), (0.35, 0.0, 1.0), 32)
    cam_key(D, (0.9, -4.4, 1.05), (1.05, -0.5, 0.6), 34); micro_shake(7.9, 8.6)
    return D


def shot_B26():   # 2:11.4 "Now the shop's bank has to answer one simple question..." (7.4 s)
    D = 7.4; top, st = build_ledger()
    tok.hide_render = True; tok_light.hide_render = True
    for nm, (piv, prt) in st.items():
        for i, t in enumerate((0, 1.8, 3.6, 5.4, 7.2)):   # stamps hover and bob, waiting
            hx, hy, hz = HOVER[nm]; piv.location = (hx, hy, hz + (0.012 if (i + (nm == "no")) % 2 else -0.012))
            piv.keyframe_insert("location", frame=F(t))
    look = LEDGER + Vector((0, 0.02, 1.02))
    cam_key(0, LEDGER + Vector((0.45, -1.15, 1.85)), look, 42); cam_key(D, LEDGER + Vector((0.2, -0.85, 1.72)), look, 42)
    return D


def stamp_shot(which):   # 2:18.8 YES / 2:23.1 NO: the stamp comes down, the print appears (1.8 s)
    D = 1.8; top, st = build_ledger(); tok.hide_render = True; tok_light.hide_render = True
    piv, prt = st[which]; hx, hy, hz = HOVER[which]
    piv.location = (hx, hy, hz); piv.keyframe_insert("location", frame=F(0))
    piv.location = (0.16, 0.05, 0.07); piv.keyframe_insert("location", frame=F(0.30))
    piv.location = (0.16, 0.05, 0.058); piv.keyframe_insert("location", frame=F(0.38))
    piv.location = (0.16, 0.05, 0.058); piv.keyframe_insert("location", frame=F(0.55))
    piv.location = (hx, hy, hz + 0.03); piv.keyframe_insert("location", frame=F(1.1))
    for o, before in ((prt, True), (QMARK[0], False)):   # the print replaces the "?"
        o.hide_render = before; o.keyframe_insert("hide_render", frame=F(0.37))
        o.hide_render = not before; o.keyframe_insert("hide_render", frame=F(0.38))
    other = st["no" if which == "yes" else "yes"][0]; other.hide_render = False
    look = LEDGER + Vector((0.05, 0, 0.98))
    cam_key(0, LEDGER + Vector((0.25, -0.8, 1.72)), look, 45); cam_key(0.38, LEDGER + Vector((0.24, -0.78, 1.71)), look, 45)
    micro_shake(0.38, 0.62, 0.004); cam_key(D, LEDGER + Vector((0.2, -0.7, 1.66)), look, 45)
    return D


def shot_B27a():
    return stamp_shot("yes")


def shot_B28a():
    return stamp_shot("no")


def shot_B27b():   # 2:20.6 "Then the shop has your money..." token slides into the shop's slot (2.5 s)
    D = 2.5; screen([(0, "dropped")]); lamp_set(0, "processing")
    tok_at(0, "mid"); tok_at(2.0, "shop"); slot("shop", 0, "green", 0.0); slot("shop", 1.9, "green", 0.0); slot("shop", 2.1, "green", 8.0)
    glow_key("call", 0, col="amber", strength=4.0, start=0.0, end=call_frac(POS["mid"])); glow_key("call", 0.6, col="green", strength=10.0, end=1.0)
    cam_key(0, (2.6, -3.6, 1.0), (1.8, -0.55, 1.0), 40); cam_key(D, (2.5, -3.0, 1.25), (2.0, -0.6, 1.35), 42)
    return D


def shot_B28b():   # 2:24.9 "Then it comes back to your bank, and into your account." (2.1 s)
    D = 2.1; screen([(0, "dropped")]); lamp_set(0, "processing")
    tok_at(0, "board"); tok_at(0.2, "board_in"); tok_at(1.8, "home")
    glow_key("debit", 0, col="green", strength=8.0, start=0.0, end=1.0); slot("home", 0, "green", 0.0); slot("home", 1.7, "green", 0.0); slot("home", 1.9, "green", 8.0)
    cam_key(0, (-1.0, -3.4, 1.0), (-1.6, -0.4, 0.8), 38); cam_key(D, (-1.4, -2.7, 1.3), (-2.1, -0.6, 1.35), 40)
    return D


def shot_B43():   # 4:02.6 bridge: "what really happens in those few seconds after you hit pay, when everything works" (9.0 s)
    D = 9.0; lamp_set(0); screen([(0, None), (1.2, "calling"), (3.0, "connected")]); lamp_set(3.0, "success")
    tok_at(0, "home"); tok_at(0.4, "home"); tok_at(1.2, "board"); tok_at(4.6, "shop")
    glow_key("debit", 0, col="green", strength=0.0, start=0.0, end=1.0); glow_key("debit", 0.4, strength=8.0)
    glow_key("call", 0, col="cyan", strength=0.0, start=0.0, end=0.0); glow_key("call", 1.2, strength=12.0, end=0.0)
    glow_key("call", 3.0, col="cyan", end=0.6); glow_key("call", 3.1, col="green", end=1.0)
    slot("shop", 0, "green", 0.0); slot("shop", 4.5, "green", 0.0); slot("shop", 4.7, "green", 8.0)
    dial(0, 0); dial(1.2, 0); dial(3.0, 1.2)
    cam_key(0, (0.0, -4.4, 1.2), (0.0, -0.2, 1.0), 32); cam_key(D, (0.0, -7.4, 1.9), (0.0, 0.0, 1.1), 30)
    return D


# ---------- stills (1920x1080 by default; pushes and pulses are added in the 2D layer) ----------
def still(where, cam_loc, look, lens=40, state=None, scr=None, slots=None, extra=None):
    def f():
        tok_at(0, where) if where else None
        if where is None:
            tok.hide_render = True; tok_light.hide_render = True
        lamp_set(0, state); screen([(0, scr)])
        if state == "processing" or where == "mid":
            glow_key("call", 0, col="amber", strength=4.0, start=0.0, end=call_frac(POS["mid"])); tok_glow(0, 7.0, 7)
        if extra:
            extra()
        cam_key(0, cam_loc, look, lens)
        return 0.0
    return f


def _slot_readout(body, col):
    def f():
        o = label3d(body, (SHOP.x, -0.58, 1.70), 0.05, mat(f"ro_{body}", C[col], 0, 0.4, C[col], 6.0), RUPEE_FONT)
        q = label3d("?", (SHOP.x + 0.11, -0.58, 1.70), 0.05, mat("ro_q", C["amber"], 0, 0.4, C["amber"], 6.0), RUPEE_FONT)
        tok.hide_render = True; tok_light.hide_render = True
    return f


def _twice():
    make_token("token_a", SHOP + Vector((-0.125, -0.01, 0))); make_token("token_b", SHOP + Vector((0.125, -0.03, 0)))
    tok.hide_render = True; tok_light.hide_render = True
    slot("shop", 0, "amber", 6.0)


STILLS = {
    "S10_board": still(None, (1.1, -2.9, 1.5), (0.0, 0.2, 1.35), 40),
    "S18_slot0": still(None, (2.55, -1.25, 1.75), (2.15, -0.55, 1.66), 60, extra=_slot_readout("₹0", "slate")),
    "S18_slot840": still(None, (2.45, -1.2, 1.72), (2.15, -0.55, 1.66), 60, extra=_slot_readout("₹840", "amber")),
    "S24_where": still("mid", (0.1, -6.3, 1.5), (0.3, 0.0, 0.95), 33, "processing", "dropped"),
    "S25a_hold": still("mid", (1.6, -3.0, 0.75), (1.15, -0.65, 0.35), 40, "processing", "dropped"),
    "S25b_hold": still("mid", (2.1, -2.3, 0.22), (1.2, -0.65, 0.33), 30, "processing", "dropped"),
    "S25c_hold": still("mid", (1.3, -1.7, 0.42), (1.15, -0.67, 0.32), 70, "processing", "dropped"),
    "S35a_lamps": still("mid", (0.5, -1.5, 1.8), (0.0, 0.16, 1.72), 50, "success", "connected"),
    "S35b_lamps": still("mid", (0.1, -1.4, 1.75), (0.0, 0.16, 1.72), 50, "failed", "declined"),
    "S35c_lamps": still("mid", (-0.35, -1.5, 1.8), (0.0, 0.16, 1.72), 50, "processing", "dropped"),
    "S36_rule": still("mid", (-0.9, -2.6, 1.3), (0.2, 0.0, 1.35), 40, "processing", "dropped"),
    "S37b_twice": still(None, (2.45, -2.1, 1.85), (2.15, -0.6, 1.62), 45, extra=_twice),
}

# ---------- render ----------
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = SAMPLES
if os.environ.get("UPI_DEVICE") == "GPU":
    cp = bpy.context.preferences.addons["cycles"].preferences
    for kind in ("OPTIX", "CUDA"):
        try:
            cp.compute_device_type = kind; cp.get_devices()
            if any(d.type == kind for d in cp.devices):
                break
        except TypeError:
            continue
    for d in cp.devices:
        d.use = d.type != "CPU"
    sc.cycles.device = "GPU"
sc.cycles.use_denoising = True; sc.cycles.denoiser = "OPENIMAGEDENOISE"
sc.cycles.max_bounces = 4; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 2
sc.cycles.transmission_bounces = 2; sc.cycles.volume_bounces = 0; sc.cycles.volume_step_rate = 4
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Medium High Contrast"
sc.render.fps = FPS; sc.render.image_settings.file_format = "PNG"
os.makedirs(OUT, exist_ok=True)
t0 = time.time()
if SHOT in STILLS:
    STILLS[SHOT]()
    sc.render.resolution_x, sc.render.resolution_y = RES if len(args) > 3 else (1920, 1080)
    sc.frame_set(1); sc.render.filepath = f"{OUT}/f_0001.png"; bpy.ops.render.render(write_still=True)
else:
    D = globals()[f"shot_{SHOT}"]()
    sc.render.resolution_x, sc.render.resolution_y = RES
    sc.frame_start, sc.frame_end = 1, F(D)
    if SPOT:
        for f in SPOT:
            sc.frame_set(f); sc.render.filepath = f"{OUT}/f_{f:04d}.png"; bpy.ops.render.render(write_still=True)
    else:
        sc.render.filepath = f"{OUT}/f_"; bpy.ops.render.render(animation=True)
print(f"FILM {SHOT} done {time.time() - t0:.1f}s -> {OUT}")
