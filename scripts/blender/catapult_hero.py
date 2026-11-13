"""Hero shots for carrier-catapult (projects/carrier-catapult/word_map.md; every shot is labelled ILLUSTRATION,
the catapult and cutaways also SIMPLIFIED).

  .venv-blender/bin/python scripts/blender/catapult_hero.py --shot NAME --out DIR --frames a-b --step 2 [--w --h]

H1 (Vikrant's deck, ramp, the flat-to-ramp morph, the hull cutaway) was tried here on 2026-11-13 and dropped: the
     Navy's own footage shows the deck better, and the morph and cutaway read clearer as Remotion drawings.
H3 · the energy store (General Atomics' motor generator: over 36 tonnes, 80,000 lb; no count is said).
  store    (0-959)  S120-125: a motor generator in cutaway on the steel inspection plate, others in shadow behind;
                            the rotor spins up (0-420), its copper glows with stored energy; at 600 the energy is
                            pulled out in three seconds (600-780: the rotor slows, the glow runs out along the bus).
H4 · 1961: the steam catapult and the boiler drum (SIMPLIFIED; the IWM photos are design reference only).
  catapult (0-599)  S50:    a cutaway under the 1961 deck: the cylinder, the piston, the slot; steam (amber) fires the
                            piston down the tube (150-330) and the shuttle drags the jet above.
  drum     (0-959)  S52-56, S70-72: the water drum on its saddles; cracks glow one by one (60-300); steel bands
                            come down and ratchet tight, one after another (420, 560, 700).
  room     (0-599)  S73-75: close on the one gauge; the needle swings towards red (150-260) and holds; the camera
                            pulls back through the almost empty boiler room.
Deterministic: fixed seed, no simulation; every motion is a function of the frame. Labels come from Remotion.
"""
import argparse
import math
import os
import random
import sys

import bpy
from mathutils import Vector

FPS = 60


def args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shot", default="store")
    ap.add_argument("--out", required=True)
    ap.add_argument("--frames", default="0-0")
    ap.add_argument("--step", type=int, default=2)
    ap.add_argument("--w", type=int, default=1920)
    ap.add_argument("--h", type=int, default=1080)
    ap.add_argument("--samples", type=int, default=24)
    ap.add_argument("--bounces", type=int, default=8)
    ap.add_argument("--threads", type=int, default=0)
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    return ap.parse_args(argv)


# ---------------------------------------------------------------- helpers
def smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def keys(f, ks):
    if f <= ks[0][0]:
        return ks[0][1]
    for (f0, v0), (f1, v1) in zip(ks, ks[1:]):
        if f <= f1:
            t = smooth((f - f0) / (f1 - f0))
            if isinstance(v0, tuple):
                return tuple(a + (b - a) * t for a, b in zip(v0, v1))
            return v0 + (v1 - v0) * t
    return ks[-1][1]


def mat(name, color, rough, metal=0.0, emit=None, strength=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = (*color, 1)
    p.inputs["Roughness"].default_value = rough
    p.inputs["Metallic"].default_value = metal
    if emit:
        p.inputs["Emission Color"].default_value = (*emit, 1)
        p.inputs["Emission Strength"].default_value = strength
    return m


def set_emit(m, strength):
    m.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = strength


def noise_bump(m, scale, strength, detail=8):
    nt = m.node_tree
    n = nt.nodes.new("ShaderNodeTexNoise")
    n.inputs["Scale"].default_value = scale
    n.inputs["Detail"].default_value = detail
    b = nt.nodes.new("ShaderNodeBump")
    b.inputs["Strength"].default_value = strength
    nt.links.new(n.outputs["Fac"], b.inputs["Height"])
    nt.links.new(b.outputs["Normal"], nt.nodes["Principled BSDF"].inputs["Normal"])


def brushed_steel(name="steel", tint=(0.36, 0.37, 0.39), rough=0.38, stretch=60):
    m = mat(name, tint, rough, metal=1.0)
    nt = m.node_tree
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (1, stretch, 1)
    n = nt.nodes.new("ShaderNodeTexNoise")
    n.inputs["Scale"].default_value = 30
    n.inputs["Detail"].default_value = 10
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], n.inputs["Vector"])
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs["To Min"].default_value = rough - 0.12
    mr.inputs["To Max"].default_value = rough + 0.12
    nt.links.new(n.outputs["Fac"], mr.inputs["Value"])
    nt.links.new(mr.outputs["Result"], nt.nodes["Principled BSDF"].inputs["Roughness"])
    return m


