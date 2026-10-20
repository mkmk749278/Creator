# Film 01 hero world: YOUR BANK rack, N.P.C.I. switchboard, SHOP'S BANK rack (screenplay.md, PLAYBOOK §4a-9).
# Dark blueprint look, photo-real materials, Cycles on CPU (8 samples + OpenImageDenoise).
# Run: <venv with bpy==5.2.2>/bin/python -I world.py -- <shot> <samples> <out.png> [frame]
#   shot: wide | board | hold;  state: idle | success | failed | processing (plan v2, review_visual_plan_v1.md)
import bpy, bmesh, math, sys, time
from mathutils import Vector

args = sys.argv[sys.argv.index("--") + 1:]
shot, samples, out = args[0], int(args[1]), args[2]
state = args[3] if len(args) > 3 else "idle"
frame = 1

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
C = {"bg": "#0d1117", "panel": "#161b22", "grid": "#30363d", "amber": "#d29922", "cyan": "#58a6ff",
     "orange": "#f0883e", "slate": "#8b949e", "readout": "#e6edf3", "green": "#3fb950", "red": "#f85149"}


def lin(h, a=1.0):
    h = h.lstrip("#"); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return [((x / 12.92) if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4) for x in c] + [a]


def mat(name, col, metal=0.0, rough=0.4, emit=None, strength=0.0, coat=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = lin(col)
    b.inputs["Metallic"].default_value = metal; b.inputs["Roughness"].default_value = rough
    b.inputs["Coat Weight"].default_value = coat
    if emit:
        b.inputs["Emission Color"].default_value = lin(emit); b.inputs["Emission Strength"].default_value = strength
    return m


def noisy_metal(name, col, rough=0.35, scale=60.0, var=0.18):
    """Brushed/powder-coated steel: roughness and a faint bump broken up by noise, so it never reads as CG plastic."""
    m = mat(name, col, 0.9, rough); nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord"); nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = scale; nz.inputs["Detail"].default_value = 8
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs["To Min"].default_value = rough - var; mr.inputs["To Max"].default_value = rough + var
    nt.links.new(nz.outputs["Fac"], mr.inputs["Value"]); nt.links.new(mr.outputs["Result"], b.inputs["Roughness"])
    bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.04
    nt.links.new(nz.outputs["Fac"], bump.inputs["Height"]); nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    return m


def box(name, size, loc, m, bevel=0.004):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object; o.name = name; o.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)  # keep the origin at loc
    if bevel:
        md = o.modifiers.new("bv", "BEVEL"); md.width = bevel; md.segments = 2
    o.data.materials.append(m)
    return o


def text(body, loc, size, m, rot=(math.radians(90), 0, 0), align="CENTER", extrude=0.0):
    bpy.ops.object.text_add(location=loc, rotation=rot)
    o = bpy.context.object; o.data.body = body; o.data.size = size
    o.data.align_x = align; o.data.extrude = extrude  # built-in font for lookdev; labels move to the HUD layer in finals
    o.data.materials.append(m)
    return o


# ---------- materials ----------
floor_m = mat("floor", "#0b0e13", 0.0, 0.22, coat=0.3)
rack_m = noisy_metal("rack", "#1b2129", 0.42)
rail_m = noisy_metal("rail", "#5b6570", 0.3)
srv_m = noisy_metal("server", "#252c35", 0.38, 120)
bezel_m = mat("bezel", "#0f1318", 0.2, 0.55)
led_g = mat("led_g", C["green"], 0, 0.3, C["green"], 9.0)
led_c = mat("led_c", C["cyan"], 0, 0.3, C["cyan"], 9.0)
patch_b = mat("patch_b", "#1f5fbf", 0.0, 0.45)
patch_w = mat("patch_w", "#c9ced6", 0.0, 0.5)
led_a = mat("led_a", C["amber"], 0, 0.3, C["amber"], 7.0)
wood_m = mat("board_wood", "#2a2018", 0.0, 0.5, coat=0.6)
brass_m = noisy_metal("brass", "#b08d57", 0.28, 200, 0.1)
bake_m = mat("bakelite", "#141414", 0.0, 0.32, coat=0.4)
cable_live = mat("cable_live", C["cyan"], 0, 0.35, C["cyan"], 14.0)
cable_dead = mat("cable_dead", "#20262e", 0.0, 0.45)
label_m = mat("label", C["readout"], 0, 0.5, C["readout"], 2.5)
label_dim = mat("label_dim", C["slate"], 0, 0.5, C["slate"], 1.2)
dial_face = mat("dial_face", "#0f1520", 0.0, 0.3, coat=1.0)
tick_m = mat("tick", C["cyan"], 0, 0.3, C["cyan"], 6.0)
grid_m = mat("gridline", C["grid"], 0, 0.5, C["cyan"], 0.35)

