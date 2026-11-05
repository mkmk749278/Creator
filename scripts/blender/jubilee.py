"""The Jubilee diamond, built and lit in Blender Cycles (PLAYBOOK §8.7: a hero shot pre-rendered and composited).

Run with the pinned Blender module (bpy==4.2.0 in .venv-blender, Python 3.11):
  .venv-blender/bin/python scripts/blender/jubilee.py --shot hero --out DIR [--frames 0-359] [--w 1920 --h 1080]
      [--samples 64] [--still FRAME]

The stone: a cushion-shaped brilliant (the real Jubilee's outline, from the Commons photo "Mouawad Jubilee", CC BY-SA
3.0, used as a shape reference only), modelled as the convex hull of facet rings (table, stars, upper girdle, girdle,
lower girdle, pavilion mains, culet), so every facet is truly flat. Diamond's dispersion (IOR 2.407 red → 2.451
violet) comes from three tinted glass shaders, red/green/blue, each with its own IOR. Light: a real photo studio (Poly Haven HDRI, CC0) seen only in the stone, a lamp pool on dark velvet, emissive
cards and small sparks for fire. It is labelled RECONSTRUCTION in
the film (CLAUDE.md honesty labels): the real stone is in a private collection.

Shots (all 60 fps, frame = time; camera moves are eased, never linear):
  hero      the cold open reveal (5 s): the camera pushes in low across the velvet and the stone turns 22°
  macro     (4 s) facets fill the frame; the light warms from white to furnace orange (signature 1, the match cut)
  table     (5 s) top-down on the table facet, slow rotation (the ownership machine's glint, the last shot of the film)
"""
import argparse
import math
import sys

import bpy  # noqa: I001 (bpy first: it makes bmesh importable)
import bmesh
from mathutils import Vector

DISPERSION = {"R": 2.407, "G": 2.419, "B": 2.451}  # diamond: IOR at ~687 nm, ~546 nm, ~431 nm


def ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * t * (t * (6 * t - 15) + 10)  # smootherstep


def superellipse(theta: float, a: float = 1.0, b: float = 0.86, n: float = 3.2) -> Vector:
    c, s = math.cos(theta), math.sin(theta)
    r = (abs(c / a) ** n + abs(s / b) ** n) ** (-1 / n)
    return Vector((r * c, r * s, 0.0))


def ring(count: int, scale: float, z: float, offset: float = 0.0) -> list[Vector]:
    pts = []
    for i in range(count):
        th = 2 * math.pi * (i + offset) / count
        p = superellipse(th) * scale
        pts.append(Vector((p.x, p.y, z)))
    return pts


def build_gem() -> bpy.types.Object:
    crown_h, pav_d = 0.32, 0.86
    cz = lambda s: crown_h * (1 - s) / 0.45  # height on the crown cone for a ring at scale s (table at 0.55)
    pz = lambda s: -pav_d * (1 - s)  # depth on the pavilion cone
    pts = []
    pts += ring(8, 0.55, crown_h, 0.0)  # table
    pts += ring(8, 0.74, cz(0.74) + 0.028, 0.5)  # stars (raised: kites form between them and the table)
    pts += ring(16, 0.93, cz(0.93) + 0.012, 0.25)  # upper girdle
    pts += ring(48, 1.0, 0.012, 0.0) + ring(48, 1.0, -0.012, 0.0)  # girdle band
    pts += ring(16, 0.80, pz(0.80) - 0.018, 0.25)  # lower girdle (bulged out: halves form)
    pts += ring(8, 0.42, pz(0.42) - 0.03, 0.0)  # pavilion mains
    pts += [Vector((0.0, 0.0, -pav_d))]  # culet
    me = bpy.data.meshes.new("Jubilee")
    bm = bmesh.new()
    vs = [bm.verts.new(p) for p in pts]
    bmesh.ops.convex_hull(bm, input=vs)
    bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(0.5), verts=bm.verts, edges=bm.edges)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = False
    ob = bpy.data.objects.new("Jubilee", me)
    bpy.context.collection.objects.link(ob)
    ob.data.materials.append(diamond_material())
    return ob


