TITLE = "A4 Link two: the station and interlocking"
BG = "none"
CSS = """
  #gl { position: absolute; inset: 0; width: 1920px; height: 1080px; display: block; }
  #vig, #sweep { display: none; }
  .pin { position: absolute; left: 0; top: 0; }
  .ctr { position: absolute; left: 0; top: -56px; width: var(--w); margin-left: calc(var(--w) / -2); }
  .chip { white-space: nowrap; box-sizing: border-box; text-align: center; padding: 8px 14px; border-radius: 10px; background: rgba(8,20,36,0.86); border: 2px solid var(--c, #38BDF8);
    font: 800 24px Inter, Arial, sans-serif; letter-spacing: 0.1em; color: #F8FAFC; opacity: 0; }
  #tag { position: absolute; right: 60px; top: 56px; font: 800 20px Inter, Arial, sans-serif; letter-spacing: 0.16em; color: rgba(248,250,252,0.9); border: 2px solid rgba(248,250,252,0.5); background: rgba(15,23,42,0.55); padding: 6px 12px; }
"""
BODY = """  <canvas id="gl" width="1920" height="1080"></canvas>
  <div class="pin" id="pS"><div class="ctr" style="--w:180px"><div class="chip" id="cS" style="--c:#F87171">SIGNAL</div></div></div>
  <div class="pin" id="pP"><div class="ctr" style="--w:180px"><div class="chip" id="cP" style="--c:#F59E0B">POINTS</div></div></div>
  <div class="pin" id="pT"><div class="ctr" style="--w:320px"><div class="chip" id="cT" style="--c:#F87171">TRACK OCCUPIED</div></div></div>
  <div class="pin" id="pK"><div class="ctr" style="--w:320px"><div class="chip" id="cK">STATION KAVACH</div></div></div>
  <div class="kav-label" id="lab1">Link 2 · Interlocking<small>THE STATION'S OWN SIGNALLING SYSTEM</small></div>
  <div id="tag">ILLUSTRATION</div>"""