# ---------- floor with a faint blueprint grid ----------
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0)); fl = bpy.context.object; fl.data.materials.append(floor_m)
nt = floor_m.node_tree; b = nt.nodes["Principled BSDF"]
tc = nt.nodes.new("ShaderNodeTexCoord"); bk = nt.nodes.new("ShaderNodeTexBrick")
bk.inputs["Scale"].default_value = 20; bk.inputs["Mortar Size"].default_value = 0.012
bk.inputs["Color1"].default_value = (0, 0, 0, 1); bk.inputs["Color2"].default_value = (0, 0, 0, 1)
bk.inputs["Mortar"].default_value = lin(C["cyan"]); bk.offset = 0.0; bk.squash = 1.0
nt.links.new(tc.outputs["Object"], bk.inputs["Vector"]); nt.links.new(bk.outputs["Color"], b.inputs["Emission Color"])
b.inputs["Emission Strength"].default_value = 0.25
nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 3
mr = nt.nodes.new("ShaderNodeMapRange"); mr.inputs["To Min"].default_value = 0.12; mr.inputs["To Max"].default_value = 0.4
nt.links.new(nz.outputs["Fac"], mr.inputs["Value"]); nt.links.new(mr.outputs["Result"], b.inputs["Roughness"])


# ---------- a 42U rack with servers ----------
def rack(cx, name, led_mat, label):
    W, D, H = 0.6, 1.0, 2.0
    box(f"{name}_frame_l", (0.04, D, H), (cx - W / 2, 0, H / 2), rack_m)
    box(f"{name}_frame_r", (0.04, D, H), (cx + W / 2, 0, H / 2), rack_m)
    box(f"{name}_top", (W + 0.04, D, 0.05), (cx, 0, H), rack_m)
    box(f"{name}_base", (W + 0.04, D, 0.08), (cx, 0, 0.04), rack_m)
    box(f"{name}_back", (W, 0.02, H), (cx, D / 2, H / 2), rack_m, 0)
    for side in (-1, 1):
        box(f"{name}_rail{side}", (0.02, 0.03, H - 0.12), (cx + side * 0.25, -D / 2 + 0.06, H / 2), rail_m, 0.002)
    u = 0.0445; z = 0.14; i = 0
    pattern = [2, 1, 1, 2, 1, 4, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 1] * 3
    for units in pattern:
        h = units * u - 0.003
        if z + h > H - 0.1:
            break
        box(f"{name}_srv{i}", (0.48, 0.8, h), (cx, 0.02, z + h / 2), srv_m, 0.002)
        box(f"{name}_bez{i}", (0.44, 0.012, h - 0.008), (cx, -D / 2 + 0.035, z + h / 2), bezel_m, 0.002)
        for k in range(3 if units > 1 else 2):  # status LEDs, deterministic pattern
            lm = led_mat if (i + k) % 3 else led_g
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.0035, location=(cx + 0.17 + k * 0.014, -D / 2 + 0.027, z + h / 2))
            bpy.context.object.data.materials.append(lm)
        # drive-bay slots as thin dark grooves
        for k in range(6 if units > 1 else 4):
            box(f"{name}_bay{i}_{k}", (0.003, 0.004, h * 0.7), (cx - 0.18 + k * 0.04, -D / 2 + 0.028, z + h / 2), rack_m, 0)
        z += h + 0.003; i += 1
    for side in (-1, 1):  # vertical cable managers with blue / white patch cords (qa/ref/datacentre.jpg 4, 5)
        box(f"{name}_mgr{side}", (0.07, 0.12, H - 0.2), (cx + side * 0.335, -D / 2 + 0.06, H / 2), rack_m, 0.004)
        for k in range(10):
            zz = 0.25 + k * 0.17; cm = patch_b if k % 3 else patch_w
            cord(f"{name}_pc{side}_{k}", [(cx + side * 0.2, -D / 2 + 0.02, zz), (cx + side * 0.27, -D / 2 - 0.02, zz - 0.02),
                                          (cx + side * 0.335, -D / 2 + 0.0, zz - 0.08), (cx + side * 0.335, -D / 2 + 0.03, zz - 0.3)], cm, 0.0035)
    text(label, (cx, -D / 2 - 0.02, H + 0.12), 0.11, label_m)




