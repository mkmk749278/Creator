TITLE = "A9 Engine, track, data, distance"
BG = "none"
CSS = """
  #gl { position: absolute; inset: 0; width: 1920px; height: 1080px; display: block; }
  #vig, #sweep { display: none; }
  .pin { position: absolute; left: 0; top: 0; }
  .lk { margin-left: -180px; width: 360px; text-align: center; font: 800 34px Inter, Arial, sans-serif; letter-spacing: 0.16em; color: #E0F2FE;
    text-shadow: 0 2px 12px rgba(0,0,0,0.95); opacity: 0; }
  .vc { position: absolute; left: 90px; bottom: 120px; padding: 16px 26px; border-radius: 12px; background: rgba(8,20,36,0.88); border-left: 6px solid var(--c);
    font: 800 48px Inter, Arial, sans-serif; letter-spacing: 0.06em; color: #F8FAFC; opacity: 0; white-space: nowrap; }
  .vc s { text-decoration-color: #DC2626; text-decoration-thickness: 6px; }
  #tag { position: absolute; right: 60px; top: 56px; font: 800 20px Inter, Arial, sans-serif; letter-spacing: 0.16em; color: rgba(248,250,252,0.9); border: 2px solid rgba(248,250,252,0.5); background: rgba(15,23,42,0.55); padding: 6px 12px; }
"""
BODY = """  <canvas id="gl" width="1920" height="1080"></canvas>
  <div class="pin" id="p0"><div class="lk" id="k0">ENGINE</div></div>
  <div class="pin" id="p1"><div class="lk" id="k1">TRACK</div></div>
  <div class="pin" id="p2"><div class="lk" id="k2">SIGNAL DATA</div></div>
  <div class="pin" id="p3"><div class="lk" id="k3">ROOM TO STOP</div></div>
  <div class="vc" id="v1" style="--c:#DC2626"><s>MAGIC</s></div>
  <div class="vc" id="v2" style="--c:#DC2626"><s>USELESS</s></div>
  <div class="vc" id="v3" style="--c:#38BDF8">INDIAN-BUILT SAFETY LAYER</div>
  <div class="vc" id="v4" style="--c:#F59E0B">BRAKES EARLY</div>
  <div id="tag">ILLUSTRATION</div>"""
JS = """
  const tE = at("V058", "the engine is fitted"), tT = at("V058", "the track section"), tD = at("V058", "the signalling data"), tR = at("V058", "enough room");
  window.A9T = { tL: [tE, tT, tD, tR] };
  // the opening verdict, one short callout per phrase (the two myths struck out first)
  const tv = [at("V058", "isn't magic"), at("V058", "isn't useless"), at("V058", "Indian-built"), at("V058", "brakes early"), at("V058", "as long as")];
  ["#v1", "#v2", "#v3", "#v4"].forEach((id, i) => { tl.fromTo(id, { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.3, ease: "power3.out" }, tv[i] - 0.1);
    tl.to(id, { opacity: 0, x: 30, duration: 0.25 }, tv[i + 1] - 0.25); });
  window.A9T.tL.forEach((t, i) => tl.fromTo("#k" + i, { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.4 }, t + 0.2));
"""
MODULE = r"""
  import { THREE, createStage, mats, buildRig, chainLink, flowLine, seg, lerp, clamp, ease, aim, camPath } from "./kav3d.js";
  const st = createStage({ sky: "dawn", fov: 40 });
  const T = window.A9T, D = st.DUR, $ = (id) => document.getElementById(id);
  const V3 = (x, y, z) => new THREE.Vector3(x, y, z);
  st.run((st) => {
    const M = mats(), S = st.scene, R = buildRig(M, S, { coaches: 2 });
    // links: engine (cab), track (tag), data (station interlocking), and the tower stays as it was
    const spots = [R.P.cab, R.P.track, R.P.station, R.P.tower], sizes = [3.2, 2.6, 3.8, 4.8];
    const links = spots.map((p, i) => { const m = chainLink({ size: sizes[i] }); m.position.copy(p); S.add(m); return m; });
    // the braking distance ruler drawn ahead of the train, with a tick every 10 m
    const ruler = flowLine([V3(0, 0.08, -0.5), V3(0, 0.08, -18), V3(0, 0.08, -36)], { radius: 0.12, base: 0, color: 0xf59e0b }); S.add(ruler);
    const ticks = []; for (let z = 6; z <= 36; z += 6) { const tk = new THREE.Mesh(new THREE.BoxGeometry(2.2, 0.03, 0.14), new THREE.MeshBasicMaterial({ color: 0xffc46b })); tk.position.set(0, 0.06, -z); tk.visible = false; S.add(tk); ticks.push([tk, z]); }
    const cam = camPath([[0, [18, 12, -50], [-1, 6.5, 6]], [D, [9, 8.5, -44], [-2, 4.5, 0]]]);
    return { R, links, ruler, ticks, cam, spots };
  }, (t, c) => {
    const { p, l } = c.cam(t); aim(st.camera, p, l); st.follow(-2, 2, -10, 50);
    c.links.forEach((m, i) => { m.lookAt(st.camera.position); m.rotateZ(0.12 * Math.sin(t * 0.9 + i));
      const k = i < 3 ? seg(t, T.tL[i], T.tL[i] + 0.5) : 0; m.userData.light(0.18 + 0.9 * k + (i < 3 ? 0.25 * k * Math.max(0, Math.sin((t - T.tL[i]) * 6)) * (1 - seg(t, T.tL[i] + 0.6, T.tL[i] + 1.2)) : 0)); });
    const kr = seg(t, T.tL[3], T.tL[3] + 1.0, ease.out); c.ruler.visible = kr > 0; c.ruler.userData.set(0, kr, 1);
    c.ticks.forEach(([tk, z]) => { tk.visible = kr * 36 >= z; });
    st.pin($("p0"), c.spots[0], 0, -90); st.pin($("p1"), c.spots[1], 0, 70); st.pin($("p2"), c.spots[2], 0, -95); st.pin($("p3"), V3(0, 0.5, -27), 0, -40);
  });
"""
