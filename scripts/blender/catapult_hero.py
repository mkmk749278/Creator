"""Hero shots for carrier-catapult (projects/carrier-catapult/word_map.md; every shot is labelled ILLUSTRATION,
the catapult and cutaways also SIMPLIFIED).

  .venv-blender/bin/python scripts/blender/catapult_hero.py --shot NAME --out DIR --frames a-b --step 2 [--w --h]

H1 · the new Vikrant in sea daylight (designed from the Navy's own footage: dark non-skid deck, white centreline,
     red-white and yellow dashed edge lines, yellow hatching, the bow ramp; ramp about 37 m long ending at 14 degrees).
  deck     (0-599)  S16-17: a sailor's eye height, walking up the deck; the ramp's lip ends against open sky.
  ramp     (0-599)  S18-22: low and close along the ramp's bare steel, rising with it to the lip.
  morph    (0-719)  S83:    side view of the bow: a flat deck with a glowing catapult slot (1961); the slot seals
                            (120-240), then the bow rises into a ramp (300-500).
  cutaway  (0-719)  S86-89: the hull cut down its centreline; four gas turbines light one by one (60-300); the space
                            under the ramp is packed solid (stores, machinery: SIMPLIFIED).
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
    m = brushed_steel(name, (0.30, 0.31, 0.33), 0.46)
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


def sky_world(sc, elevation=38, rotation=200, strength=0.35):
    w = sc.world
    nt = w.node_tree
    sky = nt.nodes.new("ShaderNodeTexSky")
    sky.sky_type = "NISHITA"
    sky.sun_elevation = math.radians(elevation)
    sky.sun_rotation = math.radians(rotation)
    sky.altitude = 20
    sky.air_density = 1.2
    sky.dust_density = 2.5
    bg = nt.nodes["Background"]
    bg.inputs["Strength"].default_value = strength
    nt.links.new(sky.outputs["Color"], bg.inputs["Color"])
    bpy.ops.object.light_add(type="SUN")
    sun = bpy.context.object
    sun.data.energy = 4.0
    sun.data.angle = math.radians(0.6)
    sun.data.color = (1.0, 0.95, 0.88)
    sun.rotation_euler = (math.radians(90 - elevation), 0, math.radians(rotation - 90))
    return sun


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


def mesh_obj(name, verts, faces, m):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
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


# ---------------------------------------------------------------- H1 · the new Vikrant
L, W = 262.0, 60.0          # flight deck length and width (m), deck at z = 0
RAMP_X0, RAMP_DEG = 225.0, 14.0
RAMP_R = (L - RAMP_X0) / math.radians(RAMP_DEG)


def ramp_z(x, m=1.0):
    """height of the deck at x; m blends from a flat deck (0) to the ramp (1)"""
    if x <= RAMP_X0:
        return 0.0
    th = (x - RAMP_X0) / RAMP_R
    return m * RAMP_R * (1 - math.cos(th))


def half_width(x):
    """the deck in plan: full width amidships, a rounded stern, the bow tapering under the ramp"""
    if x < 12:
        return W / 2 * (0.72 + 0.28 * smooth(x / 12))
    if x > 185:
        return W / 2 * (1 - 0.55 * smooth((x - 185) / (L - 185)))
    return W / 2


def deck_mesh(name, m, morph=1.0, nx=260, ny=24):
    vs, fs = [], []
    for i in range(nx + 1):
        x = L * i / nx
        hw = half_width(x)
        for j in range(ny + 1):
            y = -hw + 2 * hw * j / ny
            vs.append((x, y, ramp_z(x, morph)))
    for i in range(nx):
        for j in range(ny):
            a0 = i * (ny + 1) + j
            fs.append((a0, a0 + ny + 1, a0 + ny + 2, a0 + 1))
    return mesh_obj(name, vs, fs, m)


def hull_mesh(name, m, morph=1.0, nx=130, depth=19.0, half=False):
    """the hull below the flight deck: flared sides from the deck edge to the keel"""
    vs, fs = [], []
    ring = 7
    for i in range(nx + 1):
        x = L * i / nx
        hw = half_width(x)
        z0 = ramp_z(x, morph) - 0.4
        bow = smooth((x - 200) / 62)
        stern = 1 - smooth(x / 30)
        wl = hw * (0.78 - 0.45 * bow - 0.08 * stern)
        pts = [(hw, z0), (hw * 0.98, z0 - 3), (wl + 2, -12), (wl, -depth + 2), (wl * 0.6, -depth), (0.0, -depth - 0.5)]
        side = pts + [(-p[0], p[1]) for p in reversed(pts[:-1])]
        if half:
            side = [(p[0], p[1]) for p in side if p[0] >= -0.01]
        for (y, z) in side:
            vs.append((x, y, z))
    ring = len(vs) // (nx + 1)
    for i in range(nx):
        for j in range(ring - 1):
            a0 = i * ring + j
            fs.append((a0, a0 + 1, a0 + ring + 1, a0 + ring))
    return mesh_obj(name, vs, fs, m)


def strip(name, m, x0, x1, y, w, morph=1.0, dash=None, lift=0.03, seg=1.0):
    """a painted line on the deck (follows the ramp); dash=(on, off) metres"""
    vs, fs = [], []
    x = x0
    while x < x1:
        xe = min(x1, x + (dash[0] if dash else seg))
        n = max(1, int((xe - x) / 0.8))
        base = len(vs)
        for k in range(n + 1):
            xx = x + (xe - x) * k / n
            z = ramp_z(xx, morph) + lift
            vs += [(xx, y - w / 2, z), (xx, y + w / 2, z)]
        for k in range(n):
            b = base + 2 * k
            fs.append((b, b + 2, b + 3, b + 1))
        x = xe + (dash[1] if dash else 0)
    return mesh_obj(name, vs, fs, m)


def deck_paint():
    deck = mat("deck", (0.055, 0.058, 0.062), 0.82)
    noise_bump(deck, 900, 0.35, detail=4)
    nt = deck.node_tree
    n = nt.nodes.new("ShaderNodeTexNoise")
    n.inputs["Scale"].default_value = 0.08
    n.inputs["Detail"].default_value = 6
    cr = nt.nodes.new("ShaderNodeValToRGB")
    cr.color_ramp.elements[0].color = (0.045, 0.047, 0.05, 1)
    cr.color_ramp.elements[1].color = (0.09, 0.09, 0.095, 1)
    nt.links.new(n.outputs["Fac"], cr.inputs["Fac"])
    nt.links.new(cr.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
    return deck


def build_ship(morph=1.0, half=False, island=True):
    deck = deck_paint()
    hull = mat("hull", (0.30, 0.31, 0.33), 0.55, metal=0.2)
    noise_bump(hull, 40, 0.08)
    white = mat("white", (0.8, 0.8, 0.78), 0.6)
    red = mat("red", (0.55, 0.05, 0.04), 0.6)
    yel = mat("yellow", (0.75, 0.55, 0.05), 0.6)
    objs = {"deck": deck_mesh("deck", deck, morph)}
    objs["hull"] = hull_mesh("hull", hull, morph, half=half)
    # markings, from the Navy's footage: the white centreline, red-white and yellow dashed lines, the edge lines
    objs["paint"] = [
        strip("centre", white, 10, L - 2, 0, 0.5, morph, dash=(6, 4)),
        strip("edgeP", white, 8, 190, W / 2 - 4, 0.35, morph),
        strip("edgeS", white, 8, 190, -W / 2 + 4, 0.35, morph),
        strip("redP", red, 20, 200, 6, 0.6, morph, dash=(2, 2)),
        strip("yelS", yel, 20, 200, -9, 0.6, morph, dash=(2, 3)),
        strip("yelP", yel, 20, 200, 12, 0.6, morph, dash=(2, 3)),
    ]
    # yellow hatching near the island
    for k in range(14):
        strip(f"hatch{k}", yel, 60 + k * 1.6, 61 + k * 1.6, -W / 2 + 10, 6, morph)
    if island:
        grey = mat("island", (0.34, 0.35, 0.37), 0.5, metal=0.15)
        box("island1", (140, -W / 2 + 4, 9), (34, 7, 18), grey)
        box("island2", (125, -W / 2 + 4, 20), (14, 6, 8), grey)
        box("mast", (142, -W / 2 + 4, 27), (2, 2, 14), grey)
        box("radar", (142, -W / 2 + 4, 34), (5, 0.4, 2.2), grey)
    return objs


def sea(sc, size=1600):
    bpy.ops.mesh.primitive_plane_add(size=size, location=(L / 2, 0, -17))
    s = bpy.context.object
    o = s.modifiers.new("ocean", "OCEAN")
    o.geometry_mode = "DISPLACE"
    o.resolution = 12
    o.spatial_size = 120
    o.wave_scale = 0.9
    o.wind_velocity = 9
    o.random_seed = 7
    sub = s.modifiers.new("sub", "SUBSURF")
    sub.subdivision_type = "SIMPLE"
    sub.levels = sub.render_levels = 5
    s.modifiers.move(1, 0)
    wm = mat("sea", (0.02, 0.09, 0.13), 0.06)
    p = wm.node_tree.nodes["Principled BSDF"]
    p.inputs["Transmission Weight"].default_value = 0.0
    p.inputs["Specular IOR Level"].default_value = 0.6
    s.data.materials.append(wm)
    return o


def build_h1(a):
    sc, cam = setup(a, exposure=-0.2)
    sky_world(sc)
    shot = a.shot
    morph_f = (lambda f: smooth((f - 300) / 200)) if shot == "morph" else (lambda f: 1.0)
    state = {"ship": None}
    ocean = sea(sc)
    slot_m = mat("slot", (0.9, 0.7, 0.05), 0.4, emit=(1.0, 0.72, 0.08), strength=6)
    turb_m = [mat(f"turb{k}", (0.25, 0.22, 0.2), 0.4, metal=0.6, emit=(1.0, 0.55, 0.15), strength=0) for k in range(4)]
    fill_m = [mat(f"fill{k}", c, 0.7) for k, c in enumerate([(0.32, 0.33, 0.35), (0.42, 0.36, 0.28), (0.25, 0.27, 0.3)])]
    cut_m = mat("cutface", (0.62, 0.42, 0.18), 0.6, emit=(1.0, 0.62, 0.25), strength=0.4)

    def rebuild(m):
        for o in list(bpy.data.objects):
            if o.type == "MESH" and o.name not in ("Plane",):
                if o.name.startswith(("deck", "hull", "centre", "edge", "red", "yel", "hatch", "island", "mast", "radar",
                                      "slot", "turb", "fill", "cut")):
                    bpy.data.objects.remove(o, do_unlink=True)
        build_ship(m, half=(shot == "cutaway"))
        if shot == "morph":
            pass
        if shot == "cutaway":
            # the cut face along the centreline, warm; turbines amidships; the space under the ramp packed solid
            vs, fs = [], []
            for i in range(131):
                x = L * i / 130
                vs += [(x, 0.0, ramp_z(x) - 0.4), (x, 0.0, -19.0)]
            for i in range(130):
                b = 2 * i
                fs.append((b, b + 2, b + 3, b + 1))
            cf = mesh_obj("cutface", vs, fs, cut_m)
            cf.location.y = -0.05
            for k in range(4):
                cyl(f"turb{k}", (95 + k * 14, 3, -13), 1.6, 7, turb_m[k], rot=(0, math.pi / 2, 0), verts=32)
            random.seed(11)
            x = 186.0
            while x < 258:
                zt = ramp_z(x) - 1.0
                z = -16.0
                while z < zt - 1.0:
                    h = min(zt - z, 2.0 + random.random() * 2.5)
                    wd = 3 + random.random() * 4
                    box(f"fill{int(x)}_{int(z * 10)}", (x + wd / 2, 2.2, z + h / 2), (wd - 0.25, 4.2, h - 0.2),
                        fill_m[random.randrange(3)])
                    z += h
                x += 3 + random.random() * 3

    rebuild(morph_f(0))
    last = {"m": None}

    def frame(f):
        m = morph_f(f)
        if shot == "morph" and (last["m"] is None or abs(m - last["m"]) > 1e-4):
            rebuild(m)
            last["m"] = m
            for o in list(bpy.data.objects):
                if o.name.startswith("slotline"):
                    bpy.data.objects.remove(o, do_unlink=True)
            seal = smooth((f - 120) / 120)
            if seal < 0.999:
                s = strip("slotline", slot_m, 150 + (L - 152) * seal, L - 2, 0, 0.7, m, lift=0.05)
        ocean.time = 2.0 + f / FPS
        if shot == "deck":
            x = keys(f, [(0, 165.0), (599, 214.0)])
            aim_cam(cam, (x, -6.0, 1.75), (L + 30, 2.0, 9.0), 30)
        elif shot == "ramp":
            x = keys(f, [(0, 222.0), (599, 256.0)])
            aim_cam(cam, (x, 9.0, ramp_z(x) + 0.55), (x + 40, -4, ramp_z(min(L, x + 40)) + 5), 24)
        elif shot == "morph":
            ang = keys(f, [(0, 0.0), (719, 0.18)])
            r = 150
            aim_cam(cam, (215 + r * math.sin(ang), 25 + r * math.cos(ang), 14), (220, 0, 0), 50)
        elif shot == "cutaway":
            for k in range(4):
                set_emit(turb_m[k], 6.0 * smooth((f - 60 - 50 * k) / 40))
            set_emit(cut_m, 0.4)
            px = keys(f, [(0, 120.0), (719, 205.0)])
            aim_cam(cam, (px, 95, 6), (px + 20, 0, -6), 45)

    render(sc, a, frame)


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
    box("deckL", (LEN / 2, -3.2, 3.0), (LEN + 4, 5.6, 0.35), deckm)
    box("deckR", (LEN / 2, 3.2, 3.0), (LEN + 4, 5.6, 0.35), deckm)
    box("trough", (LEN / 2, 0, 1.4), (LEN + 4, 1.6, 0.12), cutface)
    box("wallL", (LEN / 2, -0.85, 2.2), (LEN + 4, 0.1, 1.6), cutface)
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
    jetm = mat("jet", (0.42, 0.44, 0.46), 0.45, metal=0.3)
    jet = jet_silhouette("jet", jetm, 0.42)
    area((LEN / 2, -10, 10), (LEN / 2, 0, 2), 10, 3200, (1.0, 0.85, 0.65))
    area((LEN / 2 + 8, 8, 6), (LEN / 2, 0, 2), 6, 900, (0.7, 0.8, 1.0))

    def frame(f):
        t = smooth((f - 150) / 180)
        x = 1.0 + (LEN - 3.0) * (t ** 1.6)
        piston.location.x = x
        plume.scale.z = max(0.05, (x - 0.4))
        plume.location.x = 0.4 + (x - 0.4) / 2 - 0.6
        set_emit(steam, 7.0 * smooth((f - 130) / 25) * (1 - 0.6 * smooth((f - 360) / 120)))
        jet.location = (x + 2.0, 0, 4.2)
        cx = keys(f, [(0, 2.0), (150, 4.0), (330, LEN - 4.0), (599, LEN - 2.0)])
        aim_cam(cam, (cx - 6, -9.5, 6.5), (cx + 1.5, 0, 2.2), 32)

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
    iron = brushed_steel("drumsteel", (0.33, 0.30, 0.27), 0.45, stretch=4)
    noise_bump(iron, 25, 0.15)
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
    rivet = mat("rivet", (0.3, 0.28, 0.26), 0.4, metal=1.0)
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
        t = math.radians(-70 + random.uniform(-25, 25))
        pts = []
        for s in range(9):
            tt = t + s * 0.06 * random.choice((-1, 1)) * random.random() + s * 0.05
            xx = x + s * 0.05 * random.uniform(-1, 1)
            pts.append((xx, (R + 0.004) * math.cos(tt), 1.6 + (R + 0.004) * math.sin(tt)))
        cracks.append(crack_curve(f"crack{k}", crack_m[k], pts))
    # three steel bands, each a ring that comes down and ratchets tight
    band_m = brushed_steel("band", (0.55, 0.56, 0.58), 0.25, stretch=8)
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
        clamp = box(f"clamp{k}", (bx, 0, 1.6 + R + 0.12), (0.22, 0.3, 0.16), band_m)
        clamp.parent = b
        clamp.matrix_parent_inverse = b.matrix_world.inverted()
        bands.append(b)
    area((-3, -5, 5), (0, 0, 1.6), 5, 1500, (1.0, 0.82, 0.6))
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
    sc, cam = setup(a, exposure=-0.6)
    wall = mat("wall", (0.16, 0.15, 0.14), 0.8, metal=0.2)
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
    bulb.data.energy = 260
    bulb.data.color = (1.0, 0.72, 0.42)
    bulb.data.shadow_soft_size = 0.08
    cyl("bulbglass", (0.4, 0.6, 4.6), 0.06, 0.12, mat("bulbm", (1, 0.8, 0.5), 0.2, emit=(1, 0.75, 0.45), strength=30))
    area((-4, -3, 5.8), (0, 2, 1), 2, 120, (0.6, 0.72, 1.0))

    def frame(f):
        # the needle: from normal towards the red, a tremble, then it holds
        ang = keys(f, [(0, 120.0), (150, 110.0), (260, 8.0), (599, 6.0)])
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
    if a.shot in ("deck", "ramp", "morph", "cutaway"):
        build_h1(a)
    elif a.shot == "store":
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
