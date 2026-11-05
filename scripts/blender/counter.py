"""The 1924 bank counter (RECONSTRUCTION), rendered as stills for the film's recurring counter shot (plan_v6 §1).

  .venv-blender/bin/python scripts/blender/counter.py --out DIR [--w 3840 --h 2160] [--samples 96] [--layer plate|case|both]
  .venv-blender/bin/python scripts/blender/counter.py --shot c1|c2|c3 --out DIR --frames a-b --step 2 [--w 1920 --h 1080]

Shots (60 fps frame numbers, local to the cold-open shot; rendered every 2nd frame and blended to 60 in Remotion):
  c1  (0-210)  "A man walks into a bank, carrying his wife's diamond": the camera settles low at the counter as the
      case slides into the lamp pool, landing on "diamond" (frame 155)
  c2  (0-323)  "Is he here to sell it? No. He wants a loan, with the diamond as the guarantee": a slow push in; on
      "the diamond as the guarantee" (222-290) the lid opens and the stone catches the lamp
  c3  (0-122)  "The answer is in this bank": a glide along the counter toward the closed case

Writes, per layer, a 16-bit PNG and a depth map (<name>_depth.png, white = near, for DepthPhoto's camera move):
  plate   the counter: mahogany top, a brass teller grille with an arched window, a green-shaded banker's lamp throwing
          a warm pool, an open ruled ledger (no writing: it is set dressing, never a document), inkwell and pen,
          a panelled wall behind with out-of-focus lamps.
  case    the jewellery case alone (closed), on a transparent background with its contact shadow (shadow catcher),
          so the film can slide it into the lamp pool.
Textures: Poly Haven (CC0): smoked_walnut_veneer, dark_paneled_wood, leather_red_02 (normal only), velour_velvet.
A 1920s Indian bank interior is drawn from period photos of Bombay banks (teak/mahogany counters, brass grilles);
nothing here claims to be the Imperial Bank's actual counter, and the film labels the shot RECONSTRUCTION.
"""
import argparse
import math
import os
import sys

import bpy  # noqa: I001
from mathutils import Vector

TEX = "films/tata-history/assets/media/tex"
PH = "https://dl.polyhaven.org/file/ph-assets/Textures/jpg/2k/{asset}/{asset}_{kind}_2k.jpg"  # Poly Haven, CC0


def fetch_tex(name):
    """Poly Haven textures are not in git (large media): fetch a missing one, e.g. on a GitHub runner."""
    path = f"{TEX}/{name}"
    if not os.path.exists(path):
        import urllib.request
        asset, kind = name[:-4].rsplit("_", 1)
        os.makedirs(TEX, exist_ok=True)
        urllib.request.urlretrieve(PH.format(asset=asset, kind={"nor": "nor_gl"}.get(kind, kind)), path)
    return path


def tex_mat(name, base, rough=None, nor=None, scale=1.0, tint=(1, 1, 1), rough_k=1.0, metallic=0.0, color=None):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    p = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (scale, scale, scale)
    nt.links.new(tc.outputs["UV"], mp.inputs["Vector"])

    def img(path, non_color=False):
        t = nt.nodes.new("ShaderNodeTexImage")
        t.image = bpy.data.images.load(os.path.abspath(fetch_tex(os.path.basename(path))))
        if non_color:
            t.image.colorspace_settings.name = "Non-Color"
        nt.links.new(mp.outputs[0], t.inputs["Vector"])
        return t

    if base:
        b = img(f"{TEX}/{base}")
        mix = nt.nodes.new("ShaderNodeMix")
        mix.data_type = "RGBA"
        mix.blend_type = "MULTIPLY"
        mix.inputs["Factor"].default_value = 1.0
        mix.inputs[7].default_value = (*tint, 1)
        nt.links.new(b.outputs["Color"], mix.inputs[6])
        nt.links.new(mix.outputs[2], p.inputs["Base Color"])
    elif color:
        p.inputs["Base Color"].default_value = (*color, 1)
    if rough:
        r = img(f"{TEX}/{rough}", True)
        mm = nt.nodes.new("ShaderNodeMath")
        mm.operation = "MULTIPLY"
        mm.inputs[1].default_value = rough_k
        nt.links.new(r.outputs["Color"], mm.inputs[0])
        nt.links.new(mm.outputs[0], p.inputs["Roughness"])
    if nor:
        n = img(f"{TEX}/{nor}", True)
        nm = nt.nodes.new("ShaderNodeNormalMap")
        nt.links.new(n.outputs["Color"], nm.inputs["Color"])
        nt.links.new(nm.outputs[0], p.inputs["Normal"])
    p.inputs["Metallic"].default_value = metallic
    return m


