// Props studio (see index.html). Spec = JSON in location.hash. Units: 1 = 1 cm.
//   {type:"card", ...} {type:"bill", ...} {type:"phone", ...} {type:"notice", ...} {type:"cheque", ...}
//   common: px (output width, default 3000), elev (camera elevation deg, default 58), yaw (prop turn deg), tilt (deg),
//           light ("warm" | "cool" | "neutral"), shadow (0..1)
// Sets window.__ready = true when the frame is drawn (shoot.mjs screenshots it with an alpha background).
import * as THREE from "three";
import { HDRLoader } from "three/addons/loaders/HDRLoader.js";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";

const S = JSON.parse(decodeURIComponent(location.hash.slice(1) || "{}"));
const mulberry32 = (s) => () => { s = (s + 0x6d2b79f5) >>> 0; let t = s; t = Math.imul(t ^ (t >>> 15), t | 1);
  t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
const rng = mulberry32(S.seed || 7);
const DEG = Math.PI / 180;

// ---------- fonts ----------
const FONTS = [
  ["Bricolage", 800, "bricolage-grotesque-latin-800-normal"], ["Bricolage", 800, "bricolage-grotesque-latin-ext-800-normal", "U+20B9,U+0100-024F"],
  ["Inter Tight", 800, "inter-tight-latin-800-normal"], ["Inter Tight", 800, "inter-tight-latin-ext-800-normal", "U+20B9,U+2212,U+0100-024F"],
  ["Inter Tight", 500, "inter-tight-latin-500-normal"], ["Inter Tight", 500, "inter-tight-latin-ext-500-normal", "U+20B9,U+2212,U+0100-024F"],
  ["Mono", 700, "jetbrains-mono-latin-700-normal"], ["Mono", 500, "jetbrains-mono-latin-500-normal"],
];
const fontsReady = Promise.all(FONTS.map(async ([fam, w, f, range]) => {
  const buf = await (await fetch(`vendor/fonts/${f}.woff2`)).arrayBuffer();
  const ff = new FontFace(fam, buf, { weight: String(w), ...(range ? { unicodeRange: range } : {}) }); document.fonts.add(ff); return ff.load();
}));
const F = (w, px, fam = "Inter Tight") => `${w} ${px}px "${fam}", "Inter Tight", sans-serif`;

// ---------- canvas helpers ----------
const mkCanvas = (w, h) => { const c = document.createElement("canvas"); c.width = w; c.height = h; return [c, c.getContext("2d")]; };
const tex = (c, srgb = true) => { const t = new THREE.CanvasTexture(c); if (srgb) t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 16; return t; };
const rrect = (g, x, y, w, h, r) => { g.beginPath(); g.roundRect(x, y, w, h, r); };
const textR = (g, s, x, y) => { g.fillText(s, x - g.measureText(s).width, y); };
const fibres = (g, w, h, n, a) => { for (let i = 0; i < n; i++) { g.fillStyle = `rgba(${90 + rng() * 40},${80 + rng() * 40},${70 + rng() * 30},${rng() * a})`;
  const x = rng() * w, y = rng() * h, l = 2 + rng() * 9, an = rng() * Math.PI; g.fillRect(x, y, Math.cos(an) * l + 1.2, Math.sin(an) * l + 1.2); } };
function noiseCanvas(w, h, amp, base = 128, blur = 0) {
  const [c, g] = mkCanvas(w, h); const im = g.createImageData(w, h);
  for (let i = 0; i < w * h; i++) { const v = base + (rng() - 0.5) * amp; im.data[i * 4] = im.data[i * 4 + 1] = im.data[i * 4 + 2] = v; im.data[i * 4 + 3] = 255; }
  g.putImageData(im, 0, 0); if (blur) { g.filter = `blur(${blur}px)`; g.drawImage(c, 0, 0); g.filter = "none"; } return [c, g];
}
// rubber stamp: rotated double-ruled box, uneven ink (drawn into an existing context)
function stamp(g, text, cx, cy, size, color = "#c0182b", rot = -12) {
  g.save(); g.translate(cx, cy); g.rotate(rot * DEG); g.font = F(800, size, "Bricolage");
  const tw = g.measureText(text).width, pw = tw + size * 0.9, ph = size * 1.45;
  g.strokeStyle = color; g.fillStyle = color; g.globalAlpha = 0.82;
  g.lineWidth = size * 0.09; rrect(g, -pw / 2, -ph / 2, pw, ph, size * 0.12); g.stroke();
  g.lineWidth = size * 0.035; rrect(g, -pw / 2 + size * 0.14, -ph / 2 + size * 0.14, pw - size * 0.28, ph - size * 0.28, size * 0.08); g.stroke();
  g.fillText(text, -tw / 2, size * 0.36);
  g.globalCompositeOperation = "destination-out";   // ink gaps
  for (let i = 0; i < 900; i++) { g.globalAlpha = rng() * 0.8; g.fillRect(-pw / 2 + rng() * pw, -ph / 2 + rng() * ph, 1 + rng() * size * 0.05, 1 + rng() * size * 0.03); }
  g.restore(); g.globalCompositeOperation = "source-over"; g.globalAlpha = 1;
}

// ---------- renderer / scene ----------
const PX = S.px || 3000, ASPECT = S.aspect || 1.5;
const W = PX, H = Math.round(PX / ASPECT);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1); renderer.setSize(W, H); renderer.setClearColor(0x000000, 0);
renderer.toneMapping = THREE.NeutralToneMapping; renderer.toneMappingExposure = S.exposure || 1.0;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFShadowMap;
document.body.appendChild(renderer.domElement);
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(S.fov || 18, W / H, 1, 2000);

