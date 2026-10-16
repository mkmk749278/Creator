TITLE = "A5 Link three: the UHF data radio"
BG = "none"
CSS = """
  #gl { position: absolute; inset: 0; width: 1920px; height: 1080px; display: block; }
  #vig, #sweep { display: none; }
  .bad { position: absolute; left: 1220px; width: 560px; padding: 18px 26px; border-radius: 14px; background: rgba(8,20,36,0.88); border: 2px solid #94A3B8;
    font: 800 40px Inter, Arial, sans-serif; letter-spacing: 0.06em; color: #F8FAFC; opacity: 0; display: flex; align-items: center; gap: 22px; }
  .bad svg { flex: none; }
  .bad .x { position: absolute; left: 14px; right: 14px; top: 50%; height: 6px; margin-top: -3px; background: #F87171; transform-origin: 0 50%; transform: scaleX(0); border-radius: 3px; }
  #b1 { top: 230px; } #b2 { top: 360px; }
  #tag { position: absolute; right: 60px; top: 56px; font: 800 20px Inter, Arial, sans-serif; letter-spacing: 0.16em; color: rgba(248,250,252,0.9); border: 2px solid rgba(248,250,252,0.5); background: rgba(15,23,42,0.55); padding: 6px 12px; }
"""
BODY = """  <canvas id="gl" width="1920" height="1080"></canvas>
  <div class="bad" id="b1"><svg width="44" height="56" viewBox="0 0 44 56"><rect x="6" y="2" width="32" height="52" rx="6" fill="none" stroke="#CBD5E1" stroke-width="4"/><circle cx="22" cy="46" r="3" fill="#CBD5E1"/></svg>MOBILE NETWORK<div class="x" id="x1"></div></div>
  <div class="bad" id="b2"><svg width="44" height="56" viewBox="0 0 44 56"><path d="M6 40 Q22 10 38 40 M12 42 Q22 24 32 42" fill="none" stroke="#CBD5E1" stroke-width="4"/><circle cx="22" cy="46" r="4" fill="#CBD5E1"/></svg>5G<div class="x" id="x2"></div></div>
  <div class="kav-label" id="lab1">Link 3 · UHF data radio<small>A SAFETY RADIO OF ITS OWN</small></div>
  <div id="tag">ILLUSTRATION</div>"""
