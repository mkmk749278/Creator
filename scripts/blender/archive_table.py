"""The archive table (plan_v7 §2.3): one physically lit desk where every document, letter, quote, ledger and
calendar of the film lives, so they share one light and one world instead of floating on a dark grid.

  .venv-blender/bin/python scripts/blender/archive_table.py --out DIR [--angle top|three|low] [--w 4096 --h 2304]
      [--samples 160]

Per angle it writes:
  table_<angle>.png        the plate: an oiled teak desk, a dark green leather blotter, the warm pool of a brass
                           desk lamp (off frame, upper left), and at the edges, out of focus, a stack of archive
                           folders, an inkwell, a fountain pen and a reading glass. The blotter's centre is empty.
  table_<angle>_light.png  the light map: the same light falling on a white card where the document will lie (black
                           elsewhere), for the film to multiply over the document so it sits in the lamp's falloff.
  table_<angle>.json       the document card's four corners in output pixels (tl, tr, br, bl), for a CSS matrix3d,
                           and the card's size in cm.
Nothing on the table is a document: the film lays the real ones on it. Textures: Poly Haven (CC0).
"""
import argparse
import json
import math
import os
import sys

import bpy  # noqa: I001
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

sys.path.insert(0, os.path.dirname(__file__))
from counter import box, brass, cyl, fetch_tex, plain, tex_mat, uv_cube_project  # noqa: E402

LIGHT_CARD = (0.6, 0.44)  # the light pass's card: the blotter and a little beyond
CARD = (0.32, 0.22)  # the reference document card, metres (wider than A4 so letters, cards and ledgers all fit)

ANGLES = {
    # camera location, look-at, lens (mm), f-stop: all aimed at the blotter centre (0, 0, 0)
    'top': ((0.0, -0.2, 1.1), (0.0, 0.0, 0.0), 50, 2.8),
    'three': ((0.0, -0.78, 0.68), (0.0, 0.02, 0.0), 55, 2.4),
    'low': ((0.26, -0.98, 0.33), (0.0, 0.04, 0.0), 65, 2.0),
}


def leather():
    m = tex_mat('Blotter', None, 'leather_red_02_rough.jpg', 'leather_red_02_nor.jpg', scale=3.0, color=(0.018, 0.035, 0.026), rough_k=0.85)
    return m


def paper_mat(name, tint):
    m = plain(name, tint, rough=0.85)
    nt = m.node_tree
    nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 40
    nz.inputs['Detail'].default_value = 8
    mix = nt.nodes.new('ShaderNodeMix')
    mix.data_type = 'RGBA'
    mix.blend_type = 'MULTIPLY'
    mix.inputs['Factor'].default_value = 0.25
    mix.inputs[6].default_value = (*tint, 1)
    nt.links.new(nz.outputs['Color'], mix.inputs[7])
    nt.links.new(mix.outputs[2], nt.nodes['Principled BSDF'].inputs['Base Color'])
    return m