# ---------- N.P.C.I. switchboard, copied from the manual-exchange references (qa/ref/exchange.jpg) ----------
# Tall upright with jack fields and white lamp caps (refs 2, 8, 12), a desk shelf with two rows of cord plugs and
# key switches (refs 2, 7), red cloth cords hanging in loops below the shelf (refs 2, 3), dark wood cabinet.
lamp_m = mat("lamp_cap", "#e8e2d0", 0.0, 0.35, "#ffe9b0", 0.6)
cord_m = mat("cord_cloth", "#8c2a1c", 0.0, 0.75)
cord_bump = cord_m.node_tree; _b = cord_bump.nodes["Principled BSDF"]
_w = cord_bump.nodes.new("ShaderNodeTexWave"); _w.inputs["Scale"].default_value = 400; _w.wave_profile = "SAW"
_bp = cord_bump.nodes.new("ShaderNodeBump"); _bp.inputs["Strength"].default_value = 0.25
cord_bump.links.new(_w.outputs["Fac"], _bp.inputs["Height"]); cord_bump.links.new(_bp.outputs["Normal"], _b.inputs["Normal"])
plate_m = noisy_metal("plate", "#3a3226", 0.35, 150, 0.12)


def arrayed(obj, counts, offsets):
    for i, (n, off) in enumerate(zip(counts, offsets)):
        md = obj.modifiers.new(f"arr{i}", "ARRAY"); md.count = n
        md.use_relative_offset = False; md.use_constant_offset = True; md.constant_offset_displace = off
    return obj


