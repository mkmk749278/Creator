// Session B kit: helpers shared by B1–B4. Everything is a pure function of timeline time t (seconds):
// per-frame values are computed in K.render(t), which the scene's one paused timeline calls from onUpdate
// (tl.call does not run on render seeks, PLAYBOOK §10). No Date.now, no Math.random.
(function () {
  const K = {};
  K.inr = (v) => "₹" + Math.round(v).toLocaleString("en-IN");          // 330000 -> ₹3,30,000
  K.rng = (seed) => () => { seed |= 0; seed = (seed + 0x6d2b79f5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  // piecewise value: keys [[t, v], ...]; sine ease between keys, held outside
  K.keys = (keys) => (t) => {
    if (t <= keys[0][0]) return keys[0][1];
    for (let i = 1; i < keys.length; i++) { const [t1, v1] = keys[i], [t0, v0] = keys[i - 1];
      if (t <= t1) { const u = (t - t0) / Math.max(1e-6, t1 - t0); return v0 + (v1 - v0) * (0.5 - 0.5 * Math.cos(Math.PI * u)); } }
    return keys[keys.length - 1][1];
  };
  const hooks = [];
  K.hook = (fn) => hooks.push(fn);
  K.text = (el, fn) => { let last = null; hooks.push((t) => { const s = fn(t); if (s !== last) { el.textContent = s; last = s; } }); };
  K.render = (t) => { for (const h of hooks) h(t); };

  // segments: one composition holds several VO windows back to back, each window + 0.25 s handle on both sides,
  // rounded to whole frames; scripts/split cuts them apart at these frame boundaries.
  K.FPS = 30;
  K.layout = (segs) => { let f = 0; return segs.map((s) => { const n = Math.round((s.we - s.ws + 0.5) * K.FPS - 1e-6);   // x.5 frames round down (split.py does the same)
    const o = { ...s, off: f / K.FPS, len: n / K.FPS, f0: f, nf: n }; f += n; o.v = (vt) => o.off + (vt - (s.ws - 0.25)); return o; }); };
  K.total = (L) => L.reduce((a, s) => a + s.len, 0);

  // film grain: one seeded tile, shifted per frame (24 steps a second, cycle of 7)
  K.grain = (canvas, seed = 7) => {
    const g = canvas.getContext("2d"), w = canvas.width, h = canvas.height, img = g.createImageData(w, h), r = K.rng(seed);
    for (let i = 0; i < img.data.length; i += 4) { const v = 90 + r() * 120; img.data[i] = img.data[i + 1] = img.data[i + 2] = v; img.data[i + 3] = 255; }
    g.putImageData(img, 0, 0);
    hooks.push((t) => { const f = Math.floor(t * 24) % 7; canvas.style.transform = `translate(${(f * 13) % 40 - 20}px, ${(f * 7) % 30 - 15}px) scale(4)`; });
  };
  // dust motes in the window light: positions are a function of t only
  K.dust = (canvas, n = 46, seed = 11) => {
    const g = canvas.getContext("2d"), r = K.rng(seed), W = canvas.width, H = canvas.height;
    const P = Array.from({ length: n }, () => ({ x: r() * W, y: r() * H, s: 0.6 + r() * 2.2, vx: 4 + r() * 10, vy: -3 - r() * 7, ph: r() * 6.28, a: 0.15 + r() * 0.35 }));
    hooks.push((t) => { g.clearRect(0, 0, W, H);
      for (const p of P) { const x = ((p.x + p.vx * t + 14 * Math.sin(t * 0.4 + p.ph)) % W + W) % W, y = ((p.y + p.vy * t) % H + H) % H;
        const lit = Math.max(0, 1 - x / (W * 0.75));   // motes only glow where the window light falls
        g.globalAlpha = Math.min(1, 1.8 * p.a * lit) * (0.6 + 0.4 * Math.sin(t * 0.9 + p.ph)); g.fillStyle = "#ffe7c2";
        g.beginPath(); g.arc(x, y, p.s, 0, 6.2832); g.fill(); } });
  };

  // revision v2: the documents of one family and one claim (projects/insurance-ombudsman/revision-v2.md), all SIMULATION and
  // invented. Any element with data-doc="<key>" is filled with that document at load.
  const SIM = '<div class="sim">SIMULATION</div>';
  K.DOCS = {
    D2: SIM + `<div class="ttl" style="margin-top:14px">CLAIM RECOVERY SERVICE AGREEMENT</div>
      <div class="ref">Agreement No. CRS-2026-0412 · Hyderabad · 12 Sep 2026</div><hr>
      <div class="row">Client: <b>R. Kumar</b></div>
      <div class="row">Claim No.: <b>CLM-2408-55217</b></div>
      <div class="row">Claim: <b>₹3,30,000</b></div>
      <div class="key"><span class="hl"></span><span style="position:relative">Service fee: 20% of the amount recovered + GST as applicable</span></div>
      <div class="small">1. The agency will prepare and follow up the client's claim papers.</div>
      <div class="small">2. The fee is payable on the amount recovered.</div>
      <div class="small">3. This agreement is valid for 12 months.</div>
      <div class="sign">Signature<u></u></div>`,
    D5: SIM + `<div class="org" style="margin-top:16px">Complaint to the Insurance Ombudsman, Hyderabad</div>
      <div class="ref" style="margin-top:8px">Complaint No. HYD-H-2026-0471</div><hr>
      <div class="row">Complainant: <b>R. Kumar</b></div>
      <div class="row">Against: <b>Sample Health Insurance Co. Ltd.</b></div>
      <div class="row">Relief sought: <b>₹3,30,000</b></div>`,
    D6: SIM + `<div class="org" style="margin-top:16px">Sample Health Insurance Co. Ltd.</div>
      <div class="ttl">Reply of the insurer</div>
      <div class="ref">Complaint No. HYD-H-2026-0471</div><hr>
      <div class="row">The deduction was made under the policy terms.</div>`,
    D7: SIM + `<div class="org" style="margin-top:16px">Office of the Insurance Ombudsman, Hyderabad</div>
      <div class="ttl" style="margin-top:16px">AWARD under Rule 17</div>
      <div class="ref">Complaint No. HYD-H-2026-0471<br>R. Kumar v. Sample Health Insurance Co. Ltd.</div><hr>
      <div class="key" style="font-weight:600"><span class="hl"></span><span style="position:relative">The insurer shall pay <b>₹3,30,000</b> to the complainant within 30 days of receipt of this award.</span></div>
      <div class="small" style="margin-top:14px">Hyderabad · 10 Sep 2026</div>
      <div class="sign" style="bottom:70px">Insurance Ombudsman</div>`,
    D8: SIM + `<div class="ttl" style="margin-top:16px">RECOMMENDATION<br>under Rule 16</div>
      <div class="ref">Complaint No. HYD-H-2026-0471</div><hr>
      <div class="row">Settlement offered: <b>₹2,60,000</b></div>
      <div class="row" style="margin-top:22px">Complainant: agreed <span class="ok" data-tick="1">✓</span></div>
      <div class="row">Insurer: agreed <span class="ok" data-tick="2">✓</span></div>
      <div class="key" data-closed style="color:#1f8f7b">Case closed</div>`,
    REJ: SIM + `<div class="org" style="margin-top:14px; font-size:15px">Sample Health Insurance Co. Ltd.</div>
      <div class="ref" style="font-size:14px; margin:6px 0 8px">Reply to grievance · CLM-2408-55217</div><hr style="margin:6px 0 10px">
      <div class="row" style="font-size:22px">Your grievance has been examined. It is not accepted.</div>`,
    REPLY: SIM + `<div class="org" style="margin-top:14px; font-size:15px">Sample Health Insurance Co. Ltd.</div>
      <div class="ref" style="font-size:14px; margin:6px 0 8px">Reply to grievance · CLM-2408-55217</div><hr style="margin:6px 0 10px">
      <div class="row" style="font-size:20px">We have reviewed your complaint. The deduction was made as per the policy. Our decision stands.</div>`,
  };
  K.fillDocs = () => document.querySelectorAll("[data-doc]").forEach((el) => {
    const d = document.createElement("div"); d.className = "dx"; d.innerHTML = K.DOCS[el.dataset.doc]; el.prepend(d);
    // papers lie rotated on the desk, so their line boxes overlap as rectangles: tell the layout audit this is intended
    d.querySelectorAll("*").forEach((n) => n.setAttribute("data-layout-allow-overlap", "")); });
  K.attach = (tl) => { tl.eventCallback("onUpdate", () => K.render(tl.time())); K.render(0); };
  window.K = K;
})();