const LIGHT = { warm: [0xffe2c0, 0xc8dcff], cool: [0xe6efff, 0xffe8cc], neutral: [0xfff6ec, 0xe8f0ff] }[S.light || "neutral"];
const key = new THREE.DirectionalLight(LIGHT[0], S.key ?? 2.2);
key.castShadow = true; key.shadow.mapSize.set(4096, 4096); key.shadow.radius = S.soft ?? 14; key.shadow.blurSamples = 25;
key.shadow.bias = -0.0002; key.shadow.normalBias = 0.02;
Object.assign(key.shadow.camera, { left: -40, right: 40, top: 40, bottom: -40, near: 1, far: 300 });
scene.add(key, key.target);
const fill = new THREE.DirectionalLight(LIGHT[1], 0.35); fill.position.set(60, 40, 50); scene.add(fill);

// shadow-only floor + soft contact occlusion
const floor = new THREE.Mesh(new THREE.PlaneGeometry(400, 400), new THREE.ShadowMaterial({ opacity: S.shadow ?? 0.32 }));
floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true; scene.add(floor);
function contact(w, d, op = 0.45) {   // blurred dark ellipse right under the prop
  const [c, g] = mkCanvas(512, 512); const gr = g.createRadialGradient(256, 256, 0, 256, 256, 256);
  gr.addColorStop(0, `rgba(0,0,0,${op})`); gr.addColorStop(0.55, `rgba(0,0,0,${op * 0.55})`); gr.addColorStop(1, "rgba(0,0,0,0)");
  g.fillStyle = gr; g.fillRect(0, 0, 512, 512);
  const m = new THREE.Mesh(new THREE.PlaneGeometry(w * 1.12, d * 1.12), new THREE.MeshBasicMaterial({ map: tex(c), transparent: true, depthWrite: false }));
  m.rotation.x = -Math.PI / 2; m.position.y = 0.01; m.renderOrder = -1; return m;
}