def diamond_material() -> bpy.types.Material:
    m = bpy.data.materials.new("Diamond")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    adds = []
    for ch, ior in DISPERSION.items():
        g = nt.nodes.new("ShaderNodeBsdfGlass")
        g.inputs["IOR"].default_value = ior
        g.inputs["Roughness"].default_value = 0.0
        g.inputs["Color"].default_value = {"R": (1, 0, 0, 1), "G": (0, 1, 0, 1), "B": (0, 0, 1, 1)}[ch]
        adds.append(g)
    a1 = nt.nodes.new("ShaderNodeAddShader")
    a2 = nt.nodes.new("ShaderNodeAddShader")
    nt.links.new(adds[0].outputs[0], a1.inputs[0])
    nt.links.new(adds[1].outputs[0], a1.inputs[1])
    nt.links.new(a1.outputs[0], a2.inputs[0])
    nt.links.new(adds[2].outputs[0], a2.inputs[1])
    nt.links.new(a2.outputs[0], out.inputs["Surface"])
    return m


def velvet_material(color=(0.022, 0.019, 0.017)) -> bpy.types.Material:
    m = bpy.data.materials.new("Velvet")
    m.use_nodes = True
    p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = (*color, 1)
    p.inputs["Roughness"].default_value = 0.95
    p.inputs["Specular IOR Level"].default_value = 0.0  # cloth has no shine; a rough specular would see the studio
    # Velvet's look (dark face-on, warm glow at grazing angles) built on the diffuse lobe: a sheen lobe would see the
    # studio that only the stone may see, and light the whole cloth evenly.
    nt = m.node_tree
    lw = nt.nodes.new("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = 0.55
    ramp = nt.nodes.new("ShaderNodeMix")
    ramp.data_type = "RGBA"
    ramp.inputs["A"].default_value = (*color, 1)
    ramp.inputs["B"].default_value = (0.11, 0.085, 0.068, 1)
    nt.links.new(lw.outputs["Facing"], ramp.inputs["Factor"])
    nt.links.new(ramp.outputs["Result"], p.inputs["Base Color"])
    # The pile: a fine fabric grain so the velvet reads as cloth, not as smooth plaster.
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 900.0
    nz.inputs["Detail"].default_value = 4.0
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.35
    bump.inputs["Distance"].default_value = 0.002
    nt.links.new(nz.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], p.inputs["Normal"])
    return m


def area(name, loc, target, size, energy, kelvin_rgb, shape="RECTANGLE"):
    d = bpy.data.lights.new(name, "AREA")
    d.energy, d.size, d.shape, d.color = energy, size, shape, kelvin_rgb
    o = bpy.data.objects.new(name, d)
    bpy.context.collection.objects.link(o)
    o.location = loc
    look(o, target)
    return o


def look(o, target):
    o.rotation_euler = (Vector(target) - o.location).to_track_quat("-Z", "Y").to_euler()


def panel(name, loc, target, size, strength, rgb):
    """An emissive card: invisible to the camera, seen only in the stone (and lighting the velvet softly)."""
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = (size[0], size[1], 1)
    look(o, target)
    o.rotation_euler.rotate_axis("X", math.pi)  # face the stone (planes emit along +Z; look() points -Z at it)
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs["Color"].default_value = (*rgb, 1)
    # Falloff across the card (bright core, soft edges) so the facets reflect a real softbox, not a flat white card.
    tc = nt.nodes.new("ShaderNodeTexCoord")
    grad = nt.nodes.new("ShaderNodeTexGradient")
    grad.gradient_type = "SPHERICAL"
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (1.6, 1.6, 1.6)
    mp.inputs["Location"].default_value = (0.0, 0.0, 0.0)
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    nt.links.new(mp.outputs[0], grad.inputs["Vector"])
    mul = nt.nodes.new("ShaderNodeMath")
    mul.operation = "MULTIPLY"
    mul.inputs[1].default_value = strength * 1.6
    nt.links.new(grad.outputs["Fac"], mul.inputs[0])
    nt.links.new(mul.outputs[0], e.inputs["Strength"])
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(e.outputs[0], out.inputs["Surface"])
    PANELS.append((e, rgb))
    o.data.materials.append(m)
    o.visible_camera = False
    o.visible_diffuse = False  # seen in the stone only; the velvet gets just the lamp pool
    return o