def plate_steel(name, cell):
    """The steel inspection plate: brushed steel with engraved grid lines every `cell` metres."""
    m = brushed_steel(name, (0.13, 0.135, 0.14), 0.5)
    nt = m.node_tree
    tc = nt.nodes.new("ShaderNodeTexCoord")
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.inputs["Scale"].default_value = 1.0 / cell
    br.inputs["Mortar Size"].default_value = 0.004
    br.offset = 0.0
    br.squash = 1.0
    br.inputs["Color1"].default_value = (1, 1, 1, 1)
    br.inputs["Color2"].default_value = (1, 1, 1, 1)
    br.inputs["Mortar"].default_value = (0, 0, 0, 1)
    nt.links.new(tc.outputs["Object"], br.inputs["Vector"])
    b = nt.nodes.new("ShaderNodeBump")
    b.inputs["Strength"].default_value = 0.6
    nt.links.new(br.outputs["Fac"], b.inputs["Height"])
    nt.links.new(b.outputs["Normal"], nt.nodes["Principled BSDF"].inputs["Normal"])
    return m


def setup(a, exposure=0.0, world=(0.004, 0.005, 0.007)):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = a.samples
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.use_denoising = True
    sc.cycles.denoiser = "OPENIMAGEDENOISE"
    sc.cycles.max_bounces = a.bounces
    sc.cycles.seed = 5
    sc.render.resolution_x, sc.render.resolution_y = a.w, a.h
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_depth = "16"
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "AgX - Medium High Contrast"
    sc.view_settings.exposure = exposure
    if a.threads:
        sc.render.threads_mode = "FIXED"
        sc.render.threads = a.threads
    w = bpy.data.worlds.new("w")
    sc.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs["Color"].default_value = (*world, 1)
    bpy.ops.object.camera_add()
    cam = bpy.context.object
    cam.data.clip_end = 5000
    sc.camera = cam
    return sc, cam