def plain(name, color, rough=0.5, metallic=0.0, emission=None, strength=0.0, transmission=0.0, ior=1.45):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = (*color, 1)
    p.inputs["Roughness"].default_value = rough
    p.inputs["Metallic"].default_value = metallic
    p.inputs["Transmission Weight"].default_value = transmission
    p.inputs["IOR"].default_value = ior
    if emission:
        p.inputs["Emission Color"].default_value = (*emission, 1)
        p.inputs["Emission Strength"].default_value = strength
    return m


def brass():
    m = plain("Brass", (0.78, 0.56, 0.28), rough=0.28, metallic=1.0)
    nt = m.node_tree
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 60
    ramp = nt.nodes.new("ShaderNodeMapRange")
    ramp.inputs["To Min"].default_value = 0.18
    ramp.inputs["To Max"].default_value = 0.42
    nt.links.new(nz.outputs["Fac"], ramp.inputs["Value"])
    nt.links.new(ramp.outputs[0], nt.nodes["Principled BSDF"].inputs["Roughness"])
    return m


def box(name, size, loc, mat, bevel=0.0, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.scale = size
    bpy.ops.object.transform_apply(scale=True)
    if bevel:
        mod = o.modifiers.new("Bevel", "BEVEL")
        mod.width = bevel
        mod.segments = 3
    bpy.ops.object.shade_smooth() if bevel else None
    bpy.ops.uv.smart_project() if False else None
    o.data.materials.append(mat)
    return o


def cyl(name, r, depth, loc, mat, rot=(0, 0, 0), verts=24):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc, rotation=rot, vertices=verts)
    o = bpy.context.object
    o.name = name
    bpy.ops.object.shade_smooth()
    o.data.materials.append(mat)
    return o


def uv_cube_project(o, scale=1.0):
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.cube_project(cube_size=scale)
    bpy.ops.object.mode_set(mode="OBJECT")
    o.select_set(False)


def ledger_page_image(path):
    """A blank ruled ledger page (columns and lines only, no writing): set dressing, never a document."""
    from PIL import Image, ImageDraw  # Pillow is in the Blender venv's site? fall back to Blender's own drawing
    w, h = 1400, 1800
    im = Image.new("RGB", (w, h), (214, 198, 164))
    d = ImageDraw.Draw(im)
    for y in range(160, h - 60, 44):
        d.line([(40, y), (w - 40, y)], fill=(150, 170, 190), width=2)
    for x in (180, 210, w - 380, w - 350, w - 200):
        d.line([(x, 120), (x, h - 60)], fill=(190, 90, 80), width=3)
    d.line([(40, 130), (w - 40, 130)], fill=(190, 90, 80), width=4)
    im.save(path)


