TITLE = "E3 Both forwards crack: what really happens on the track"
BG = "none"
LIBS = ["e.js"]
CSS = """
  #gl { position: absolute; inset: 0; width: 1920px; height: 1080px; display: block; }
  #vig, #sweep { display: none; }
  #top { position: absolute; inset: 0; }
  #bg { position: absolute; inset: -60px; filter: blur(7px); }
  #dim { position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 50%, rgba(8,12,20,0.35), rgba(8,12,20,0.8)); }
  .ck { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; pointer-events: none; }
  #flash { position: absolute; inset: 0; background: #E0F2FE; opacity: 0; }
"""
BODY = """  <canvas id="gl" width="1920" height="1080"></canvas>
  <div id="top"><div id="bg"></div><div id="dim"></div><div id="cards"></div>
    <svg class="ck" id="ck" viewBox="0 0 1920 1080" data-layout-allow-overflow></svg></div>
  <div id="flash" data-layout-allow-occlusion></div>"""
JS = """
  const T = E.table(document.getElementById("bg")), F = E.twoForwards(document.getElementById("cards"));
  const tF = at("V005", "playing with your fear"), tM = at("V005", "both are missing"), tT = at("V005", "on the track");
  // cracks stay inside each card's glass: clip to the measured card boxes (rotation included)
  const svg = document.getElementById("ck"), NS = "http://www.w3.org/2000/svg";
  const clipFor = (card, id, rot) => { const cp = document.createElementNS(NS, "clipPath"); cp.setAttribute("id", id);
    const r = document.createElementNS(NS, "rect"), x = card.offsetLeft, y = card.offsetTop, w = card.offsetWidth, h = card.offsetHeight;
    Object.entries({ x, y, width: w, height: h, rx: 22, transform: `rotate(${rot} ${x + w / 2} ${y + h / 2})` }).forEach(([k, v]) => r.setAttribute(k, v)); cp.appendChild(r); svg.appendChild(cp);
    const g = document.createElementNS(NS, "g"); g.setAttribute("clip-path", `url(#${id})`); svg.appendChild(g); return { g, cx: x + w * 0.62, cy: y + h * 0.55 }; };
  const A = clipFor(F.L, "cpL", -2.5), B = clipFor(F.R, "cpR", 2);
  const cl = E.crack(A.g, A.cx, A.cy, 3, 13, 380, "rgba(31,35,42,0.9)"), cr = E.crack(B.g, B.cx, B.cy, 8, 13, 380, "rgba(31,35,42,0.9)");
  // fear: the cards jitter and flush red; then glass cracks race across both; then we crash-zoom through the crack
  tl.fromTo(["#fL", "#fR"], { x: 0 }, { x: 6, duration: 0.05, yoyo: true, repeat: 9 }, tF);
  tl.to(["#fL h3", "#fR h3"], { color: "#B91C1C", duration: 0.3 }, tF);
  [...cl, ...cr].forEach((p, i) => tl.to(p, { attr: { "stroke-dashoffset": 0 }, duration: 0.35, ease: "power3.out" }, tM + (i % 15) * 0.025));
  const tZ = tM + 1.0;
  tl.to("#top", { scale: 5, opacity: 0, transformOrigin: "1440px 520px", duration: 0.85, ease: "power3.in" }, tZ);
  tl.to("#flash", { opacity: 0.35, duration: 0.08 }, tZ + 0.75).to("#flash", { opacity: 0, duration: 0.4 }, tZ + 0.83);
  window.E3T = { tZ, tT };
"""
MODULE = r"""
  import { THREE, createStage, seg, lerp, aim, camPath, ease } from "./kav3d.js";
  import { nightTrack } from "./nighttrack.mjs";
  const st = createStage({ sky: "night", fov: 46, near: 0.03, bloom: { intensity: 1.1, threshold: 0.7, smoothing: 0.3 } });
  const D = st.DUR, T = window.E3T;
  st.run((st) => { const N = nightTrack(st, { tagZ: -40 });
    return { N }; },
  (t, c) => { // low dolly along the rails at night, starting fast (the crash zoom) and settling
    const u = seg(t, T.tZ, D, ease.out), z = lerp(14, -6, u);
    aim(st.camera, new THREE.Vector3(0.3, lerp(1.6, 0.55, u), z), new THREE.Vector3(0, -0.05, z - 14), 0.03 * (1 - u));
    st.camera.fov = lerp(70, 44, u); st.camera.updateProjectionMatrix(); st.follow(0, 0, z - 6, 14); });
"""