def area(loc, aim, size, energy, color):
    bpy.ops.object.light_add(type="AREA", location=loc)
    l = bpy.context.object
    l.data.size = size
    l.data.energy = energy
    l.data.color = color
    l.rotation_euler = (Vector(aim) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    return l


def aim_cam(cam, loc, aim, lens, fstop=None):
    cam.location = loc
    cam.rotation_euler = (Vector(aim) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = lens
    if fstop:
        cam.data.dof.use_dof = True
        cam.data.dof.aperture_fstop = fstop
        cam.data.dof.focus_distance = (Vector(aim) - Vector(loc)).length
    else:
        cam.data.dof.use_dof = False


def box(name, loc, size, m, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.scale = size
    o.data.materials.append(m)
    return o


def cyl(name, loc, r, depth, m, rot=(0, 0, 0), verts=64):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc, rotation=rot, vertices=verts)
    o = bpy.context.object
    o.name = name
    o.data.materials.append(m)
    return o


def render(sc, a, build_frame):
    lo, hi = map(int, a.frames.split("-"))
    os.makedirs(a.out, exist_ok=True)
    for f in range(lo, hi + 1, a.step):
        build_frame(f)
        sc.frame_set(f)
        sc.render.filepath = os.path.join(a.out, f"{a.shot}_{f:04d}.png")
        bpy.ops.render.render(write_still=True)
        print(f"frame {f}", flush=True)


# ---------------------------------------------------------------- H3 · the energy store
def motor_generator(name, loc, cut, steel, dark, copper_m, glow_m):
    """GA's EMALS motor generator, simplified: a long cylindrical housing on a skid; in cutaway, the rotor (a stack
    of discs with permanent magnets round the rim) inside the stator's copper windings."""
    x0, y0, z0 = loc
    grp = {"rotor": []}
    box(f"{name}_skid", (x0, y0, z0 + 0.15), (4.6, 2.4, 0.3), dark)
    for dx in (-1.6, 1.6):
        box(f"{name}_saddle{dx}", (x0 + dx, y0, z0 + 0.55), (0.35, 2.0, 0.6), dark)
    h = cyl(f"{name}_housing", (x0, y0, z0 + 1.45), 1.15, 3.9, steel, rot=(0, math.pi / 2, 0), verts=96)
    inner = cyl(f"{name}_inner", (x0, y0, z0 + 1.45), 1.05, 3.7, dark, rot=(0, math.pi / 2, 0), verts=96)
    for o in (h,):
        sol = o.modifiers.new("shell", "SOLIDIFY")
        sol.thickness = 0.06
    if cut:
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x0 + 0.2, y0 - 0.9, z0 + 2.3))
        cutter = bpy.context.object
        cutter.scale = (3.4, 1.9, 1.9)
        cutter.hide_render = True
        cutter.display_type = "WIRE"
        for o in (h, inner):
            b = o.modifiers.new("cut", "BOOLEAN")
            b.object = cutter
            b.operation = "DIFFERENCE"
        # the stator: copper windings round the inside of the housing
        for k in range(9):
            bpy.ops.mesh.primitive_torus_add(major_radius=0.98, minor_radius=0.06, location=(x0 - 1.4 + k * 0.35, y0, z0 + 1.45),
                                             rotation=(0, math.pi / 2, 0), major_segments=96, minor_segments=12)
            t = bpy.context.object
            t.name = f"{name}_wind{k}"
            t.data.materials.append(copper_m)
            b = t.modifiers.new("cut", "BOOLEAN")
            b.object = cutter
            b.operation = "DIFFERENCE"
    # the rotor: a shaft and a stack of discs with magnets round the rim (so the spin reads)
    shaft = cyl(f"{name}_shaft", (x0, y0, z0 + 1.45), 0.12, 4.6, steel, rot=(0, math.pi / 2, 0), verts=32)
    bpy.ops.object.empty_add(location=(x0, y0, z0 + 1.45))
    pivot = bpy.context.object
    pivot.name = f"{name}_pivot"
    for k in range(6):
        d = cyl(f"{name}_disc{k}", (x0 - 1.25 + k * 0.5, y0, z0 + 1.45), 0.82, 0.32, steel, rot=(0, math.pi / 2, 0), verts=96)
        d.parent = pivot
        d.matrix_parent_inverse = pivot.matrix_world.inverted()
        bpy.ops.mesh.primitive_torus_add(major_radius=0.84, minor_radius=0.05, location=(x0 - 1.25 + k * 0.5, y0, z0 + 1.45),
                                         rotation=(0, math.pi / 2, 0), major_segments=96, minor_segments=12)
        ring = bpy.context.object
        ring.name = f"{name}_ring{k}"
        ring.data.materials.append(copper_m)
        ring.parent = pivot
        ring.matrix_parent_inverse = pivot.matrix_world.inverted()
        for j in range(24):
            t = j / 24 * math.tau
            mg = box(f"{name}_mag{k}_{j}", (x0 - 1.25 + k * 0.5, y0 + 0.78 * math.cos(t), z0 + 1.45 + 0.78 * math.sin(t)),
                     (0.3, 0.11, 0.07), glow_m if j % 6 == 0 else dark, rot=(t, 0, 0))
            mg.parent = pivot
            mg.matrix_parent_inverse = pivot.matrix_world.inverted()
    grp["pivot"] = pivot
    return grp