// ---------- props ----------
function card(o) {
  const w = 8.56, h = 5.398, t = 0.076, r = 0.318, TW = 2048, TH = Math.round(TW * h / w);
  const pal = { navy: ["#0d1b3d", "#1f3a73", "#3f6fb5"], black: ["#0b0b0d", "#1c1c22", "#3a3a44"], maroon: ["#3a0b16", "#6d1426", "#a8324a"],
    teal: ["#062b2b", "#0e5c5a", "#2aa39b"], gold: ["#5a4214", "#a07a2c", "#e3c376"], silver: ["#6f747c", "#b9bec6", "#eef1f4"] }[o.color || "navy"];
  const dark = (o.color || "navy") !== "silver" && o.color !== "gold";
  // colour
  const [c, g] = mkCanvas(TW, TH);
  const gr = g.createLinearGradient(0, TH, TW, 0); gr.addColorStop(0, pal[0]); gr.addColorStop(0.62, pal[1]); gr.addColorStop(1, pal[2]);
  g.fillStyle = gr; g.fillRect(0, 0, TW, TH);
  g.globalAlpha = 0.09; g.strokeStyle = dark ? "#ffffff" : "#000000"; g.lineWidth = 2;   // guilloche
  for (let k = 0; k < 38; k++) { g.beginPath(); for (let x = 0; x <= TW; x += 8) { const y = TH * 0.55 + k * 14 - 260 + Math.sin(x / 190 + k * 0.33) * 90 + Math.sin(x / 61 + k) * 8; x ? g.lineTo(x, y) : g.moveTo(x, y); } g.stroke(); }
  g.globalAlpha = 0.16; const sw = g.createRadialGradient(TW * 0.85, TH * 0.1, 10, TW * 0.85, TH * 0.1, TW * 0.7);
  sw.addColorStop(0, dark ? "#ffffff" : "#ffffff"); sw.addColorStop(1, "rgba(255,255,255,0)"); g.fillStyle = sw; g.fillRect(0, 0, TW, TH); g.globalAlpha = 1;
  const ink = dark ? "#f3f5f8" : "#1b1f27";
  g.fillStyle = ink; g.font = F(800, 74, "Bricolage"); g.fillText(o.brand || "CREDIT CARD", 120, 190);
  g.font = F(500, 50, "Mono"); g.globalAlpha = 0.85; textR(g, o.tier || "PLATINUM", TW - 120, 182); g.globalAlpha = 1;
  // chip (metal maps below give it the gold sheen)
  const cx = 150, cy = 470, cw = 300, ch = 228;
  const cg = g.createLinearGradient(cx, cy, cx + cw, cy + ch); cg.addColorStop(0, "#d9b867"); cg.addColorStop(0.5, "#f3dc9c"); cg.addColorStop(1, "#b8923f");
  g.fillStyle = cg; rrect(g, cx, cy, cw, ch, 36); g.fill();
  g.strokeStyle = "rgba(90,64,20,.75)"; g.lineWidth = 5;
  for (const yy of [cy + ch * 0.33, cy + ch * 0.66]) { g.beginPath(); g.moveTo(cx, yy); g.lineTo(cx + cw * 0.36, yy); g.moveTo(cx + cw * 0.64, yy); g.lineTo(cx + cw, yy); g.stroke(); }
  g.beginPath(); g.moveTo(cx + cw * 0.36, cy); g.lineTo(cx + cw * 0.36, cy + ch); g.moveTo(cx + cw * 0.64, cy); g.lineTo(cx + cw * 0.64, cy + ch); g.stroke();
  rrect(g, cx + cw * 0.36, cy + ch * 0.33, cw * 0.28, ch * 0.33, 10); g.stroke();
  // contactless
  g.strokeStyle = ink; g.lineWidth = 12; g.lineCap = "round"; g.globalAlpha = 0.9;
  for (let k = 0; k < 4; k++) { g.beginPath(); g.arc(cx + cw + 70, cy + ch / 2, 26 + k * 24, -0.75, 0.75); g.stroke(); } g.globalAlpha = 1;
  // printed number, name, date (flat print with a tiny emboss in the bump map)
  const num = o.number || "4821 •••• •••• 7730";
  const drawText = (gg, col) => { gg.fillStyle = col; gg.font = F(500, 116, "Mono"); gg.fillText(num, 140, 930);
    gg.font = F(500, 40, "Mono"); gg.fillText("VALID THRU", 980, 1048); gg.font = F(500, 64, "Mono"); gg.fillText(o.expiry || "08/29", 1250, 1056);
    gg.font = F(500, 64, "Mono"); gg.fillText(o.name || "RAVI KUMAR", 140, 1160); };
  drawText(g, ink);
  if (o.label) { g.font = F(800, 46, "Mono"); g.fillStyle = ink; g.globalAlpha = 0.7; textR(g, o.label, TW - 120, 1160); g.globalAlpha = 1; }
  // roughness/metal map: chip metal, print satin, card body glossy
  const [rc, rg] = mkCanvas(TW, TH); rg.fillStyle = `rgb(0,${dark ? 120 : 95},${o.metal ? 200 : 0})`; rg.fillRect(0, 0, TW, TH);
  rg.fillStyle = "rgb(0,70,255)"; rrect(rg, cx, cy, cw, ch, 36); rg.fill();
  const [bc, bg] = mkCanvas(TW, TH); bg.fillStyle = "#808080"; bg.fillRect(0, 0, TW, TH); drawText(bg, "#a8a8a8");
  bg.strokeStyle = "#5a5a5a"; bg.lineWidth = 6; rrect(bg, cx, cy, cw, ch, 36); bg.stroke();
  const shape = new THREE.Shape(); shape.moveTo(-w / 2 + r, -h / 2); shape.lineTo(w / 2 - r, -h / 2); shape.quadraticCurveTo(w / 2, -h / 2, w / 2, -h / 2 + r);
  shape.lineTo(w / 2, h / 2 - r); shape.quadraticCurveTo(w / 2, h / 2, w / 2 - r, h / 2); shape.lineTo(-w / 2 + r, h / 2);
  shape.quadraticCurveTo(-w / 2, h / 2, -w / 2, h / 2 - r); shape.lineTo(-w / 2, -h / 2 + r); shape.quadraticCurveTo(-w / 2, -h / 2, -w / 2 + r, -h / 2);
  const geo = new THREE.ExtrudeGeometry(shape, { depth: t, bevelEnabled: true, bevelThickness: 0.012, bevelSize: 0.012, bevelSegments: 3, curveSegments: 24 });
  geo.translate(0, 0, -t / 2);
  const uv = geo.attributes.uv, pos = geo.attributes.position;
  for (let i = 0; i < uv.count; i++) uv.setXY(i, (pos.getX(i) + w / 2) / w, (pos.getY(i) + h / 2) / h);
  const face = new THREE.MeshPhysicalMaterial({ map: tex(c), roughnessMap: tex(rc, false), metalnessMap: tex(rc, false), metalness: 1, roughness: 1,
    bumpMap: tex(bc, false), bumpScale: 0.6, clearcoat: o.matte ? 0.15 : 0.85, clearcoatRoughness: o.matte ? 0.6 : 0.16 });
  const edge = new THREE.MeshPhysicalMaterial({ color: dark ? 0xe9e6e0 : 0xd8d8d8, roughness: 0.45 });
  const m = new THREE.Mesh(geo, [face, edge]); m.castShadow = true; m.receiveShadow = true;
  m.rotation.x = -Math.PI / 2; m.position.y = t / 2 + 0.013;
  const grp = new THREE.Group(); grp.add(m, contact(w, h, 0.5)); grp.userData.size = [w, h]; return grp;
}

