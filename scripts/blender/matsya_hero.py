"""Hero shots for matsya-6000 (plan §7, §8a; ILLUSTRATION or SIMPLIFIED in the film, labels from Remotion).

  .venv-blender/bin/python scripts/blender/matsya_hero.py --shot NAME --out DIR --frames a-b --step 2 [--w --h]

The ball is drawn from ISRO's own drawing (Samudrayaan video, 23 Jul 2025, about 1:56; claim M18): five forged pieces
(top hatch, rings 1-3, bottom dome) joined by seven welds: four belts (W2 at the hatch, W7, W1 at the equator, W6) and
three round the viewports (W3 primary, W4 and W5 secondary). Outside diameter 2,260 mm, wall 80 mm (M01). The equator
seam is the 7.1 m one (OUR CALCULATION, pi x 2.26 m). Bare machined titanium for the making; painted grey with red
viewport rims (ISRO and PIB photos) for the finished ball.

Frame 0 of each shot is the first word of its passage in vo/timing.json (60 fps); word frames are noted in each pose.
  dive     (0-659)    0.00 s  "Six kilometres under the sea ... this titanium ball ... Imagine you're inside it ..."
  squeeze  (0-779)   69.68 s  "Now cover the whole ball with fingernails ... from every side at once."
  pieces   (0-959)  177.54 s  "Isro's drawing shows five pieces ... Three go round its windows."
  seam     (0-959)  233.93 s  "Then came the real thing ... about seven metres long ... thirty-two minutes, in one go."
  cutaway  (0-999)  266.91 s  "Now step inside with me ... just over two metres ... Lie down ... You and two others ..."
  dark     (0-719)  422.08 s  "Now, one last time, come back inside the ball with me." (lights off, the porthole)
Deterministic: fixed seed, no simulation; every motion is a function of the frame.
"""
import argparse
import math
import os
import random
import sys

import bpy
from mathutils import Vector

FPS = 60
RO = 1.13          # outside radius, m (2,260 mm diameter)
RI = RO - 0.08     # inside radius (80 mm wall)
# belt seams, as heights on the outside (fractions of RO), from ISRO's drawing
H_HATCH, H_W7, H_W1, H_W6 = 0.857, 0.468, 0.0, -0.44
AMBER = (0.82, 0.6, 0.13)          # bp_pressure
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shot", default="pieces")
    ap.add_argument("--out", required=True)
    ap.add_argument("--frames", default="0-0")
    ap.add_argument("--step", type=int, default=2)
    ap.add_argument("--w", type=int, default=1920)
    ap.add_argument("--h", type=int, default=1080)
    ap.add_argument("--samples", type=int, default=16)
    ap.add_argument("--bounces", type=int, default=6)
    ap.add_argument("--threads", type=int, default=0)
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    return ap.parse_args(argv)


# ---------------------------------------------------------------- easing and keys
def smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def ramp(f, f0, f1):
    return smooth((f - f0) / max(1e-6, f1 - f0))


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


# ---------------------------------------------------------------- materials
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


def noise_bump(m, scale, strength, detail=8, coord="Object"):
    nt = m.node_tree
    tc = nt.nodes.new("ShaderNodeTexCoord")
    n = nt.nodes.new("ShaderNodeTexNoise")
    n.inputs["Scale"].default_value = scale
    n.inputs["Detail"].default_value = detail
    nt.links.new(tc.outputs[coord], n.inputs["Vector"])
    b = nt.nodes.new("ShaderNodeBump")
    b.inputs["Strength"].default_value = strength
    nt.links.new(n.outputs["Fac"], b.inputs["Height"])
    nt.links.new(b.outputs["Normal"], nt.nodes["Principled BSDF"].inputs["Normal"])


def titanium(name="ti"):
    """bare machined Ti-6Al-4V: warm grey metal, fine lathe rings around the vertical axis"""
    m = mat(name, (0.56, 0.54, 0.51), 0.26, metal=1.0)
    nt = m.node_tree
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Object"], sep.inputs["Vector"])
    wave = nt.nodes.new("ShaderNodeTexWave")
    wave.wave_type = "RINGS"
    wave.rings_direction = "Z"
    wave.inputs["Scale"].default_value = 90
    wave.inputs["Distortion"].default_value = 0.5
    wave.inputs["Detail"].default_value = 3
    nt.links.new(tc.outputs["Object"], wave.inputs["Vector"])
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs["To Min"].default_value = 0.24
    mr.inputs["To Max"].default_value = 0.3
    nt.links.new(wave.outputs["Fac"], mr.inputs["Value"])
    nt.links.new(mr.outputs["Result"], nt.nodes["Principled BSDF"].inputs["Roughness"])
    b = nt.nodes.new("ShaderNodeBump")
    b.inputs["Strength"].default_value = 0.012
    nt.links.new(wave.outputs["Fac"], b.inputs["Height"])
    nt.links.new(b.outputs["Normal"], nt.nodes["Principled BSDF"].inputs["Normal"])
    return m


def painted(name="paint"):
    m = mat(name, (0.2, 0.21, 0.22), 0.42)
    noise_bump(m, 40, 0.05)
    return m


def plate_steel():
    """the film's steel inspection plate: brushed steel with an engraved half-metre grid"""
    m = mat("plate", (0.3, 0.31, 0.33), 0.34, metal=1.0)
    nt = m.node_tree
    p = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (1, 40, 1)
    n = nt.nodes.new("ShaderNodeTexNoise")
    n.inputs["Scale"].default_value = 6
    n.inputs["Detail"].default_value = 10
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], n.inputs["Vector"])
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs["To Min"].default_value = 0.24
    mr.inputs["To Max"].default_value = 0.44
    nt.links.new(n.outputs["Fac"], mr.inputs["Value"])
    nt.links.new(mr.outputs["Result"], p.inputs["Roughness"])
    # grid: distance to the nearest half-metre line in x or y
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Object"], sep.inputs["Vector"])

    def line(axis):
        a = nt.nodes.new("ShaderNodeMath")
        a.operation = "PINGPONG"
        a.inputs[1].default_value = 0.25
        nt.links.new(sep.outputs[axis], a.inputs[0])
        c = nt.nodes.new("ShaderNodeMath")
        c.operation = "LESS_THAN"
        c.inputs[1].default_value = 0.004
        nt.links.new(a.outputs[0], c.inputs[0])
        return c
    mx = nt.nodes.new("ShaderNodeMath")
    mx.operation = "MAXIMUM"
    nt.links.new(line("X").outputs[0], mx.inputs[0])
    nt.links.new(line("Y").outputs[0], mx.inputs[1])
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.inputs["A"].default_value = (0.3, 0.31, 0.33, 1)
    mix.inputs["B"].default_value = (0.06, 0.065, 0.07, 1)
    nt.links.new(mx.outputs[0], mix.inputs["Factor"])
    nt.links.new(mix.outputs["Result"], p.inputs["Base Color"])
    return m