def build_store(a):
    sc, cam = setup(a, exposure=-0.4)
    bpy.ops.mesh.primitive_plane_add(size=60)
    bpy.context.object.data.materials.append(plate_steel("plate", 2.0))
    steel = brushed_steel("hsteel", (0.42, 0.43, 0.45), 0.3)
    dark = mat("dark", (0.05, 0.05, 0.055), 0.5, metal=0.6)
    copper = mat("copper", (0.72, 0.36, 0.16), 0.28, metal=1.0, emit=(1.0, 0.45, 0.12), strength=0.0)
    glow = mat("magglow", (0.8, 0.5, 0.2), 0.3, metal=0.5, emit=(1.0, 0.6, 0.2), strength=0.0)
    hero = motor_generator("mg0", (0, 0, 0), True, steel, dark, copper, glow)
    others = [motor_generator(f"mg{k}", (-1.0 + 6.0 * k, 7.5, 0), False, steel, dark, copper, glow) for k in (1, 2)]
    # the bus: a heavy cable from the hero machine out of frame, towards the deck; a pulse runs along it at launch
    bus_m = mat("bus", (0.08, 0.08, 0.09), 0.5, emit=(1.0, 0.7, 0.2), strength=0.0)
    cyl("bus", (4.5, -0.0, 0.25), 0.16, 9, bus_m, rot=(0, math.pi / 2, 0), verts=24)
    key = area((-5, -7, 7), (0, 0, 1.4), 6, 1400, (1.0, 0.86, 0.68))
    area((6, -5, 3), (0, 0, 1.4), 4, 700, (0.75, 0.82, 1.0))
    area((0, 12, 6), (0, 0, 1.4), 8, 900, (1.0, 0.8, 0.6))

    # speed profile (rev per second of the drawn rotor; the real one turns far faster): spin up, hold, give it back
    def speed(f):
        up = smooth(f / 420)
        out = 0.55 * smooth((f - 600) / 180)
        back = 0.55 * smooth((f - 820) / 140)
        return 1.6 * up * (1 - out + back)

    def angle(f):
        s, step = 0.0, 1
        for k in range(0, int(f), step):
            s += speed(k) / FPS
        return s * math.tau

    def frame(f):
        hero["pivot"].rotation_euler = (angle(f), 0, 0)
        for o in others:
            o["pivot"].rotation_euler = (angle(f) * 0.97 + 1.0, 0, 0)
        e = speed(f) / 1.6
        set_emit(copper, 3.5 * e)
        set_emit(glow, 9.0 * e)
        pulse = smooth((f - 600) / 30) * (1 - smooth((f - 700) / 80))
        set_emit(bus_m, 14 * pulse)
        x = keys(f, [(0, -6.0), (959, -3.2)])
        aim_cam(cam, (x, -6.4 + 0.0012 * f, 2.9 - 0.0006 * f), (0.3, 0, 1.45), 35, fstop=4.0)

    render(sc, a, frame)


# ---------------------------------------------------------------- H4 · 1961
def jet_silhouette(name, m, scale=1.0):
    """a simple straight-winged jet of the Sea Hawk's period (no markings): fuselage, wings, tail"""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, segments=32, ring_count=16)
    fus = bpy.context.object
    fus.name = name
    fus.scale = (6.0 * scale, 0.7 * scale, 0.75 * scale)
    fus.data.materials.append(m)
    parts = [box(f"{name}_wing", (0.3 * scale, 0, 0), (2.6 * scale, 11.8 * scale, 0.18 * scale), m),
             box(f"{name}_tail", (-5.0 * scale, 0, 0.4 * scale), (1.4 * scale, 4.4 * scale, 0.14 * scale), m),
             box(f"{name}_fin", (-5.0 * scale, 0, 1.4 * scale), (1.6 * scale, 0.14 * scale, 2.0 * scale), m)]
    for p in parts:
        p.parent = fus
        p.matrix_parent_inverse = fus.matrix_world.inverted()
    return fus