def build(args):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s = bpy.context.scene
    s.render.engine = "CYCLES"
    s.cycles.device = "CPU"
    s.cycles.samples = args.samples
    s.cycles.use_denoising = True
    s.cycles.use_adaptive_sampling = True
    s.render.resolution_x, s.render.resolution_y = args.w, args.h
    s.view_settings.view_transform = "AgX"
    s.view_settings.look = "AgX - Medium High Contrast"
    s.render.image_settings.color_depth = "16"
    s.view_layers[0].use_pass_z = True
    w = bpy.data.worlds.new("W")
    s.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.002, 0.0018, 0.0015, 1)

    mahog = tex_mat("Mahogany", "smoked_walnut_veneer_diff.jpg", "smoked_walnut_veneer_rough.jpg", "smoked_walnut_veneer_nor.jpg",
                    scale=1.4, tint=(0.13, 0.06, 0.038), rough_k=0.6)
    panel = tex_mat("Panels", "dark_paneled_wood_diff.jpg", "dark_paneled_wood_rough.jpg", "dark_paneled_wood_nor.jpg",
                    scale=0.6, tint=(0.35, 0.22, 0.15))
    br = brass()

    # Counter top (top surface at z = 0), front moulding toward the camera.
    top = box("CounterTop", (3.2, 1.0, 0.05), (0, 0.2, -0.025), mahog, bevel=0.006)
    uv_cube_project(top, 1.0)
    front = box("CounterFront", (3.2, 0.06, 0.9), (0, -0.33, -0.48), mahog, bevel=0.01)
    uv_cube_project(front, 1.0)

    # Brass teller grille on the far edge, with an arched window in the middle.
    gy = 0.52
    box("GrilleSill", (3.2, 0.09, 0.03), (0, gy, 0.015), br, bevel=0.004)
    box("GrilleRail", (3.2, 0.05, 0.03), (0, gy, 0.72), br, bevel=0.004)
    for i in range(-24, 25):
        x = i * 0.062
        if abs(x) < 0.3:  # the window
            continue
        cyl(f"Bar{i}", 0.0065, 0.7, (x, gy, 0.365), br)
    # the arch over the window: one smooth brass rail (a bevelled curve)
    cu = bpy.data.curves.new("ArchCurve", "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = 0.009
    cu.bevel_resolution = 4
    sp = cu.splines.new("POLY")
    pts = [(0.3 * math.cos(math.pi * k / 48), gy, 0.42 + 0.22 * math.sin(math.pi * k / 48)) for k in range(49)]
    sp.points.add(len(pts) - 1)
    for pt, (x, y, z) in zip(sp.points, pts):
        pt.co = (x, y, z, 1)
    arch = bpy.data.objects.new("Arch", cu)
    s.collection.objects.link(arch)
    arch.data.materials.append(br)
    for x in (-0.3, 0.3):
        cyl(f"Jamb{x}", 0.012, 0.42, (x, gy, 0.21), br)

    # Back wall: dark panelling, with a few warm out-of-focus lamps (bokeh) further back.
    wall = box("Wall", (6, 0.05, 3), (0, 2.4, 0.8), panel)
    uv_cube_project(wall, 1.0)
    for i, (x, z) in enumerate([(-1.4, 0.75), (1.1, 0.9), (2.0, 0.55), (-0.4, 1.15), (0.55, 0.62)]):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.035, location=(x, 2.2, z))
        o = bpy.context.object
        o.data.materials.append(plain(f"Bulb{i}", (1, 0.7, 0.4), emission=(1, 0.55, 0.25), strength=14))

    # Banker's lamp, left: brass base and stem, green glass shade glowing from inside, a warm pool on the counter.
    lx, ly = -0.62, 0.18
    cyl("LampBase", 0.075, 0.025, (lx, ly, 0.0125), br, verts=48)
    cyl("LampStem", 0.009, 0.32, (lx, ly + 0.03, 0.17), br)
    green = plain("GreenGlass", (0.02, 0.22, 0.08), rough=0.08, emission=(0.1, 0.5, 0.2), strength=0.6)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=0.36, location=(lx, ly - 0.02, 0.34), rotation=(0, math.pi / 2, 0), vertices=48)
    shade = bpy.context.object
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.bisect(plane_co=(lx, ly - 0.02, 0.34), plane_no=(0, 0, 1), clear_inner=True)
    bpy.ops.object.mode_set(mode="OBJECT")
    mod = shade.modifiers.new("Solid", "SOLIDIFY")
    mod.thickness = 0.004
    bpy.ops.object.shade_smooth()
    shade.data.materials.append(green)
    lamp = bpy.data.lights.new("LampPool", "AREA")
    lamp.energy, lamp.size, lamp.color = 42, 0.4, (1.0, 0.64, 0.34)
    lamp.spread = math.radians(80)  # a cone: the pool, not a wash
    lo = bpy.data.objects.new("LampPool", lamp)
    s.collection.objects.link(lo)
    lo.location = (lx + 0.05, ly - 0.05, 0.31)
    lo.rotation_euler = (Vector((0.0, 0.02, 0.0)) - lo.location).to_track_quat("-Z", "Y").to_euler()  # the pool falls where the case will rest

    # The open ledger, right of centre: leather boards and two ruled pages (no writing).
    page_png = os.path.abspath(f"{TEX}/ledger_page.png")
    if not os.path.exists(page_png):
        ledger_page_image(page_png)
    paper = bpy.data.materials.new("LedgerPage")
    paper.use_nodes = True
    pn = paper.node_tree
    ti = pn.nodes.new("ShaderNodeTexImage")
    ti.image = bpy.data.images.load(page_png)
    pn.links.new(ti.outputs["Color"], pn.nodes["Principled BSDF"].inputs["Base Color"])
    pn.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.85
    leather = tex_mat("Leather", None, None, "leather_red_02_nor.jpg", scale=2, color=(0.12, 0.03, 0.025))
    bx, by = 0.42, 0.12
    for side in (-1, 1):
        box(f"Board{side}", (0.21, 0.29, 0.012), (bx + side * 0.108, by, 0.006), leather, bevel=0.003, rot=(0, math.radians(-side * 3), 0))
        bpy.ops.mesh.primitive_plane_add(size=1, location=(bx + side * 0.103, by, 0.0165), rotation=(0, math.radians(-side * 3.5), 0))
        pg = bpy.context.object
        pg.scale = (0.2, 0.28, 1)
        pg.data.materials.append(paper)
    box("Inkwell", (0.05, 0.05, 0.045), (0.72, 0.24, 0.0225), plain("Glass", (0.9, 0.95, 1), rough=0.02, transmission=1.0), bevel=0.006)
    cyl("Pen", 0.004, 0.16, (0.6, 0.0, 0.005), plain("PenBlack", (0.01, 0.01, 0.01), rough=0.2), rot=(math.radians(90), 0, math.radians(62)))

    # Fill: a dim cool window light from the right, so the brass has a second highlight.
    fill = bpy.data.lights.new("Fill", "AREA")
    fill.energy, fill.size, fill.color = 30, 1.2, (0.75, 0.82, 1.0)
    fo = bpy.data.objects.new("Fill", fill)
    s.collection.objects.link(fo)
    fo.location = (1.9, -0.4, 1.2)
    fo.rotation_euler = (math.radians(60), 0, math.radians(60))

    # Camera: low across the counter, as if standing at it.
    cd = bpy.data.cameras.new("Cam")
    cd.lens = 32
    cd.dof.use_dof = True
    cd.dof.aperture_fstop = 1.6
    cam = bpy.data.objects.new("Cam", cd)
    s.collection.objects.link(cam)
    s.camera = cam
    cam.location = (0.04, -1.05, 0.36)
    target = Vector((0.0, 0.42, 0.2))
    cam.rotation_euler = (target - cam.location).to_track_quat("-Z", "Y").to_euler()
    cd.dof.focus_distance = (Vector((0, 0.0, 0.03)) - cam.location).length
    return s