def trace_mat(name, coord="Object", hot=(1.0, 0.92, 0.75)):
    """a weld bead that is laid as a travelling glow: a Value node 'p' (0-1) is the head; behind it the bead cools
    from white-hot through orange to a dull red; ahead of it the seam is plain metal. 'k' scales the cooling length,
    'g' the overall glow. Object coord: the angle round local Z; UV coord: u along the strip."""
    m = mat(name, (0.45, 0.43, 0.4), 0.35, metal=1.0)
    nt = m.node_tree
    p = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    if coord == "UV":
        nt.links.new(tc.outputs["UV"], sep.inputs["Vector"])
        u = sep.outputs["X"]
    else:
        nt.links.new(tc.outputs["Object"], sep.inputs["Vector"])
        at = nt.nodes.new("ShaderNodeMath")
        at.operation = "ARCTAN2"
        nt.links.new(sep.outputs["Y"], at.inputs[0])
        nt.links.new(sep.outputs["X"], at.inputs[1])
        mr = nt.nodes.new("ShaderNodeMapRange")
        mr.inputs["From Min"].default_value = -math.pi
        mr.inputs["From Max"].default_value = math.pi
        nt.links.new(at.outputs[0], mr.inputs["Value"])
        u = mr.outputs["Result"]
    pv = nt.nodes.new("ShaderNodeValue")
    pv.name = "p"
    kv = nt.nodes.new("ShaderNodeValue")
    kv.name = "k"
    kv.outputs[0].default_value = 1.0
    gv = nt.nodes.new("ShaderNodeValue")
    gv.name = "g"
    gv.outputs[0].default_value = 1.0
    d = nt.nodes.new("ShaderNodeMath")
    d.operation = "SUBTRACT"
    nt.links.new(pv.outputs[0], d.inputs[0])
    nt.links.new(u, d.inputs[1])
    dk = nt.nodes.new("ShaderNodeMath")
    dk.operation = "DIVIDE"
    nt.links.new(d.outputs[0], dk.inputs[0])
    nt.links.new(kv.outputs[0], dk.inputs[1])
    on = nt.nodes.new("ShaderNodeMath")
    on.operation = "GREATER_THAN"
    on.inputs[1].default_value = -0.0005
    nt.links.new(d.outputs[0], on.inputs[0])
    cr = nt.nodes.new("ShaderNodeValToRGB")
    e = cr.color_ramp.elements
    e[0].position, e[0].color = 0.0, (*hot, 1)
    e[1].position, e[1].color = 0.6, (0.35, 0.03, 0.0, 1)
    mid = e.new(0.08)
    mid.color = (1.0, 0.42, 0.06, 1)
    nt.links.new(dk.outputs[0], cr.inputs["Fac"])
    st = nt.nodes.new("ShaderNodeMapRange")
    st.inputs["From Min"].default_value = 0.0
    st.inputs["From Max"].default_value = 0.6
    st.inputs["To Min"].default_value = 80.0
    st.inputs["To Max"].default_value = 3.0
    nt.links.new(dk.outputs[0], st.inputs["Value"])
    m1 = nt.nodes.new("ShaderNodeMath")
    m1.operation = "MULTIPLY"
    nt.links.new(st.outputs["Result"], m1.inputs[0])
    nt.links.new(on.outputs[0], m1.inputs[1])
    m2 = nt.nodes.new("ShaderNodeMath")
    m2.operation = "MULTIPLY"
    nt.links.new(m1.outputs[0], m2.inputs[0])
    nt.links.new(gv.outputs[0], m2.inputs[1])
    nt.links.new(cr.outputs["Color"], p.inputs["Emission Color"])
    nt.links.new(m2.outputs[0], p.inputs["Emission Strength"])
    return m


def set_trace(m, p, k=None, g=None):
    nt = m.node_tree
    if "p" not in nt.nodes:
        return
    nt.nodes["p"].outputs[0].default_value = p
    if k is not None:
        nt.nodes["k"].outputs[0].default_value = k
    if g is not None:
        nt.nodes["g"].outputs[0].default_value = g


def glow_mat(name, color, strength):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.remove(nt.nodes["Principled BSDF"])
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*color, 1)
    em.inputs["Strength"].default_value = strength
    nt.links.new(em.outputs[0], nt.nodes["Material Output"].inputs["Surface"])
    return m


def glass_mat(name, tint=(0.75, 0.85, 0.9)):
    m = mat(name, tint, 0.03)
    p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Transmission Weight"].default_value = 1.0
    p.inputs["IOR"].default_value = 1.49   # acrylic
    return m


# ---------------------------------------------------------------- scene
def setup(a, exposure=0.0, world=(0.004, 0.005, 0.007), hdri=None, hdri_strength=0.3):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = a.samples
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.use_denoising = True
    sc.cycles.denoiser = "OPENIMAGEDENOISE"
    sc.cycles.max_bounces = a.bounces
    sc.cycles.transmission_bounces = max(4, a.bounces)
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
    nt = w.node_tree
    bg = nt.nodes["Background"]
    if hdri:
        env = nt.nodes.new("ShaderNodeTexEnvironment")
        env.image = bpy.data.images.load(os.path.join(ROOT, "library", "hdri", hdri))
        nt.links.new(env.outputs["Color"], bg.inputs["Color"])
        bg.inputs["Strength"].default_value = hdri_strength
        # the camera sees a dark studio, reflections see the HDRI
        lp = nt.nodes.new("ShaderNodeLightPath")
        mix = nt.nodes.new("ShaderNodeMixShader")
        dark = nt.nodes.new("ShaderNodeBackground")
        dark.inputs["Color"].default_value = (*world, 1)
        nt.links.new(lp.outputs["Is Camera Ray"], mix.inputs["Fac"])
        nt.links.new(bg.outputs[0], mix.inputs[1])
        nt.links.new(dark.outputs[0], mix.inputs[2])
        nt.links.new(mix.outputs[0], nt.nodes["World Output"].inputs["Surface"])
    else:
        bg.inputs["Color"].default_value = (*world, 1)
    bpy.ops.object.camera_add()
    cam = bpy.context.object
    cam.data.clip_start = 0.02
    cam.data.clip_end = 400
    sc.camera = cam
    return sc, cam


def area(loc, aim, size, energy, color, shape="SQUARE"):
    bpy.ops.object.light_add(type="AREA", location=loc)
    l = bpy.context.object
    l.data.shape = shape
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


def link(name, verts, faces, m=None, smooth_shade=True, uvs=None):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    if uvs:
        uv = me.uv_layers.new(name="UVMap")
        for poly in me.polygons:
            for li, vi in zip(poly.loop_indices, poly.vertices):
                uv.data[li].uv = uvs[vi]
    me.update()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    if m:
        ob.data.materials.append(m)
    for p in me.polygons:
        p.use_smooth = smooth_shade
    return ob


def crisp(ob, angle=0.6):
    bpy.ops.object.select_all(action="DESELECT")
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.shade_smooth_by_angle(angle=angle)


def lathe(name, prof, m, seg=96):
    """a closed body of revolution round local Z; prof is a list of (r, z) from the axis round and back"""
    verts, faces = [], []
    n = len(prof)
    for j in range(seg):
        a = j / seg * math.tau
        for r, z in prof:
            verts.append((r * math.cos(a), r * math.sin(a), z))
    for j in range(seg):
        j2 = (j + 1) % seg
        for i in range(n - 1):
            faces.append((j * n + i, j2 * n + i, j2 * n + i + 1, j * n + i + 1))
    return link(name, verts, faces, m)


