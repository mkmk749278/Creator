"""H3 · Matsya 6000, the vehicle (plan §7; ILLUSTRATION in the film, labels from Remotion).

  .venv-blender/bin/python scripts/blender/matsya_vehicle.py --shot NAME --out DIR --frames a-b --step 2

Drawn from ISRO's video (about 1:12, the frame on the crane) and PIB's wet-test photos (Kattupalli, Feb 2025): a cream
open frame about three ball-widths long, the ball at the front, ducted thrusters at the back, skids, lights and an arm
at the front, steel drop weights underneath, yellow syntactic-foam blocks over the top and sides. Proportions are
measured off those photos; no published drawing gives exact sizes, so it stays ILLUSTRATION.

Frame 0 is the given time in vo/timing.json (60 fps; audio r2); word frames are noted in each pose.
  weights  (0-539)  124.90 s  "And if something goes wrong down there? The crew can drop heavy weights, and the sub rises"
  assemble (0-779)  313.10 s  "This ball is only part of the sub. Around it go batteries, lights ... wrapped in a special foam."
  seabed   (0-959)  362.65 s  "Six thousand metres down ... Your lights are the only lights ... black lumps of metal"
  descent  (0-539)  444.35 s  "This story isn't over. When Matsya makes its first deep dive, we'll be there."
"""
import math
import os
import random
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matsya_hero as H  # noqa: E402

FPS = 60
BALL_C = Vector((0.0, -2.55, 1.55))     # the ball's centre, vehicle frame (front is -Y, up is +Z, skids at z=0)
FY0, FY1 = -1.75, 4.2                   # the frame's length behind the ball
FX = 1.05                               # half width
FZ0, FZ1 = 0.32, 2.75                   # frame bottom and top
CREAM = (0.62, 0.58, 0.48)
LAMP = 1400.0                           # watts per lamp in the scattering water
FOAM = (0.86, 0.64, 0.04)


def box(name, loc, size, m, parent=None, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    b = bpy.context.object
    b.name = name
    b.scale = size
    b.data.materials.append(m)
    if bevel:
        md = b.modifiers.new("bev", "BEVEL")
        md.width = bevel
        md.segments = 2
    if parent:
        b.parent = parent
    return b


def tube(name, a, b, r, m, parent=None, verts=12):
    a, b = Vector(a), Vector(b)
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=(b - a).length, vertices=verts, location=(a + b) / 2)
    c = bpy.context.object
    c.name = name
    c.rotation_euler = (b - a).to_track_quat("Z", "Y").to_euler()
    c.data.materials.append(m)
    if parent:
        c.parent = parent
    return c