def build(a):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s = bpy.context.scene
    s.render.engine = 'CYCLES'
    s.cycles.device = 'CPU'
    s.cycles.samples = a.samples
    s.cycles.use_denoising = True
    s.cycles.denoiser = 'OPENIMAGEDENOISE'
    s.cycles.use_adaptive_sampling = True
    s.render.resolution_x, s.render.resolution_y = a.w, a.h
    s.view_settings.view_transform = 'AgX'
    s.view_settings.look = 'AgX - Medium High Contrast'
    s.render.image_settings.color_depth = '16'
    w = bpy.data.worlds.new('W')
    s.world = w
    w.use_nodes = True
    w.node_tree.nodes['Background'].inputs[0].default_value = (0.004, 0.0045, 0.006, 1)

    teak = tex_mat('Teak', 'smoked_walnut_veneer_diff.jpg', 'smoked_walnut_veneer_rough.jpg', 'smoked_walnut_veneer_nor.jpg',
                   scale=1.1, tint=(0.36, 0.2, 0.11), rough_k=0.55)
    br = brass()

    # desk top (surface z = 0), big enough to fill every angle
    top = box('Desk', (2.4, 1.6, 0.04), (0, 0.25, -0.02), teak, bevel=0.004)
    uv_cube_project(top, 0.9)
    # leather blotter with a thin raised edge (surface z = 0.004)
    blot = box('Blotter', (0.5, 0.36, 0.004), (0, 0.0, 0.002), leather(), bevel=0.0015)
    uv_cube_project(blot, 0.5)
    for sx in (-1, 1):  # leather end-pieces, like a real desk blotter
        e = box(f'BlotEnd{sx}', (0.07, 0.36, 0.007), (sx * 0.285, 0.0, 0.0035), plain('EndLeather', (0.05, 0.022, 0.012), rough=0.45), bevel=0.002)

    # out-of-focus props at the edges: a stack of archive folders (upper left), an inkwell and a pen (right),
    # a reading glass (lower left)
    for i, (dx, dy, rz, t) in enumerate([(0, 0, 4, (0.42, 0.33, 0.2)), (0.01, -0.008, -3, (0.33, 0.24, 0.14)), (-0.006, 0.006, 7, (0.46, 0.36, 0.22))]):
        f = box(f'Folder{i}', (0.36, 0.26, 0.012), (-0.42 + dx, 0.27 + dy, 0.006 + i * 0.013), paper_mat(f'Card{i}', t), bevel=0.002, rot=(0, 0, math.radians(rz)))
    tie = box('Tape', (0.02, 0.27, 0.003), (-0.4, 0.27, 0.046), plain('Tape', (0.32, 0.05, 0.03), rough=0.7))
    glass = plain('Glass', (0.9, 0.9, 0.9), rough=0.02, transmission=1.0, ior=1.5)
    cyl('Inkwell', 0.035, 0.05, (0.37, 0.22, 0.025), glass, verts=8)
    cyl('Ink', 0.026, 0.03, (0.37, 0.22, 0.018), plain('Ink', (0.005, 0.008, 0.02), rough=0.1))
    cyl('InkCap', 0.02, 0.016, (0.37, 0.22, 0.058), br)
    pen = cyl('Pen', 0.0065, 0.15, (0.33, -0.17, 0.0068), plain('Lacquer', (0.012, 0.01, 0.01), rough=0.12), rot=(0, math.radians(90), math.radians(28)))
    cyl('PenBand', 0.0068, 0.01, (0.33 + 0.03 * math.cos(math.radians(28)), -0.17 + 0.03 * math.sin(math.radians(28)), 0.0068), br, rot=(0, math.radians(90), math.radians(28)))
    bpy.ops.mesh.primitive_torus_add(major_radius=0.045, minor_radius=0.004, location=(-0.37, -0.2, 0.005))
    ring = bpy.context.object
    ring.data.materials.append(br)
    cyl('Lens', 0.043, 0.004, (-0.37, -0.2, 0.005), glass, verts=48)
    cyl('Handle', 0.007, 0.11, (-0.37 + 0.1, -0.2 - 0.04, 0.007), plain('Horn', (0.06, 0.03, 0.015), rough=0.3), rot=(0, math.radians(90), math.radians(-22)))
    # the lamp: a brass base and green shade just off frame upper left; its bulb is the key light
    cyl('LampBase', 0.08, 0.02, (-0.66, 0.5, 0.01), br, verts=48)
    cyl('LampStem', 0.008, 0.36, (-0.66, 0.5, 0.19), br)
    shade = cyl('Shade', 0.11, 0.07, (-0.54, 0.38, 0.38), plain('ShadeGlass', (0.02, 0.12, 0.05), rough=0.25), rot=(math.radians(-25), math.radians(20), 0), verts=48)
    bpy.ops.object.light_add(type='SPOT', location=(-0.5, 0.34, 0.35))
    key = bpy.context.object
    key.data.energy = 85
    key.data.color = (1.0, 0.72, 0.42)
    key.data.spot_size = math.radians(72)
    key.data.spot_blend = 1.0
    # v8: a bulb the size of the shade's mouth, not a point: at 0.04 the folder stack threw a dead-black, hard-edged
    # shadow that read as a black notched block at the frame's edge (outside review B)
    key.data.shadow_soft_size = 0.26
    key.rotation_euler = (Vector((0.02, -0.03, 0)) - key.location).to_track_quat('-Z', 'Y').to_euler()
    # a faint cool window fill from the right, so the shadows are not dead black
    bpy.ops.object.light_add(type='AREA', location=(1.2, -0.3, 1.0))
    fill = bpy.context.object
    fill.data.energy = 18
    fill.data.size = 1.2
    fill.data.color = (0.55, 0.68, 0.9)
    fill.rotation_euler = (Vector((0, 0, 0)) - fill.location).to_track_quat('-Z', 'Y').to_euler()

    # the reference card where documents lie (only visible in the light pass)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0.0045))
    card = bpy.context.object
    card.name = 'Card'
    card.scale = (CARD[0], CARD[1], 1)
    bpy.ops.object.transform_apply(scale=True)
    card.data.materials.append(plain('White', (0.8, 0.8, 0.8), rough=0.9))
    card.hide_render = True
    return s, card