def build_catapult(a):
    sc, cam = setup(a, exposure=-0.5)
    bpy.ops.mesh.primitive_plane_add(size=80)
    bpy.context.object.data.materials.append(plate_steel("plate", 1.0))
    deckm = mat("deck61", (0.18, 0.19, 0.2), 0.75)
    noise_bump(deckm, 300, 0.2)
    cutface = mat("cut61", (0.55, 0.38, 0.18), 0.6, emit=(1.0, 0.6, 0.25), strength=0.25)
    steel = brushed_steel("cylsteel", (0.5, 0.5, 0.52), 0.28)
    brass = mat("brass", (0.75, 0.55, 0.25), 0.3, metal=1.0)
    steam = mat("steam", (1.0, 0.7, 0.35), 0.5, emit=(1.0, 0.62, 0.25), strength=0.0)
    LEN = 24.0
    # a slab of the 1961 deck, cut open along the slot: the deck plate, the slot, the trough below
    box("deckEdge", (LEN / 2, -0.95, 3.0), (LEN + 4, 0.2, 0.35), cutface)
    box("deckR", (LEN / 2, 3.2, 3.0), (LEN + 4, 5.6, 0.35), deckm)
    box("trough", (LEN / 2, 0, 1.4), (LEN + 4, 1.6, 0.12), cutface)
    box("wallR", (LEN / 2, 0.85, 2.2), (LEN + 4, 0.1, 1.6), cutface)
    # the cylinder, cut open on top so the piston shows, and the steam behind the piston
    tube = cyl("tube", (LEN / 2, 0, 2.0), 0.42, LEN, steel, rot=(0, math.pi / 2, 0), verts=64)
    sol = tube.modifiers.new("shell", "SOLIDIFY")
    sol.thickness = 0.05
    bpy.ops.mesh.primitive_cube_add(size=1, location=(LEN / 2, 0.0, 2.45))
    cutter = bpy.context.object
    cutter.scale = (LEN + 2, 1.2, 0.55)
    cutter.hide_render = True
    b = tube.modifiers.new("cut", "BOOLEAN")
    b.object = cutter
    b.operation = "DIFFERENCE"
    piston = cyl("piston", (1.0, 0, 2.0), 0.39, 1.2, brass, rot=(0, math.pi / 2, 0), verts=48)
    shuttle = box("shuttle", (1.0, 0, 2.95), (1.4, 0.18, 0.95), brass)
    shuttle.parent = piston
    shuttle.matrix_parent_inverse = piston.matrix_world.inverted()
    plume = cyl("plume", (0.5, 0, 2.0), 0.38, 1.0, steam, rot=(0, math.pi / 2, 0), verts=48)
    jetm = mat("jet", (0.2, 0.22, 0.24), 0.5, metal=0.3)
    jet = jet_silhouette("jet", jetm, 0.3)
    area((LEN / 2, -10, 10), (LEN / 2, 0, 2), 10, 1400, (1.0, 0.85, 0.65))
    area((LEN / 2 + 8, 8, 6), (LEN / 2, 0, 2), 6, 900, (0.7, 0.8, 1.0))

    def frame(f):
        t = smooth((f - 150) / 180)
        x = 1.0 + (LEN - 3.0) * (t ** 1.6)
        piston.location.x = x
        plume.scale.z = max(0.05, (x - 0.4))
        plume.location.x = 0.4 + (x - 0.4) / 2 - 0.6
        set_emit(steam, 7.0 * smooth((f - 130) / 25) * (1 - 0.6 * smooth((f - 360) / 120)))
        jet.location = (x + 1.6, 0, 3.9)
        cx = keys(f, [(0, 2.0), (150, 4.0), (330, LEN - 4.0), (599, LEN - 2.0)])
        aim_cam(cam, (cx - 4.5, -6.2, 5.6), (cx + 1.5, 0, 2.3), 30)

    render(sc, a, frame)


def crack_curve(name, m, pts, r=0.012):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = r
    sp = cu.splines.new("POLY")
    sp.points.add(len(pts) - 1)
    for p, c in zip(sp.points, pts):
        p.co = (*c, 1)
    o = bpy.data.objects.new(name, cu)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(m)
    return o