def build_vehicle(lights_on=True):
    """returns a dict of parts, all parented to an empty 'matsya' at the skids' centre"""
    root = bpy.data.objects.new("matsya", None)
    bpy.context.collection.objects.link(root)
    frame_m = H.mat("frame", CREAM, 0.55, metal=0.1)
    H.noise_bump(frame_m, 8, 0.12)
    dark = H.mat("housing", (0.05, 0.05, 0.055), 0.45, metal=0.7)
    alu = H.mat("alu", (0.5, 0.5, 0.52), 0.35, metal=1.0)
    orange = H.mat("battery", (0.75, 0.22, 0.04), 0.5)
    steel = H.mat("weight", (0.55, 0.55, 0.57), 0.4, metal=0.9)
    foam_m = H.mat("foam", FOAM, 0.62)
    H.noise_bump(foam_m, 60, 0.15)
    parts = dict(frame=[], boxes=[], batteries=[], thrusters=[], lights=[], lamps=[], arm=[], foam=[], weights=[],
                 lamphouse=[])
    grp = bpy.data.objects.new("framegrp", None)
    bpy.context.collection.objects.link(grp)
    grp.parent = root
    s = 0.12
    # longerons, the four corners
    for x in (-FX, FX):
        for z in (FZ0, FZ1):
            parts["frame"].append(box("lon", (x, (FY0 + FY1) / 2, z), (s, FY1 - FY0, s), frame_m, grp))
    # posts and cross members every metre or so
    ys = [FY0 + (FY1 - FY0) * i / 5 for i in range(6)]
    for y in ys:
        for x in (-FX, FX):
            parts["frame"].append(box("post", (x, y, (FZ0 + FZ1) / 2), (s, s, FZ1 - FZ0), frame_m, grp))
        for z in (FZ0, FZ1):
            parts["frame"].append(box("cross", (0, y, z), (2 * FX, s, s), frame_m, grp))
    # side gussets toward the ball, with lightening holes (the curved plates in ISRO's photo)
    for x in (-FX, FX):
        g = box("gusset", (x, FY0 + 0.35, 1.1), (0.04, 1.1, 1.3), frame_m, grp)
        parts["frame"].append(g)
        for zz in (0.85, 1.4):
            bpy.ops.mesh.primitive_cylinder_add(radius=0.16, depth=0.3, vertices=32, location=(x, FY0 + 0.35, zz),
                                                rotation=(0, math.pi / 2, 0))
            cut = bpy.context.object
            H.bool_cut(g, cut)
            bpy.data.objects.remove(cut)
    # the cradle under the ball
    for x in (-0.55, 0.55):
        parts["frame"].append(box("cradle", (x, BALL_C.y + 0.2, 0.55), (0.1, 1.6, 0.1), frame_m, grp))
        parts["frame"].append(tube("cradleleg", (x, BALL_C.y, 0.32), (x * 0.6, BALL_C.y, BALL_C.z - 1.0), 0.05,
                                   frame_m, grp))
    # skids
    for x in (-0.8, 0.8):
        parts["frame"].append(tube("skid", (x, BALL_C.y - 0.5, 0.06), (x, FY1 + 0.2, 0.06), 0.07, frame_m, grp, 16))
        for y in (BALL_C.y, 0.5, 3.6):
            parts["frame"].append(tube("skidleg", (x, y, 0.06), (x * 1.2, y, FZ0), 0.04, frame_m, grp))
    # equipment inside: pressure housings, boxes, the orange battery packs low down
    rnd = random.Random(4)
    for i in range(8):
        y = FY0 + 0.6 + i * 0.68
        parts["boxes"].append(box("unit", (rnd.uniform(-0.4, 0.4), y, rnd.uniform(1.5, 2.3)),
                                  (rnd.uniform(0.4, 0.8), rnd.uniform(0.35, 0.55), rnd.uniform(0.3, 0.5)),
                                  alu if i % 2 else dark, root, 0.02))
    for i in range(6):
        y = FY0 + 0.9 + i * 0.85
        for x in (-0.5, 0.5):
            parts["batteries"].append(box("battery", (x, y, 0.62), (0.75, 0.7, 0.42), orange, root, 0.03))
    # thrusters: four ducted ones at the back, pointing aft, two vertical on top
    for x in (-0.95, 0.95):
        for z in (0.95, 2.1):
            parts["thrusters"].append(thruster((x * 1.05, FY1 + 0.25, z), (0, 1, 0), dark, alu, root))
    for y in (0.2, 3.0):
        parts["thrusters"].append(thruster((0, y, FZ1 + 0.25), (0, 0, 1), dark, alu, root, r=0.24))
    # lights: lamp heads on short arms round the ball, aimed forward and down
    for k, (x, z) in enumerate(((-1.0, 2.55), (1.0, 2.55), (-1.1, 0.75), (1.1, 0.75))):
        p = Vector((x, BALL_C.y - 0.2, z))
        parts["frame"].append(tube("lamparm", p + Vector((0, 0.6, 0)), p, 0.035, frame_m, grp))
        bpy.ops.mesh.primitive_cylinder_add(radius=0.09, depth=0.2, vertices=24, location=p,
                                            rotation=(math.pi / 2, 0, 0))
        lamp = bpy.context.object
        lamp.data.materials.append(dark)
        lamp.parent = root
        parts["lamphouse"].append(lamp)
        bpy.ops.mesh.primitive_circle_add(radius=0.075, fill_type="NGON", location=p + Vector((0, -0.101, 0)),
                                          rotation=(math.pi / 2, 0, 0))
        face = bpy.context.object
        face.data.materials.append(H.glow_mat(f"lampface{k}", (1.0, 0.95, 0.85), 30.0))
        face.parent = root
        parts["lamps"].append(face)
        bpy.ops.object.light_add(type="SPOT", location=p + Vector((0, -0.12, 0)))
        sl = bpy.context.object
        sl.data.energy = LAMP if lights_on else 0
        sl.data.spot_size = math.radians(55)
        sl.data.spot_blend = 0.5
        sl.data.shadow_soft_size = 0.06
        sl.data.color = (1.0, 0.95, 0.88)
        aim = p + Vector((x * 0.6, -6.0, -2.5 - (z - 1.5)))
        sl.rotation_euler = (aim - sl.location).to_track_quat("-Z", "Y").to_euler()
        sl.parent = root
        parts["lights"].append(sl)
    # the arm, folded under the ball
    a0 = Vector((0.6, BALL_C.y + 0.4, 0.45))
    a1 = a0 + Vector((0.1, -0.9, 0.15))
    a2 = a1 + Vector((-0.2, -0.5, -0.25))
    for p, q in ((a0, a1), (a1, a2)):
        parts["arm"].append(tube("arm", p, q, 0.06, alu, root, 16))
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.08, location=a1)
    parts["arm"].append(bpy.context.object)
    bpy.context.object.data.materials.append(dark)
    bpy.context.object.parent = root
    # drop weights: two steel blocks hung under the frame
    for y in (-0.6, 2.6):
        w = box("weight", (0, y, 0.2), (1.0, 0.6, 0.3), steel, root, 0.015)
        parts["weights"].append(w)
    # foam: yellow blocks over the top and down the sides (PIB wet-test photo)
    rnd = random.Random(7)
    for i in range(7):
        for j in range(3):
            y = FY0 + 0.45 + i * 0.84
            x = (j - 1) * 0.72
            fb = box("foam", (x, y, FZ1 + 0.3), (0.68, 0.78, 0.48 + rnd.uniform(-0.04, 0.06)), foam_m, root, 0.03)
            parts["foam"].append(fb)
    for i in range(6):
        for x in (-1, 1):
            y = FY0 + 0.75 + i * 0.9
            fb = box("foam", (x * (FX + 0.3), y, 1.85), (0.42, 0.85, 0.75), foam_m, root, 0.03)
            parts["foam"].append(fb)
    for fb in parts["foam"]:
        fb["home"] = tuple(fb.location)
    # the ball, painted, with its windows
    b = H.build_ball("painted", glass=H.glass_mat("acrylic"))
    b["root"].parent = root
    b["root"].location = BALL_C
    H.set_seams(b, 0, 0)
    # a warm glow inside the ball, seen through the windows
    bpy.ops.object.light_add(type="POINT", location=BALL_C)
    il = bpy.context.object
    il.data.energy = 25
    il.data.color = (1.0, 0.85, 0.65)
    il.parent = root
    for k in ("frame", "boxes", "batteries", "arm", "foam", "weights"):
        for ob in parts[k]:
            ob["home"] = tuple(ob.location)
    return dict(root=root, grp=grp, ball=b, inner=il, **parts)