def zone(name, h0, h1, m, seg=192, rings=40):
    """a piece of the 80 mm shell between two horizontal cuts at heights h0 < h1 (metres from the centre), closed"""
    prof = []
    zo0, zo1 = max(h0, -RO), min(h1, RO)
    for i in range(rings + 1):
        z = zo0 + (zo1 - zo0) * i / rings
        prof.append((math.sqrt(max(0.0, RO * RO - z * z)), z))
    zi0, zi1 = max(h0, -RI), min(h1, RI)
    inner = []
    for i in range(rings + 1):
        z = zi0 + (zi1 - zi0) * i / rings
        inner.append((math.sqrt(max(0.0, RI * RI - z * z)), z))
    if h1 >= RI:   # closed at the top by the outer skin only (not used: the hatch closes the top)
        inner = [(0.0, RI)] + inner[::-1][1:]
    prof = prof + inner[::-1] + [prof[0]]
    ob = lathe(name, prof, m, seg)
    return ob


def radial_frame(ob, lat, az):
    """put an object whose local Z is its axis on the ball surface at latitude/azimuth (front is -Y), axis outward"""
    d = Vector((math.cos(lat) * math.sin(az), -math.cos(lat) * math.cos(az), math.sin(lat)))
    ob.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
    return d


def bool_cut(ob, cutter, mode="DIFFERENCE"):
    md = ob.modifiers.new("b", "BOOLEAN")
    md.operation = mode
    md.object = cutter
    md.solver = "EXACT"
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.modifier_apply(modifier=md.name)


# viewports from ISRO's drawing: (lat, az, outside flange radius, window radius)
PRIMARY = (math.radians(-3), 0.0, 0.30, 0.10)
SECONDARY = [(math.radians(-13.5), math.radians(-30), 0.17, 0.05),
             (math.radians(-13.5), math.radians(30), 0.17, 0.05)]


def build_ball(finish="bare", glass=None):
    """the five pieces, the three viewport inserts and the seven seam beads; returns a dict"""
    shell = titanium("ti") if finish == "bare" else painted("paint")
    rim = shell if finish == "bare" else mat("rim", (0.42, 0.04, 0.03), 0.4)
    pieces = {}
    cuts = [-RO, H_W6 * RO, H_W1 * RO, H_W7 * RO, H_HATCH * RO]
    names = ["dome", "ring3", "ring2", "ring1"]
    for nm, h0, h1 in zip(names, cuts, cuts[1:]):
        pieces[nm] = zone(nm, h0, h1, shell)
    # the hatch: a stepped frustum on top, from ISRO's drawing (base on the ring-1 cut, about 0.2 m tall)
    zb = H_HATCH * RO
    rb = math.sqrt(RO * RO - zb * zb)
    zi = math.sqrt(max(0.0, RI * RI - rb * rb * 0.0))
    prof = [(0.0, zb - 0.06), (rb - 0.07, zb - 0.06), (rb, zb), (rb - 0.02, zb + 0.05), (rb - 0.05, zb + 0.06),
            (rb - 0.05, zb + 0.1), (rb - 0.08, zb + 0.11), (rb - 0.08, zb + 0.15), (rb - 0.11, zb + 0.16),
            (rb - 0.11, zb + 0.2), (0.0, zb + 0.2)]
    pieces["hatch"] = lathe("hatch", prof, shell, 128)
    # viewport holes through rings 2 and 3, then the inserts
    inserts, wseams, windows = [], [], []
    for i, (lat, az, rf, rw) in enumerate([PRIMARY] + SECONDARY):
        bpy.ops.mesh.primitive_cylinder_add(radius=rf * 0.78, depth=0.6, vertices=96)
        cut = bpy.context.object
        d = radial_frame(cut, lat, az)
        cut.location = d * RO
        bpy.context.view_layer.update()
        for nm in (["ring2", "ring3"] if i == 0 else ["ring3"]):
            bool_cut(pieces[nm], cut)
        bpy.data.objects.remove(cut)
        # the insert: a thick flanged ring, local Z outward, origin at the outer skin
        t_in, t_out = 0.16, 0.035
        p = [(rw, -t_in), (rf * 0.78, -t_in), (rf * 0.78, -0.02), (rf, -0.012), (rf, t_out - 0.006),
             (rf - 0.006, t_out), (rw * 1.3, t_out), (rw * 1.3, t_out - 0.012), (rw, t_out - 0.02), (rw, -t_in)]
        ins = lathe(f"insert{i}", p, rim, 96)
        nb = 12 if i == 0 else 8
        for k in range(nb):
            a = k / nb * math.tau
            rr = (rf + rw * 1.3) / 2
            bpy.ops.mesh.primitive_cylinder_add(radius=0.012 if i == 0 else 0.008, depth=0.016, vertices=6,
                                                location=(rr * math.cos(a), rr * math.sin(a), t_out + 0.004))
            bolt = bpy.context.object
            bolt.data.materials.append(rim)
            bolt.parent = ins
        ins.location = d * (RO - 0.005)
        radial_frame(ins, lat, az)
        inserts.append(ins)
        if glass is not None:
            bpy.ops.mesh.primitive_cylinder_add(radius=rw * 1.02, depth=0.1, vertices=64)
            g = bpy.context.object
            g.data.materials.append(glass)
            g.location = d * (RO - 0.04)
            radial_frame(g, lat, az)
            windows.append(g)
        # the window seam (W3 primary, W4/W5 secondary): a bead where the insert meets the shell
        tm = trace_mat(f"wseam{i}")
        bpy.ops.mesh.primitive_torus_add(major_radius=rf * 0.79, minor_radius=0.011, major_segments=96,
                                         minor_segments=12)
        s = bpy.context.object
        s.data.materials.append(tm)
        s.location = d * (RO - 0.004)
        radial_frame(s, lat, az)
        wseams.append(s)
    # belt seams: W6, W1, W7 at the ring cuts, W2 at the hatch base
    belts = {}
    for nm, h in (("W6", H_W6), ("W1", H_W1), ("W7", H_W7), ("W2", H_HATCH)):
        z = h * RO
        r = math.sqrt(RO * RO - z * z)
        tm = trace_mat(f"seam{nm}")
        bpy.ops.mesh.primitive_torus_add(major_radius=r + 0.002, minor_radius=0.013, major_segments=256,
                                         minor_segments=12, location=(0, 0, z))
        s = bpy.context.object
        s.scale = (1, 1, 0.7)
        s.data.materials.append(tm)
        belts[nm] = s
    for ob in list(pieces.values()) + inserts + list(belts.values()) + wseams:
        for p in ob.data.polygons:
            p.use_smooth = True
    for ob in inserts + [pieces["hatch"]]:
        crisp(ob)
    if finish != "bare":
        for s in list(belts.values()) + wseams:
            s.scale = (1, 1, 0.25) if s in belts.values() else (1, 1, 1)
            s.data.materials[0] = shell
    root = bpy.data.objects.new("ball", None)
    bpy.context.collection.objects.link(root)
    for ob in list(pieces.values()) + inserts + list(belts.values()) + wseams + windows:
        ob.parent = root
    return dict(root=root, pieces=pieces, inserts=inserts, belts=belts, wseams=wseams, windows=windows,
                shell=shell)


