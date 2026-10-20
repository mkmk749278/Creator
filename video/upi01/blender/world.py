# Film 01 hero world: YOUR BANK rack, N.P.C.I. switchboard, SHOP'S BANK rack (screenplay.md, PLAYBOOK §4a-9).
# Dark blueprint look, photo-real materials, Cycles on CPU (8 samples + OpenImageDenoise).
# Run: <venv with bpy==5.2.2>/bin/python -I world.py -- <shot> <samples> <out.png> [frame]
#   shot: wide | board | hold   (lookdev stills; animation passes come after the owner sees the look)
import bpy, bmesh, math, sys, time
from mathutils import Vector

args = sys.argv[sys.argv.index("--") + 1:]
shot, samples, out = args[0], int(args[1]), args[2]
frame = int(args[3]) if len(args) > 3 else 1

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
C = {"bg": "#0d1117", "panel": "#161b22", "grid": "#30363d", "amber": "#d29922", "cyan": "#58a6ff",
     "orange": "#f0883e", "slate": "#8b949e", "readout": "#e6edf3", "green": "#3fb950"}


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
    bpy.ops.object.transform_apply(scale=True)
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
    text(label, (cx, -D / 2 - 0.02, H + 0.12), 0.11, label_m)


rack(-2.2, "yourbank", led_c, "YOUR BANK")
rack(2.2, "shopbank", led_c, "SHOP'S BANK")


# ---------- N.P.C.I. switchboard: an old exchange board, blueprint-coloured ----------
def switchboard(cx):
    W, H = 1.5, 1.7
    box("sb_cab", (W, 0.5, 0.85), (cx, 0.1, 0.425), wood_m, 0.01)          # desk
    box("sb_shelf", (W + 0.06, 0.62, 0.04), (cx, 0.04, 0.87), wood_m, 0.008)
    box("sb_panel", (W, 0.12, H - 0.9), (cx, 0.3, 0.9 + (H - 0.9) / 2), bake_m, 0.01)
    box("sb_crown", (W + 0.08, 0.2, 0.08), (cx, 0.3, H + 0.04), wood_m, 0.01)
    # jack field: 10 x 6 brass jacks
    for r in range(6):
        for c in range(10):
            x = cx - 0.6 + c * 0.133; zz = 1.05 + r * 0.1
            bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=0.02, location=(x, 0.235, zz), rotation=(math.radians(90), 0, 0))
            bpy.context.object.data.materials.append(brass_m)
            bpy.ops.mesh.primitive_cylinder_add(radius=0.006, depth=0.022, location=(x, 0.233, zz), rotation=(math.radians(90), 0, 0))
            bpy.context.object.data.materials.append(bake_m)
    # cord plugs standing on the shelf
    for k in range(8):
        x = cx - 0.5 + k * 0.14
        bpy.ops.mesh.primitive_cylinder_add(radius=0.014, depth=0.09, location=(x, -0.12, 0.935))
        bpy.context.object.data.materials.append(brass_m if k != 3 else cable_live)
    # 15-second dial on the crown
    bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=0.03, location=(cx, 0.22, 1.98), rotation=(math.radians(90), 0, 0))
    bpy.context.object.data.materials.append(dial_face)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.2, minor_radius=0.012, location=(cx, 0.205, 1.98), rotation=(math.radians(90), 0, 0))
    bpy.context.object.data.materials.append(brass_m)
    for t in range(15):
        a = math.radians(90 - t * 24)
        box(f"tick{t}", (0.014, 0.006, 0.04 if t % 5 else 0.06),
            (cx + 0.155 * math.cos(a), 0.196, 1.98 + 0.155 * math.sin(a)), tick_m, 0)
        bpy.context.object.rotation_euler = (0, -a + math.radians(90), 0)
    text("N.P.C.I.", (cx, 0.18, 1.62), 0.09, label_m)
    text("SWITCH", (cx, 0.18, 1.53), 0.045, label_dim)


switchboard(0.0)


# ---------- patch cables: bezier tubes from the board to each rack ----------
def cable(name, pts, m, r=0.012):
    cu = bpy.data.curves.new(name, "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = r; cu.bevel_resolution = 4
    sp = cu.splines.new("BEZIER"); sp.bezier_points.add(len(pts) - 1)
    for bp, p in zip(sp.bezier_points, pts):
        bp.co = p; bp.handle_left_type = bp.handle_right_type = "AUTO"
    o = bpy.data.objects.new(name, cu); sc.collection.objects.link(o); o.data.materials.append(m)
    return o


cable("call_out", [(-0.07, -0.12, 0.98), (0.4, -0.5, 0.35), (1.3, -0.6, 0.06), (1.9, -0.55, 0.3), (2.2, -0.52, 1.2)], cable_live)
cable("debit_done", [(-0.21, -0.12, 0.98), (-0.8, -0.5, 0.3), (-1.6, -0.6, 0.06), (-2.0, -0.55, 0.4), (-2.2, -0.52, 1.0)], cable_dead)

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