function paperMesh(w, h, tc, opts = {}) {   // printed sheet with creases (fold lines along y) and a soft curl
  const segX = 80, segY = Math.round(80 * h / w);
  const geo = new THREE.PlaneGeometry(w, h, segX, segY); const p = geo.attributes.position;
  const folds = opts.folds || [], amp = opts.foldAmp ?? 0.35;
  for (let i = 0; i < p.count; i++) { const x = p.getX(i), y = p.getY(i); let z = 0;
    folds.forEach((fy, k) => { const d = Math.abs(y - (fy - 0.5) * h); z += (k % 2 ? -1 : 1) * amp * Math.max(0, 1 - d / (h * 0.36)); });
    z += 0.25 * Math.pow(Math.max(0, (x / w + 0.5) - 0.8) / 0.2, 2) * (opts.curl ?? 1);   // right edge lifts a little
    z += 0.05 * Math.sin(x * 0.7 + y * 0.3);
    p.setZ(i, z); }
  geo.computeVertexNormals();
  let minZ = Infinity; for (let i = 0; i < p.count; i++) minZ = Math.min(minZ, p.getZ(i)); geo.translate(0, 0, -minZ + 0.02);
  const [nc] = noiseCanvas(1024, 1024, 60, 128, 0.6);
  const bump = tex(nc, false); bump.wrapS = bump.wrapT = THREE.RepeatWrapping; bump.repeat.set(3, 3 * h / w);
  const mat = new THREE.MeshPhysicalMaterial({ map: tex(tc), roughness: 0.92, bumpMap: bump, bumpScale: 0.25, sheen: 0.25, sheenRoughness: 0.8, sheenColor: 0xffffff, side: THREE.DoubleSide });
  const m = new THREE.Mesh(geo, mat); m.rotation.x = -Math.PI / 2; m.castShadow = m.receiveShadow = true;
  const grp = new THREE.Group(); grp.add(m, contact(w, h, 0.3)); grp.userData.size = [w, h]; return grp;
}

function paperBase(TW, TH) {
  const [c, g] = mkCanvas(TW, TH); g.fillStyle = "#f7f5ef"; g.fillRect(0, 0, TW, TH); fibres(g, TW, TH, 9000, 0.06);
  const v = g.createRadialGradient(TW / 2, TH / 2, TW * 0.2, TW / 2, TH / 2, TW * 0.9); v.addColorStop(0, "rgba(0,0,0,0)"); v.addColorStop(1, "rgba(120,100,70,.08)");
  g.fillStyle = v; g.fillRect(0, 0, TW, TH); return [c, g];
}