def cord(name, pts, m, r=0.006):
    cu = bpy.data.curves.new(name, "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = r; cu.bevel_resolution = 3
    sp = cu.splines.new("BEZIER"); sp.bezier_points.add(len(pts) - 1)
    for bp, p in zip(sp.bezier_points, pts):
        bp.co = p; bp.handle_left_type = bp.handle_right_type = "AUTO"
    o = bpy.data.objects.new(name, cu); sc.collection.objects.link(o); o.data.materials.append(m)
    return o


def switchboard(cx):
    W = 1.6
    box("sb_desk", (W, 0.62, 0.74), (cx, 0.0, 0.37), wood_m, 0.012)
    box("sb_shelf", (W + 0.06, 0.5, 0.035), (cx, -0.08, 0.76), wood_m, 0.01)
    box("sb_upright", (W, 0.16, 1.32), (cx, 0.26, 0.78 + 0.66), wood_m, 0.012)
    box("sb_face", (W - 0.12, 0.02, 1.16), (cx, 0.175, 0.86 + 0.58), bake_m, 0.004)
    box("sb_crown", (W + 0.1, 0.24, 0.07), (cx, 0.26, 2.135), wood_m, 0.012)
    # 4 jack fields of 14 x 9; each jack = brass ring + dark hole; a lamp cap row above each field row
    for f in range(4):
        x0 = cx - 0.66 + f * 0.34; z0 = 0.92
        bpy.ops.mesh.primitive_cylinder_add(radius=0.0075, depth=0.012, vertices=12, location=(x0, 0.163, z0), rotation=(math.radians(90), 0, 0))
        j = bpy.context.object; j.data.materials.append(brass_m); arrayed(j, (14, 9), ((0.022, 0, 0), (0, 0, 0.075)))
        bpy.ops.mesh.primitive_cylinder_add(radius=0.0038, depth=0.014, vertices=8, location=(x0, 0.161, z0), rotation=(math.radians(90), 0, 0))
        h = bpy.context.object; h.data.materials.append(bake_m); arrayed(h, (14, 9), ((0.022, 0, 0), (0, 0, 0.075)))
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.0062, segments=10, ring_count=6, location=(x0, 0.163, z0 + 0.03))
        l = bpy.context.object; l.scale = (1, 0.6, 1); l.data.materials.append(lamp_m); arrayed(l, (14, 9), ((0.022, 0, 0), (0, 0, 0.075)))
        box(f"sb_strip{f}", (0.32, 0.006, 1.1), (x0 + 0.143, 0.17, 0.86 + 0.55), plate_m, 0.001)
    # desk: two rows of 16 cord plugs (brass sleeves, red cord tails) + key switches in front
    for row, y in enumerate((-0.02, 0.06)):
        for k in range(16):
            x = cx - 0.7 + k * 0.093
            bpy.ops.mesh.primitive_cylinder_add(radius=0.008, depth=0.07, vertices=12, location=(x, y, 0.81))
            bpy.context.object.data.materials.append(brass_m)
            if row == 0:
                box(f"key{k}", (0.012, 0.02, 0.035), (x, -0.2, 0.795), bake_m, 0.002)
                bpy.context.object.rotation_euler = (math.radians(-18 if k % 3 else 18), 0, 0)
            # cord tail dropping through the shelf into a hanging loop (deterministic sag per plug)
            sag = 0.18 + 0.07 * ((k * 7 + row * 3) % 5)
            cord(f"tail{row}_{k}", [(x, y, 0.77), (x, y - 0.02, 0.62), (x + 0.01, y - 0.12, 0.76 - sag - 0.25), (x + 0.02, y - 0.25, 0.6)], cord_m)
    # three patched calls: cords arcing from desk plugs up into jacks on the face
    for (k, fx, fy) in ((2, 3, 4), (6, 7, 6), (11, 9, 2)):
        x = cx - 0.7 + k * 0.093; jx = cx - 0.66 + (fx // 1) * 0.022 + (k % 4) * 0.34; jz = 0.92 + fy * 0.075
        cord(f"patch{k}", [(x, -0.02, 0.85), (x + 0.02, 0.0, 1.05), ((x + jx) / 2, 0.08, jz + 0.12), (jx, 0.15, jz)], cord_m)
    # the 15-second dial on the crown
    bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=0.03, location=(cx, 0.12, 2.38), rotation=(math.radians(90), 0, 0))
    bpy.context.object.data.materials.append(dial_face)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.2, minor_radius=0.012, location=(cx, 0.105, 2.38), rotation=(math.radians(90), 0, 0))
    bpy.context.object.data.materials.append(brass_m)
    bm = bmesh.new()
    for t in range(15):
        a = math.radians(90 - t * 24); L = 0.06 if t % 5 == 0 else 0.04; w2 = 0.007
        ux, uz = math.cos(a), math.sin(a); px, pz = -uz, ux
        r1, r2 = 0.17 - L, 0.17
        vs = [bm.verts.new((cx + ux * r + px * s2 * w2, 0.103, 2.38 + uz * r + pz * s2 * w2)) for r, s2 in ((r1, -1), (r2, -1), (r2, 1), (r1, 1))]
        bm.faces.new(vs)
    me = bpy.data.meshes.new("ticks"); bm.to_mesh(me); tk = bpy.data.objects.new("ticks", me); sc.collection.objects.link(tk)
    me.materials.append(tick_m)
    text("N.P.C.I.", (cx, 0.15, 1.93), 0.075, label_m)


switchboard(0.0)
rack(-2.2, "yourbank", led_c, "YOUR BANK")
rack(2.2, "shopbank", led_c, "SHOP'S BANK")