def seams_all(b):
    return list(b["belts"].values()) + b["wseams"]


def set_seams(b, p=0.0, g=1.0):
    for s in seams_all(b):
        set_trace(s.data.materials[0], p, g=g)


def plate(size=(40, 40), z=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, z - 0.03))
    pl = bpy.context.object
    pl.scale = (size[0], size[1], 0.06)
    pl.data.materials.append(plate_steel())
    bev = pl.modifiers.new("bev", "BEVEL")
    bev.width = 0.01
    return pl


def stand(radius=0.55, height=0.32, z=0.0):
    """a machined support ring on the plate; the ball rests on its lip"""
    m = mat("stand", (0.08, 0.085, 0.09), 0.45, metal=0.8)
    prof = [(radius - 0.06, 0.0), (radius + 0.08, 0.0), (radius + 0.08, 0.04), (radius + 0.02, 0.06),
            (radius + 0.02, height), (radius - 0.06, height), (radius - 0.06, 0.0)]
    ob = lathe("stand", prof, m, 96)
    crisp(ob)
    ob.location.z = z
    return ob


BALL_Z = 0.32 + math.sqrt(RO * RO - 0.55 * 0.55)   # centre height on the stand


def mannequin(m, pose="stand"):
    """a plain grey figure (no face, no person), 1.75 m, for scale; origin at the feet; standing along +Z or lying
    along +X"""
    parts = []

    def cap(a, b, r):
        a, b = Vector(a), Vector(b)
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=(b - a).length, vertices=24,
                                            location=(a + b) / 2)
        c = bpy.context.object
        c.rotation_euler = (b - a).to_track_quat("Z", "Y").to_euler()
        parts.append(c)
        for p in (a, b):
            bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=24, ring_count=12, location=p)
            parts.append(bpy.context.object)
    cap((0.1, 0, 0.05), (0.1, 0, 0.85), 0.065)
    cap((-0.1, 0, 0.05), (-0.1, 0, 0.85), 0.065)
    cap((0, 0, 0.95), (0, 0, 1.38), 0.16)
    cap((0.23, 0, 1.42), (0.27, 0, 0.82), 0.05)
    cap((-0.23, 0, 1.42), (-0.27, 0, 0.82), 0.05)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.11, segments=32, ring_count=16, location=(0, 0, 1.62))
    parts.append(bpy.context.object)
    for p in parts:
        p.data.materials.append(m)
        for poly in p.data.polygons:
            poly.use_smooth = True
    bpy.ops.object.select_all(action="DESELECT")
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    ob = bpy.context.object
    ob.name = "figure"
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
    if pose == "lie":
        ob.rotation_euler = (0, math.pi / 2, 0)
    return ob


def deep_water(sc, glow=(0.006, 0.03, 0.06)):
    """the deep: a backdrop dome brighter overhead (the last of the light) fading to black below, and marine snow"""
    m = bpy.data.materials.new("deep")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.remove(nt.nodes["Principled BSDF"])
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Object"], sep.inputs["Vector"])
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs["From Min"].default_value = -25.0
    mr.inputs["From Max"].default_value = 60.0
    nt.links.new(sep.outputs["Z"], mr.inputs["Value"])
    pw = nt.nodes.new("ShaderNodeMath")
    pw.operation = "POWER"
    pw.inputs[1].default_value = 1.6
    nt.links.new(mr.outputs["Result"], pw.inputs[0])
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*glow, 1)
    nt.links.new(pw.outputs[0], em.inputs["Strength"])
    nt.links.new(em.outputs[0], nt.nodes["Material Output"].inputs["Surface"])
    bpy.ops.mesh.primitive_uv_sphere_add(radius=60, segments=64, ring_count=32)
    dome = bpy.context.object
    dome.data.materials.append(m)
    dome.visible_shadow = False
    dome.visible_diffuse = False
    dome.visible_glossy = True
    bpy.ops.object.shade_smooth()
    return dome


class Snow:
    """marine snow: a few hundred specks drifting slowly down and sideways, positions a function of the frame"""

    def __init__(self, n=700, box=(9, 9, 6), center=(0, 0, 0), size=0.006, seed=11):
        rnd = random.Random(seed)
        self.p = [(rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(0.5, 1.5),
                   rnd.uniform(0.4, 1.6)) for _ in range(n)]
        self.box, self.c, self.size = box, center, size
        m = mat("snow", (0.75, 0.82, 0.85), 0.8, emit=(0.6, 0.75, 0.85), strength=0.6)
        verts, faces = [], []
        for i in range(n):
            base = len(verts)
            for v in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
                verts.append(v)
            for fa in ((0, 2, 4), (2, 1, 4), (1, 3, 4), (3, 0, 4), (2, 0, 5), (1, 2, 5), (3, 1, 5), (0, 3, 5)):
                faces.append(tuple(base + k for k in fa))
        self.ob = link("snow", verts, faces, m, smooth_shade=False)
        self.ob.visible_shadow = False

    def pose(self, f):
        t = f / FPS
        bx, by, bz = self.box
        cx, cy, cz = self.c
        co = []
        for x, y, z, sp, sz in self.p:
            zz = ((z * bz / 2 - t * 0.05 * sp + bz / 2) % bz) - bz / 2
            xx = x * bx / 2 + 0.04 * math.sin(t * 0.3 * sp + y * 9)
            yy = y * by / 2 + 0.04 * math.cos(t * 0.25 * sp + x * 7)
            s = self.size * sz
            p = (cx + xx, cy + yy, cz + zz)
            for v in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
                co.extend((p[0] + v[0] * s, p[1] + v[1] * s, p[2] + v[2] * s))
        self.ob.data.vertices.foreach_set("co", co)
        self.ob.data.update()


def fib_points(n):
    pts = []
    g = math.pi * (3 - math.sqrt(5))
    for i in range(n):
        z = 1 - 2 * (i + 0.5) / n
        r = math.sqrt(1 - z * z)
        pts.append(Vector((r * math.cos(g * i), r * math.sin(g * i), z)))
    return pts