def add_case(s, gem=False):
    """The jewellery case: dark leather outside, velvet lip, brass clasp; closed; at the lamp pool's centre.
    Returns (case root, lid hinge): move the root to slide the case, turn the hinge (−X) to open the lid."""
    velvet = tex_mat("CaseVelvet", "velour_velvet_diff.jpg", "velour_velvet_rough.jpg", "velour_velvet_nor.jpg", scale=6, tint=(0.002, 0.008, 0.06))  # deep navy velvet: the stone reads against it
    # velvet has no glossy coat: a rough dielectric specular turns it a pale grey under the lamp (as in jubilee.py)
    velvet.node_tree.nodes["Principled BSDF"].inputs["Specular IOR Level"].default_value = 0.0
    leather = tex_mat("CaseLeather", None, None, "leather_red_02_nor.jpg", scale=4, color=(0.014, 0.0025, 0.003))
    br = bpy.data.materials.get("Brass") or brass()
    cx, cy = 0.0, 0.0
    root = bpy.data.objects.new("CaseRoot", None)
    s.collection.objects.link(root)
    hinge = bpy.data.objects.new("CaseHinge", None)
    s.collection.objects.link(hinge)
    hinge.location = (cx, cy + 0.0585, 0.031)
    hinge.parent = root
    parts = [box("CaseBase", (0.15, 0.115, 0.03), (cx, cy, 0.015), leather, bevel=0.005),
             box("CaseLip", (0.146, 0.111, 0.004), (cx, cy, 0.031), velvet, bevel=0.001),
             box("Clasp", (0.02, 0.006, 0.012), (cx, cy - 0.06, 0.032), br, bevel=0.001)]
    for o in parts:
        o.parent = root  # box() bakes the position into the mesh (transform_apply), so the object sits at 0
    lid = box("CaseLid", (0.152, 0.117, 0.028), (cx, cy, 0.045), leather, bevel=0.005)
    lid.parent = hinge
    lid.location = (-hinge.location.x, -hinge.location.y, -hinge.location.z)  # its mesh already carries its place
    # the inside of the lid: ivory satin, as in a real jewellery case. Opened, it stands behind the stone, and the
    # crown's facets mirror it as bright planes (a leather lid there turns the stone grey)
    satin = plain("LidSatin", (0.64, 0.6, 0.5), rough=0.3)
    lining = box("LidLining", (0.142, 0.107, 0.002), (cx, cy, 0.0305), satin, bevel=0.0005)
    lining.parent = hinge
    lining.location = lid.location
    if gem:
        # The stone inside, on the velvet: the same cushion brilliant as the hero shot (scripts/blender/jubilee.py),
        # at its real size (about 38 mm across).
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import jubilee
        g = jubilee.build_gem()
        g.scale = (0.019, 0.019, 0.019)
        g.parent = root
        # sitting on the lining, not sunk into the solid case (a buried pavilion refracts grey velvet: a milky blob),
        # tipped toward the camera so the crown facets catch the sparks
        g.location = (cx, cy - 0.006, 0.048)
        # a small velvet cushion under it, as in a real jewellery case: the stone rests on it, its pavilion free
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(cx, cy - 0.004, 0.0335), segments=48, ring_count=24)
        pad = bpy.context.object
        pad.scale = (0.034, 0.03, 0.0045)
        bpy.ops.object.shade_smooth()
        pad.data.materials.append(velvet)
        pad.parent = root
        g.rotation_euler = (math.radians(-24), 0, math.radians(8))
        # Light the stone only (Cycles light linking): small hard sources for fire and a soft card for the table
        # flash, none of which touch the counter, so the room keeps its one lamp.
        only = bpy.data.collections.new("GemOnly")
        s.collection.children.link(only)
        only.objects.link(g)
        # small hard sources for fire, plus white cards either side (jeweller's lighting: the crown facets read as
        # bright planes against the dark velvet, not a grey blur)
        for i, (x, y, z, e, size) in enumerate([(-0.10, -0.16, 0.22, 60, 0.008), (0.14, -0.12, 0.18, 50, 0.008),
                                                 (0.02, -0.22, 0.12, 40, 0.006), (-0.16, 0.06, 0.20, 50, 0.01),
                                                 (0.06, 0.10, 0.16, 45, 0.008), (0.0, -0.05, 0.30, 14, 0.12),
                                                 (-0.18, -0.10, 0.10, 18, 0.07), (0.18, -0.08, 0.10, 18, 0.07),
                                                 (0.0, 0.10, 0.22, 16, 0.06)]):
            d = bpy.data.lights.new(f"GemLight{i}", "AREA")
            d.energy, d.size, d.color = e, size, (1.0, 0.95, 0.88)
            if size < 0.05:
                d.shape = "DISK"
            o = bpy.data.objects.new(f"GemLight{i}", d)
            s.collection.objects.link(o)
            o.location = (x, y, z)
            o.rotation_euler = (Vector((cx, cy, 0.036)) - o.location).to_track_quat("-Z", "Y").to_euler()
            o.light_linking.receiver_collection = only
        # A photo studio only the stone sees (as the hero shot's world, jubilee.py): an emissive sphere carrying the
        # Poly Haven HDRI, invisible to the camera, to shadows and to diffuse rays, and light-linked to the stone, so
        # its facets break into the studio's softboxes and dark gaps instead of refracting a grey or navy blur.
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.3, location=(cx, cy, 0.05), segments=64, ring_count=32)
        dome = bpy.context.object
        dome.name = "GemStudio"
        dome.parent = root
        dm = bpy.data.materials.new("GemStudio")
        dm.use_nodes = True
        nt = dm.node_tree
        nt.nodes.clear()
        tc = nt.nodes.new("ShaderNodeTexCoord")
        env = nt.nodes.new("ShaderNodeTexEnvironment")
        env.image = bpy.data.images.load(os.path.abspath(jubilee.ensure_hdri("studio_small_09")))
        nt.links.new(tc.outputs["Object"], env.inputs["Vector"])
        em = nt.nodes.new("ShaderNodeEmission")
        em.inputs["Strength"].default_value = 1.4
        nt.links.new(env.outputs["Color"], em.inputs["Color"])
        out = nt.nodes.new("ShaderNodeOutputMaterial")
        nt.links.new(em.outputs[0], out.inputs["Surface"])
        dome.data.materials.append(dm)
        dome.visible_camera = False
        dome.visible_shadow = False
        dome.visible_diffuse = False
        dome.visible_volume_scatter = False
        dome.light_linking.receiver_collection = only
    return root, hinge