function bill(o) {
  const w = 21, h = 29.7, TW = 2100, TH = 2970, M = 150;
  const [c, g] = paperBase(TW, TH);
  const accent = o.accent || "#1b2a41";
  g.fillStyle = accent; g.fillRect(0, 0, TW, 300);
  g.fillStyle = "#fff"; g.font = F(800, 84, "Bricolage"); g.fillText(o.title || "CREDIT CARD STATEMENT", M, 175);
  g.font = F(500, 36, "Mono"); g.globalAlpha = 0.75; g.fillText(o.period || "STATEMENT DATE  10 OCT 2026", M, 248); g.globalAlpha = 1;
  g.fillStyle = "#374151"; g.font = F(500, 46, "Mono");
  g.fillText(o.name || "RAVI KUMAR", M, 440); g.fillText(o.cardno || "CARD  4821 •••• •••• 7730", M, 510);
  g.fillStyle = "#6b7280"; g.font = F(500, 38, "Mono"); g.fillText(o.address || "FLAT 12, 2ND FLOOR, AMEERPET, HYDERABAD 500016", M, 580);
  // summary boxes
  const boxes = o.boxes || [["TOTAL AMOUNT DUE", "₹10,000"], ["MINIMUM AMOUNT DUE", "₹500"], ["PAYMENT DUE DATE", "05 NOV 2026"]];
  const bw = (TW - 2 * M - 2 * 40) / 3;
  boxes.forEach(([k, v], i) => { const x = M + i * (bw + 40), y = 680; const hi = (o.hiBox ?? -1) === i;
    g.fillStyle = hi ? "#fff2c2" : "#eef0f4"; rrect(g, x, y, bw, 260, 18); g.fill();
    if (hi) { g.strokeStyle = "#e0a400"; g.lineWidth = 6; rrect(g, x, y, bw, 260, 18); g.stroke(); }
    g.fillStyle = "#6b7280"; g.font = F(500, 34, "Mono"); g.fillText(k, x + 36, y + 78);
    g.fillStyle = i === 1 ? "#b42318" : "#111827"; g.font = F(800, v.length > 9 ? 70 : 92); g.fillText(v, x + 36, y + 200); });
  // transactions / charges
  let y = 1120; g.fillStyle = "#111827"; g.font = F(800, 54, "Bricolage"); g.fillText(o.tableTitle || "THIS MONTH", M, y); y += 40;
  g.fillStyle = "#d1d5db"; g.fillRect(M, y, TW - 2 * M, 4); y += 110;
  for (const row of o.rows || [["Previous balance", "₹10,000"], ["Payments received", "₹0"], ["Late payment fee", "₹750"], ["Interest (3.75% a month)", "₹375"], ["GST 18% on fee + interest", "₹203"]]) {
    const [a, b, hi] = row;
    if (hi) { g.fillStyle = "rgba(250,204,21,.45)"; g.fillRect(M - 20, y - 76, TW - 2 * M + 40, 112); }
    g.fillStyle = "#1f2937"; g.font = F(500, 56); g.fillText(a, M, y); g.font = F(800, 58); textR(g, b, TW - M, y);
    g.fillStyle = "#e5e7eb"; g.fillRect(M, y + 40, TW - 2 * M, 3); y += 150;
  }
  if (o.total) { y += 20; g.fillStyle = "#111827"; g.font = F(800, 66, "Bricolage"); g.fillText(o.total[0], M, y); g.font = F(800, 84); textR(g, o.total[1], TW - M, y + 6); y += 120; }
  // fine print
  g.fillStyle = "#c4c8ce"; g.font = F(500, 30, "Mono");   // fine print, greyed like small type
  for (let k = 0; k < 7; k++) { const yy = TH - 470 + k * 46; let x = M; const end = M + (TW - 2 * M) * (k === 6 ? 0.5 : 0.97);
    while (x < end) { const ww = 30 + rng() * 90; g.fillRect(x, yy, Math.min(ww, end - x), 11); x += ww + 14; } }
  g.fillText(o.foot || "SIMULATION · NOT A REAL BANK STATEMENT", M, TH - 90);
  if (o.stamp) stamp(g, o.stamp, TW * 0.66, o.stampY || 1880, 150, "#c0182b", -14);
  return paperMesh(w, h, c, { folds: o.flat ? [] : [1 / 3, 2 / 3], foldAmp: 0.32 });
}

function notice(o) {
  const w = 21, h = 29.7, TW = 2100, TH = 2970, M = 170;
  const [c, g] = paperBase(TW, TH);
  g.fillStyle = "#111827"; g.font = F(800, 64, "Bricolage"); g.fillText(o.from || "LAW CHAMBERS", M, 230);
  g.fillStyle = "#6b7280"; g.font = F(500, 34, "Mono"); g.fillText(o.fromLine || "ADVOCATES · HYDERABAD", M, 290);
  g.fillStyle = "#111827"; g.fillRect(M, 340, TW - 2 * M, 5);
  g.font = F(800, 92, "Bricolage"); const head = o.head || "LEGAL NOTICE"; const hw = g.measureText(head).width; g.fillText(head, (TW - hw) / 2, 520);
  g.font = F(500, 40, "Mono"); g.fillStyle = "#374151"; g.fillText(o.ref || "REF: CC/2026/0417", M, 640); textR(g, o.date || "DATE: 12 OCT 2026", TW - M, 640);
  let y = 800; g.font = F(500, 50); g.fillStyle = "#1f2937";
  for (const line of o.lines || ["To: Mr. Ravi Kumar", "Subject: Unpaid credit card dues", "", "Our client calls upon you to pay the outstanding", "amount within 15 days of this notice."]) {
    if (line) g.fillText(line, M, y); y += 92; }
  g.fillStyle = "#b9bdc4";   // body text as greyed lines
  for (let k = 0; k < (o.bodyLines ?? 11); k++) { g.fillRect(M, y + k * 74, (TW - 2 * M) * (k % 4 === 3 ? 0.55 : 0.92 + 0.08 * rng()), 18); }
  g.fillStyle = "#6b7280"; g.font = F(500, 30, "Mono"); g.fillText("SIMULATION", M, TH - 90);
  if (o.stamp) stamp(g, o.stamp, TW * 0.64, o.stampY || 2350, 130, o.stampColor || "#1d3fb3", -10);
  return paperMesh(w, h, c, { folds: o.flat ? [] : [1 / 3, 2 / 3], foldAmp: 0.3 });
}