def interior(b, lights_on=True, dark=False):
    """inside the 2.1 m ball: a padded wall, a floor deck, three low seats facing the viewports, screens, LED strips"""
    pad = mat("pad", (0.025, 0.03, 0.04), 0.7)
    noise_bump(pad, 18, 0.08)
    # a 30 mm padded liner (a hollow shell, so a section cut leaves only a thin ring)
    ro_l, ri_l = RI - 0.005, RI - 0.035
    prof = [(math.sin(math.pi * i / 48) * ro_l, -math.cos(math.pi * i / 48) * ro_l) for i in range(49)]
    prof += [(math.sin(math.pi * i / 48) * ri_l, -math.cos(math.pi * i / 48) * ri_l) for i in range(48, -1, -1)]
    liner = lathe("liner", prof, pad, 128)
    # cut the liner where the viewports are, so the windows show from inside
    for lat, az, rf, rw in [PRIMARY] + SECONDARY:
        bpy.ops.mesh.primitive_cylinder_add(radius=rw * 1.6, depth=0.6, vertices=48)
        cut = bpy.context.object
        d = radial_frame(cut, lat, az)
        cut.location = d * RI
        bpy.context.view_layer.update()
        bool_cut(liner, cut)
        bpy.data.objects.remove(cut)
    deck_z = -0.5
    dm = mat("deck", (0.12, 0.125, 0.13), 0.5, metal=0.6)
    noise_bump(dm, 300, 0.15)
    r = math.sqrt(RI * RI - deck_z * deck_z) - 0.05
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=0.04, vertices=96, location=(0, 0, deck_z))
    deck = bpy.context.object
    deck.data.materials.append(dm)
    # three low seats: a cushion and a back, facing the three viewports
    seat_m = mat("seat", (0.05, 0.07, 0.11), 0.65)
    seats = []
    for az in (0.0, math.radians(-52), math.radians(52)):
        d = Vector((-math.sin(az), math.cos(az), 0))     # from the centre toward the seat, at the back
        c = d * 0.46 + Vector((0, 0, deck_z + 0.1))
        bpy.ops.mesh.primitive_cube_add(size=1, location=c)
        cu = bpy.context.object
        cu.scale = (0.4, 0.4, 0.14)
        cu.rotation_euler = (0, 0, az)
        bev = cu.modifiers.new("bev", "BEVEL")
        bev.width = 0.05
        bev.segments = 4
        cu.data.materials.append(seat_m)
        bk = c + d * 0.22 + Vector((0, 0, 0.26))
        bpy.ops.mesh.primitive_cube_add(size=1, location=bk)
        ba = bpy.context.object
        ba.scale = (0.38, 0.1, 0.46)
        ba.rotation_euler = (math.radians(12), 0, az)
        bev = ba.modifiers.new("bev", "BEVEL")
        bev.width = 0.04
        bev.segments = 4
        ba.data.materials.append(seat_m)
        seats += [cu, ba]
    # screens and panels on the upper walls, LED strips round the top
    scr_on = (0.25, 0.75, 1.0)
    screens = []
    for k, (az, el, w, h) in enumerate([(math.radians(150), 0.15, 0.42, 0.28), (math.radians(-150), 0.15, 0.42, 0.28),
                                        (math.radians(110), 0.3, 0.3, 0.2), (math.radians(-110), 0.3, 0.3, 0.2),
                                        (math.radians(180), 0.42, 0.36, 0.22)]):
        d = Vector((math.cos(el) * math.sin(az), -math.cos(el) * math.cos(az), math.sin(el)))
        bpy.ops.mesh.primitive_cube_add(size=1, location=d * (RI - 0.09))
        bx = bpy.context.object
        bx.scale = (w + 0.04, 0.05, h + 0.04)
        bx.rotation_euler = (-d).to_track_quat("Y", "Z").to_euler()
        bx.data.materials.append(mat(f"panel{k}", (0.03, 0.03, 0.035), 0.5, metal=0.5))
        bpy.ops.mesh.primitive_plane_add(size=1, location=d * (RI - 0.118))
        sp = bpy.context.object
        sp.scale = (w, h, 1)
        sp.rotation_euler = (-d).to_track_quat("Z", "Y").to_euler()
        strength = 0.2 if dark else 1.2
        sm = screen_mat(f"scr{k}", scr_on, strength, seed=k)
        sp.data.materials.append(sm)
        screens.append(sp)
    leds = None
    if lights_on and not dark:
        bpy.ops.mesh.primitive_torus_add(major_radius=math.sqrt(RI ** 2 - 0.62 ** 2) - 0.05, minor_radius=0.012,
                                         location=(0, 0, 0.62), major_segments=128, minor_segments=8)
        leds = bpy.context.object
        leds.data.materials.append(glow_mat("led", (1.0, 0.86, 0.68), 9.0))
        bpy.ops.object.light_add(type="POINT", location=(0, 0.1, 0.45))
        l = bpy.context.object
        l.data.energy = 60
        l.data.color = (1.0, 0.88, 0.75)
        l.data.shadow_soft_size = 0.3
    else:
        # a few status LEDs only
        for k in range(14):
            a = k * 0.45 + 2.2
            p = Vector((math.sin(a) * 0.8, math.cos(a) * 0.55, 0.05 + 0.1 * math.sin(k)))
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.006, location=p.normalized() * (RI - 0.05))
            bpy.context.object.data.materials.append(
                glow_mat(f"sled{k}", (0.2, 1.0, 0.4) if k % 3 else (1.0, 0.3, 0.1), 25))
    return dict(liner=liner, deck=deck, seats=seats, screens=screens, leds=leds)


def screen_mat(name, color, strength, seed=0):
    """a dim instrument screen: a dark field with soft bands (no text, no real UI)"""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.remove(nt.nodes["Principled BSDF"])
    tc = nt.nodes.new("ShaderNodeTexCoord")
    wv = nt.nodes.new("ShaderNodeTexNoise")
    wv.inputs["Scale"].default_value = 2.5 + seed * 0.7
    wv.inputs["Detail"].default_value = 2
    nt.links.new(tc.outputs["UV"], wv.inputs["Vector"])
    cr = nt.nodes.new("ShaderNodeValToRGB")
    cr.color_ramp.elements[0].color = (0.005, 0.02, 0.035, 1)
    cr.color_ramp.elements[1].color = (*color, 1)
    cr.color_ramp.elements[0].position = 0.35
    cr.color_ramp.elements[1].position = 0.8
    nt.links.new(wv.outputs["Fac"], cr.inputs["Fac"])
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Strength"].default_value = strength
    nt.links.new(cr.outputs["Color"], em.inputs["Color"])
    nt.links.new(em.outputs[0], nt.nodes["Material Output"].inputs["Surface"])
    return m


def studio_lights(scale=1.0):
    area((-4.5, -5.5, 6.0), (0, 0, 1.2), 4.0, 2600 * scale, (0.92, 0.95, 1.0))
    area((5.5, 3.5, 3.8), (0, 0, 1.4), 3.0, 1500 * scale, (0.55, 0.72, 1.0))
    area((3.5, -6.0, 1.0), (0, 0, 1.0), 6.0, 500 * scale, (1.0, 0.85, 0.7))
    area((0, 0, 8.0), (0, 0, 0), 6.0, 900 * scale, (0.9, 0.93, 1.0))


# ---------------------------------------------------------------- shots
def build_pieces(a):
    sc, cam = setup(a, exposure=-0.4, hdri="studio_small_09_1k.hdr", hdri_strength=0.35)
    b = build_ball("bare")
    b["root"].location = (0, 0, BALL_Z)
    plate()
    stand()
    studio_lights()
    for ob in b["inserts"] + b["wseams"]:
        ob.parent = b["pieces"]["ring3"]
    return sc, cam, b


PIECE_ORDER = ["dome", "ring3", "ring2", "ring1", "hatch"]