def render(s, out, name):
    s.use_nodes = True
    nt = s.node_tree
    nt.nodes.clear()
    rl = nt.nodes.new("CompositorNodeRLayers")
    comp = nt.nodes.new("CompositorNodeComposite")
    nt.links.new(rl.outputs["Image"], comp.inputs["Image"])
    # depth: map Z (metres) to white = near, 0.4 m → 1, 3.0 m → 0
    mr = nt.nodes.new("CompositorNodeMapRange")
    mr.inputs["From Min"].default_value = 0.4
    mr.inputs["From Max"].default_value = 3.0
    mr.inputs["To Min"].default_value = 1.0
    mr.inputs["To Max"].default_value = 0.0
    mr.use_clamp = True
    nt.links.new(rl.outputs["Depth"], mr.inputs["Value"])
    fo = nt.nodes.new("CompositorNodeOutputFile")
    fo.base_path = out
    fo.file_slots[0].path = f"{name}_depth_"
    fo.format.color_mode = "BW"
    fo.format.color_depth = "8"
    nt.links.new(mr.outputs[0], fo.inputs[0])
    s.render.filepath = f"{out}/{name}.png"
    bpy.ops.render.render(write_still=True)
    # the file output node appends the frame number: give the depth map its plain name
    for f in os.listdir(out):
        if f.startswith(f"{name}_depth_") and f.endswith(".png"):
            os.replace(f"{out}/{f}", f"{out}/{name}_depth.png")
    print("wrote", name, flush=True)


def ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * t * (t * (6 * t - 15) + 10)


def lerp3(a, b, u):
    return Vector(a).lerp(Vector(b), u)


def place(shot, f, cam, cd, root, hinge):
    """Camera, case and lid at 60 fps frame f of a shot (moves eased, never linear)."""
    def aim(target, focus):
        cam.rotation_euler = (Vector(target) - cam.location).to_track_quat("-Z", "Y").to_euler()
        cd.dof.focus_distance = (Vector(focus) - cam.location).length
    hinge.rotation_euler.x = 0.0
    if shot == "c1":
        u = ease(f / 210)
        cam.location = lerp3((0.22, -1.32, 0.46), (0.03, -0.80, 0.27), u)
        k = ease((f - 20) / 135)  # the case slides in from the left, landing on "diamond" (155)
        root.location = lerp3((-0.62, -0.08, 0.0), (0.0, 0.0, 0.0), k)
        root.rotation_euler.z = math.radians(-14 * (1 - k))
        aim(lerp3((0.0, 0.42, 0.2), (0.0, 0.18, 0.08), u), root.location + Vector((0, 0, 0.03)))
    elif shot == "c2":
        u = ease(f / 323)
        cam.location = lerp3((0.30, -0.80, 0.30), (-0.01, -0.30, 0.22), u)
        cd.lens = 32 + 30 * u
        hinge.rotation_euler.x = math.radians(-72 * ease((f - 222) / 68))  # "the diamond as the guarantee"
        cd.dof.aperture_fstop = 1.6 + 5.0 * u  # stop down as we close in, so the stone itself is sharp
        aim((0.0, 0.05, 0.035), (0.0, -0.006, 0.052))
    elif shot == "c3":
        u = ease(f / 122)
        cam.location = lerp3((0.62, -0.72, 0.24), (0.10, -0.90, 0.31), u)
        aim(lerp3((0.1, 0.2, 0.1), (0.0, 0.3, 0.14), u), (0.0, 0.0, 0.03))


