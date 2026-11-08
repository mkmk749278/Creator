"""H3 and H4 · hero shots for aip-submarines (word_map.md; ILLUSTRATION in the film).

  .venv-blender/bin/python scripts/blender/aip_hero.py --shot powder|drydock --out DIR --frames a-b --step 2 [--w --h]

  powder  (0-599)  "Instead, it carries a dry white powder. Sodium borohydride. Add water, and the powder gives off
                   hydrogen.": a heap of white powder on a steel inspection plate, macro; a drop of water falls and
                   lands at frame 300; bubbles rise from the wet patch after it. (Sodium borohydride is a white
                   crystalline powder; the reaction with water gives off hydrogen gas, claim C04.)
  drydock (0-959)  "You open the submarine like a book … It slides into the gap, and the two parts are joined around
                   it.": a Kalvari-type hull on keel blocks in a covered dock; a cut line glows at the middle (0-60),
                   the aft half rolls back on rails (60-250), the new section rolls in from the side (330-700), slides
                   into the gap (700-830), the seams glow as they are welded (840-959). The hull's shape matches the
                   film's Three.js and SVG boat (67.5 m, 6.2 m beam); the plug is about ten metres (claim C09).
  thumb    (still) the YouTube thumbnail hero (owner asked for the package, 2026-11-08): the same dry-dock boat
                   held at the moment the film's words describe ("the hull is cut in two ... slides into the gap"):
                   the halves apart, both cut edges glowing, the new section sliding in from the side. --view a|b|c
                   picks the camera. Lit brighter than the film shot so it reads at phone size.
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
    ap.add_argument("--shot", default="powder")
    ap.add_argument("--out", required=True)
    ap.add_argument("--frames", default="0-0")
    ap.add_argument("--step", type=int, default=2)
    ap.add_argument("--w", type=int, default=1920)
    ap.add_argument("--h", type=int, default=1080)
    ap.add_argument("--samples", type=int, default=24)
    ap.add_argument("--bounces", type=int, default=6)
    ap.add_argument("--threads", type=int, default=0)
    ap.add_argument("--view", default="a")
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    return ap.parse_args(argv)


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


def mat(name, color, rough, metal=0.0, emit=None, strength=0.0, sss=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = (*color, 1)
    p.inputs["Roughness"].default_value = rough
    p.inputs["Metallic"].default_value = metal
    if sss:
        p.inputs["Subsurface Weight"].default_value = sss
        p.inputs["Subsurface Radius"].default_value = (0.2, 0.2, 0.2)
    if emit:
        p.inputs["Emission Color"].default_value = (*emit, 1)
        p.inputs["Emission Strength"].default_value = strength
    return m


def noise_bump(m, scale, strength, detail=8):
    nt = m.node_tree
    n = nt.nodes.new("ShaderNodeTexNoise")
    n.inputs["Scale"].default_value = scale
    n.inputs["Detail"].default_value = detail
    b = nt.nodes.new("ShaderNodeBump")
    b.inputs["Strength"].default_value = strength
    nt.links.new(n.outputs["Fac"], b.inputs["Height"])
    nt.links.new(b.outputs["Normal"], nt.nodes["Principled BSDF"].inputs["Normal"])
    return n


def brushed_steel(name="steel", tint=(0.36, 0.37, 0.39), rough=0.38):
    m = mat(name, tint, rough, metal=1.0)
    nt = m.node_tree
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (1, 60, 1)
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


def setup(a, exposure=0.0):
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
    w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.004, 0.005, 0.007, 1)
    bpy.ops.object.camera_add()
    cam = bpy.context.object
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


# ---------------------------------------------------------------- H3 powder
def build_powder(a):
    sc, cam = setup(a, exposure=-0.7)
    # the steel inspection plate (the film's one physical base), with engraved grid lines
    bpy.ops.mesh.primitive_plane_add(size=0.6)
    plate = bpy.context.object
    st = brushed_steel("plate", (0.30, 0.31, 0.33), 0.32)
    plate.data.materials.append(st)
    # the heap: a displaced disc, white and slightly translucent
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, segments=96, ring_count=48, location=(0, 0, 0))
    heap = bpy.context.object
    heap.scale = (1.0, 0.9, 0.62)
    tex = bpy.data.textures.new("grain", "CLOUDS")
    tex.noise_scale = 0.0012
    tex.noise_depth = 4
    d = heap.modifiers.new("disp", "DISPLACE")
    d.texture = tex
    d.strength = 0.005
    sub = heap.modifiers.new("sub", "SUBSURF")
    sub.levels = 1
    sub.render_levels = 2
    pw = mat("powder", (0.82, 0.82, 0.8), 0.9, sss=0.2)
    noise_bump(pw, 1400, 1.0, detail=6)
    heap.data.materials.append(pw)
    bpy.ops.object.shade_smooth()
    # loose grains around the heap
    random.seed(3)
    for i in range(110):
        r = 0.05 + random.random() * 0.05
        t = random.random() * math.tau
        bpy.ops.mesh.primitive_ico_sphere_add(radius=0.0003 + random.random() * 0.0005, subdivisions=1,
                                              location=(math.cos(t) * r, math.sin(t) * r * 0.9, 0.0005))
        bpy.context.object.data.materials.append(pw)
    # the water drop and the wet patch; bubbles
    water = mat("water", (0.8, 0.9, 1.0), 0.02)
    p = water.node_tree.nodes["Principled BSDF"]
    p.inputs["Transmission Weight"].default_value = 1.0
    p.inputs["IOR"].default_value = 1.333
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.006, segments=32, ring_count=16)
    drop = bpy.context.object
    drop.data.materials.append(water)
    bpy.ops.object.shade_smooth()
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.02, segments=48, ring_count=24, location=(0.004, -0.004, 0.019))
    wet = bpy.context.object
    wet.scale = (1, 1, 0.18)
    wetm = mat("wetpowder", (0.55, 0.6, 0.65), 0.08)
    wetm.node_tree.nodes["Principled BSDF"].inputs["Transmission Weight"].default_value = 0.5
    wet.data.materials.append(wetm)
    bpy.ops.object.shade_smooth()
    bubbles = []
    random.seed(9)
    for i in range(70):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, segments=16, ring_count=8)
        b = bpy.context.object
        b.data.materials.append(water)
        bpy.ops.object.shade_smooth()
        bubbles.append((b, random.random(), random.random() * math.tau, 0.3 + random.random() * 0.7, random.random()))
    # light: a cool overhead softbox, a warm rim, a low fill
    area((0.25, -0.2, 0.45), (0, 0, 0), 0.4, 30, (0.85, 0.92, 1.0))
    area((-0.3, 0.35, 0.12), (0, 0, 0.02), 0.25, 6, (1.0, 0.75, 0.45))
    area((0.0, -0.5, 0.05), (0, 0, 0.02), 0.6, 4, (0.6, 0.7, 0.85))
    return sc, cam, dict(drop=drop, wet=wet, bubbles=bubbles)


def pose_powder(f, cam, o):
    hit = 300
    t = (f - (hit - 40)) / 40  # falls over 40 frames
    drop = o["drop"]
    if f < hit - 40:
        drop.location = (0.004, -0.004, 0.2)
        drop.hide_render = True
    elif f < hit:
        drop.hide_render = False
        drop.location = (0.004, -0.004, 0.15 - 0.13 * t * t)
        drop.scale = (0.9, 0.9, 1.15)
    else:
        drop.hide_render = True
    s = smooth((f - hit) / 30)
    o["wet"].hide_render = f < hit
    o["wet"].scale = (0.2 + 0.8 * s, 0.2 + 0.8 * s, 0.18 * (0.3 + 0.7 * s))
    for b, ph, ang, spd, sz in o["bubbles"]:
        age = (f - hit - ph * 200) / (150 * spd)
        if f < hit or age < 0:
            b.hide_render = True
            continue
        age = age % 1.0
        b.hide_render = False
        r = 0.012 * (0.3 + sz)
        b.location = (0.004 + math.cos(ang) * r, -0.004 + math.sin(ang) * r, 0.02 + age * 0.06)
        k = (0.0006 + 0.0014 * sz) * (0.5 + age)
        b.scale = (k, k, k)
    loc = keys(f, [(0, (0.0, -0.42, 0.2)), (300, (0.03, -0.3, 0.14)), (600, (0.04, -0.24, 0.11))])
    aim = keys(f, [(0, (0, 0, 0.012)), (300, (0.004, -0.004, 0.02)), (600, (0.004, -0.004, 0.03))])
    aim_cam(cam, loc, aim, keys(f, [(0, 60), (600, 75)]), fstop=4)


# ---------------------------------------------------------------- H4 dry dock
HULL_LEN = 67.5
R = 3.1


def radius(x):
    bow, stern = 9, 20
    if x > HULL_LEN - bow:
        u = (HULL_LEN - x) / bow
        return R * math.sqrt(max(0.0, 1 - (1 - u) ** 2))
    if x < stern:
        u = x / stern
        return 0.35 + (R - 0.35) * math.sin(u * math.pi / 2) ** 1.35
    return R


def hull_piece(x0, x1, name, m, n=60, seg=64):
    """a body of revolution between x0 and x1 (metres from the stern tip), capped, axis along +x"""
    verts, faces = [], []
    xs = [x0 + (x1 - x0) * i / n for i in range(n + 1)]
    for x in xs:
        r = max(0.02, radius(x))
        for j in range(seg):
            a = j / seg * math.tau
            verts.append((x, r * math.cos(a), r * math.sin(a)))
    for i in range(n):
        for j in range(seg):
            a, b = i * seg + j, i * seg + (j + 1) % seg
            faces.append((a, b, b + seg, a + seg))
    for end, i0 in ((0, 0), (1, n * seg)):
        c = len(verts)
        verts.append((xs[0] if end == 0 else xs[-1], 0, 0))
        for j in range(seg):
            a, b = i0 + j, i0 + (j + 1) % seg
            faces.append((c, b, a) if end == 0 else (c, a, b))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    ob.data.materials.append(m)
    for p in me.polygons:
        p.use_smooth = True
    return ob


def build_drydock(a):
    sc, cam = setup(a, exposure=-0.6)
    hullm = mat("hull", (0.035, 0.038, 0.042), 0.6, metal=0.2)
    noise_bump(hullm, 3, 0.08)
    cutx = 33.0  # the cut, metres from the stern tip
    aft = hull_piece(0.2, cutx, "aft", hullm)
    fwd = hull_piece(cutx, HULL_LEN, "fwd", hullm)
    # the fin on the forward part
    bpy.ops.mesh.primitive_cube_add(size=1, location=(HULL_LEN - 26 + 4.75, 0, R + 1.8))
    fin = bpy.context.object
    fin.scale = (9.5, 1.4, 4.6)
    fin.modifiers.new("b", "BEVEL").width = 0.05
    fin.data.materials.append(hullm)
    fin.parent = fwd
    # stern planes on the aft part
    for i in range(4):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(2.6, 0, 0))
        p = bpy.context.object
        p.scale = (2.6, 0.16, 7.4)
        p.rotation_euler = (i * math.pi / 2 + math.pi / 4 * 0, 0, 0)
        p.data.materials.append(hullm)
        p.parent = aft
    # the new section: same diameter, ten metres, lighter primer grey with amber bands where it will be welded
    plugm = mat("plug", (0.18, 0.19, 0.2), 0.5, metal=0.3)
    bpy.ops.mesh.primitive_cylinder_add(radius=R, depth=10.0, vertices=64, rotation=(0, math.pi / 2, 0))
    plug = bpy.context.object
    plug.data.materials.append(plugm)
    bpy.ops.object.shade_smooth()
    # glowing seams (cut line, then weld lines)
    glow = mat("glow", (0, 0, 0), 1, emit=(1.0, 0.45, 0.12), strength=0)
    rings = []
    for k in range(3):
        bpy.ops.mesh.primitive_torus_add(major_radius=R + 0.03, minor_radius=0.07, major_segments=96, minor_segments=8,
                                         rotation=(0, math.pi / 2, 0))
        t = bpy.context.object
        t.data.materials.append(glow)
        rings.append(t)
    # the dock: concrete floor, rails, keel blocks, side walls, roof lights, haze
    conc = mat("concrete", (0.07, 0.068, 0.066), 0.9)
    noise_bump(conc, 2, 0.3)
    bpy.ops.mesh.primitive_plane_add(size=400, location=(30, 0, -R - 1.4))
    bpy.context.object.data.materials.append(conc)
    railm = mat("rail", (0.25, 0.25, 0.26), 0.35, metal=1.0)
    for y in (-1.6, 1.6):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(30, y, -R - 1.3))
        r = bpy.context.object
        r.scale = (140, 0.18, 0.2)
        r.data.materials.append(railm)
    blockm = mat("blocks", (0.22, 0.14, 0.07), 0.8)
    for x in range(-20, 90, 6):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, -R - 0.7))
        b = bpy.context.object
        b.scale = (1.2, 2.4, 1.2)
        b.data.materials.append(blockm)
    wallm = mat("wall", (0.07, 0.075, 0.08), 0.85)
    for y in (18,):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(30, y, 6))
        w = bpy.context.object
        w.scale = (200, 0.5, 22)
        w.data.materials.append(wallm)
    for x in range(-10, 90, 14):
        area((x, 0, 16), (x, 0, 0), 4, 2600, (1.0, 0.82, 0.6))
    area((60, -16, 4), (33, 0, 0), 8, 1800, (0.6, 0.75, 1.0))
    # haze
    vol = bpy.data.materials.new("haze")
    vol.use_nodes = True
    vn = vol.node_tree
    vn.nodes.remove(vn.nodes["Principled BSDF"])
    pv = vn.nodes.new("ShaderNodeVolumePrincipled")
    pv.inputs["Density"].default_value = 0.0015
    vn.links.new(pv.outputs["Volume"], vn.nodes["Material Output"].inputs["Volume"])
    bpy.ops.mesh.primitive_cube_add(size=1, location=(30, 0, 6))
    hz = bpy.context.object
    hz.scale = (200, 90, 26)
    hz.data.materials.append(vol)
    sc.cycles.volume_step_rate = 4
    return sc, cam, dict(aft=aft, fwd=fwd, plug=plug, rings=rings, glow=glow, cutx=cutx)


def pose_drydock(f, cam, o):
    cutx = o["cutx"]
    gap = keys(f, [(0, 0.0), (60, 0.0), (250, 12.0), (960, 12.0)])  # the aft half rolls back 12 m
    # the plug comes in from the side (y) into the 12 m gap; then the aft half closes the last 2 m on it
    py = keys(f, [(0, -22.0), (330, -22.0), (700, 0.0), (960, 0.0)])
    close = keys(f, [(700, 0.0), (830, 1.0)])
    o["aft"].location = (-gap + close * 2.0, 0, 0)
    o["plug"].location = (cutx - 5.0, py, 0)
    o["plug"].hide_render = f < 300
    # glow: the cut line (0-120), then the two weld seams (840-)
    cut_glow = keys(f, [(0, 0.0), (10, 8.0), (60, 12.0), (120, 0.0)])
    weld = keys(f, [(830, 0.0), (870, 14.0), (960, 9.0)])
    em = o["glow"].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
    r0, r1, r2 = o["rings"]
    r0.location = (cutx, 0, 0)
    r0.hide_render = f > 130
    r1.location = (cutx - 10.0 + 0.0, 0, 0)
    r2.location = (cutx, 0, 0)
    r1.hide_render = r2.hide_render = f < 830
    em.default_value = max(cut_glow, weld)
    loc = keys(f, [(0, (52, -30, 9)), (330, (40, -34, 12)), (700, (30, -30, 10)), (960, (26, -24, 7))])
    aim = keys(f, [(0, (30, 0, 0)), (330, (24, -6, 0)), (700, (26, 0, 0)), (960, (27, 0, 0))])
    aim_cam(cam, loc, aim, keys(f, [(0, 32), (960, 38)]), fstop=8)


THUMB_VIEWS = {
    # camera location, aim point, lens (mm)
    "a": ((44.0, -30.0, 2.0), (25.0, 0.0, 1.2), 30),
    "b": ((10.0, -30.0, 5.0), (26.0, 0.0, 0.8), 30),
    "c": ((30.0, -17.0, 9.0), (27.0, 0.0, 0.0), 26),
}


def pose_thumb(a, sc, cam, o):
    """the halves 12 m apart, both cut edges hot, the new section part-way in from the side"""
    cutx = o["cutx"]
    o["aft"].location = (-12.0, 0, 0)
    o["plug"].location = (cutx - 6.0, -4.5, 0)
    o["plug"].hide_render = False
    r0, r1, r2 = o["rings"]
    r0.location = (cutx, 0, 0)            # the cut edge on the forward half
    r1.location = (cutx - 12.0, 0, 0)     # the cut edge on the aft half
    r2.location = (cutx - 6.0 - 5.0, -4.5, 0)  # the new section's aft weld band
    for r in (r0, r1, r2):
        r.hide_render = False
    o["glow"].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 22.0
    # warm light spilling out of the gap, a cool rim from behind the boat, a soft key from above
    area((cutx - 6.0, -9.0, -1.0), (cutx - 6.0, 0, 0.5), 5, 2600, (1.0, 0.5, 0.18))
    area((cutx + 5, 14.0, 6.0), (cutx, 0, 0), 30, 9000, (0.45, 0.62, 1.0))
    area((cutx - 20, 12.0, 4.0), (cutx - 20, 0, 0), 30, 6000, (0.45, 0.62, 1.0))
    area((cutx, -12.0, 14.0), (cutx, 0, 0), 20, 5000, (1.0, 0.9, 0.8))
    sc.view_settings.exposure = 0.3
    loc, aim, lens = THUMB_VIEWS[a.view]
    aim_cam(cam, loc, aim, lens, fstop=11)


def main():
    a = args()
    if a.shot == "thumb":
        sc, cam, o = build_drydock(a)
        pose_thumb(a, sc, cam, o)
        os.makedirs(a.out, exist_ok=True)
        sc.render.filepath = os.path.join(os.path.abspath(a.out), f"thumb_{a.view}.png")
        bpy.ops.render.render(write_still=True)
        print(f"thumb {a.view}", flush=True)
        return
    if a.shot == "powder":
        sc, cam, o = build_powder(a)
        pose = pose_powder
    else:
        sc, cam, o = build_drydock(a)
        pose = pose_drydock
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