def thruster(p, axis, dark, alu, parent, r=0.3):
    bpy.ops.mesh.primitive_torus_add(major_radius=r, minor_radius=0.05, major_segments=48, minor_segments=12,
                                     location=p)
    duct = bpy.context.object
    duct.scale = (1, 1, 2.6)
    duct.rotation_euler = Vector(axis).to_track_quat("Z", "Y").to_euler()
    duct.data.materials.append(dark)
    duct.parent = parent
    bpy.ops.mesh.primitive_cylinder_add(radius=r * 0.3, depth=0.3, vertices=24, location=p)
    hub = bpy.context.object
    hub.rotation_euler = duct.rotation_euler
    hub.data.materials.append(alu)
    hub.parent = parent
    duct["hub"] = hub.name
    return duct


def water(sc, density=0.012, glow=(0.0, 0.0, 0.0)):
    """deep water: a scattering volume (so the lamps cut beams) and a black backdrop"""
    vol = bpy.data.materials.new("water")
    vol.use_nodes = True
    vn = vol.node_tree
    vn.nodes.remove(vn.nodes["Principled BSDF"])
    pv = vn.nodes.new("ShaderNodeVolumePrincipled")
    pv.inputs["Color"].default_value = (0.55, 0.8, 0.9, 1)
    pv.inputs["Density"].default_value = density
    pv.inputs["Anisotropy"].default_value = 0.55
    pv.inputs["Absorption Color"].default_value = (0.25, 0.6, 0.75, 1)
    vn.links.new(pv.outputs["Volume"], vn.nodes["Material Output"].inputs["Volume"])
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -4, 2))
    v = bpy.context.object
    v.scale = (40, 40, 30)
    v.data.materials.append(vol)
    sc.cycles.volume_step_rate = 4
    sc.cycles.volume_max_steps = 64
    sc.world.node_tree.nodes["Background"].inputs["Color"].default_value = (*glow, 1)
    fill = H.area((-9, -10, 9), (0, -2, 1.5), 8.0, 900, (0.45, 0.62, 0.9))
    v["fill"] = fill.name
    return v