HDRI_DIR = "films/tata-history/assets/media/hdri"
HDRI_URL = "https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/2k/{}_2k.hdr"  # Poly Haven, CC0


def ensure_hdri(name: str) -> str:
    """The Poly Haven studio's 2k HDR on disk (fetched once): the path."""
    import os
    import urllib.request
    path = f"{HDRI_DIR}/{name}_2k.hdr"
    if not os.path.exists(path):
        os.makedirs(HDRI_DIR, exist_ok=True)
        urllib.request.urlretrieve(HDRI_URL.format(name), path)
    return path


def studio_world(w, name: str, strength: float) -> None:
    """A real photo studio (Poly Haven HDRI, CC0) that only the stone sees: reflection and refraction rays get the
    studio's softboxes, windows and dark gaps (the structure a flat card can't give), while camera and diffuse rays
    get near-black, so the backdrop stays dark and the velvet is lit only by the lamp pool."""
    import os
    import urllib.request
    path = f"{HDRI_DIR}/{name}_2k.hdr"
    if not os.path.exists(path):
        os.makedirs(HDRI_DIR, exist_ok=True)
        urllib.request.urlretrieve(HDRI_URL.format(name), path)
    nt = w.node_tree
    nt.nodes.clear()
    env = nt.nodes.new("ShaderNodeTexEnvironment")
    env.image = bpy.data.images.load(os.path.abspath(path))
    mp = nt.nodes.new("ShaderNodeMapping")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nt.links.new(tc.outputs["Generated"], mp.inputs["Vector"])
    nt.links.new(mp.outputs[0], env.inputs["Vector"])
    STUDIO.append(mp)
    bright = nt.nodes.new("ShaderNodeBackground")
    bright.inputs["Strength"].default_value = strength
    nt.links.new(env.outputs["Color"], bright.inputs["Color"])
    dark = nt.nodes.new("ShaderNodeBackground")
    dark.inputs["Color"].default_value = (0.004, 0.0035, 0.003, 1)
    lp = nt.nodes.new("ShaderNodeLightPath")
    mx = nt.nodes.new("ShaderNodeMath")
    mx.operation = "MAXIMUM"
    nt.links.new(lp.outputs["Is Camera Ray"], mx.inputs[0])
    nt.links.new(lp.outputs["Is Diffuse Ray"], mx.inputs[1])
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(mx.outputs[0], mix.inputs["Fac"])
    nt.links.new(bright.outputs[0], mix.inputs[1])
    nt.links.new(dark.outputs[0], mix.inputs[2])
    out = nt.nodes.new("ShaderNodeOutputWorld")
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    # The Light Path mix alone is not enough: direct light sampling of the world still reaches diffuse surfaces.
    w.cycles_visibility.diffuse = False
    w.cycles_visibility.camera = False


STUDIOS = {"hero": ("brown_photostudio_02", 1.6), "macro": ("brown_photostudio_02", 1.6), "table": ("studio_small_09", 1.0)}
STUDIO: list = []  # the studio's mapping node: turned slowly so the reflections travel across the facets
PANELS: list = []  # (emission node, base colour): the macro shot warms them to furnace orange
WARM = (1.0, 0.62, 0.32)  # ~2900 K lamp
EMBER = (1.0, 0.30, 0.04)
COOL = (0.75, 0.85, 1.0)


