"""H1 · The snorkel at night (aip-submarines, word_map.md; RECONSTRUCTION in the film).

  .venv-blender/bin/python scripts/blender/snorkel.py --shot a|b|c --out DIR --frames a-b --step 2 [--w 1920 --h 1080]

Shots (60 fps frame numbers, local to the shot; rendered every 2nd frame and blended to 60 in Remotion):
  a  (0-299)  "Night. The Arabian Sea.": black swell, a moon path, camera low on the water, drifting forward.
  b  (0-599)  "Raise the snorkel. A thin steel mast rises through black water. The diesel engines roar to life.":
              the mast breaks the surface at about frame 90 (on "rises"), stands at 260; foam at its foot; the camera
              eases back to a wider frame for the radar sweep the film draws on top.
  c  (0-299)  "And this time, the mast stays down.": the same sea, untouched; the camera sinks to the waterline.
The water is Blender's Ocean modifier (deterministic per time: no bake); the mast follows the Kalvari class's
snorkel head shape from photographs (a cylinder mast with a box head). Labels and the exhaust come from Remotion.
"""
import argparse
import math
import os
import sys

import bpy
from mathutils import Vector

FPS = 60


def args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shot", default="b")
    ap.add_argument("--out", required=True)
    ap.add_argument("--frames", default="0-0")
    ap.add_argument("--step", type=int, default=2)
    ap.add_argument("--w", type=int, default=1920)
    ap.add_argument("--h", type=int, default=1080)
    ap.add_argument("--samples", type=int, default=24)
    ap.add_argument("--bounces", type=int, default=6)
    ap.add_argument("--threads", type=int, default=0)
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    return ap.parse_args(argv)


def smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def lerp(a, b, t):
    return a + (b - a) * t


def keys(f, ks):
    """piecewise smooth interpolation over [(frame, value), ...]"""
    if f <= ks[0][0]:
        return ks[0][1]
    for (f0, v0), (f1, v1) in zip(ks, ks[1:]):
        if f <= f1:
            t = smooth((f - f0) / (f1 - f0))
            if isinstance(v0, tuple):
                return tuple(lerp(a, b, t) for a, b in zip(v0, v1))
            return lerp(v0, v1, t)
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