# ---------- patch cables: bezier tubes from the board to each rack ----------
def cable(name, pts, m, r=0.012):
    cu = bpy.data.curves.new(name, "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = r; cu.bevel_resolution = 4
    sp = cu.splines.new("BEZIER"); sp.bezier_points.add(len(pts) - 1)
    for bp, p in zip(sp.bezier_points, pts):
        bp.co = p; bp.handle_left_type = bp.handle_right_type = "AUTO"
    o = bpy.data.objects.new(name, cu); sc.collection.objects.link(o); o.data.materials.append(m)
    return o


RUPEE_FONT = bpy.data.fonts.load("/usr/share/fonts/opentype/inter/Inter-Bold.otf")
STATE_COL = {"idle": C["cyan"], "success": C["green"], "failed": C["red"], "processing": C["amber"]}
SCREEN = {"idle": "CALLING...", "success": "CONNECTED", "failed": "DECLINED", "processing": "CALL DROPPED"}
sc_col = STATE_COL[state]

call_pts = [(-0.049, -0.02, 0.85), (0.4, -0.5, 0.35), (1.3, -0.6, 0.06), (1.9, -0.55, 0.3), (1.95, -0.53, 1.2)]
if state == "processing":   # the line goes dark past the middle: a live stub, then a dead cable
    cable("call_live", call_pts[:3], mat("cable_amber", C["amber"], 0, 0.35, C["amber"], 6.0))
    cable("call_dead", call_pts[2:], cable_dead)
else:
    cable("call", call_pts, mat(f"cable_{state}", sc_col, 0, 0.35, sc_col, 14.0))
cable("debit_done", [(-0.235, -0.02, 0.85), (-0.8, -0.5, 0.3), (-1.6, -0.6, 0.06), (-2.0, -0.55, 0.4), (-1.95, -0.53, 1.0)],
      mat("cable_back", C["red"], 0, 0.35, C["red"], 10.0) if state == "failed" else cable_dead)


def label3d(body, loc, size, m, font=None):
    o = text(body, loc, size, m)
    if font:
        o.data.font = font
    return o


# bank identity (review #7): lit name plate, a vault-door panel with a wheel, a row of ₹ account slots
plate_lit = mat("plate_lit", "#0f1520", 0.2, 0.3, C["readout"], 0.15)
vault_m = noisy_metal("vault", "#6c7682", 0.3, 90, 0.12)
slot_m = mat("slot", "#0b0f14", 0.0, 0.4, C["cyan"], 0.8)
for bx, nm in ((-2.2, "YOUR BANK"), (2.2, "SHOP'S BANK")):
    box(f"vault_{bx}", (0.5, 0.03, 0.62), (bx, -0.53, 0.5), vault_m, 0.01)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.12, minor_radius=0.012, location=(bx, -0.555, 0.52), rotation=(math.radians(90), 0, 0))
    bpy.context.object.data.materials.append(brass_m)
    for k in range(3):
        box(f"spoke{bx}{k}", (0.24, 0.012, 0.014), (bx, -0.56, 0.52), brass_m, 0.003)
        bpy.context.object.rotation_euler = (0, math.radians(k * 60), 0)
    for k in range(4):  # account slots, each with a ₹ glyph
        box(f"slot{bx}{k}", (0.09, 0.02, 0.05), (bx - 0.165 + k * 0.11, -0.53, 1.62), slot_m, 0.004)
        label3d("₹", (bx - 0.165 + k * 0.11, -0.545, 1.607), 0.035, label_dim, RUPEE_FONT)

# the switchboard's call screen and three outcome lamps (review #6, #8)
box("screen", (0.62, 0.03, 0.13), (0.0, 0.155, 1.80), mat("screen_glass", "#05080c", 0.0, 0.12, coat=1.0), 0.006)
label3d(SCREEN[state], (0.0, 0.135, 1.78), 0.06, mat("screen_txt", sc_col, 0, 0.4, sc_col, 6.0), RUPEE_FONT)
for k, (key, _glyph) in enumerate((("success", "✓"), ("failed", "✕"), ("processing", "⧗"))):
    lx = (-0.42, 0.0, 0.42)[k]
    on = state == key
    lm2 = (mat(f"lamp_{key}", STATE_COL[key], 0, 0.25, STATE_COL[key], 9.0) if on
           else mat(f"lamp_{key}_off", "#1a1d22", 0.0, 0.2, STATE_COL[key], 0.08))  # off = dark glass
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.04, location=(lx, 0.16, 1.645))
    bpy.context.object.scale = (1, 0.55, 1); bpy.context.object.data.materials.append(lm2)

# the ₹840 token: where it sits IS the status (review #1, #2)
TOKEN_AT = {"idle": (-1.95, -0.62, 1.05), "success": (1.95, -0.62, 1.62),
            "failed": (-1.95, -0.62, 1.62), "processing": (1.3, -0.62, 0.32)}