def seabed(extent=40, n=2600, seed=3):
    """sediment with polymetallic nodules: dark, knobbly lumps a few centimetres to ten across, half buried"""
    sed = H.mat("sediment", (0.22, 0.2, 0.17), 0.95)
    H.noise_bump(sed, 3, 0.4)
    bpy.ops.mesh.primitive_plane_add(size=extent * 2, location=(0, 0, 0))
    floor = bpy.context.object
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.subdivide(number_cuts=60)
    bpy.ops.object.mode_set(mode="OBJECT")
    tex = bpy.data.textures.new("dunes", "CLOUDS")
    tex.noise_scale = 4.0
    d = floor.modifiers.new("disp", "DISPLACE")
    d.texture = tex
    d.strength = 0.25
    floor.data.materials.append(sed)
    bpy.ops.object.shade_smooth()
    nod = H.mat("nodule", (0.025, 0.022, 0.02), 0.55, metal=0.2)
    H.noise_bump(nod, 40, 0.6)
    rnd = random.Random(seed)
    verts, faces = [], []
    base_v, base_f = icosphere()
    for i in range(n):
        x, y = rnd.uniform(-14, 14), rnd.uniform(-22, 8)
        r = 0.025 + rnd.random() ** 2 * 0.08
        sx, sy, sz = r * rnd.uniform(0.8, 1.3), r * rnd.uniform(0.8, 1.3), r * rnd.uniform(0.5, 0.8)
        k = len(verts)
        for vx, vy, vz in base_v:
            j = 1 + 0.18 * math.sin(vx * 7 + i) * math.cos(vy * 5 + i * 0.3)
            verts.append((x + vx * sx * j, y + vy * sy * j, 0.02 + vz * sz * j))
        faces.extend(tuple(k + q for q in f) for f in base_f)
    nods = H.link("nodules", verts, faces, nod)
    return floor, nods


def icosphere():
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1)
    o = bpy.context.object
    v = [tuple(p.co) for p in o.data.vertices]
    f = [tuple(p.vertices) for p in o.data.polygons]
    bpy.data.objects.remove(o)
    return v, f


def lights_level(o, k):
    for sl in o["lights"]:
        sl.data.energy = LAMP * k
    for face in o["lamps"]:
        em = face.data.materials[0].node_tree.nodes["Emission"]
        em.inputs["Strength"].default_value = 30 * k


# ---------------------------------------------------------------- shots
def build_weights(a):
    sc, cam = H.setup(a, exposure=0.3, world=(0, 0, 0))
    o = build_vehicle()
    water(sc)
    seabed()
    snow = H.Snow(n=500, box=(14, 14, 8), center=(0, -4, 3), size=0.008)
    o["snow"] = snow
    return sc, cam, o


def pose_weights(f, cam, o):
    # word frames: wrong 68, drop 180, heavy 195, weights 214, rises 286, up 323, air 433, ninety-six 461; end 522
    o["snow"].pose(f)
    t = f / FPS
    rise = 0.5 * 0.35 * max(0.0, (f - 250) / FPS) ** 2 if f > 250 else 0.0
    rise = min(rise, 0.9 * max(0.0, (f - 250) / FPS))
    hover = 2.6 + 0.05 * math.sin(t * 0.9)
    o["root"].location = (0, 0, hover + rise)
    o["root"].rotation_euler = (math.radians(1.5 * math.sin(t * 0.6)), 0, math.radians(-8))
    rot = o["root"].rotation_euler.to_matrix()
    for w in o["weights"]:
        w.parent = None
        w.rotation_euler = o["root"].rotation_euler
        # held under the frame until "drop"; the frame's position at that moment is where it falls from
        fh = min(f, 180)
        held = Vector((0, 0, 2.6 + 0.05 * math.sin(fh / FPS * 0.9))) + rot @ Vector(w["home"])
        if f < 180:
            w.location = Vector(o["root"].location) + rot @ Vector(w["home"])
        else:
            dt = (f - 180) / FPS   # slowed by the water
            drop = min(0.5 * 2.2 * dt * dt, held.z - 0.16)
            w.location = held - Vector((0, 0, drop))
    cam_loc = H.keys(f, [(0, (-9.5, -8.0, 1.2)), (200, (-7.6, -6.6, 0.9)), (330, (-7.4, -6.4, 0.9)),
                         (539, (-8.6, -7.0, 2.6))])
    aim = H.keys(f, [(0, (0, 0.2, 2.6)), (200, (0, 0.6, 1.5)), (330, (0, 0.6, 1.8)), (539, (0, 0.6, 4.0))])
    H.aim_cam(cam, cam_loc, aim, 24)