def build(a):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = a.samples
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.use_denoising = True
    sc.cycles.denoiser = "OPENIMAGEDENOISE"
    sc.cycles.max_bounces = a.bounces
    sc.cycles.glossy_bounces = 3
    sc.cycles.transmission_bounces = 2
    sc.cycles.seed = 11
    sc.render.resolution_x, sc.render.resolution_y = a.w, a.h
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_depth = "16"
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "AgX - Medium High Contrast"
    sc.view_settings.exposure = 0.2
    if a.threads:
        sc.render.threads_mode = "FIXED"
        sc.render.threads = a.threads

    # night sky: deep blue at the horizon, near black above; a faint haze band
    w = bpy.data.worlds.new("night")
    sc.world = w
    w.use_nodes = True
    nt = w.node_tree
    bg = nt.nodes["Background"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Normal"], sep.inputs["Vector"])  # world: the view direction
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs["From Min"].default_value = -0.02
    mr.inputs["From Max"].default_value = 0.45
    nt.links.new(sep.outputs["Z"], mr.inputs["Value"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[0].color = (0.010, 0.017, 0.032, 1)   # moonlit haze at the horizon
    ramp.color_ramp.elements[1].position = 1.0
    ramp.color_ramp.elements[1].color = (0.0015, 0.0025, 0.0055, 1)
    nt.links.new(mr.outputs["Result"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = 1.0

    # the moon: a small bright disc low ahead, and the sun lamp that makes its path on the water
    moon_dir = Vector((0.0, 1.0, math.tan(math.radians(6.5)))).normalized()
    bpy.ops.object.light_add(type="SUN")
    sun = bpy.context.object
    sun.data.energy = 1.0
    sun.data.color = (0.75, 0.84, 1.0)
    sun.data.angle = math.radians(0.25)
    sun.data.use_shadow = False  # moonlight on water reads as glitter, not cast shadows
    sun.rotation_euler = (-moon_dir).to_track_quat("-Z", "Y").to_euler()
    bpy.ops.mesh.primitive_uv_sphere_add(radius=6, location=moon_dir * 900)
    moon = bpy.context.object
    moon.data.materials.append(mat("moon", (0, 0, 0), 1, emit=(0.85, 0.9, 1.0), strength=2.5))
    moon.visible_shadow = False

    # the sea
    bpy.ops.mesh.primitive_plane_add(size=2)
    sea = bpy.context.object
    oc = sea.modifiers.new("ocean", "OCEAN")
    oc.geometry_mode = "GENERATE"
    oc.resolution = 20 if a.w >= 1920 else 12
    oc.spatial_size = 120
    oc.repeat_x = 3
    oc.repeat_y = 3
    oc.wave_scale = 1.15
    oc.choppiness = 1.1
    oc.wind_velocity = 9
    oc.wave_alignment = 0.35
    oc.wave_direction = math.radians(70)
    oc.random_seed = 4
    oc.use_normals = True
    sea.location = (-180, -60, 0)
    water = mat("water", (0.003, 0.006, 0.010), 0.05)
    water.node_tree.nodes["Principled BSDF"].inputs["IOR"].default_value = 1.333
    water.node_tree.nodes["Principled BSDF"].inputs["Specular IOR Level"].default_value = 0.6
    wn = water.node_tree
    rip = wn.nodes.new("ShaderNodeTexNoise")
    rip.inputs["Scale"].default_value = 2.2
    rip.inputs["Detail"].default_value = 10
    rip.inputs["Roughness"].default_value = 0.62
    wtc = wn.nodes.new("ShaderNodeTexCoord")
    wmap = wn.nodes.new("ShaderNodeMapping")
    wmap.inputs["Scale"].default_value = (0.35, 0.35, 0.35)
    wn.links.new(wtc.outputs["Object"], wmap.inputs["Vector"])
    wn.links.new(wmap.outputs["Vector"], rip.inputs["Vector"])
    bump = wn.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.9
    wn.links.new(rip.outputs["Fac"], bump.inputs["Height"])
    wn.links.new(bump.outputs["Normal"], wn.nodes["Principled BSDF"].inputs["Normal"])
    sea.data.materials.append(water)
    bpy.ops.object.shade_smooth()
    bpy.ops.mesh.primitive_plane_add(size=6000, location=(0, 2900, -0.15))
    far = bpy.context.object
    far.data.materials.append(water)

    # the snorkel mast and head (Kalvari class: a round mast, a box head with its float valve)
    steel = mat("mast", (0.03, 0.033, 0.037), 0.22, metal=0.75)
    parts = []
    bpy.ops.mesh.primitive_cylinder_add(radius=0.28, depth=7, location=(0, 0, -3.5), vertices=48)
    parts.append(bpy.context.object)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.55))
    head = bpy.context.object
    head.scale = (0.62, 0.46, 1.45)
    bpy.ops.object.modifier_add(type="BEVEL")
    head.modifiers["Bevel"].width = 0.16
    head.modifiers["Bevel"].segments = 5
    parts.append(head)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=0.35, location=(0.1, 0, 1.25), vertices=32)
    parts.append(bpy.context.object)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=2.2, location=(-1.6, 0, -0.6), vertices=24)  # periscope beside it
    peri = bpy.context.object
    parts.append(peri)
    for p in parts:
        p.data.materials.append(steel)
        bpy.context.view_layer.objects.active = p
        bpy.ops.object.shade_smooth()
    bpy.ops.object.empty_add(location=(0, 0, 0))
    rig = bpy.context.object
    for p in parts:
        p.parent = rig
    rig.location = (-4, 46, -6)
    rig.rotation_euler = (0, 0, math.radians(25))

    # foam collar where the mast cuts the water: a ring of rough white, opacity by noise
    foam = bpy.data.materials.new("foam")
    foam.use_nodes = True
    fn = foam.node_tree
    fp = fn.nodes["Principled BSDF"]
    fp.inputs["Base Color"].default_value = (0.55, 0.62, 0.7, 1)
    fp.inputs["Roughness"].default_value = 0.9
    noise = fn.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 22
    noise.inputs["Detail"].default_value = 8
    cr = fn.nodes.new("ShaderNodeValToRGB")
    cr.color_ramp.elements[0].position = 0.48
    cr.color_ramp.elements[1].position = 0.62
    fn.links.new(noise.outputs["Fac"], cr.inputs["Fac"])
    fn.links.new(cr.outputs["Color"], fp.inputs["Alpha"])
    foam.blend_method = "BLEND" if hasattr(foam, "blend_method") else None
    bpy.ops.mesh.primitive_circle_add(vertices=64, radius=0.6, fill_type="NGON", location=(0, 0, 0.05))
    collar = bpy.context.object
    collar.data.materials.append(foam)
    collar.parent = None

    bpy.ops.object.camera_add()
    cam = bpy.context.object
    sc.camera = cam
    cam.data.lens = 50
    cam.data.sensor_width = 36
    cam.data.dof.use_dof = True
    cam.data.dof.aperture_fstop = 5.6
    return sc, oc, rig, collar, cam


def pose(shot, f, oc, rig, collar, cam):
    t = f / FPS
    oc.time = 40 + t * 0.85
    mast_z = -9.0
    if shot == "b":
        # breaks the surface at ~90 (on "rises"), fully up by 260
        mast_z = keys(f, [(0, -6.5), (40, -6.0), (90, -1.2), (260, 2.2), (600, 2.35)])
    rig.location.z = mast_z
    rig.location.y = 46 - t * 0.9  # the boat makes way, slowly
    up = max(0.0, min(1.0, (mast_z + 1.4) / 2.5))
    collar.location = (rig.location.x, rig.location.y, 0.06)
    collar.scale = (0.2 + 1.1 * up, 0.2 + 1.6 * up, 1)
    collar.hide_render = up <= 0.02

    if shot == "a":
        loc = keys(f, [(0, (0, -2, 1.6)), (300, (0, 6, 1.9))])
        aim = (0, 120, 2.5)
        cam.data.lens = 40
    elif shot == "b":
        loc = keys(f, [(0, (-1.5, 18, 1.7)), (260, (-2, 14, 1.9)), (600, (-1.0, 4, 3.2))])
        aim = (rig.location.x, rig.location.y, keys(f, [(0, 0.2), (260, 1.2), (600, 1.4)]))
        cam.data.lens = keys(f, [(0, 70), (260, 62), (600, 40)])
    else:
        loc = keys(f, [(0, (0, -2, 2.4)), (300, (0, 4, 0.55))])
        aim = (0, 120, keys(f, [(0, 2.5), (300, 0.3)]))
        cam.data.lens = 38
    cam.location = loc
    d = Vector(aim) - Vector(loc)
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    cam.data.dof.focus_distance = max(2.0, d.length)


def main():
    a = args()
    sc, oc, rig, collar, cam = build(a)
    f0, f1 = map(int, a.frames.split("-"))
    os.makedirs(a.out, exist_ok=True)
    for f in range(f0, f1 + 1, a.step):
        pose(a.shot, f, oc, rig, collar, cam)
        sc.frame_set(0)
        bpy.context.view_layer.update()
        sc.render.filepath = os.path.join(os.path.abspath(a.out), f"{a.shot}_{f:04d}.png")
        bpy.ops.render.render(write_still=True)
        print(f"frame {a.shot} {f}", flush=True)


if __name__ == "__main__":
    main()