def pose_pieces(f, cam, b):
    # word frames: five 75, top 149, hatch 163, three rings 205, bottom dome 262, together 329, tonnes 464,
    # seven 540, welds 562, four 650, belts 775, three 827, windows 890; end 922
    close = ramp(f, 330, 500)                       # "Together, they weigh about five and a half tonnes"
    gaps = {"dome": 0.0, "ring3": 0.42, "ring2": 0.84, "ring1": 1.26, "hatch": 1.72}
    present = {"hatch": (149, 200), "ring3": (205, 262), "ring2": (205, 262), "ring1": (205, 262),
               "dome": (262, 320)}
    for i, nm in enumerate(PIECE_ORDER):
        ob = b["pieces"][nm]
        lift = gaps[nm] * (1 - close)
        p0, p1 = present[nm]
        nod = math.sin(math.pi * max(0.0, min(1.0, (f - p0) / (p1 - p0)))) if p0 <= f <= p1 else 0.0
        ob.location = (0, -0.18 * nod * (1 - close), lift + 0.06 * nod)
        ob.rotation_euler = (0, 0, (1 - close) * 0.35 * math.sin(f / 140 + i))
    # belts only show once the ball is closed; before that they would float in the gaps
    show = f >= 500
    for s in seams_all(b):
        s.hide_render = not show
    # "Seven welds join them": every seam a dull warm line; then the four belts trace (W6, W7, W2, then W1 the
    # longest, last and brightest), then the three window seams
    base = 0.12 * ramp(f, 540, 580)
    order = [("W6", 650), ("W7", 685), ("W2", 720), ("W1", 760)]
    for nm, f0 in order:
        m = b["belts"][nm].data.materials[0]
        p = ramp(f, f0, f0 + (70 if nm == "W1" else 45)) * 1.08
        g = (1.6 if nm == "W1" else 1.0)
        set_trace(m, p if f >= f0 else 0.0, k=1.2, g=g)
        if f < f0:
            set_trace(m, 1.0, k=40.0, g=base * 3)
    for i, s in enumerate(b["wseams"]):
        f0 = [887, 827, 857][i]                     # W3 (primary) last, at "windows"
        m = s.data.materials[0]
        if f < f0:
            set_trace(m, 1.0, k=40.0, g=base * 3)
        else:
            set_trace(m, ramp(f, f0, f0 + 35) * 1.08, k=1.2, g=1.0)
    # camera: a slow orbit from the front-left, rising, pulling in as the pieces close
    az = math.radians(keys(f, [(0, -28), (500, 4), (959, 22)]))
    dist = keys(f, [(0, 10.5), (330, 10.0), (500, 6.8), (959, 5.6)])
    hgt = keys(f, [(0, 3.0), (500, 2.0), (959, 2.6)])
    aimz = keys(f, [(0, 2.15), (330, 2.1), (500, BALL_Z + 0.08), (959, BALL_Z)])
    lens = keys(f, [(0, 36), (330, 38), (500, 50), (959, 50)])
    loc = (dist * math.sin(az), -dist * math.cos(az), hgt)
    aim_cam(cam, loc, (0, 0, aimz), lens, fstop=8)


def build_seam(a):
    sc, cam = setup(a, exposure=-0.4, hdri="studio_small_09_1k.hdr", hdri_strength=0.35)
    b = build_ball("bare")
    b["root"].location = (0, 0, BALL_Z)
    plate()
    stand()
    studio_lights()
    # the unrolled seam: a strip along the plate in front of the ball, 7.1 m (pi x 2.26 m)
    n = 400
    L = math.pi * 2 * RO
    verts, faces, uvs = [], [], []
    cs = [(-0.02, 0.0), (0.02, 0.0), (0.02, 0.08), (-0.02, 0.08)]   # 40 mm bead face, 80 mm deep
    for i in range(n + 1):
        for (w, h) in cs:
            verts.append((0, 0, 0))
            uvs.append((i / n, h / 0.08))
    for i in range(n):
        for k in range(4):
            a0, a1 = i * 4 + k, i * 4 + (k + 1) % 4
            faces.append((a0, a1, a1 + 4, a0 + 4))
    faces.append((0, 1, 2, 3))
    faces.append((n * 4 + 3, n * 4 + 2, n * 4 + 1, n * 4))
    tm = trace_mat("strip", coord="UV")
    strip = link("strip", verts, faces, tm, smooth_shade=False, uvs=uvs)
    fig = mannequin(mat("figure", (0.05, 0.055, 0.06), 0.6))
    return sc, cam, dict(b=b, strip=strip, n=n, L=L, cs=cs, fig=fig)


def strip_pose(o, u_unroll):
    """each section of the bead goes from its place on the equator to its place on the line; it peels from the front
    (u = 0.5) outward, so the line opens both ways like a ring cut and laid flat"""
    n, L, cs = o["n"], o["L"], o["cs"]
    co = []
    y_line = -2.4
    for i in range(n + 1):
        u = i / n
        # on the ball: angle measured from the front (-Y), u = 0.5 at the front
        ang = (u - 0.5) * math.tau
        on = Vector((RO * math.sin(ang), -RO * math.cos(ang), BALL_Z))
        out = Vector((math.sin(ang), -math.cos(ang), 0))
        line = Vector(((u - 0.5) * L, y_line, 0.0))
        # stagger: the front sections move first
        lag = abs(u - 0.5) * 2
        t = smooth((u_unroll * 1.6 - lag * 0.6))
        # an arc on the way down, so it reads as peeling off
        mid = on.lerp(line, t) + Vector((0, 0, 0.6 * math.sin(math.pi * t)))
        tang = Vector((math.cos(ang), math.sin(ang), 0)).lerp(Vector((1, 0, 0)), t).normalized()
        nrm = out.lerp(Vector((0, 0, 1)), t).normalized()
        side = tang.cross(nrm).normalized()
        for (w, h) in cs:
            p = mid + side * w + nrm * (h - (0.08 if t < 0.5 else 0.0) * (1 - t * 2 if t < 0.5 else 0))
            co.extend(p)
    o["strip"].data.vertices.foreach_set("co", co)
    o["strip"].data.update()