def build_assemble(a):
    sc, cam = H.setup(a, exposure=0.2, world=(0, 0, 0))
    o = build_vehicle()
    H.deep_water(sc, glow=(0.008, 0.04, 0.08))
    o["snow"] = H.Snow(n=600, box=(14, 14, 10), center=(0, -2, 0), size=0.008)
    H.area((-5, -6, 9), (0, 0, 1.5), 5.0, 2600, (0.6, 0.78, 1.0))
    H.area((6, 4, 0), (0, 0, 1.5), 5.0, 600, (0.35, 0.5, 0.8))
    return sc, cam, o


def fly(ob, k, offset):
    hx, hy, hz = ob["home"]
    ob.location = (hx + offset[0] * (1 - k), hy + offset[1] * (1 - k), hz + offset[2] * (1 - k))
    s = max(0.001, k ** 0.5)
    ob.hide_render = k <= 0.001


def pose_assemble(f, cam, o):
    # word frames: ball 18, sub 107, Around 147, batteries 206, lights 250, motors 281, arms 330, together 416,
    # sinks 515, stone 555, wrapped 627, foam 706, glass bubbles 876-899; end 779
    o["snow"].pose(f)
    rnd = random.Random(1)
    kf = H.ramp(f, 147, 200)
    for ob in o["frame"]:
        r = rnd.random()
        fly(ob, H.ramp(f, 147 + r * 30, 190 + r * 30), (0, 3.0, 2.5))
    for ob in o["boxes"]:
        r = rnd.random()
        fly(ob, H.ramp(f, 180 + r * 25, 215 + r * 25), (0, 0, 3.0))
    for i, ob in enumerate(o["batteries"]):
        fly(ob, H.ramp(f, 200 + i * 4, 235 + i * 4), (2.5 * (1 if ob["home"][0] > 0 else -1), 0, 0))
    lights_level(o, H.ramp(f, 250, 262))
    for i, ob in enumerate(o["thrusters"]):
        ob.hide_render = f < 281 + i * 3
        bpy.data.objects[ob["hub"]].hide_render = ob.hide_render
    for ob in o["lamphouse"] + o["lamps"]:
        ob.hide_render = f < 246
    for ob in o["arm"]:
        fly(ob, H.ramp(f, 326, 360), (0, -1.0, 0))
    for ob in o["weights"]:
        fly(ob, H.ramp(f, 360, 400), (0, 0, -1.5))
    o["grp"].hide_render = False
    # "the whole thing sinks like a stone": it drops, fast; then the foam arrives and it slows to a hover
    k_foam = H.ramp(f, 627, 700)
    for i, ob in enumerate(o["foam"]):
        r = (i * 0.37) % 1
        fly(ob, H.ramp(f, 627 + r * 40, 670 + r * 40), (0, 0, 4.0 + r * 2))
    sink = 0.0
    if f > 470:
        tt = min(f, 640) - 470
        sink = 0.5 * 0.0012 * tt * tt
        if f > 640:
            sink += (0.0012 * 170) * (f - 640) * (1 - 0.5 * H.ramp(f, 640, 760)) * (1 - k_foam)
    o["root"].location = (0, 0, -sink)
    o["root"].rotation_euler = (0, 0, math.radians(-20))
    cam_loc = H.keys(f, [(0, (-3.2, -7.4, 2.0)), (140, (-4.6, -9.0, 2.6)), (420, (-7.0, -7.0, 3.2)),
                         (779, (-6.4, -6.6, 2.6))])
    aim = H.keys(f, [(0, tuple(BALL_C)), (140, (0, -1.5, 1.6)), (420, (0, 0.5, 1.5)), (779, (0, 0.5, 1.5))])
    cam_loc = (cam_loc[0], cam_loc[1], cam_loc[2] - sink * 0.85)
    aim = (aim[0], aim[1], aim[2] - sink * 0.92)
    H.aim_cam(cam, cam_loc, aim, H.keys(f, [(0, 40), (420, 28), (779, 28)]))


