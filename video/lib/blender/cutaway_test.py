# Test frame: a cut-away pneumatic valve in the dark blueprint look, rendered with Cycles on CPU (PLAYBOOK §4a-9).
# Run: <venv with bpy==5.2.2>/bin/python -I cutaway_test.py -- <samples> <out.png>
# Measured 2026-10-20 on a 4 vCPU session VM, 1920x1080: 32 samples 68.5 s; 8 samples + reduced bounces 27.3 s,
# visually the same after OpenImageDenoise.
import bpy, math, sys, time

samples = int(sys.argv[-2]); out = sys.argv[-1]
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

def hexcol(h, a=1.0):
    h = h.lstrip("#"); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    return [((x / 12.92) if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4) for x in c] + [a]

def mat(name, col, metal=0.0, rough=0.4, emit=None, strength=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = hexcol(col)
    b.inputs["Metallic"].default_value = metal; b.inputs["Roughness"].default_value = rough
    if emit:
        b.inputs["Emission Color"].default_value = hexcol(emit); b.inputs["Emission Strength"].default_value = strength
    return m

steel = mat("steel", "#9aa4ae", 1.0, 0.28)
cast = mat("cast", "#5a6470", 0.8, 0.45)
cut = mat("cutface", "#f0883e", 0.0, 0.6, "#f0883e", 0.6)
air = mat("air", "#d29922", 0.0, 0.3, "#d29922", 3.0)
rubber = mat("rubber", "#1a1d22", 0.0, 0.7)

# valve body: hollow cylinder, front half cut away
bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=1.0, depth=2.4); body = bpy.context.object
bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=0.78, depth=2.6); bore = bpy.context.object
m = body.modifiers.new("bore", "BOOLEAN"); m.object = bore; m.operation = "DIFFERENCE"
bpy.ops.mesh.primitive_cube_add(size=3); cutter = bpy.context.object; cutter.location = (0, -1.5, 0)
m = body.modifiers.new("cut", "BOOLEAN"); m.object = cutter; m.operation = "DIFFERENCE"
bore.hide_render = cutter.hide_render = True; bore.hide_viewport = cutter.hide_viewport = True
body.data.materials.append(cast); body.data.materials.append(cut)
bpy.context.view_layer.objects.active = body
bpy.ops.object.modifier_apply(modifier="bore"); bpy.ops.object.modifier_apply(modifier="cut")
for p in body.data.polygons:  # faces on the cut plane get the orange cut-face material
    if abs(p.normal.y + 1) < 1e-3 and abs(p.center.y) < 1e-3: p.material_index = 1
bpy.ops.object.shade_auto_smooth()

# pressurised chamber (glowing amber) below the diaphragm
bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=0.77, depth=0.9, location=(0, 0, -0.7)); ch = bpy.context.object
ch.data.materials.append(air)
bpy.ops.mesh.primitive_cube_add(size=3, location=(0, -1.5, -0.7)); c2 = bpy.context.object
m = ch.modifiers.new("cut", "BOOLEAN"); m.object = c2; m.operation = "DIFFERENCE"; c2.hide_render = c2.hide_viewport = True

# diaphragm + hollow stem
bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=0.77, depth=0.08, location=(0, 0, -0.2)); d = bpy.context.object
d.data.materials.append(rubber)
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.14, depth=1.6, location=(0, 0, 0.6)); st = bpy.context.object
st.data.materials.append(steel); bpy.ops.object.shade_smooth()

# spring: helix curve with bevel
cu = bpy.data.curves.new("spring", "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = 0.035; cu.bevel_resolution = 6
sp = cu.splines.new("POLY"); n = 400; sp.points.add(n - 1)
for i in range(n):
    t = i / (n - 1) * 7 * 2 * math.pi
    sp.points[i].co = (0.45 * math.cos(t), 0.45 * math.sin(t), -0.12 + 1.1 * i / (n - 1), 1)
spr = bpy.data.objects.new("spring", cu); sc.collection.objects.link(spr); cu.materials.append(steel)

# blueprint floor with grid
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, -1.2)); fl = bpy.context.object
fm = bpy.data.materials.new("floor"); fm.use_nodes = True; nt = fm.node_tree; b = nt.nodes["Principled BSDF"]
tc = nt.nodes.new("ShaderNodeTexCoord"); br = nt.nodes.new("ShaderNodeTexBrick")
br.inputs["Scale"].default_value = 20; br.inputs["Mortar Size"].default_value = 0.01; br.offset = 0; br.squash = 1
br.inputs["Color1"].default_value = hexcol("#0d1117"); br.inputs["Color2"].default_value = hexcol("#0d1117")
br.inputs["Mortar"].default_value = hexcol("#30363d")
nt.links.new(tc.outputs["Object"], br.inputs["Vector"]); nt.links.new(br.outputs["Color"], b.inputs["Base Color"])
b.inputs["Roughness"].default_value = 0.35; fl.data.materials.append(fm)

# lights: cool key, warm rim, dark world
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Color"].default_value = hexcol("#0d1117"); w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.4
for loc, col, e, size in [((4, -5, 5), "#cfe3ff", 900, 3), ((-4, 3, 3), "#58a6ff", 600, 2), ((3, 4, -0.5), "#ffcf8a", 250, 1.5)]:
    L = bpy.data.lights.new("l", "AREA"); L.energy = e; L.size = size; L.color = hexcol(col)[:3]
    o = bpy.data.objects.new("l", L); o.location = loc; sc.collection.objects.link(o)
    o.rotation_euler = (0, 0, 0); c = o.constraints.new("TRACK_TO"); c.target = body; c.track_axis = "TRACK_NEGATIVE_Z"

cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam
cam.location = (3.2, -4.6, 1.6); cam.data.lens = 45
c = cam.constraints.new("TRACK_TO"); c.target = body; c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"

sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = samples
sc.cycles.use_denoising = True; sc.cycles.denoiser = "OPENIMAGEDENOISE"
sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Medium High Contrast"
sc.cycles.max_bounces = 4; sc.cycles.glossy_bounces = 2; sc.cycles.transmission_bounces = 0; sc.cycles.diffuse_bounces = 1
sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.05
sc.render.filepath = out
t = time.time(); bpy.ops.render.render(write_still=True); print(f"RENDER_SECONDS {time.time()-t:.1f}")