def pose_seam(f, cam, o):
    # word frames: One 115, big 141, round 214, ball 242, Eight 299, deep 357, seven 418, metres 438, long 461,
    # It took 508, thirty-two 538, minutes 578, one go 629-645, Isro says 691; end 955
    b = o["b"]
    set_seams(b, 0.0, 0.0)
    for s in seams_all(b):
        s.hide_render = s is not b["belts"]["W1"]
    w1 = b["belts"]["W1"].data.materials[0]
    # the ball turns under the beam: one full turn while the glow goes round (115-300)
    p = ramp(f, 115, 300) * 1.12
    # the head of the bead (local angle -pi + 2 pi p) is held at the front-right, under the beam
    b["root"].rotation_euler = (0, 0, -math.pi / 2 + 0.5 - (-math.pi + math.tau * min(p, 1.0)))
    set_trace(w1, p, k=1.0, g=1.4)
    # at "seven metres" the bead peels off and lies down as a straight line; the ring on the ball goes dark
    un = ramp(f, 400, 520)
    b["belts"]["W1"].hide_render = un > 0.02
    o["strip"].hide_render = f < 400
    strip_pose(o, un)
    sm = o["strip"].data.materials[0]
    if f < 540:
        set_trace(sm, 0.5 + 0.0, k=0.25, g=0.8)
        set_trace(sm, 1.2, k=1.0, g=0.6)
    else:
        # "thirty-two minutes, in one go": one pass runs end to end along the line, then it cools
        set_trace(sm, ramp(f, 540, 660) * 1.1, k=0.6, g=1.4 * (1 - 0.6 * ramp(f, 700, 955)))
    # the figure for scale stands at the right end of the line
    o["fig"].location = (o["L"] / 2 + 0.6, -2.4, 0.0)
    o["fig"].rotation_euler = (0, 0, math.radians(-20))
    o["fig"].hide_render = f < 440
    # camera: close on the seam while it is welded, out wide for the line
    loc = keys(f, [(0, (3.4, -4.6, BALL_Z + 0.9)), (300, (2.2, -3.2, BALL_Z + 0.35)),
                   (400, (2.2, -6.5, 2.6)), (560, (0.8, -11.5, 3.6)), (955, (-0.6, -12.5, 4.2))])
    aim = keys(f, [(0, (0, 0, BALL_Z)), (300, (0.5, -0.9, BALL_Z)), (400, (0, -1.6, 0.9)),
                   (560, (0, -1.4, 0.6)), (955, (0, -1.2, 0.7))])
    lens = keys(f, [(0, 42), (300, 50), (400, 40), (560, 32), (955, 32)])
    aim_cam(cam, loc, aim, lens, fstop=11)