def camera(s, angle):
    loc, look, lens, fstop = ANGLES[angle]
    bpy.ops.object.camera_add(location=loc)
    cam = bpy.context.object
    cam.rotation_euler = (Vector(look) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    cam.data.lens = lens
    cam.data.dof.use_dof = True
    cam.data.dof.focus_distance = (Vector(look) - Vector(loc)).length
    cam.data.dof.aperture_fstop = fstop
    s.camera = cam
    return cam


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--angle', default='top', choices=list(ANGLES))
    ap.add_argument('--w', type=int, default=4096)
    ap.add_argument('--h', type=int, default=2304)
    ap.add_argument('--samples', type=int, default=160)
    ap.add_argument('--skip-light', action='store_true')
    ap.add_argument('--gain', type=float, default=0.33, help='linear exposure gain on the plate (not the light pass)')
    a = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else None)
    os.makedirs(a.out, exist_ok=True)
    s, card = build(a)
    cam = camera(s, a.angle)
    s.render.filepath = os.path.abspath(f'{a.out}/table_{a.angle}.png')
    bpy.ops.render.render(write_still=True)
    if a.gain != 1.0:
        # v8: the softer, larger bulb lights the whole desk more; bring the plate back to the v7 exposure (blotter
        # centre ~33/255) on the output, in linear light, so a hundred desk shots keep their mood
        from PIL import Image
        import numpy as np
        im = Image.open(s.render.filepath)
        px = np.asarray(im).astype(np.float32)
        px[..., :3] = np.clip(((px[..., :3] / 255) ** 2.2 * a.gain) ** (1 / 2.2) * 255 + 0.5, 0, 255)
        Image.fromarray(px.astype(np.uint8), im.mode).save(s.render.filepath)
    # corners of the card in output pixels (y down), for the film's matrix3d
    corners = []
    for v in [(-0.5, 0.5), (0.5, 0.5), (0.5, -0.5), (-0.5, -0.5)]:  # tl, tr, br, bl as seen from the front
        p = card.matrix_world @ Vector((v[0] * CARD[0], v[1] * CARD[1], 0))
        c = world_to_camera_view(s, cam, p)
        corners.append([round(c.x * a.w, 2), round((1 - c.y) * a.h, 2)])
    meta = {'angle': a.angle, 'px': [a.w, a.h], 'card_cm': [CARD[0] * 100, CARD[1] * 100], 'corners': corners}
    with open(f'{a.out}/table_{a.angle}.json', 'w') as f:
        json.dump(meta, f, indent=1)
    print(json.dumps(meta))
    if a.skip_light:
        return
    # light pass: everything black and matte except the white card, same lights and camera
    black = plain('Black', (0, 0, 0), rough=1.0)
    for o in s.objects:
        if o.type == 'MESH' and o.name != 'Card':
            o.data.materials.clear()
            o.data.materials.append(black)
            o.visible_shadow = o.name.startswith(('Pen', 'Ink', 'Lens', 'Handle'))  # props near the card may shade it
    # light the whole blotter, not just the reference card, so a larger document still gets the lamp's falloff
    card.scale = (LIGHT_CARD[0] / CARD[0], LIGHT_CARD[1] / CARD[1], 1)
    card.hide_render = False
    cam.data.dof.use_dof = False
    s.cycles.samples = max(32, a.samples // 4)
    s.view_settings.view_transform = 'Standard'
    s.view_settings.look = 'None'
    s.render.filepath = os.path.abspath(f'{a.out}/table_{a.angle}_light.png')
    bpy.ops.render.render(write_still=True)


if __name__ == '__main__':
    main()