function cheque(o) {
  const w = 20.3, h = 9.2, TW = 2436, TH = Math.round(2436 * h / w);
  const [c, g] = mkCanvas(TW, TH);
  const gr = g.createLinearGradient(0, 0, TW, TH); gr.addColorStop(0, "#e9f0f4"); gr.addColorStop(1, "#dfe9ee"); g.fillStyle = gr; g.fillRect(0, 0, TW, TH);
  g.globalAlpha = 0.12; g.strokeStyle = "#5b7c8f"; g.lineWidth = 2;
  for (let k = 0; k < 60; k++) { g.beginPath(); for (let x = 0; x <= TW; x += 10) { const yy = k * 20 + Math.sin(x / 120 + k * 0.5) * 18; x ? g.lineTo(x, yy) : g.moveTo(x, yy); } g.stroke(); }
  g.globalAlpha = 1; fibres(g, TW, TH, 3000, 0.04);
  g.fillStyle = "#1e3a4c"; g.font = F(800, 56, "Bricolage"); g.fillText(o.bank || "SAVINGS BANK", 90, 120);
  g.font = F(500, 34, "Mono"); textR(g, "DATE  " + (o.date || "1 0 1 1 2 0 2 6"), TW - 90, 120);
  g.fillStyle = "#334155"; g.font = F(500, 40, "Mono"); g.fillText("PAY", 90, 300); g.fillText("RUPEES", 90, 430);
  g.fillStyle = "#94a3b8"; g.fillRect(230, 312, TW - 760, 3); g.fillRect(300, 442, TW - 830, 3); g.fillRect(90, 570, TW - 760, 3);
  g.fillStyle = "#1e3a8a"; g.font = `italic 500 70px "Inter Tight"`; g.fillText(o.payee || "Credit Card Dues", 250, 290); g.font = `italic 500 58px "Inter Tight"`;
  g.fillText(o.words || "Ten thousand only", 330, 420);
  g.fillStyle = "#ffffff"; g.fillRect(TW - 600, 360, 510, 120); g.strokeStyle = "#334155"; g.lineWidth = 4; g.strokeRect(TW - 600, 360, 510, 120);
  g.fillStyle = "#1e3a8a"; g.font = F(800, 70); g.fillText(o.amount || "₹10,000/-", TW - 570, 448);
  g.fillStyle = "#111827"; g.font = F(500, 52, "Mono"); g.fillText("⑈004821⑈ 500229017⑆ 000123⑈ 31", 200, TH - 70);
  g.font = F(500, 26, "Mono"); g.fillStyle = "#64748b"; textR(g, "SIMULATION", TW - 90, TH - 150);
  if (o.stamp) stamp(g, o.stamp, TW * 0.5, TH * 0.48, 120, "#c0182b", -8);
  return paperMesh(w, h, c, { folds: [], curl: 0.6 });
}

