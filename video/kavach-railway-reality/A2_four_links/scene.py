TITLE = "A2 Kavach is a chain of four links"
BG = "none"
CSS = """
  #gl { position: absolute; inset: 0; width: 1920px; height: 1080px; display: block; }
  #vig, #sweep { display: none; }
  .pin { position: absolute; left: 0; top: 0; }
  .lk { margin-left: -90px; width: 180px; text-align: center; font: 800 26px Inter, Arial, sans-serif; letter-spacing: 0.16em; color: #E0F2FE;
    text-shadow: 0 2px 10px rgba(0,0,0,0.9); opacity: 0; }
  #tag { position: absolute; right: 60px; top: 56px; font: 800 20px Inter, Arial, sans-serif; letter-spacing: 0.16em; color: rgba(248,250,252,0.9); border: 2px solid rgba(248,250,252,0.5); background: rgba(15,23,42,0.55); padding: 6px 12px; }
"""
BODY = """  <canvas id="gl" width="1920" height="1080"></canvas>
  <div class="pin" id="p0"><div class="lk" id="k0">TRACK</div></div>
  <div class="pin" id="p1"><div class="lk" id="k1">STATION</div></div>
  <div class="pin" id="p2"><div class="lk" id="k2">RADIO</div></div>
  <div class="pin" id="p3"><div class="lk" id="k3">ENGINE</div></div>
  <div id="tag">ILLUSTRATION</div>"""
JS = """
  const tC = at("V012", "chain of four links"), tE = at("V012", "every link");
  window.A2T = { tC, tE, tL: [tC - 0.2, tC + 0.45, tC + 1.1, tC + 1.75] };
  window.A2T.tL.forEach((t, i) => tl.fromTo("#k" + i, { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.35 }, t + 0.35));
"""
MODULE = r"""
  import { THREE, createStage, mats, buildRig, chainLink, flowLine, seg, lerp, clamp, ease, aim, camPath, mulberry32 } from "./kav3d.js";
  const st = createStage({ sky: "void", fov: 40, bloom: { intensity: 1.1, threshold: 0.8, smoothing: 0.3, radius: 0.8 } });
  const T = window.A2T, D = st.DUR, $ = (id) => document.getElementById(id);
  st.run((st) => {
    const M = mats(), S = st.scene, R = buildRig(M, S, { coaches: 2, trees: false });
    const order = ["track", "station", "tower", "cab"], sizes = [2.6, 3.8, 4.8, 3.2];
    const r = mulberry32(12);
    const links = order.map((k, i) => { const m = chainLink({ size: sizes[i] }); m.position.copy(R.P[k]); S.add(m);
      return { m, home: R.P[k].clone(), from: new THREE.Vector3((r() - 0.5) * 30, 12 + r() * 10, (r() - 0.5) * 30), spin: (r() - 0.5) * 6 }; });
    // the chain: glowing joins between neighbouring links, drawn when every link is in place
    const lift = (a, b, h) => [a, a.clone().lerp(b, 0.5).add(new THREE.Vector3(0, h, 0)), b];
    const joins = [[0, 1, 4], [1, 2, 6], [2, 3, 3], [3, 0, 2]].map(([a, b, h]) => { const f = flowLine(lift(R.P[order[a]], R.P[order[b]], h), { radius: 0.09, base: 0 }); S.add(f); return f; });
    const cam = camPath([[0, [14, 10, -47], [-1, 7.5, 6]], [D, [7, 9.5, -50], [-1, 7.5, 6]]]);
    const kl = new THREE.PointLight(0x7dd3fc, 0, 120, 1.2); kl.position.set(0, 18, -14); S.add(kl);
    return { R, links, joins, cam, kl };
  }, (t, c) => {
    const { p, l } = c.cam(t); aim(st.camera, p, l);
    st.follow(-2, 2, 0, 45);
    c.links.forEach((L, i) => { const t0 = T.tL[i], k = seg(t, t0, t0 + 0.7, ease.out);
      L.m.position.lerpVectors(L.home.clone().add(L.from), L.home, k); L.m.visible = t >= t0 - 0.01;
      L.m.lookAt(st.camera.position); L.m.rotateZ((1 - k) * L.spin + 0.15 * Math.sin(t * 1.3 + i));
      L.m.userData.light(0.35 + 0.65 * seg(t, t0 + 0.5, t0 + 0.9) + 0.6 * seg(t, T.tE, T.tE + 0.4));
      st.pin($("p" + i), L.home, 0, i === 2 ? -150 : i === 0 ? 70 : -90); });
    c.joins.forEach((j, i) => { const k = seg(t, T.tE + i * 0.12, T.tE + 0.6 + i * 0.12, ease.lin); j.visible = k > 0; j.userData.set(0, k, 1); });
    // the whole rig lights when the chain closes
    const on = seg(t, T.tE + 0.3, T.tE + 1.0);
    st.hemi.intensity = lerp(0.35, 1.1, on); st.sun.intensity = lerp(0.6, 1.6, on); c.kl.intensity = 400 * on;
  });
"""
