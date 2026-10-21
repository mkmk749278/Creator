# Film 01 hook and Answer beats: a generic UPI payment soundbox on a kirana counter (ILLUSTRATION; no brand).
# Shapes from the kirana reference sheet (qa/ref/kirana.jpg): a QR standee on the counter, packets behind.
# Run: <bpy venv>/bin/python -I soundbox.py -- <off|on> <samples> <out.png> [WxH]
import bpy, math, os, sys
from mathutils import Vector
args = sys.argv[sys.argv.index("--") + 1:]
STATE, SPP, OUT = args[0], int(args[1]), args[2]
W, H = (int(v) for v in (args[3] if len(args) > 3 else "1920x1080").split("x"))
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene


def lin(h):
    h = h.lstrip("#"); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return [((x / 12.92) if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4) for x in c] + [1.0]


def mat(name, col, metal=0.0, rough=0.5, emit=None, strength=0.0, coat=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = lin(col); b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = rough; b.inputs["Coat Weight"].default_value = coat
    if emit:
        b.inputs["Emission Color"].default_value = lin(emit); b.inputs["Emission Strength"].default_value = strength
    return m


def add(o, m):
    o.data.materials.append(m); return o


# counter top: worn laminate wood with grain
wood = mat("counter", "#6b4a32", 0.0, 0.42, coat=0.25); nt = wood.node_tree; b = nt.nodes["Principled BSDF"]
wv = nt.nodes.new("ShaderNodeTexWave"); wv.inputs["Scale"].default_value = 3.0; wv.inputs["Distortion"].default_value = 6.0
wv.inputs["Detail"].default_value = 6.0; ramp = nt.nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].color = lin("#4a3020"); ramp.color_ramp.elements[1].color = lin("#7a573c")
nt.links.new(wv.outputs["Fac"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 0, 0)); add(bpy.context.object, wood)
# soundbox: rounded black body, front grille, LED ring, a small top display
body = mat("sb_body", "#141618", 0.1, 0.35, coat=0.6)
bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=0.14, vertices=64, location=(0, 0, 0.07)); sb = add(bpy.context.object, body)
bv = sb.modifiers.new("bv", "BEVEL"); bv.width = 0.012; bv.segments = 5
grille = mat("grille", "#0a0b0c", 0.6, 0.55); g = grille.node_tree; gb = g.nodes["Principled BSDF"]
vor = g.nodes.new("ShaderNodeTexVoronoi"); vor.inputs["Scale"].default_value = 260; bump = g.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.6
g.links.new(vor.outputs["Distance"], bump.inputs["Height"]); g.links.new(bump.outputs["Normal"], gb.inputs["Normal"])
bpy.ops.mesh.primitive_cylinder_add(radius=0.066, depth=0.07, vertices=64, location=(0, 0, 0.065)); add(bpy.context.object, grille).scale = (1.002, 1.002, 1)
on = STATE == "on"
ring = mat("led_ring", "#1b2a1f" if not on else "#3fb950", 0.0, 0.3, "#3fb950", 12.0 if on else 0.0)
bpy.ops.mesh.primitive_torus_add(major_radius=0.071, minor_radius=0.0035, location=(0, 0, 0.128)); add(bpy.context.object, ring)
disp = mat("display", "#06090b", 0.0, 0.1, "#58a6ff" if on else None, 2.0 if on else 0.0, coat=1.0)
bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=0.004, vertices=48, location=(0, 0, 0.141)); add(bpy.context.object, disp)
# QR standee behind: card on an easel stand, generic QR pattern (deterministic), no brand
qr_m = mat("qr", "#f2f2f2", 0.0, 0.6); q = qr_m.node_tree; qb = q.nodes["Principled BSDF"]
chk = q.nodes.new("ShaderNodeTexBrick"); chk.inputs["Scale"].default_value = 9; chk.inputs["Mortar Size"].default_value = 0.0
chk.inputs["Color1"].default_value = lin("#111111"); chk.inputs["Color2"].default_value = lin("#f2f2f2"); chk.squash = 1.0; chk.offset = 0.5
tc = q.nodes.new("ShaderNodeTexCoord"); q.links.new(tc.outputs["Object"], chk.inputs["Vector"]); q.links.new(chk.outputs["Color"], qb.inputs["Base Color"])
card = mat("card", "#e9eef2", 0.0, 0.5)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0.2, 0.12, 0.13)); c = bpy.context.object; c.scale = (0.15, 0.006, 0.22); c.rotation_euler = (math.radians(-12), 0, math.radians(-14)); add(c, card)
bpy.ops.mesh.primitive_plane_add(size=0.1, location=(0.2, 0.113, 0.15)); p = bpy.context.object; p.rotation_euler = (math.radians(78), 0, math.radians(-14)); add(p, qr_m)
# packets and jars behind, defocused (colourful shop clutter from the references)
cols = ["#d23a2a", "#f2b632", "#2e7d32", "#1565c0", "#e65100", "#ad1457", "#fdd835"]
for i in range(14):
    x = -0.5 + i * 0.08; h = 0.12 + 0.05 * ((i * 7) % 3)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0.55 + 0.04 * (i % 2), h / 2)); o = bpy.context.object
    o.scale = (0.06, 0.03, h); add(o, mat(f"pk{i}", cols[i % len(cols)], 0.0, 0.45, coat=0.5))
# light: warm shop bulb + cool phone-screen fill
for nm, loc, e, col, sz in (("bulb", (0.4, -0.3, 0.9), 60, "#ffd9a0", 0.4), ("fill", (-0.5, -0.4, 0.4), 8, "#b8d4ff", 0.6), ("rim", (0, 0.8, 0.6), 30, "#ffe2b8", 0.5)):
    l = bpy.data.lights.new(nm, "AREA"); l.energy = e; l.color = lin(col)[:3]; l.size = sz
    o = bpy.data.objects.new(nm, l); o.location = loc; sc.collection.objects.link(o)
    d = Vector((0, 0, 0.08)) - Vector(loc); o.rotation_euler = d.to_track_quat("-Z", "Y").to_euler(); o.visible_camera = False
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; w.node_tree.nodes["Background"].inputs["Color"].default_value = lin("#120d09")
cd = bpy.data.cameras.new("cam"); cd.lens = 55; cd.dof.use_dof = True; cd.dof.focus_distance = 0.66; cd.dof.aperture_fstop = 2.8
cam = bpy.data.objects.new("cam", cd); sc.collection.objects.link(cam); cam.location = (-0.26, -0.62, 0.24)
d = Vector((0.02, 0.0, 0.085)) - cam.location; cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler(); sc.camera = cam
sc.render.engine = "CYCLES"; sc.cycles.samples = SPP; sc.cycles.use_denoising = True
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Medium High Contrast"
sc.render.resolution_x, sc.render.resolution_y = W, H; sc.render.filepath = OUT; bpy.ops.render.render(write_still=True)
print("SOUNDBOX done", OUT)