def build_drum(a):
    sc, cam = setup(a, exposure=-0.5)
    bpy.ops.mesh.primitive_plane_add(size=40)
    bpy.context.object.data.materials.append(plate_steel("plate", 0.5))
    iron = brushed_steel("drumsteel", (0.16, 0.15, 0.14), 0.5, stretch=40)
    noise_bump(iron, 25, 0.02)
    dark = mat("dark", (0.05, 0.05, 0.05), 0.6, metal=0.5)
    R, LEN = 0.75, 4.0
    drum = cyl("drum", (0, 0, 1.6), R, LEN, iron, rot=(0, math.pi / 2, 0), verts=96)
    for s in (-1, 1):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=R, segments=64, ring_count=32, location=(s * LEN / 2, 0, 1.6))
        e = bpy.context.object
        e.scale = (0.45, 1, 1)
        e.data.materials.append(iron)
        box(f"saddle{s}", (s * 1.3, 0, 0.55), (0.4, 1.4, 1.1), dark)
    # rivet seams
    rivet = mat("rivet", (0.12, 0.11, 0.1), 0.5, metal=1.0)
    for sx in (-1.0, 0.0, 1.0):
        for j in range(40):
            t = j / 40 * math.tau
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.022, segments=8, ring_count=6,
                                                 location=(sx, R * math.cos(t), 1.6 + R * math.sin(t)))
            bpy.context.object.data.materials.append(rivet)
    # the cracks: thin glowing lines on the drum's front face, each appearing in turn
    crack_m = [mat(f"crack{k}", (0.1, 0.05, 0.02), 0.5, emit=(1.0, 0.35, 0.08), strength=0.0) for k in range(7)]
    random.seed(4)
    cracks = []
    for k in range(7):
        x = -1.5 + k * 0.48 + random.uniform(-0.1, 0.1)
        t = math.radians(random.uniform(-25, 30))
        pts = []
        xx, tt = x, t
        for s in range(15):
            tt += 0.035 + random.uniform(-0.015, 0.015)
            xx += random.uniform(-0.018, 0.018)
            pts.append((xx, -(R + 0.004) * math.cos(tt), 1.6 + (R + 0.004) * math.sin(tt)))
        cracks.append(crack_curve(f"crack{k}", crack_m[k], pts, r=0.005))
    # three steel bands, each a ring that comes down and ratchets tight
    band_m = brushed_steel("band", (0.42, 0.43, 0.45), 0.3, stretch=60)
    bands = []
    for k, bx in enumerate((-1.1, 0.0, 1.1)):
        bpy.ops.mesh.primitive_cylinder_add(radius=R + 0.035, depth=0.16, location=(bx, 0, 1.6), rotation=(0, math.pi / 2, 0),
                                            vertices=96)
        b = bpy.context.object
        b.name = f"band{k}"
        sol = b.modifiers.new("shell", "SOLIDIFY")
        sol.thickness = 0.03
        b.data.materials.append(band_m)
        bpy.ops.mesh.primitive_cylinder_add(radius=R + 0.035, depth=0.2, location=(bx, 0, 1.6), rotation=(0, math.pi / 2, 0))
        hole = bpy.context.object
        hole.hide_render = True
        hole.display_type = "WIRE"
        # make it a ring: remove the caps by a boolean with a slightly smaller cylinder
        bpy.ops.mesh.primitive_cylinder_add(radius=R + 0.005, depth=0.4, location=(bx, 0, 1.6), rotation=(0, math.pi / 2, 0),
                                            vertices=96)
        inner = bpy.context.object
        inner.hide_render = True
        inner.display_type = "WIRE"
        bo = b.modifiers.new("ring", "BOOLEAN")
        bo.object = inner
        bo.operation = "DIFFERENCE"
        bpy.data.objects.remove(hole, do_unlink=True)
        inner.parent = b
        inner.matrix_parent_inverse = b.matrix_world.inverted()
        clamp = box(f"clamp{k}", (bx, 0, 1.6 + R + 0.07), (0.2, 0.2, 0.09), dark)
        clamp.parent = b
        clamp.matrix_parent_inverse = b.matrix_world.inverted()
        bands.append(b)
    area((-3, -5, 5), (0, 0, 1.6), 5, 700, (1.0, 0.82, 0.6))
    area((4, -3, 2.5), (0, 0, 1.6), 3, 350, (0.7, 0.8, 1.0))
    area((0, 5, 4), (0, 0, 1.6), 6, 500, (1.0, 0.75, 0.5))
    starts = (420, 560, 700)

    def frame(f):
        for k, c in enumerate(cracks):
            set_emit(crack_m[k], 9.0 * smooth((f - 60 - 34 * k) / 20) * (1 - 0.75 * smooth((f - starts[0] + 40) / 60)))
        for k, b in enumerate(bands):
            s0 = starts[k]
            drop = 1 - smooth((f - s0) / 60)
            # ratchet: three clicks of tightening after it lands
            tight = sum(smooth((f - s0 - 60 - 18 * c) / 6) for c in range(3)) / 3
            sc_ = 1.25 - 0.25 * tight
            b.location.z = 1.6 + 2.6 * drop
            b.scale = (1, sc_, sc_)
        x = keys(f, [(0, -1.8), (400, -0.6), (959, 0.4)])
        aim_cam(cam, (x, -4.6, 2.5), (x * 0.5, 0, 1.55), 38, fstop=5.6)

    render(sc, a, frame)