JS = """
  const tK = at("V015", "A Kavach computer"), tS = at("V015", "reads the signals"), tP = at("V015", "the points"), tT = at("V015", "which tracks"),
        tF = at("V015", "straight from"), tI = at("V015", "called interlocking"), tR = at("V015", "Remember");
  window.A4T = { tK, tS, tP, tT, tF, tI, tR };
  tl.to("#lab1", { opacity: 1, duration: 0.5 }, 0.5); tl.to("#lab1", { opacity: 0, duration: 0.4 }, tK + 1.2);
  for (const [id, t] of [["#cK", tK + 0.3], ["#cS", tS], ["#cP", tP], ["#cT", tT]]) tl.fromTo(id, { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.35 }, t);
  tl.to(["#cS", "#cP", "#cT", "#cK"], { opacity: 0, duration: 0.4 }, tI - 0.6);
  tl.to("#lab1", { opacity: 1, duration: 0.5 }, tI + 0.2);
"""
MODULE = r"""
  import { THREE, createStage, mats, buildTrack, buildGround, buildTrees, buildOHE, buildSignal, buildCoach, buildStationRoom, buildRelayRack, buildStationKavach, flowLine, seg, lerp, clamp, ease, aim, camPath } from "./kav3d.js";
  const st = createStage({ sky: "dusk", fov: 38 });
  const T = window.A4T, D = st.DUR, $ = (id) => document.getElementById(id);
  const V3 = (x, y, z) => new THREE.Vector3(x, y, z);
  st.run((st) => {
    const M = mats(), S = st.scene;
    S.add(buildGround(M), buildTrack(M, { cx: 9, z0: -120, z1: 80 }), buildOHE(M, { cx: 9, mx: 12.4, z0: -120, z1: 80, phase: 30 }), buildTrees({ clear: 22 }));
    const room = buildStationRoom(M, { w: 10, d: 6, h: 3.6, right: false }); room.position.set(0, -0.75, 0); S.add(room);
    const racks = [0, 1, 2, 3].map((i) => { const r = buildRelayRack(M, { seed: 7 + i }); r.position.set(-4.0 + i * 1.12, -0.55, -2.6); S.add(r); return r; });
    const kav = buildStationKavach(M); kav.position.set(2.8, -0.55, -2.4); S.add(kav);
    // the INTERLOCKING name plate over the relay racks (lights on "called interlocking")
    const pc = document.createElement("canvas"); pc.width = 1024; pc.height = 160; const pg = pc.getContext("2d");
    pg.fillStyle = "#0B2540"; pg.fillRect(0, 0, 1024, 160); pg.strokeStyle = "#7DD3FC"; pg.lineWidth = 8; pg.strokeRect(8, 8, 1008, 144);
    pg.fillStyle = "#F0F9FF"; pg.font = "800 96px Inter, Arial"; pg.textAlign = "center"; pg.fillText("INTERLOCKING", 512, 116);
    const ptex = new THREE.CanvasTexture(pc); ptex.colorSpace = THREE.SRGBColorSpace;
    const plateM = new THREE.MeshStandardMaterial({ map: ptex, emissive: 0xffffff, emissiveMap: ptex, emissiveIntensity: 0.04, roughness: 0.6 });
    const plate = new THREE.Mesh(new THREE.PlaneGeometry(3.6, 0.56), plateM); plate.position.set(-2.32, 2.55, -2.84); S.add(plate);
    // outside: a signal, a set of points with its machine, and an occupied track section with a coach on it
    const sig = buildSignal(M, { x: 6.9, z: -9, plate: true }); S.add(sig); sig.userData.set([0, 0, 0, 1]);
    const pm = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.4, 0.5), new THREE.MeshStandardMaterial({ color: 0x6b7280, roughness: 0.6, metalness: 0.4 })); pm.position.set(7.4, -0.45, -1); pm.castShadow = true; S.add(pm);
    const rod = new THREE.Mesh(new THREE.BoxGeometry(1.3, 0.05, 0.08), M.darkSteel); rod.position.set(8.2, -0.25, -1); S.add(rod);
    const blade = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.15, 6.0), new THREE.MeshStandardMaterial({ color: 0xd6d9dc, emissive: 0xf59e0b, emissiveIntensity: 0, metalness: 1, roughness: 0.3 }));
    blade.position.set(9 - 0.8, -0.08, 2); blade.rotation.y = 0.012; S.add(blade);
    const coach = buildCoach(M); coach.position.set(9, 0, -62); S.add(coach);
    const occ = [-1, 1].map((sx) => { const m = new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.02, 30), new THREE.MeshBasicMaterial({ color: 0xff3b2a, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false }));
      m.position.set(9 + sx * 0.874, 0.012, -50); S.add(m); return m; });
    // cables (in a trough along the ground, into the room through the side wall, up to the racks)
    const wS = flowLine([V3(6.9, -0.6, -9), V3(6.0, -0.6, -4.5), V3(5.4, 0.1, -2.6), V3(3.6, 0.35, -2.9), V3(-2.4, 0.4, -2.9), V3(-2.9, 1.2, -2.35)], { color: 0xff3b2a, radius: 0.05 });
    const wP = flowLine([V3(7.4, -0.5, -1), V3(6.4, -0.6, -1.4), V3(5.4, 0.1, -1.8), V3(3.6, 0.35, -2.5), V3(-1.2, 0.4, -2.6), V3(-1.7, 1.2, -2.3)], { color: 0xf59e0b, radius: 0.05 });
    const wT = flowLine([V3(8.1, -0.55, -36), V3(7.0, -0.6, -14), V3(5.6, 0.0, -3.0), V3(3.6, 0.3, -2.7), V3(-3.3, 0.4, -2.7), V3(-3.9, 1.2, -2.35)], { color: 0xff6a4a, radius: 0.05 });
    const wK = flowLine([V3(-0.5, 2.1, -2.35), V3(0.8, 2.25, -2.3), V3(2.0, 2.1, -2.3), V3(2.8, 1.65, -2.0)], { color: 0x38bdf8, radius: 0.07 });
    S.add(wS, wP, wT, wK);
    const cam = camPath([
      [0.0, [15, 7.5, 19], [2, 1.0, -2]],
      [T.tS - 0.2, [12, 5.5, 15], [3, 0.8, -3]],
      [T.tT + 0.6, [13, 6.5, 12], [4, 0.6, -6]],
      [T.tF + 0.2, [7.5, 3.6, 9.5], [0, 1.2, -2]],
      [T.tI - 0.2, [2.4, 2.8, 5.5], [-1.6, 2.0, -2.6]],
      [D, [-0.9, 2.65, 2.1], [-2.3, 2.5, -2.8]],
    ]);
    return { room, racks, kav, plateM, sig, blade, occ, wS, wP, wT, wK, cam };
  }, (t, c) => {
    const { p, l } = c.cam(t); aim(st.camera, p, l); st.follow(3, 0, -3, 20);
    const run = (w, t0, d = 1.2) => { const k = seg(t, t0, t0 + d, ease.lin); w.userData.set(Math.max(0, k - 0.25), k, t >= t0 ? 1 : 0.35); };
    run(c.wS, T.tS); run(c.wP, T.tP); run(c.wT, T.tT); run(c.wK, T.tF + 0.3, 1.0);
    c.blade.material.emissiveIntensity = 1.5 * seg(t, T.tP, T.tP + 0.4) * (1 - 0.6 * seg(t, T.tI - 0.5, T.tI));
    c.occ.forEach((m) => { m.material.opacity = 0.85 * seg(t, T.tT, T.tT + 0.4) * (0.75 + 0.25 * Math.sin(t * 6)); });
    c.kav.userData.glow.material.opacity = 0.28 * seg(t, T.tK, T.tK + 0.5) + 0.4 * seg(t, T.tF + 1.2, T.tF + 1.6);
    c.racks.forEach((r) => r.userData.leds.forEach((led, i) => { led.visible = Math.sin(t * 3 + i * 1.7) > -0.6; }));
    c.plateM.emissiveIntensity = 0.04 + 2.3 * seg(t, T.tI, T.tI + 0.6);
    st.pin($("pS"), new THREE.Vector3(6.9, 4.6, -9), 120, 30); st.pin($("pP"), new THREE.Vector3(7.6, 0.5, -1), 0, -30);
    st.pin($("pT"), new THREE.Vector3(9, 1.0, -40), 0, -30); st.pin($("pK"), new THREE.Vector3(2.8, 1.4, -2.4), 0, -70);
  });
"""