function phone(o) {
  const w = 7.16, h = 14.76, d = 0.78, r = 0.95, SW = 1170, SH = 2412;   // screen texture at ~460 ppi
  const [c, g] = mkCanvas(SW, SH);
  const bgc = o.wall || ["#1d2a44", "#4a3b5c", "#a35d57"];
  const wg = g.createLinearGradient(0, 0, SW * 0.4, SH); bgc.forEach((col, i) => wg.addColorStop(i / (bgc.length - 1), col)); g.fillStyle = wg; g.fillRect(0, 0, SW, SH);
  for (let k = 0; k < 5; k++) { const bx = SW * rng(), by = SH * rng(); const bl = g.createRadialGradient(bx, by, 0, bx, by, SW * 0.9); bl.addColorStop(0, "rgba(255,255,255,.08)"); bl.addColorStop(1, "rgba(255,255,255,0)"); g.fillStyle = bl; g.fillRect(0, 0, SW, SH); }
  g.fillStyle = "#fff"; g.font = F(500, 40); g.fillText(o.clock || "10:42", 90, 90); textR(g, "5G  ▮▮▮  82%", SW - 90, 90);
  g.fillStyle = "#000"; rrect(g, SW / 2 - 60, 40, 120, 120, 60); g.fill();   // punch-hole camera
  if ((o.screen || "sms") === "call") {
    g.fillStyle = "rgba(255,255,255,.75)"; g.font = F(500, 52); let s = o.callLabel || "Incoming call"; g.fillText(s, (SW - g.measureText(s).width) / 2, 520);
    g.fillStyle = "#fff"; g.font = F(800, 110); s = o.caller || "Unknown number"; g.fillText(s, (SW - g.measureText(s).width) / 2, 700);
    g.font = F(500, 64, "Mono"); s = o.number || "+91 9•••• •••21"; g.fillStyle = "rgba(255,255,255,.85)"; g.fillText(s, (SW - g.measureText(s).width) / 2, 820);
    g.fillStyle = "rgba(255,255,255,.12)"; g.beginPath(); g.arc(SW / 2, 1220, 180, 0, Math.PI * 2); g.fill();
    g.fillStyle = "rgba(255,255,255,.85)"; g.font = F(800, 150); s = o.initial || (o.caller ? o.caller[0] : "?"); if (/^unknown/i.test(o.caller || "Unknown")) s = "?"; g.fillText(s, (SW - g.measureText(s).width) / 2, 1275);
    for (const [x, col, rot] of [[SW * 0.25, "#e5484d", 135], [SW * 0.75, "#2fb35a", 0]]) {
      g.fillStyle = col; g.beginPath(); g.arc(x, SH - 420, 120, 0, Math.PI * 2); g.fill();
      g.save(); g.translate(x, SH - 420 + 14); g.rotate(rot * DEG); g.strokeStyle = "#fff"; g.fillStyle = "#fff"; g.lineWidth = 26; g.lineCap = "round";
      g.beginPath(); g.arc(0, 40, 70, 1.18 * Math.PI, 1.82 * Math.PI); g.stroke();
      for (const sx of [-1, 1]) { g.save(); g.translate(sx * 60, -2); g.rotate(sx * 0.5); rrect(g, -22, -6, 44, 30, 10); g.fill(); g.restore(); }
      g.restore(); }
    g.fillStyle = "rgba(255,255,255,.8)"; g.font = F(500, 44); g.fillText("Decline", SW * 0.25 - 80, SH - 230); g.fillText("Accept", SW * 0.75 - 72, SH - 230);
  } else {
    g.fillStyle = "#fff"; g.font = F(500, 220); let s = o.clock || "10:42"; g.fillText(s, (SW - g.measureText(s).width) / 2, 480);
    g.font = F(500, 56); s = o.date || "Tuesday, 14 October"; g.fillStyle = "rgba(255,255,255,.85)"; g.fillText(s, (SW - g.measureText(s).width) / 2, 580);
    let y = 760;
    for (const n of o.notes || [{ app: "Messages", when: "now", title: "AX-CARDSV", body: "Your credit card payment of Rs.500 is overdue. Pay now to avoid charges." }]) {
      const lines = []; g.font = F(500, 50); let cur = "";
      for (const word of n.body.split(" ")) { const tt = cur ? cur + " " + word : word; if (g.measureText(tt).width > SW - 260) { lines.push(cur); cur = word; } else cur = tt; } lines.push(cur);
      const bh = 190 + lines.length * 66;
      g.fillStyle = "rgba(245,245,248,.9)"; rrect(g, 60, y, SW - 120, bh, 56); g.fill();
      g.fillStyle = "#2fb35a"; rrect(g, 100, y + 44, 64, 64, 16); g.fill();
      g.fillStyle = "#6b7280"; g.font = F(500, 40); g.fillText(n.app.toUpperCase(), 190, y + 90); textR(g, n.when, SW - 110, y + 90);
      g.fillStyle = "#111827"; g.font = F(800, 52); g.fillText(n.title, 100, y + 170);
      g.font = F(500, 50); g.fillStyle = "#1f2937"; lines.forEach((l, i) => g.fillText(l, 100, y + 240 + i * 66));
      y += bh + 34;
    }
  }
  g.fillStyle = "rgba(255,255,255,.7)"; rrect(g, SW / 2 - 200, SH - 60, 400, 14, 7); g.fill();
  const scrTex = tex(c);
  const [ac, ag] = mkCanvas(SW, SH); const grp = new THREE.Group(); ag.fillStyle = "#000"; ag.fillRect(0, 0, SW, SH); ag.fillStyle = "#fff"; rrect(ag, 0, 0, SW, SH, 120); ag.fill();
  const rr = (W2, H2, R2) => { const sh = new THREE.Shape(); sh.moveTo(-W2 / 2 + R2, -H2 / 2); sh.lineTo(W2 / 2 - R2, -H2 / 2); sh.absarc(W2 / 2 - R2, -H2 / 2 + R2, R2, -Math.PI / 2, 0);
    sh.lineTo(W2 / 2, H2 / 2 - R2); sh.absarc(W2 / 2 - R2, H2 / 2 - R2, R2, 0, Math.PI / 2); sh.lineTo(-W2 / 2 + R2, H2 / 2); sh.absarc(-W2 / 2 + R2, H2 / 2 - R2, R2, Math.PI / 2, Math.PI);
    sh.lineTo(-W2 / 2, -H2 / 2 + R2); sh.absarc(-W2 / 2 + R2, -H2 / 2 + R2, R2, Math.PI, 1.5 * Math.PI); return sh; };
  const bev = 0.16, frameMat = new THREE.MeshPhysicalMaterial({ color: o.body || 0x3a3d44, metalness: 0.9, roughness: 0.28, clearcoat: 0.5, clearcoatRoughness: 0.2 });
  const bgeo = new THREE.ExtrudeGeometry(rr(w - 2 * bev, h - 2 * bev, r - bev), { depth: d - 2 * bev, bevelEnabled: true, bevelThickness: bev, bevelSize: bev, bevelSegments: 8, curveSegments: 32 });
  const body = new THREE.Mesh(bgeo, frameMat); body.rotation.x = -Math.PI / 2; body.position.y = bev + 0.02; body.castShadow = body.receiveShadow = true; grp.add(body);
  // glass front (black) with the screen just under its surface
  const bez = 0.2, glassGeo = new THREE.ShapeGeometry(rr(w - 0.16, h - 0.16, r - 0.08), 32);
  const glass = new THREE.Mesh(glassGeo, new THREE.MeshPhysicalMaterial({ color: 0x050506, roughness: 0.05, clearcoat: 1, clearcoatRoughness: 0.03 }));
  glass.rotation.x = -Math.PI / 2; glass.position.y = d + 0.02; grp.add(glass);
  const screen = new THREE.Mesh(new THREE.PlaneGeometry(w - 2 * bez, h - 2 * bez), new THREE.MeshPhysicalMaterial({ map: scrTex, emissiveMap: scrTex, emissive: 0xffffff,
    emissiveIntensity: o.glow ?? 0.85, color: 0x222222, roughness: 0.05, clearcoat: 1, clearcoatRoughness: 0.02, alphaMap: tex(ac, false), transparent: true }));
  screen.rotation.x = -Math.PI / 2; screen.position.y = d + 0.03; grp.add(screen);
  // faint glare across the glass (what a real phone photo always has)
  const [gc, gg] = mkCanvas(512, 1024); const gl = gg.createLinearGradient(0, 0, 512, 1024);
  gl.addColorStop(0, "rgba(255,255,255,0)"); gl.addColorStop(0.38, "rgba(255,255,255,0)"); gl.addColorStop(0.47, "rgba(255,255,255,.10)"); gl.addColorStop(0.6, "rgba(255,255,255,.03)"); gl.addColorStop(1, "rgba(255,255,255,0)");
  gg.fillStyle = gl; gg.fillRect(0, 0, 512, 1024);
  const glare = new THREE.Mesh(new THREE.PlaneGeometry(w - 2 * bez, h - 2 * bez), new THREE.MeshBasicMaterial({ map: tex(gc), transparent: true, depthWrite: false, alphaMap: tex(ac, false) }));
  glare.rotation.x = -Math.PI / 2; glare.position.y = d + 0.035; grp.add(glare);
  for (const [zz, l] of [[-3.2, 1.6], [-1.2, 0.9]]) { const b = new THREE.Mesh(new RoundedBoxGeometry(0.08, 0.24, l, 3, 0.035), frameMat); b.position.set(w / 2 + 0.02, d / 2 + 0.02, zz); grp.add(b); }
  grp.add(contact(w, h, 0.55)); grp.userData.size = [w, h]; return grp;
}