tx, ty, tz = TOKEN_AT[state]
tok_m = mat("token", "#0c1118", 0.6, 0.3)  # dark coin face; the rim and the amount carry the glow
rim_m = mat("token_rim", C["amber"], 0.9, 0.25, C["amber"], 6.0 if state == "processing" else 3.0)
bpy.ops.mesh.primitive_cylinder_add(radius=0.11, depth=0.022, vertices=64, location=(tx, ty, tz), rotation=(math.radians(90), 0, 0))
bpy.context.object.data.materials.append(tok_m)
md = bpy.context.object.modifiers.new("bv", "BEVEL"); md.width = 0.006; md.segments = 3
bpy.ops.mesh.primitive_torus_add(major_radius=0.11, minor_radius=0.012, location=(tx, ty, tz), rotation=(math.radians(90), 0, 0))
bpy.context.object.data.materials.append(rim_m)
label3d("₹840", (tx, ty - 0.013, tz - 0.024), 0.068, mat("token_txt", C["amber"], 0, 0.4, C["amber"], 8.0), RUPEE_FONT)
pl = bpy.data.lights.new("token_glow", "POINT"); pl.energy = 8 if state == "processing" else 4; pl.color = lin(C["amber"])[:3]
po = bpy.data.objects.new("token_glow", pl); po.location = (tx, ty - 0.2, tz); sc.collection.objects.link(po)

# ---------- lighting: dark room, cool key, rim lights, volumetric haze ----------
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
bgn = w.node_tree.nodes["Background"]; bgn.inputs["Color"].default_value = lin(C["bg"]); bgn.inputs["Strength"].default_value = 0.6


def area(name, loc, rot, size, power, col):
    l = bpy.data.lights.new(name, "AREA"); l.size = size; l.energy = power; l.color = lin(col)[:3]
    o = bpy.data.objects.new(name, l); o.location = loc; o.rotation_euler = rot; sc.collection.objects.link(o)
    o.visible_camera = False; o.visible_glossy = False  # light panels never show in frame or in the floor


area("key", (-1.5, -4.0, 3.6), (math.radians(55), 0, math.radians(-20)), 2.5, 380, "#cfe3ff")
area("rimL", (-3.8, 2.5, 2.6), (math.radians(-60), math.radians(-30), 0), 1.0, 220, C["cyan"])
area("rimR", (3.8, 2.5, 2.6), (math.radians(-60), math.radians(30), 0), 1.0, 220, C["cyan"])
area("warm", (0.0, -1.5, 2.6), (math.radians(20), 0, 0), 0.6, 60, "#ffcf8a")

# volumetric haze in a box around the set (cheap: low density, large steps)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 1.6)); hz = bpy.context.object; hz.scale = (9, 6, 3.4)
vm = bpy.data.materials.new("haze"); vm.use_nodes = True; vn = vm.node_tree
vn.nodes.remove(vn.nodes["Principled BSDF"]); pv = vn.nodes.new("ShaderNodeVolumePrincipled")
pv.inputs["Density"].default_value = 0.018; pv.inputs["Anisotropy"].default_value = 0.3
vn.links.new(pv.outputs["Volume"], vn.nodes["Material Output"].inputs["Volume"]); hz.data.materials.append(vm)

# ---------- camera ----------
cams = {
    "wide": ((0.0, -6.6, 1.55), (0.0, 0.0, 1.05), 32, 5.4, 2.8),
    "board": ((0.9, -2.3, 1.45), (0.0, 0.2, 1.35), 50, 2.4, 2.0),
    "hold": ((1.0, -3.2, 0.5), (1.3, -0.6, 0.2), 40, 1.7, 1.8),
}
loc, tgt, lens, focus, fstop = cams[shot]
cd = bpy.data.cameras.new("cam"); cd.lens = lens; cd.dof.use_dof = True; cd.dof.focus_distance = focus; cd.dof.aperture_fstop = fstop
cam = bpy.data.objects.new("cam", cd); sc.collection.objects.link(cam); cam.location = loc
d = Vector(tgt) - Vector(loc); cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler(); sc.camera = cam

# ---------- render ----------
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = samples
sc.cycles.use_denoising = True; sc.cycles.denoiser = "OPENIMAGEDENOISE"
sc.cycles.max_bounces = 4; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 2
sc.cycles.transmission_bounces = 2; sc.cycles.volume_bounces = 0; sc.cycles.volume_step_rate = 4
sc.render.resolution_x, sc.render.resolution_y = 1920, 1080; sc.render.resolution_percentage = 100
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Medium High Contrast"
sc.render.film_transparent = False; sc.frame_set(frame)
sc.render.filepath = out; sc.render.image_settings.file_format = "PNG"
t0 = time.time(); bpy.ops.render.render(write_still=True); print(f"RENDER {shot} {samples}spp {time.time() - t0:.1f}s -> {out}")
