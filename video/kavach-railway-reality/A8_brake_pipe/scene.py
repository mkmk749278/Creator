TITLE = "A8 Steel on steel, and the brake pipe"
BG = "none"
CSS = """
  #gl { position: absolute; inset: 0; width: 1920px; height: 1080px; display: block; }
  #vig, #sweep { display: none; }
  .pin { position: absolute; left: 0; top: 0; }
  .ctr { position: absolute; left: 0; top: -70px; width: var(--w); margin-left: calc(var(--w) / -2); }
  .chip { white-space: nowrap; box-sizing: border-box; text-align: center; padding: 10px 16px; border-radius: 10px; background: rgba(8,20,36,0.88);
    border: 2px solid var(--c, #38BDF8); font: 800 30px Inter, Arial, sans-serif; letter-spacing: 0.1em; color: #F8FAFC; opacity: 0; }
  #tag { position: absolute; right: 60px; top: 56px; font: 800 20px Inter, Arial, sans-serif; letter-spacing: 0.16em; color: rgba(248,250,252,0.9); border: 2px solid rgba(248,250,252,0.5); background: rgba(15,23,42,0.55); padding: 6px 12px; }
"""
BODY = """  <canvas id="gl" width="1920" height="1080"></canvas>
  <div class="pin" id="q0"><div class="ctr" style="--w:380px"><div class="chip" id="c0" style="--c:#F59E0B">STEEL ON STEEL</div></div></div>
  <div class="pin" id="q1"><div class="ctr" style="--w:360px"><div class="chip" id="c1" style="--c:#F59E0B">LAST COACH</div></div></div>
  <div class="kav-label" id="lab1">Brake pipe<small>AIR PRESSURE CHANGES COACH BY COACH</small></div>
  <div id="tag">ILLUSTRATION</div>"""
JS = """
  const tS = at("V022", "steel wheels"), tG = at("V022", "very little grip"), tH = at("V022", "enormously heavy"), tB = at("V022", "when the brakes go on"), tA = at("V022", "all the way down"), tL = at("V022", "last coach");
  window.A8T = { tS, tG, tH, tB, tA, tL };
  tl.fromTo("#c0", { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.4 }, tS + 0.4); tl.to("#c0", { opacity: 0, duration: 0.3 }, tH - 0.4);
  tl.to("#lab1", { opacity: 1, duration: 0.5 }, tB + 0.2);
  tl.fromTo("#c1", { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.4 }, tL - 0.2);
"""
MODULE = r"""
  import { THREE, createStage, mats, buildTrack, buildGround, buildTrees, buildOHE, buildTrain, flowLine, RAIL_X, seg, lerp, clamp, ease, aim, camPath } from "./kav3d.js";
  const st = createStage({ sky: "dusk", fov: 36, near: 0.02 });
  const T = window.A8T, D = st.DUR, $ = (id) => document.getElementById(id);
  const V3 = (x, y, z) => new THREE.Vector3(x, y, z);
  const V = 4, NC = 8;
  st.run((st) => {
    const M = mats(), S = st.scene;
    S.add(buildGround(M), buildTrack(M, { cx: 0, z0: -200, z1: 320 }), buildOHE(M, { cx: 0, mx: -3.4, z0: -200, z1: 320, phase: 15 }), buildTrees({ clear: 34, z0: -500, z1: 700 }));
    const train = buildTrain(M, { coaches: NC }); S.add(train);
    const cars = train.userData.cars;
    // the contact patch: a tiny glowing ellipse where the first coach's wheel touches the rail
    const c1 = cars[1], zc = c1.position.z + c1.userData.L / 2 - 7.45 - 1.28;
    const patch = new THREE.Mesh(new THREE.SphereGeometry(1, 20, 10), new THREE.MeshBasicMaterial({ color: 0xffb347 })); patch.scale.set(0.05, 0.006, 0.11);
    patch.position.set(RAIL_X, 0.003, zc); train.add(patch);
    // the pressure front: a bright bead riding the brake pipe from the engine to the last coach
    const bead = new THREE.Mesh(new THREE.SphereGeometry(0.16, 16, 10), new THREE.MeshBasicMaterial({ color: 0xbfefff })); train.add(bead);
    const pipes = cars.map((c) => c.userData.bpipe || c.userData.parts.bpipe);
    // a glowing line along the whole rake shows the pressure change travelling back (seen from the wide shots)
    const wave = flowLine([V3(1.7, 0.8, 0.4), V3(1.7, 0.8, train.userData.length / 2), V3(1.7, 0.8, train.userData.length)], { radius: 0.09, base: 0 }); train.add(wave);
    const cam = camPath([
      [0.0, [RAIL_X + 0.42, 0.06, zc - 0.95], [RAIL_X, 0.01, zc]],
      [T.tG + 0.2, [RAIL_X + 0.75, 0.2, zc - 1.35], [RAIL_X, 0.03, zc]],
      [T.tH + 0.3, [5.5, 2.2, zc - 9], [0, 1.0, zc + 12]],
      [T.tB + 0.3, [9, 4.6, -14], [0, 1.4, 45]],
      [D, [14, 8.5, -24], [0, 1.0, 95]],
    ]);
    return { train, cars, patch, bead, pipes, wave, cam, zc, len: train.userData.length };
  }, (t, c) => {
    const s = V * t, zN = -s; c.train.userData.place(zN, s);
    const { p, l } = c.cam(t); p.z += zN; l.z += zN; aim(st.camera, p, l);
    st.camera.fov = lerp(30, 40, seg(t, T.tG, T.tB)); st.camera.updateProjectionMatrix();
    st.follow(0, 1, zN + lerp(c.zc, 60, seg(t, T.tH, T.tB)), lerp(6, 60, seg(t, T.tH, T.tB)));
    c.patch.material.color.setRGB(1.0 * (0.6 + 0.4 * Math.sin(t * 5)) * 3, 0.65 * 3, 0.25 * 3);
    // brake application: the pressure change travels car by car, cyan near the engine turning amber towards the rear
    const n = c.cars.length, u = seg(t, T.tB, T.tL, ease.lin), zf = u * c.len;
    c.cars.forEach((car, i) => { const z0 = car.position.z, L = car.userData.L, k = clamp((zf - z0) / L);
      const col = new THREE.Color(0x38bdf8).lerp(new THREE.Color(0xf59e0b), i / (n - 1));
      c.pipes[i].material.emissive.copy(col); c.pipes[i].material.emissiveIntensity = 3.5 * k; });
    c.wave.visible = t > T.tB; c.wave.userData.set(0, u, 1);
    c.bead.visible = t > T.tB && t < T.tL + 0.3; c.bead.position.set(1.62, 0.8, zf);
    c.train.updateMatrixWorld(); st.pin($("q0"), c.train.localToWorld(V3(RAIL_X, 0.05, c.zc)));
    const lastCar = c.cars[n - 1]; st.pin($("q1"), c.train.localToWorld(V3(0, 4.6, lastCar.position.z + lastCar.userData.L / 2)));
  });
"""