def build_squeeze(a):
    sc, cam = setup(a, exposure=0.2, world=(0.0, 0.0, 0.0))
    b = build_ball("painted")
    deep_water(sc)
    snow = Snow(center=(0, 0, 0))
    # the squeeze glow on the paint: a fresnel rim that grows with the squeeze (SIMPLIFIED, amber = pressure)
    m = b["shell"]
    nt = m.node_tree
    p = nt.nodes["Principled BSDF"]
    lw = nt.nodes.new("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = 0.35
    sv = nt.nodes.new("ShaderNodeValue")
    sv.name = "sq"
    mu = nt.nodes.new("ShaderNodeMath")
    mu.operation = "MULTIPLY"
    nt.links.new(lw.outputs["Facing"], mu.inputs[0])
    nt.links.new(sv.outputs[0], mu.inputs[1])
    p.inputs["Emission Color"].default_value = (0.95, 0.42, 0.03, 1)
    nt.links.new(mu.outputs[0], p.inputs["Emission Strength"])
    # arrows: one per patch of surface, pointing in
    am = glow_mat("arrow", (0.95, 0.42, 0.03), 0.45)
    arrows = []
    for i, d in enumerate(fib_points(110)):
        bpy.ops.mesh.primitive_cone_add(radius1=0.055, depth=0.13, vertices=16)
        tip = bpy.context.object
        bpy.ops.mesh.primitive_cylinder_add(radius=0.016, depth=0.26, vertices=12, location=(0, 0, -0.195))
        sh = bpy.context.object
        bpy.ops.object.select_all(action="DESELECT")
        tip.select_set(True)
        sh.select_set(True)
        bpy.context.view_layer.objects.active = tip
        bpy.ops.object.join()
        ar = bpy.context.object
        ar.data.materials.append(am)
        # the cone points along +Z: turn it to point at the centre
        ar.rotation_euler = (-d).to_track_quat("Z", "Y").to_euler()
        arrows.append((ar, d))
    area((-3, -4, 6), (0, 0, 0), 3.0, 900, (0.6, 0.78, 1.0))
    area((4, 3, -2), (0, 0, 0), 4.0, 160, (0.3, 0.45, 0.7))
    bpy.ops.object.light_add(type="SPOT", location=(0, 0, 9))
    s = bpy.context.object
    s.data.energy = 4000
    s.data.spot_size = math.radians(30)
    s.data.spot_blend = 0.8
    s.data.color = (0.5, 0.75, 1.0)
    return sc, cam, dict(b=b, snow=snow, arrows=arrows, sq=sv)


def pose_squeeze(f, cam, o):
    # word frames: cover 29, ball 73, fingernails 88-130, Every one 151, buffalo 254, Add it all up 320,
    # squeezes 432, one lakh tonnes 555-591, from every side 609-697, end 721
    b = o["b"]
    set_seams(b, 0.0, 0.0)
    o["snow"].pose(f)
    front = Vector((0, -1, 0.15)).normalized()
    push = ramp(f, 432, 600)
    for ar, d in o["arrows"]:
        ang = math.acos(max(-1.0, min(1.0, d.dot(front))))
        f0 = 29 + ang / math.pi * 130        # a wave of arrows spreads from the front round to the back
        grow = ramp(f, f0, f0 + 24)
        pulse = 1 + 0.25 * math.exp(-((f - 254) / 12) ** 2) + 0.15 * math.exp(-((f - 591) / 14) ** 2)
        dist = RO + 0.42 - 0.24 * push + 0.03 * math.sin(f / 9 + ang * 4) * (1 - push)
        ar.location = d * dist
        s = max(0.001, grow * pulse)
        ar.scale = (s, s, s)
        ar.hide_render = grow <= 0.001
    # the ball gives a little (exaggerated many times: SIMPLIFIED) and the rim glows
    k = 1 - 0.035 * push + 0.006 * math.sin(f / 6) * push
    b["root"].scale = (k, k, k)
    o["sq"].outputs[0].default_value = 0.25 * push
    az = math.radians(keys(f, [(0, -20), (720, 26), (779, 30)]))
    dist = keys(f, [(0, 7.5), (300, 6.6), (600, 5.4), (779, 5.2)])
    loc = (dist * math.sin(az), -dist * math.cos(az), keys(f, [(0, 1.4), (779, 0.8)]))
    aim_cam(cam, loc, (0, 0, 0), 45)


def build_dive(a):
    sc, cam = setup(a, exposure=0.1, world=(0.0, 0.0, 0.0))
    glass = glass_mat("acrylic")
    b = build_ball("painted", glass=glass)
    deep_water(sc)
    snow = Snow(center=(0, -2.5, 0), box=(10, 12, 7))
    inside = interior(b, lights_on=True)
    area((-3, -4, 6), (0, 0, 0), 3.0, 700, (0.6, 0.78, 1.0))
    area((4, 3, -2), (0, 0, 0), 4.0, 120, (0.3, 0.45, 0.7))
    bpy.ops.object.light_add(type="SPOT", location=(0.5, -1.0, 9))
    s = bpy.context.object
    s.data.energy = 3500
    s.data.spot_size = math.radians(26)
    s.data.spot_blend = 0.8
    s.data.color = (0.5, 0.75, 1.0)
    return sc, cam, dict(b=b, snow=snow, inside=inside)


def pose_dive(f, cam, o):
    # word frames: squeeze 179, titanium 221, ball 250, lakh 349, tonnes 368; Imagine 434, inside 475, two 533,
    # Indians 562; end 589; held to 659 for the cut
    b = o["b"]
    set_seams(b, 0.0, 0.0)
    o["snow"].pose(f)
    d = Vector((math.cos(PRIMARY[0]) * math.sin(PRIMARY[1]), -math.cos(PRIMARY[0]) * math.cos(PRIMARY[1]),
                math.sin(PRIMARY[0])))
    win = d * RO
    if f < 380:
        az = math.radians(keys(f, [(0, -38), (380, -6)]))
        dist = keys(f, [(0, 8.5), (250, 5.0), (380, 2.6)])
        hgt = keys(f, [(0, 2.2), (380, 0.1)])
        loc = (dist * math.sin(az), -dist * math.cos(az), hgt)
        aim = keys(f, [(0, (0, 0, 0)), (250, (0, -0.3, 0)), (380, tuple(win))])
        aim_cam(cam, loc, aim, keys(f, [(0, 40), (380, 45)]))
        cam.data.clip_start = 0.02
    else:
        # straight in through the primary viewport
        t = ramp(f, 380, 500)
        start = Vector(keys(379, [(0, (0, -8.5, 2.2)), (380, (0, 0, 0))]))
        az = math.radians(-6)
        p0 = Vector((2.6 * math.sin(az), -2.6 * math.cos(az), 0.1))
        p1 = Vector((0.0, -0.62, 0.12))
        loc = p0.lerp(p1, t) + Vector((0.05 * math.sin(f / 70), 0, 0.03 * ramp(f, 500, 659)))
        aim = win.lerp(Vector((0, 0.8, -0.28)), ramp(f, 420, 540))
        aim_cam(cam, tuple(loc), tuple(aim), keys(f, [(380, 45), (500, 20), (659, 17)]))
        # clip away the wall and the window as the camera passes them
        wall_dist = (loc - win).length
        cam.data.clip_start = 0.02 if loc.y < -RO - 0.35 else min(0.6, max(0.02, wall_dist + 0.12))
        if loc.y > -RI + 0.15:
            cam.data.clip_start = 0.02


CUT_X = -0.45   # the section plane: everything with x below it is cut away


def build_cutaway(a):
    sc, cam = setup(a, exposure=-0.8, hdri="studio_small_09_1k.hdr", hdri_strength=0.3)
    b = build_ball("painted")
    inside = interior(b, lights_on=True)
    # cut the left side away; the cut faces take the bare-titanium material, so the 80 mm wall shows as metal
    cutface = titanium("cutface")
    bpy.ops.mesh.primitive_cube_add(size=1, location=(CUT_X - 3.0, 0, 0))
    box = bpy.context.object
    box.scale = (6, 6, 6)
    box.data.materials.append(cutface)
    bpy.context.view_layer.update()
    for ob in list(b["pieces"].values()) + b["inserts"] + [inside["liner"], inside["deck"]]:
        md = ob.modifiers.new("cut", "BOOLEAN")
        md.operation = "DIFFERENCE"
        md.object = box
        md.solver = "EXACT"
        md.material_mode = "TRANSFER"
        bpy.context.view_layer.objects.active = ob
        bpy.ops.object.modifier_apply(modifier=md.name)
    bpy.data.objects.remove(box)
    for ob in b["windows"] + b["wseams"] + list(b["belts"].values()):
        ob.hide_render = True
    bpy.context.view_layer.update()
    for ob in bpy.data.objects:
        if ob.type == "MESH" and ob.name not in [p.name for p in b["pieces"].values()] and \
                ob not in b["inserts"] and ob not in (inside["liner"], inside["deck"]):
            if ob.matrix_world.translation.x < CUT_X + 0.05 and ob.dimensions.x < 3:
                ob.hide_render = True
    plate(z=-BALL_Z)
    stand(z=-BALL_Z)
    studio_lights(0.45)
    for l in [o for o in bpy.data.objects if o.type == "LIGHT" and o.data.type == "AREA"]:
        l.location.z -= BALL_Z
    fig = mannequin(mat("figure", (0.42, 0.43, 0.45), 0.55))
    # lying on the deck along Y: head toward the window (-Y), feet toward the back wall
    fig.rotation_euler = (math.pi / 2, 0, 0)
    return sc, cam, dict(b=b, inside=inside, fig=fig)


def pose_cutaway(f, cam, o):
    # word frames: step inside 14-25, wall 127, eight 153, thick 212, inside 260, two 363, metres 377,
    # Lie 426, head 523, feet 574, touch 638, walls 675, You 750, two others 781-797, sit 822, twelve 939, end 988
    set_seams(o["b"], 0.0, 0.0)
    deck_z = -0.5
    fig = o["fig"]
    vis = ramp(f, 420, 470) * (1 - ramp(f, 715, 750))
    fig.hide_render = vis < 0.02
    fig.location = (0.12, 1.75 / 2, deck_z + 0.02 + 0.17 + (1 - vis) * 0.5)
    for s in o["inside"]["seats"]:
        s.hide_render = 426 < f < 745
    loc = keys(f, [(0, (-6.2, -2.6, 2.2)), (260, (-4.4, -1.2, 0.8)), (420, (-3.6, -0.4, 0.45)),
                   (700, (-3.4, 0.2, 0.4)), (999, (-4.4, 1.2, 1.0))])
    aim = keys(f, [(0, (0, 0, -0.2)), (260, (0, 0, -0.05)), (420, (0, 0, -0.25)), (999, (0, 0, -0.2))])
    aim_cam(cam, loc, aim, keys(f, [(0, 34), (420, 34), (999, 32)]), fstop=10)


def build_dark(a):
    sc, cam = setup(a, exposure=0.6, world=(0.0, 0.0, 0.0))
    glass = glass_mat("acrylic", (0.6, 0.75, 0.85))
    b = build_ball("painted", glass=glass)
    inside = interior(b, lights_on=False, dark=True)
    # outside the window: the faint blue of the sub's own lights in the water, and drifting specks
    deep_water(sc, glow=(0.04, 0.18, 0.36))
    snow = Snow(center=(0, -4.5, 0), box=(6, 5, 5), size=0.008)
    bpy.ops.object.light_add(type="SPOT", location=(0, -1.4, 0.9))
    s = bpy.context.object
    s.data.energy = 2500
    s.data.spot_size = math.radians(50)
    area((0.3, 0.6, 0.6), (0, -0.6, -0.3), 0.6, 4, (0.35, 0.55, 1.0))
    s.data.color = (0.45, 0.7, 1.0)
    s.rotation_euler = (Vector((0, -5, -0.5)) - Vector((0, -1.4, 0.9))).to_track_quat("-Z", "Y").to_euler()
    return sc, cam, dict(b=b, snow=snow)


def pose_dark(f, cam, o):
    set_seams(o["b"], 0.0, 0.0)
    o["snow"].pose(f)
    loc = keys(f, [(0, (0.3, 0.55, 0.3)), (719, (0.06, -0.25, 0.08))])
    aim = keys(f, [(0, (0, -RO, -0.1)), (719, (0, -RO, -0.06))])
    aim_cam(cam, loc, aim, keys(f, [(0, 30), (719, 40)]))


SHOTS = {"pieces": (build_pieces, pose_pieces), "seam": (build_seam, pose_seam),
         "squeeze": (build_squeeze, pose_squeeze), "dive": (build_dive, pose_dive),
         "cutaway": (build_cutaway, pose_cutaway), "dark": (build_dark, pose_dark)}


def main():
    a = args()
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