def scene(args):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s = bpy.context.scene
    s.render.engine = "CYCLES"
    s.cycles.device = "CPU"
    s.cycles.samples = args.samples
    s.cycles.use_denoising = True
    s.cycles.denoiser = "OPENIMAGEDENOISE"
    s.cycles.max_bounces = args.bounces
    s.cycles.transmission_bounces = args.bounces
    s.cycles.glossy_bounces = 8
    s.cycles.diffuse_bounces = 2
    s.cycles.denoising_prefilter = "ACCURATE"
    s.cycles.denoising_quality = "HIGH"
    s.cycles.use_adaptive_sampling = True
    s.cycles.adaptive_threshold = 0.006
    s.render.use_persistent_data = True  # keep the BVH between frames
    s.render.threads_mode = "FIXED"
    s.render.threads = args.threads  # leave a core free for Remotion stills while shots render in the background
    s.cycles.caustics_reflective = False
    s.cycles.caustics_refractive = False
    s.cycles.sample_clamp_indirect = 20
    s.render.resolution_x, s.render.resolution_y = args.w, args.h
    s.render.fps = 60
    s.view_settings.view_transform = "AgX"
    s.view_settings.look = "AgX - Punchy"
    s.render.film_transparent = False
    w = bpy.data.worlds.new("W")
    s.world = w
    w.use_nodes = True
    studio_world(w, args.hdri, args.hdri_strength)

    gem = build_gem()
    gem.scale = (0.5, 0.5, 0.5)
    gem.location = (0, 0, 0.0)
    gem.rotation_euler = (math.radians(0), 0, math.radians(8))

    # The open case: a velvet bed the stone sits in (crown up, tilted toward camera), inside a dark lid.
    bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, -0.39))  # wide: its edge never shows  # the culet sinks into the velvet
    bed = bpy.context.object
    bed.data.materials.append(velvet_material())
    bpy.ops.object.modifier_add(type="SUBSURF")
    tex = bpy.data.textures.new("Folds", "CLOUDS")
    tex.noise_scale = 3.0
    tex.noise_depth = 1
    bpy.ops.object.modifier_add(type="DISPLACE")
    bed.modifiers["Subdivision"].levels = bed.modifiers["Subdivision"].render_levels = 8
    bed.modifiers["Displace"].texture = tex
    bed.modifiers["Displace"].strength = 0.07
    for poly in bed.data.polygons:
        poly.use_smooth = True

    # Light, as a jeweller lights a stone: a diamond shows what surrounds it. Bright panels seen IN the facets
    # (emission planes, visible to reflection and refraction rays) with black gaps between them for contrast:
    # a white softbox overhead (the white table), warm strips at the sides (the lamp, later the furnace),
    # and small hard sources that throw the fire (dispersion needs small bright lights, not big soft ones).
    # The overhead softbox is a ring with a hole in the middle (as a jeweller shoots through the tent): the table
    # then shows the pavilion's black-and-white pattern instead of a flat white mirror.
    for i, a in enumerate(range(0, 360, 60)):
        r = math.radians(a)
        panel(f"Top{i}", (1.3 * math.cos(r), 1.3 * math.sin(r), 2.8), (0, 0, 0), (1.25, 0.8), args.top, (1, 0.97, 0.92))
    for i, a in enumerate(range(0, 360, 30)):
        r = math.radians(a + 15)
        panel(f"Strip{i}", (2.4 * math.cos(r), 2.4 * math.sin(r), 1.1), (0, 0, 0.2), (0.45, 1.8),
              9.0 if i % 2 else 4.0, WARM if i % 3 else (1, 0.92, 0.84))
    # The lamp: a soft spot whose pool fades to black, so the velvet falls off into darkness (no horizon line).
    kd = bpy.data.lights.new("Key", "SPOT")
    kd.energy, kd.color, kd.shadow_soft_size = args.key, (1.0, 0.80, 0.60), 0.9  # big soft source: a soft shadow
    kd.spot_size, kd.spot_blend = math.radians(args.pool), 1.0
    key = bpy.data.objects.new("Key", kd)
    bpy.context.collection.objects.link(key)
    key.location = (-1.0, -0.8, 2.4)
    look(key, (0, 0, 0))
    # Rim and sparks are for the stone only (glossy and refraction rays): the velvet stays in the lamp's pool.
    rim = area("Rim", (1.4, 2.2, 1.2), (0, 0, 0), 0.8, 80, COOL)
    rim.visible_diffuse = False
    for i, (x, y, z) in enumerate([(-0.6, -1.8, 1.9), (0.9, -1.4, 2.2), (0.2, -2.2, 1.0), (-1.2, 0.8, 1.6)]):
        area(f"Spark{i}", (x, y, z), (0, 0, 0), 0.04, 30, (1, 1, 1), "DISK").visible_diffuse = False

    cam_d = bpy.data.cameras.new("Cam")
    cam_d.lens = 85
    cam_d.dof.use_dof = True
    cam_d.dof.aperture_fstop = 2.0
    cam = bpy.data.objects.new("Cam", cam_d)
    bpy.context.collection.objects.link(cam)
    s.camera = cam
    return s, gem, cam, cam_d