// ---------- build ----------
Promise.all([fontsReady, new HDRLoader().loadAsync("vendor/library/hdri/studio_small_09_1k.hdr")]).then(([, hdr]) => {
  const pm = new THREE.PMREMGenerator(renderer); scene.environment = pm.fromEquirectangular(hdr).texture; scene.environmentIntensity = S.env ?? 0.9;
  const prop = ({ card, bill, notice, cheque, phone })[S.type || "card"](S);
  prop.rotation.y = (S.yaw || 0) * DEG; prop.rotation.z = (S.tilt || 0) * DEG; scene.add(prop);
  const [pw, ph] = prop.userData.size;
  const R = Math.hypot(pw, ph) / 2;
  // light from upper left, a little behind: soft long shadow toward lower right
  key.position.set(-R * 2.2, R * 4.2, -R * 1.6); key.target.position.set(0, 0, 0);
  const el = (S.elev ?? 58) * DEG, az = (S.az ?? 0) * DEG;
  const dist = (R * (S.fit || 1.18)) / Math.tan((camera.fov / 2) * DEG) * (ASPECT < 1 ? 1 / ASPECT : 1);
  camera.position.set(Math.sin(az) * Math.cos(el) * dist, Math.sin(el) * dist, Math.cos(az) * Math.cos(el) * dist);
  camera.lookAt(0, 0, 0);
  renderer.render(scene, camera);
  window.__ready = true;
});