JS = """
  const tT = at("V016", "Tall towers"), tC = at("V016", "carry messages"), tU = at("V016", "U-H-F"), tM = at("V016", "it's not your mobile"), t5 = at("V016", "not five G");
  window.A5T = { tT, tC, tU, tM, t5 };
  tl.to("#lab1", { opacity: 1, duration: 0.5 }, tU - 0.2);
  tl.fromTo("#b1", { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }, tM - 0.1);
  tl.to("#x1", { scaleX: 1, duration: 0.3, ease: "power2.in" }, tM + 0.9);
  tl.to("#b1", { opacity: 0.45, filter: "grayscale(1)", duration: 0.4 }, tM + 1.2);
  tl.fromTo("#b2", { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }, t5 - 0.4);
  tl.to("#x2", { scaleX: 1, duration: 0.3, ease: "power2.in" }, t5 + 0.25);
  tl.to("#b2", { opacity: 0.45, duration: 0.4 }, t5 + 0.55);
"""
MODULE = r"""
  import { THREE, createStage, mats, buildTrack, buildGround, buildTrees, buildOHE, buildLoco, buildTower, ringPulse, flowLine, seg, lerp, clamp, ease, aim, camPath } from "./kav3d.js";
  const st = createStage({ sky: "night", fov: 40, exposure: 1.1, bloom: { intensity: 1.2, threshold: 0.7, smoothing: 0.3 } });
  const T = window.A5T, D = st.DUR;
  const V3 = (x, y, z) => new THREE.Vector3(x, y, z);
  st.run((st) => {
    const M = mats(), S = st.scene;
    S.add(buildGround(M), buildTrack(M, { cx: 16, z0: -300, z1: 200 }), buildOHE(M, { cx: 16, mx: 19.4, z0: -300, z1: 200, phase: 20 }), buildTrees({ clear: 26, n: 380 }));
    const tower = buildTower(M, { h: 40, base: 6, top: 1.2 }); S.add(tower);
    // the station: a small lit building with its own radio mast
    const stn = new THREE.Group(); stn.position.set(-36, -0.75, 26); S.add(stn);
    const bld = new THREE.Mesh(new THREE.BoxGeometry(14, 4.2, 7), new THREE.MeshStandardMaterial({ color: 0xd9b96a, roughness: 0.9 })); bld.position.y = 2.1; bld.castShadow = true; stn.add(bld);
    for (let i = 0; i < 5; i++) { const w = new THREE.Mesh(new THREE.PlaneGeometry(1.2, 1.3), new THREE.MeshStandardMaterial({ color: 0x221a10, emissive: 0xffd9a0, emissiveIntensity: 2.2 })); w.position.set(-5 + i * 2.5, 2.4, 3.51); stn.add(w); }
    const sm = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 7, 6), M.galv); sm.position.set(5, 7.7, 0); stn.add(sm);
    const lamps = [new THREE.PointLight(0xffe2b0, 30, 30, 1.6)]; lamps[0].position.set(0, 4, 8); stn.add(lamps[0]);
    const loco = buildLoco(M); S.add(loco);
    const hl = new THREE.SpotLight(0xfff2d0, 600, 160, 0.32, 0.5, 1.2); S.add(hl, hl.target);
    // radio paths: station mast -> tower top -> engine roof (packets ride these arcs), rings pulse at each antenna
    const top = V3(0, 39.2, 0), sTop = V3(-31, 10.6, 26);
    const pathA = [sTop, V3(-16, 30, 14), top];
    const pA = flowLine(pathA, { radius: 0.18, base: 0.04 }); S.add(pA);
    const pB = flowLine([top, V3(10, 26, -12), V3(16, 5, -26)], { radius: 0.18, base: 0.04 }); S.add(pB);
    const rings = [0, 1, 2, 3].map(() => { const r = ringPulse({ r0: 0.5, r1: 9, thick: 0.05 }); S.add(r); return r; });
    const cam = camPath([
      [0.0, [-6, 1.4, 12], [0, 3, 0]],
      [T.tT + 1.2, [-8, 3, 15], [0, 30, 0]],
      [T.tC + 0.6, [30, 14, 52], [-4, 18, 4]],
      [D, [44, 18, 66], [-6, 16, 2]],
    ]);
    return { tower, loco, hl, pA, pB, rings, top, sTop, cam };
  }, (t, c) => {
    const { p, l } = c.cam(t); aim(st.camera, p, l); st.follow(0, 4, 0, 50);
    c.tower.userData.lamp.material.emissiveIntensity = 4 * (0.5 + 0.5 * Math.sin(t * 4.2));
    const zn = 30 - 6 * t; c.loco.position.set(16, 0, zn); c.loco.userData.setS(-zn);
    c.hl.position.set(16, 3.9, zn - 0.5); c.hl.target.position.set(16, 0, zn - 40);
    c.loco.updateMatrixWorld(); const lr = c.loco.localToWorld(V3(0, 4.4, 2.3));
    // the tower -> engine arc follows the moving engine (geometry rebuilt from t alone)
    c.pB.geometry.dispose(); c.pB.geometry = new THREE.TubeGeometry(new THREE.CatmullRomCurve3([c.top, c.top.clone().lerp(lr, 0.5).add(V3(0, 6, 0)), lr]), 48, 0.18, 6);
    // a message every 1.6 s from the first "carry messages": station -> tower, then tower -> engine
    const per = 1.6, t0 = T.tC - 0.2, k = t - t0, ph = ((k % per) + per) % per / per, on = k > 0 ? 1 : 0;
    c.pA.userData.set(Math.max(0, ph * 1.4 - 0.25), Math.min(1, ph * 1.4), on);
    const ph2 = clamp((ph - 0.45) / 0.55); c.pB.userData.set(Math.max(0, ph2 * 1.15 - 0.25), ph2, on * (ph >= 0.45 ? 1 : 0.4));
    const pts = [c.sTop, c.top, c.top, lr], offs = [0.0, 0.62, 0.7, 1.0];
    c.rings.forEach((r, i) => { r.position.copy(pts[i]); r.lookAt(st.camera.position); r.userData.at(on ? ((ph - offs[i] * 0.9 + 1) % 1) / 0.5 : 0); });
  });
"""