def place_shot(shot, f, gem, cam, cam_d):
    t = f / 60.0
    for mp in STUDIO:  # the studio turns slowly, so reflections travel across the facets
        mp.inputs["Rotation"].default_value[2] = math.radians(30 * t)
    if shot == "hero":
        u = ease(t / 5.0)
        dist = 9.0 - 3.2 * u
        el = math.radians(24 - 6 * u)
        az = math.radians(-90 + 10 * u)
        cam.location = Vector((dist * math.cos(el) * math.cos(az), dist * math.cos(el) * math.sin(az), dist * math.sin(el)))
        look(cam, (0, 0, 0.02))
        cam_d.dof.focus_distance = (cam.location - Vector((0, 0, 0.05))).length
        gem.rotation_euler.z = math.radians(8 + 22 * ease(t / 5.0))
    if shot == "macro":
        # Signature 1: over the last 2 s every light in the room warms to furnace orange (then the film hard-cuts
        # to molten iron on the same colour).
        k = ease((t - 2.0) / 2.0)
        for e, rgb in PANELS:
            e.inputs["Color"].default_value = tuple((a + (b - a) * k) * (1 + 0.8 * k) for a, b in zip(rgb, EMBER)) + (1,)
    if shot == "macro":
        cam.location = Vector((0.0, -1.55, 1.45))
        look(cam, (0, 0, 0.05))
        cam_d.lens = 100
        cam_d.dof.focus_distance = (cam.location - Vector((0, 0, 0.12))).length
        gem.rotation_euler.z = math.radians(8 + 10 * ease(t / 4.0))
    elif shot == "table":
        cam.location = Vector((0.0, -0.05, 3.3))
        look(cam, (0, 0, 0))
        gem.rotation_euler.z = math.radians(8 + 20 * ease(t / 5.0))
        cam_d.dof.focus_distance = 3.15


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    ap = argparse.ArgumentParser()
    ap.add_argument("--shot", default="hero")
    ap.add_argument("--out", required=True)
    ap.add_argument("--frames", default="0-0")
    ap.add_argument("--still", type=int)
    ap.add_argument("--w", type=int, default=1920)
    ap.add_argument("--h", type=int, default=1080)
    ap.add_argument("--samples", type=int, default=64)
    ap.add_argument("--bounces", type=int, default=12)
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--hdri", help="Poly Haven studio; default per shot (see STUDIOS)")
    ap.add_argument("--hdri_strength", type=float)
    ap.add_argument("--top", type=float, default=2.0, help="overhead softbox ring strength")
    ap.add_argument("--key", type=float, default=400.0, help="lamp (spot) power, W")
    ap.add_argument("--pool", type=float, default=70.0, help="lamp cone, degrees: the lit pool on the velvet")
    ap.add_argument("--step", type=int, default=1, help="render every Nth frame (2 = 30 fps, blended to 60 in Remotion)")
    args = ap.parse_args(argv)
    # Per shot: the low hero and macro angles want the warm brown studio; top-down, its strip light crosses the table
    # facet like a scratch, so the table shot uses the small softbox studio, dimmer, for blacker contrast.
    hdri, strength = STUDIOS.get(args.shot, STUDIOS["hero"])
    args.hdri = args.hdri or hdri
    args.hdri_strength = args.hdri_strength if args.hdri_strength is not None else strength
    s, gem, cam, cam_d = scene(args)
    a, b = map(int, args.frames.split("-"))
    frames = [args.still] if args.still is not None else range(a, b + 1, args.step)
    import os
    os.makedirs(args.out, exist_ok=True)
    for f in frames:
        path = f"{args.out}/{args.shot}_{f:04d}.png"
        if os.path.exists(path):
            continue  # resumable: finished frames are skipped
        place_shot(args.shot, f, gem, cam, cam_d)
        s.render.filepath = path + ".tmp.png"
        bpy.ops.render.render(write_still=True)
        os.replace(path + ".tmp.png", path)
        print("frame", f, flush=True)


if __name__ == "__main__":
    main()