def build_seabed(a):
    sc, cam = H.setup(a, exposure=0.4, world=(0, 0, 0))
    o = build_vehicle(lights_on=False)
    o["fill"] = bpy.data.objects[water(sc)["fill"]]
    seabed()
    o["snow"] = H.Snow(n=600, box=(12, 14, 6), center=(0, -6, 2.0), size=0.007)
    return sc, cam, o


def pose_seabed(f, cam, o):
    # word frames: no sunlight 136-188, Your lights 237-255, only lights 309-327, kilometres 381, Outside 453,
    # window 491, freezing 612, seafloor 701, black lumps 785-805, stones 888; end 917
    o["snow"].pose(f)
    t = f / FPS
    # the four lamps come on one after another at "Your lights"
    for i, (sl, face) in enumerate(zip(o["lights"], o["lamps"])):
        k = H.ramp(f, 255 + i * 12, 262 + i * 12)
        sl.data.energy = LAMP * k
        face.data.materials[0].node_tree.nodes["Emission"].inputs["Strength"].default_value = 30 * k
    o["inner"].data.energy = 25 * H.ramp(f, 240, 300)
    o["fill"].data.energy = 40 + 860 * H.ramp(f, 250, 330)
    o["root"].location = (0, 2.0 - t * 0.25, 2.2 + 0.04 * math.sin(t * 0.8))
    o["root"].rotation_euler = (math.radians(4), 0, 0)
    r = o["root"].location
    # in the dark the camera sits off the bow; at "Outside your window" it is close on the viewport; at
    # "the seafloor" it drops and looks ahead along the lit nodules
    win = Vector(r) + BALL_C + Vector((0, -H.RO, -0.06))
    rv = Vector(r)
    # offsets are in the vehicle's frame (skids at z 0, the ball's front window at y -3.68, z 1.49): for "Outside
    # your window" the camera stays in front of the ball (an earlier path ran under it and through the frame)
    off = H.keys(f, [(0, (-3.2, -7.0, 0.8)), (380, (-2.8, -5.8, 0.4)), (453, (-0.9, -5.4, 1.6)),
                     (640, (-0.5, -5.0, 1.5)), (720, (-0.7, -4.6, -0.6)), (917, (-0.5, -5.2, -0.9))])
    cam_loc = rv + Vector(off)
    aim = H.keys(f, [(0, tuple(rv + Vector((0, -1, 1.5)))), (453, tuple(win)), (640, tuple(win)),
                     (720, tuple(rv + Vector((0, -10, -2.1)))), (917, tuple(rv + Vector((0.3, -11, -2.2))))])
    H.aim_cam(cam, tuple(cam_loc), aim, H.keys(f, [(0, 28), (453, 40), (640, 40), (720, 26), (917, 26)]))


def build_descent(a):
    sc, cam = H.setup(a, exposure=0.4, world=(0, 0, 0))
    o = build_vehicle()
    water(sc)
    o["snow"] = H.Snow(n=700, box=(14, 14, 16), center=(0, -2, -4), size=0.008)
    return sc, cam, o


def pose_descent(f, cam, o):
    # word frames: Matsya 123, first deep dive 179-215, we'll be there 249-268, Subscribe 302; end 455
    o["snow"].pose(f)
    t = f / FPS
    o["root"].location = (0, 0, 4.0 - t * 0.9)
    o["root"].rotation_euler = (math.radians(-6), 0, math.radians(25 + t * 2))
    z = o["root"].location.z
    H.aim_cam(cam, (-6.5, -9.0, -6.0), (0, -1.0, z + 1.2), H.keys(f, [(0, 28), (539, 32)]))


SHOTS = {"weights": (build_weights, pose_weights), "assemble": (build_assemble, pose_assemble),
         "seabed": (build_seabed, pose_seabed), "descent": (build_descent, pose_descent)}


def main():
    a = H.args()
    build, pose = SHOTS[a.shot]
    sc, cam, o = build(a)
    f0, f1 = map(int, a.frames.split("-"))
    os.makedirs(a.out, exist_ok=True)
    for f in range(f0, f1 + 1, a.step):
        pose(f, cam, o)
        bpy.context.view_layer.update()
        sc.render.filepath = os.path.join(os.path.abspath(a.out), f"{a.shot}_{f:04d}.png")
        bpy.ops.render.render(write_still=True)
        print(f"frame {a.shot} {f}", flush=True)


if __name__ == "__main__":
    main()