def build_room(a):
    sc, cam = setup(a, exposure=0.0)
    wall = mat("wall", (0.30, 0.28, 0.25), 0.8, metal=0.2)
    noise_bump(wall, 8, 0.3)
    floor = plate_steel("floor", 0.6)
    pipe = brushed_steel("pipe", (0.3, 0.28, 0.26), 0.45)
    # the boiler room: floor grating, walls, the boiler's front, pipes overhead, one bulb
    bpy.ops.mesh.primitive_plane_add(size=1)
    fl = bpy.context.object
    fl.scale = (14, 10, 1)
    fl.data.materials.append(floor)
    box("back", (0, 5, 3), (14, 0.2, 6), wall)
    box("left", (-7, 0, 3), (0.2, 10, 6), wall)
    box("right", (7, 0, 3), (0.2, 10, 6), wall)
    box("ceiling", (0, 0, 6), (14, 10, 0.2), wall)
    box("boiler", (0, 3.6, 2.4), (6, 2.4, 4.8), mat("boilerface", (0.22, 0.2, 0.18), 0.55, metal=0.5))
    for k in range(5):
        cyl(f"pipe{k}", (0, -3 + k * 1.6, 5.4 - 0.15 * k), 0.14, 14, pipe, rot=(0, math.pi / 2, 0), verts=24)
    cyl("riser", (-2.2, 3.0, 3.0), 0.18, 6, pipe, verts=24)
    cyl("riser2", (2.6, 3.0, 3.0), 0.12, 6, pipe, verts=24)
    # the gauge on the boiler front: brass bezel, white face, red sector, black needle
    brass = mat("gbrass", (0.78, 0.58, 0.28), 0.25, metal=1.0)
    face = mat("gface", (0.85, 0.83, 0.78), 0.5)
    redm = mat("gred", (0.75, 0.06, 0.04), 0.5)
    blk = mat("gblack", (0.02, 0.02, 0.02), 0.4)
    gx, gy, gz = 0.9, 2.36, 2.1
    cyl("bezel", (gx, gy, gz), 0.34, 0.08, brass, rot=(math.pi / 2, 0, 0))
    cyl("face", (gx, gy - 0.045, gz), 0.3, 0.02, face, rot=(math.pi / 2, 0, 0))
    for k in range(13):
        t = math.radians(225 - k * 22.5)
        box(f"tick{k}", (gx + 0.26 * math.cos(t), gy - 0.06, gz + 0.26 * math.sin(t)), (0.05, 0.004, 0.012), blk,
            rot=(0, -t, 0))
    for k in range(10):
        t = math.radians(-20 - k * 5)
        box(f"red{k}", (gx + 0.24 * math.cos(t), gy - 0.058, gz + 0.24 * math.sin(t)), (0.06, 0.004, 0.035), redm,
            rot=(0, -t, 0))
    bpy.ops.object.empty_add(location=(gx, gy - 0.07, gz))
    hub = bpy.context.object
    needle = box("needle", (gx + 0.11, gy - 0.07, gz), (0.24, 0.006, 0.02), blk)
    needle.parent = hub
    needle.matrix_parent_inverse = hub.matrix_world.inverted()
    # one bulb, warm, and a cold fill from the hatch above
    bpy.ops.object.light_add(type="POINT", location=(0.4, 0.6, 4.6))
    bulb = bpy.context.object
    bulb.data.energy = 1100
    bulb.data.color = (1.0, 0.72, 0.42)
    bulb.data.shadow_soft_size = 0.08
    cyl("bulbglass", (0.4, 0.6, 4.6), 0.06, 0.12, mat("bulbm", (1, 0.8, 0.5), 0.2, emit=(1, 0.75, 0.45), strength=30))
    area((-4, -3, 5.8), (0, 2, 1), 3, 600, (0.6, 0.72, 1.0))
    area((3, -4, 2), (0.9, 2.3, 2.1), 1.5, 120, (1.0, 0.8, 0.6))

    def frame(f):
        # the needle: from normal towards the red, a tremble, then it holds
        ang = keys(f, [(0, 120.0), (150, 110.0), (260, -40.0), (599, -42.0)])
        ang += 1.2 * math.sin(f * 0.9) * smooth((f - 200) / 40) * (1 - smooth((f - 330) / 60))
        hub.rotation_euler = (0, -math.radians(ang), 0)
        pull = smooth((f - 300) / 299)
        loc = keys(f, [(0, (gx, gy - 1.1, gz)), (300, (gx, gy - 1.25, gz)), (599, (-3.6, -4.4, 2.6))])
        aim = keys(f, [(0, (gx, gy, gz)), (300, (gx, gy, gz)), (599, (0.6, 3.0, 2.0))])
        aim_cam(cam, loc, aim, keys(f, [(0, 50.0), (599, 24.0)]))
        cam.data.dof.use_dof = pull < 0.5
        if pull < 0.5:
            cam.data.dof.aperture_fstop = 2.8
            cam.data.dof.focus_distance = (Vector(aim) - Vector(loc)).length

    render(sc, a, frame)


def main():
    a = args()
    if a.shot == "store":
        build_store(a)
    elif a.shot == "catapult":
        build_catapult(a)
    elif a.shot == "drum":
        build_drum(a)
    elif a.shot == "room":
        build_room(a)
    else:
        sys.exit(f"unknown shot {a.shot}")


if __name__ == "__main__":
    main()