def shots(args):
    s = build(args)
    s.render.threads_mode = "FIXED"
    s.render.threads = args.threads
    s.render.image_settings.color_depth = "8"
    s.view_layers[0].use_pass_z = False
    s.cycles.denoising_prefilter = "ACCURATE"
    root, hinge = add_case(s, gem=args.shot == "c2")
    cam, cd = s.camera, s.camera.data
    a, b = map(int, args.frames.split("-"))
    os.makedirs(args.out, exist_ok=True)
    for f in range(a, b + 1, args.step):
        path = f"{args.out}/{args.shot}_{f:04d}.png"
        if os.path.exists(path):
            continue  # resumable
        place(args.shot, f, cam, cd, root, hinge)
        s.render.filepath = path + ".tmp.png"
        bpy.ops.render.render(write_still=True)
        os.replace(path + ".tmp.png", path)
        print("frame", f, flush=True)


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    ap = argparse.ArgumentParser()
    ap.add_argument("--shot", help="c1 | c2 | c3: an animated shot (see the module docstring)")
    ap.add_argument("--frames", default="0-0")
    ap.add_argument("--step", type=int, default=2)
    ap.add_argument("--bounces", type=int, default=8)
    ap.add_argument("--out", required=True)
    ap.add_argument("--w", type=int, default=3840)
    ap.add_argument("--h", type=int, default=2160)
    ap.add_argument("--samples", type=int, default=96)
    ap.add_argument("--layer", default="both")
    ap.add_argument("--threads", type=int, default=4)
    args = ap.parse_args(argv)
    os.makedirs(args.out, exist_ok=True)
    if args.shot:
        shots(args)
        return
    if args.layer in ("plate", "both"):
        s = build(args)
        s.render.threads_mode = "FIXED"
        s.render.threads = args.threads
        render(s, args.out, "counter_plate")
    if args.layer in ("case", "both"):
        s = build(args)
        s.render.threads_mode = "FIXED"
        s.render.threads = args.threads
        add_case(s)
        # Only the case and its shadow: the counter becomes a shadow catcher, everything else hidden.
        for o in s.objects:
            if o.type == "MESH" and not o.name.startswith(("Case", "Clasp", "CounterTop")):
                o.hide_render = True
        s.objects["CounterTop"].is_shadow_catcher = True
        s.render.film_transparent = True
        s.render.image_settings.color_mode = "RGBA"
        render(s, args.out, "counter_case")


if __name__ == "__main__":
    main()
