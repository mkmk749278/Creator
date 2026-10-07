// Scene library for the breath-hold documentary.
// HF_build(tl, scenes, opts) creates one <section class="clip"> per scene inside #stage
// and adds seek-safe tweens at absolute times. Every scene type is pure DOM/SVG + GSAP:
// no randomness (seeded LCG only), no Date.now, no infinite repeats.
(function () {
  const E = "power3.out";
  const NS = "http://www.w3.org/2000/svg";
  let seed = 16;
  const rand = () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const h = (html) => { const d = document.createElement("div"); d.innerHTML = html.trim(); return d.firstChild; };
  const mmss = (s) => { s = Math.max(0, Math.round(s)); return String(Math.floor(s / 60)).padStart(2, "0") + ":" + String(s % 60).padStart(2, "0"); };
  const inn = (tl, el, t, from, d) => tl.fromTo(el, Object.assign({ opacity: 0 }, from || { y: 30 }),
    { opacity: 1, x: 0, y: 0, scale: 1, duration: d || 0.6, ease: E, immediateRender: false }, t);
  const counter = (tl, el, a, b, t, d, fmt, ease) => {
    const o = { v: a };
    tl.fromTo(o, { v: a }, { v: b, duration: d, ease: ease || "none", immediateRender: false,
      onUpdate: () => { el.textContent = fmt(o.v); } }, t);
    // Make the value correct when seeking before the counter starts.
    tl.call(() => { el.textContent = fmt(a); }, null, Math.max(0, t - 0.01));
  };
  // Slow push-in on a whole scene so nothing is ever fully static.
  const drift = (tl, el, t, d, s) => tl.fromTo(el, { scale: 1 }, { scale: s || 1.035, duration: d, ease: "none", immediateRender: false }, t);

  const B = {};

  // ------------------------------------------------------------ title
  B.title = (el, s, tl, t) => {
    el.innerHTML = `<div class="scene" style="flex-direction:column;justify-content:center;gap:34px;${s.center ? "align-items:center;text-align:center;" : ""}">
      ${s.eyebrow ? `<div class="eyebrow">${s.eyebrow}</div>` : ""}
      <h1 class="h1 te" style="max-width:1500px;${s.size ? "font-size:" + s.size + "px" : ""}">${s.title}</h1>
      ${s.sub ? `<p class="sub te" style="max-width:1300px">${s.sub}</p>` : ""}
      ${s.tag ? `<div><span class="tag ${s.tagClass || "o2"}">${s.tag}</span></div>` : ""}</div>`;
    const sc = el.querySelector(".scene");
    [...sc.children].forEach((c, i) => inn(tl, c, t + 0.15 + i * (s.stagger || 0.45)));
    drift(tl, sc, t, s.dur, 1.03);
  };

  // ------------------------------------------------------------ question (hook): huge "?" + text
  B.question = (el, s, tl, t) => {
    el.innerHTML = `<div class="scene" style="align-items:center;gap:80px">
      <div class="qmark" style="font-size:520px;font-weight:800;line-height:0.8;color:var(--o2);opacity:.9">?</div>
      <div style="display:flex;flex-direction:column;gap:30px;max-width:1150px">
        <h1 class="h1 te" style="font-size:88px">${s.title}</h1>
        ${s.sub ? `<p class="sub te">${s.sub}</p>` : ""}</div></div>`;
    inn(tl, el.querySelector(".qmark"), t + 0.1, { scale: 0.6, rotation: -12 }, 0.9);
    el.querySelectorAll("h1, .sub").forEach((c, i) => inn(tl, c, t + 0.4 + i * 0.7));
    drift(tl, el.querySelector(".scene"), t, s.dur);
  };

  // ------------------------------------------------------------ ladder: what happens minute by minute
  B.ladder = (el, s, tl, t) => {
    const rows = s.items.map((it, i) => `<div class="lrow" style="display:grid;grid-template-columns:220px 1fr;align-items:center;gap:40px;height:${s.rowH || 150}px;padding:0 44px;border-left:8px solid var(--${it.color || "o2"})" >
        <div class="num" style="font-size:72px;font-weight:800;color:var(--${it.color || "o2"})">${it.t}</div>
        <div class="te" style="font-size:46px;font-weight:700;line-height:1.3">${it.te}</div></div>`).join("");
    el.innerHTML = `<div class="scene" style="flex-direction:column;gap:22px;justify-content:center">
      ${s.title ? `<div class="h2 te" style="font-size:60px;margin-bottom:16px">${s.title}</div>` : ""}${rows}</div>`;
    const sc = el.querySelector(".scene");
    if (s.title) inn(tl, sc.firstElementChild, t + 0.1);
    el.querySelectorAll(".lrow").forEach((r, i) => inn(tl, r, t + (s.at ? s.at[i] : 0.5 + i * 1.2), { x: -60 }));
    drift(tl, sc, t, s.dur, 1.02);
  };

  // ------------------------------------------------------------ timer: big stopwatch ring
  B.timer = (el, s, tl, t) => {
    const R = 330, C = 2 * Math.PI * R;
    el.innerHTML = `<div class="scene" style="align-items:center;justify-content:center;gap:110px">
      <svg width="800" height="800" viewBox="0 0 800 800" class="ring">
        <circle cx="400" cy="400" r="${R}" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="26"/>
        ${Array.from({ length: 60 }, (_, i) => { const a = i / 60 * 2 * Math.PI; const r1 = i % 5 ? 372 : 360;
          return `<line x1="${400 + Math.sin(a) * r1}" y1="${400 - Math.cos(a) * r1}" x2="${400 + Math.sin(a) * 384}" y2="${400 - Math.cos(a) * 384}" stroke="rgba(255,255,255,${i % 5 ? 0.18 : 0.45})" stroke-width="${i % 5 ? 2 : 4}"/>`; }).join("")}
        <circle class="arc" cx="400" cy="400" r="${R}" fill="none" stroke="var(--${s.color || "o2"})" stroke-width="26" stroke-linecap="round"
          transform="rotate(-90 400 400)" stroke-dasharray="${C}" stroke-dashoffset="${C}"/>
        <text class="tval num" x="400" y="440" text-anchor="middle" fill="var(--ink)" font-size="150" font-weight="800" font-family="Inter">${mmss(s.from)}</text>
        <text x="400" y="520" text-anchor="middle" fill="var(--ink-dim)" font-size="34" font-weight="600" font-family="Inter" letter-spacing="6">MIN : SEC</text>
      </svg>
      <div class="side" style="display:flex;flex-direction:column;gap:30px;max-width:720px">
        ${s.eyebrow ? `<div class="eyebrow">${s.eyebrow}</div>` : ""}
        <div class="h2 te">${s.title}</div>
        ${s.sub ? `<p class="sub te">${s.sub}</p>` : ""}
        ${s.tag ? `<div><span class="tag ${s.tagClass || "co2"}">${s.tag}</span></div>` : ""}</div></div>`;
    const svg = el.querySelector(".ring"), arc = el.querySelector(".arc"), tv = el.querySelector(".tval");
    inn(tl, svg, t + 0.05, { scale: 0.85 }, 0.8);
    el.querySelectorAll(".side > *").forEach((c, i) => inn(tl, c, t + 0.35 + i * 0.4, { x: 40 }));
    const rs = t + (s.runAt ?? 0.6), rd = s.runDur ?? Math.max(1, s.dur - 1.5);
    const full = s.full || 960;
    tl.fromTo(arc, { attr: { "stroke-dashoffset": C * (1 - s.from / full) } },
      { attr: { "stroke-dashoffset": C * (1 - s.to / full) }, duration: rd, ease: s.ease || "power1.inOut", immediateRender: false }, rs);
    counter(tl, tv, s.from, s.to, rs, rd, mmss, s.ease || "power1.inOut");
  };

  // ------------------------------------------------------------ monitor: SpO2 traces (illustration)
  B.monitor = (el, s, tl, t) => {
    const W = 1300, H = 520;
    const path = (pts) => pts.map((p, i) => (i ? "L" : "M") + (p[0] * W).toFixed(1) + " " + ((1 - p[1]) * H).toFixed(1)).join(" ");
    // y in [0..1] maps oxygen 50%..100%
    const y = (o) => (o - 50) / 50;
    const normal = [], trained = [];
    for (let i = 0; i <= 60; i++) {
      const x = i / 60;                        // 0..16 minutes
      const m = x * 16;
      normal.push([x, y(m < 2 ? 98 - m * 1.5 : Math.max(55, 95 - (m - 2) * 14))]);
      trained.push([x, y(98 - m * 0.9)]);
    }
    el.innerHTML = `<div class="scene" style="flex-direction:column;gap:26px">
      <div class="hdr" style="display:flex;align-items:baseline;gap:28px"><div class="h2 te" style="font-size:58px">${s.title}</div>
        <span class="tag calm">${s.tag || "Illustration, not measured data"}</span></div>
      <div class="glass panel" style="position:relative;padding:40px 60px 50px 120px;width:1640px">
        <svg width="${W}" height="${H + 60}" viewBox="0 -10 ${W} ${H + 70}" style="overflow:visible">
          ${[50, 75, 100].map((o) => `<line x1="0" x2="${W}" y1="${(1 - y(o)) * H}" y2="${(1 - y(o)) * H}" stroke="rgba(255,255,255,0.1)"/><text x="-24" y="${(1 - y(o)) * H + 10}" text-anchor="end" fill="var(--ink-dim)" font-size="30" font-family="Inter">${o}%</text>`).join("")}
          ${[0, 4, 8, 12, 16].map((m) => `<text x="${m / 16 * W}" y="${H + 50}" text-anchor="middle" fill="var(--ink-dim)" font-size="30" font-family="Inter">${m} min</text>`).join("")}
          <line x1="0" x2="${W}" y1="${(1 - y(90)) * H}" y2="${(1 - y(90)) * H}" stroke="var(--alarm)" stroke-dasharray="10 10" opacity="0.6"/>
          <text x="10" y="${(1 - y(90)) * H - 14}" text-anchor="start" fill="var(--alarm)" font-size="30" font-family="Inter" font-weight="700">${s.danger || "Danger zone"}</text>
          <path class="pn" d="${path(normal)}" fill="none" stroke="var(--co2)" stroke-width="7" stroke-linecap="round"/>
          <path class="pt" d="${path(trained)}" fill="none" stroke="var(--o2)" stroke-width="7" stroke-linecap="round"/>
        </svg>
        <div class="legend" style="position:absolute;right:60px;bottom:120px;display:flex;flex-direction:column;gap:12px;font-size:32px;font-weight:700">
          <div class="co2 te">● ${s.a || "సాధారణ మనిషి"}</div><div class="o2 te">● ${s.b || "శిక్షణ పొందిన యోగి"}</div></div>
      </div></div>`;
    inn(tl, el.querySelector(".hdr"), t + 0.1);
    inn(tl, el.querySelector(".panel"), t + 0.3, { y: 40 });
    inn(tl, el.querySelector(".legend"), t + 1.0, { x: 30 });
    ["pn", "pt"].forEach((c, i) => {
      const p = el.querySelector("." + c), L = 2600;
      p.setAttribute("stroke-dasharray", L);
      tl.fromTo(p, { attr: { "stroke-dashoffset": L } }, { attr: { "stroke-dashoffset": 0 }, duration: Math.min(s.dur - 1.5, 7), ease: "power1.inOut", immediateRender: false }, t + 0.9 + i * 0.6);
    });
  };

  // ------------------------------------------------------------ records: horizontal bars
  B.records = (el, s, tl, t) => {
    const max = (s.max || Math.max(...s.rows.map((r) => r.secs))) / 0.72;
    const rows = s.rows.map((r) => `<div class="rrow" style="display:grid;grid-template-columns:470px 1fr;gap:34px;align-items:center">
        <div><div style="font-size:42px;font-weight:800">${r.name}</div><div class="te" style="font-size:30px;color:var(--ink-dim);margin-top:6px">${r.sub}</div></div>
        <div style="position:relative;height:96px"><div class="bar" style="position:absolute;left:0;top:0;bottom:0;width:${r.secs / max * 100}%;border-radius:18px;background:var(--${r.color});transform-origin:left center"></div>
          <div class="bv num" style="position:absolute;top:50%;transform:translateY(-50%);left:calc(${r.secs / max * 100}% + 26px);font-size:56px;font-weight:800;white-space:nowrap">${mmss(r.secs)}${r.tag ? ` <span class="tag" style="font-size:22px;vertical-align:middle;color:var(--${r.color})">${r.tag}</span>` : ""}</div></div></div>`).join("");
    el.innerHTML = `<div class="scene" style="flex-direction:column;gap:46px;justify-content:center">
      <div class="h2 te" style="font-size:60px">${s.title}</div>${rows}
      ${s.note ? `<div class="sub te note" style="font-size:30px">${s.note}</div>` : ""}</div>`;
    inn(tl, el.querySelector(".h2"), t + 0.1);
    el.querySelectorAll(".rrow").forEach((r, i) => {
      const at = t + (s.at ? s.at[i] : 0.6 + i * 1.4);
      inn(tl, r.firstElementChild, at, { x: -40 });
      tl.fromTo(r.querySelector(".bar"), { scaleX: 0 }, { scaleX: 1, duration: 1.2, ease: E, immediateRender: false }, at + 0.1);
      inn(tl, r.querySelector(".bv"), at + 1.0, { x: -20 });
    });
    if (s.note) inn(tl, el.querySelector(".note"), t + (s.noteAt || s.dur - 3));
  };

  // ------------------------------------------------------------ lungs: CO2 build-up, pH, diaphragm spasm
  B.lungs = (el, s, tl, t) => {
    const parts = Array.from({ length: 70 }, () => [rand(), rand(), rand()]);
    el.innerHTML = `<div class="scene" style="align-items:center;gap:90px">
      <svg class="torso" width="760" height="760" viewBox="0 0 760 760">
        <path d="M380 40 L380 210" stroke="rgba(255,255,255,0.35)" stroke-width="22" stroke-linecap="round"/>
        <path d="M380 210 C330 230 300 250 290 280 M380 210 C430 230 460 250 470 280" stroke="rgba(255,255,255,0.35)" stroke-width="14" fill="none" stroke-linecap="round"/>
        <g class="lung">
          <path d="M290 200 C180 210 120 330 110 460 C100 560 150 600 230 590 C300 580 340 560 350 500 L350 260 C350 220 320 198 290 200Z" fill="rgba(79,209,197,0.16)" stroke="var(--o2)" stroke-width="4"/>
          <path d="M470 200 C580 210 640 330 650 460 C660 560 610 600 530 590 C460 580 420 560 410 500 L410 260 C410 220 440 198 470 200Z" fill="rgba(79,209,197,0.16)" stroke="var(--o2)" stroke-width="4"/>
          <path class="tint" d="M290 200 C180 210 120 330 110 460 C100 560 150 600 230 590 C300 580 340 560 350 500 L350 260 C350 220 320 198 290 200Z M470 200 C580 210 640 330 650 460 C660 560 610 600 530 590 C460 580 420 560 410 500 L410 260 C410 220 440 198 470 200Z" fill="var(--co2)" opacity="0"/>
        </g>
        <path class="dia" d="M90 640 C200 560 300 548 380 548 C460 548 560 560 670 640" fill="none" stroke="var(--gold)" stroke-width="16" stroke-linecap="round"/>
        <g class="pts">${parts.map(([a, b, c]) => { const left = a < 0.5; const cx = left ? 150 + b * 180 : 430 + b * 180; const cy = 280 + c * 280;
          return `<circle cx="${cx.toFixed(0)}" cy="${cy.toFixed(0)}" r="${(5 + c * 6).toFixed(1)}" fill="var(--co2)" opacity="0"/>`; }).join("")}</g>
        <text x="380" y="720" text-anchor="middle" fill="var(--gold)" font-size="32" font-weight="700" font-family="Inter">${s.diaLabel || "Diaphragm"}</text>
      </svg>
      <div class="side" style="display:flex;flex-direction:column;gap:34px;max-width:780px">
        ${s.eyebrow ? `<div class="eyebrow co2">${s.eyebrow}</div>` : ""}
        <div class="h2 te" style="font-size:62px">${s.title}</div>
        <div class="glass meters" style="padding:34px 40px;display:flex;flex-direction:column;gap:24px">
          <div style="display:flex;justify-content:space-between;align-items:baseline"><span class="te" style="font-size:34px;font-weight:700">CO₂</span><span class="co2v num co2" style="font-size:52px;font-weight:800">${s.co2From || "40"} mmHg</span></div>
          <div style="height:16px;border-radius:9px;background:rgba(255,255,255,0.08);overflow:hidden"><div class="co2b" style="height:100%;width:100%;background:var(--co2);transform-origin:left;transform:scaleX(0.35)"></div></div>
          <div style="display:flex;justify-content:space-between;align-items:baseline"><span class="te" style="font-size:34px;font-weight:700">Blood pH</span><span class="phv num" style="font-size:52px;font-weight:800">7.40</span></div>
          <div class="te" style="font-size:30px;color:var(--ink-dim)">${s.meterNote || "CO₂ + H₂O → carbonic acid → రక్తం ఆమ్లంగా మారుతుంది"}</div>
        </div>
        ${s.sub ? `<p class="sub te" style="font-size:34px">${s.sub}</p>` : ""}</div></div>`;
    const svg = el.querySelector(".torso");
    inn(tl, svg, t + 0.1, { scale: 0.9 }, 0.8);
    el.querySelectorAll(".side > *").forEach((c, i) => inn(tl, c, t + 0.4 + i * 0.4, { x: 40 }));
    const a = t + 1.2, d = Math.max(2, s.dur - 2.5);
    const dots = el.querySelectorAll(".pts circle");
    tl.fromTo(dots, { opacity: 0, scale: 0.2, transformOrigin: "50% 50%" }, { opacity: 0.85, scale: 1, duration: 0.6, stagger: d * 0.6 / dots.length, ease: E, immediateRender: false }, a);
    tl.fromTo(el.querySelector(".tint"), { opacity: 0 }, { opacity: 0.35, duration: d, ease: "power1.in", immediateRender: false }, a);
    tl.fromTo(el.querySelector(".co2b"), { scaleX: 0.35 }, { scaleX: 0.9, duration: d, ease: "power1.in", immediateRender: false }, a);
    counter(tl, el.querySelector(".co2v"), +(s.co2From || 40), +(s.co2To || 70), a, d, (v) => Math.round(v) + " mmHg", "power1.in");
    counter(tl, el.querySelector(".phv"), 7.4, +(s.phTo || 7.25), a, d, (v) => v.toFixed(2), "power1.in");
    // Diaphragm: breathing sway, then involuntary twitches (finite repeats) near the end
    const dia = el.querySelector(".dia");
    const sp = a + d * (s.spasmAt ?? 0.55);
    const reps = Math.max(1, Math.floor((t + s.dur - sp - 0.4) / 0.36));
    tl.fromTo(dia, { y: 0 }, { y: -26, duration: 0.18, ease: "power2.out", yoyo: true, repeat: reps * 2 - 1, immediateRender: false }, sp);
    tl.fromTo(dia, { stroke: "#e8c27a" }, { stroke: "#ff5d6c", duration: 0.4, immediateRender: false }, sp);
    tl.fromTo(el.querySelector(".lung"), { y: 0 }, { y: -6, duration: 0.18, ease: "power2.out", yoyo: true, repeat: reps * 2 - 1, immediateRender: false }, sp);
  };

  // ------------------------------------------------------------ chemo: brainstem + carotid alarm loop
  B.chemo = (el, s, tl, t) => {
    el.innerHTML = `<div class="scene" style="align-items:center;gap:80px">
      <svg width="820" height="800" viewBox="0 0 820 800" class="head">
        <path d="M410 70 C250 70 150 180 150 320 C150 420 200 470 260 500 L270 600 L330 610 L340 540 C380 545 420 545 460 530 C560 500 660 430 660 300 C660 160 560 70 410 70Z" fill="rgba(143,156,255,0.08)" stroke="rgba(255,255,255,0.35)" stroke-width="4"/>
        <path d="M250 260 C300 200 380 190 440 210 C500 190 570 220 590 280 C610 340 560 390 500 380 C460 410 380 410 340 380 C280 390 230 330 250 260Z" fill="rgba(143,156,255,0.18)" stroke="var(--calm)" stroke-width="3"/>
        <path class="stem" d="M400 380 C400 430 395 470 380 520" stroke="var(--calm)" stroke-width="22" stroke-linecap="round" fill="none"/>
        <path d="M330 600 L330 790 M450 560 L460 790" stroke="rgba(255,90,108,0.55)" stroke-width="14" stroke-linecap="round"/>
        <circle class="car" cx="330" cy="680" r="18" fill="var(--co2)"/><circle class="car" cx="456" cy="680" r="18" fill="var(--co2)"/>
        <path class="sig" d="M330 680 C320 600 340 520 380 500" stroke="var(--alarm)" stroke-width="7" fill="none" stroke-dasharray="14 12"/>
        <path class="sig" d="M456 680 C450 600 420 530 395 505" stroke="var(--alarm)" stroke-width="7" fill="none" stroke-dasharray="14 12"/>
        <circle class="core" cx="392" cy="470" r="34" fill="var(--alarm)" opacity="0.25"/>
        <text x="560" y="470" fill="var(--calm)" font-size="30" font-weight="700" font-family="Inter">Brainstem</text>
        <text x="500" y="690" fill="var(--co2)" font-size="30" font-weight="700" font-family="Inter">Carotid body</text>
      </svg>
      <div class="side" style="display:flex;flex-direction:column;gap:30px;max-width:820px">
        ${s.eyebrow ? `<div class="eyebrow alarm">${s.eyebrow}</div>` : ""}
        <div class="h2 te" style="font-size:62px">${s.title}</div>
        ${s.sub ? `<p class="sub te">${s.sub}</p>` : ""}
        <div class="alarmtxt te" style="font-size:72px;font-weight:800;color:var(--alarm)">${s.alarm || "BREATHE!"}</div></div></div>`;
    inn(tl, el.querySelector(".head"), t + 0.1, { scale: 0.92 }, 0.8);
    el.querySelectorAll(".side > *").forEach((c, i) => inn(tl, c, t + 0.4 + i * 0.5, { x: 40 }));
    const a = t + 1.4, d = s.dur - 1.8;
    const reps = Math.max(1, Math.floor(d / 0.5));
    tl.fromTo(el.querySelectorAll(".sig"), { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": -26 * reps }, duration: d, ease: "none", immediateRender: false }, a);
    tl.fromTo(el.querySelectorAll(".car"), { scale: 1, transformOrigin: "50% 50%" }, { scale: 1.45, duration: 0.25, yoyo: true, repeat: reps * 2 - 1, ease: "sine.inOut", immediateRender: false }, a);
    tl.fromTo(el.querySelector(".core"), { opacity: 0.2, scale: 1, transformOrigin: "50% 50%" }, { opacity: 0.9, scale: 1.5, duration: 0.25, yoyo: true, repeat: reps * 2 - 1, ease: "sine.inOut", immediateRender: false }, a);
    tl.fromTo(el.querySelector(".alarmtxt"), { scale: 1 }, { scale: 1.06, duration: 0.25, yoyo: true, repeat: reps * 2 - 1, ease: "sine.inOut", immediateRender: false }, a + 0.6);
  };

  // ------------------------------------------------------------ heart: ECG trace, BPM slows
  B.heart = (el, s, tl, t) => {
    const W = 1640, H = 300;
    // Beat spacing widens from left to right: heart rate falling.
    let d = "M0 150", x = 0;
    const b0 = s.bpmFrom || 72, b1 = s.bpmTo || 40;
    while (x < W - 80) {
      const bpm = b0 + (b1 - b0) * (x / W);
      const gap = 9000 / bpm;
      d += ` L${x + gap * 0.45} 150 L${x + gap * 0.5} 130 L${x + gap * 0.55} 150 L${x + gap * 0.62} 160 L${x + gap * 0.66} 30 L${x + gap * 0.7} 220 L${x + gap * 0.74} 150 L${x + gap * 0.86} 150 L${x + gap * 0.9} 120 L${x + gap * 0.95} 150`;
      x += gap;
    }
    d += ` L${W} 150`;
    el.innerHTML = `<div class="scene" style="flex-direction:column;gap:40px;justify-content:center">
      <div class="top" style="display:flex;align-items:flex-end;justify-content:space-between;width:1640px">
        <div style="display:flex;flex-direction:column;gap:20px;max-width:1050px">${s.eyebrow ? `<div class="eyebrow">${s.eyebrow}</div>` : ""}<div class="h2 te" style="font-size:62px">${s.title}</div></div>
        <div style="text-align:right"><div class="bpm num" style="font-size:170px;font-weight:800;line-height:1;color:var(--alarm)">${b0}</div><div style="font-size:32px;font-weight:700;color:var(--ink-dim);letter-spacing:.2em">BPM</div></div></div>
      <div class="glass" style="padding:40px 0;width:1640px"><svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
        <path class="ecg" d="${d}" fill="none" stroke="var(--alarm)" stroke-width="6" stroke-linejoin="round"/></svg></div>
      ${s.sub ? `<p class="sub te" style="max-width:1640px">${s.sub}</p>` : ""}</div>`;
    el.querySelectorAll(".scene > *").forEach((c, i) => inn(tl, c, t + 0.1 + i * 0.35));
    const p = el.querySelector(".ecg"), L = 9000;
    p.setAttribute("stroke-dasharray", L);
    const a = t + 0.7, dd = Math.max(2, s.dur - 1.6);
    tl.fromTo(p, { attr: { "stroke-dashoffset": L } }, { attr: { "stroke-dashoffset": L * 0.0 }, duration: dd, ease: "none", immediateRender: false }, a);
    counter(tl, el.querySelector(".bpm"), b0, b1, a, dd, (v) => String(Math.round(v)));
    tl.fromTo(el.querySelector(".bpm"), { color: "#ff5d6c" }, { color: "#4fd1c5", duration: dd, immediateRender: false }, a);
  };

  // ------------------------------------------------------------ waves: beta (busy) -> alpha/theta (calm)
  B.waves = (el, s, tl, t) => {
    const W = 1640, H = 200;
    const wave = (f, A, n) => { let d = `M0 ${H / 2}`; for (let i = 1; i <= n; i++) { const x = i / n * W; d += ` L${x.toFixed(1)} ${(H / 2 + Math.sin(x / W * f * 2 * Math.PI) * A * (0.7 + 0.3 * Math.sin(i * 1.7))).toFixed(1)}`; } return d; };
    const rows = [
      { id: "beta", label: "Beta 13–30 Hz", te: s.betaTe || "ఆలోచనలు, ఒత్తిడి", f: 60, A: 70, c: "co2" },
      { id: "alpha", label: "Alpha 8–12 Hz", te: s.alphaTe || "ప్రశాంతత", f: 20, A: 75, c: "o2" },
      { id: "theta", label: "Theta 4–7 Hz", te: s.thetaTe || "లోతైన ధ్యానం", f: 9, A: 80, c: "calm" },
    ];
    el.innerHTML = `<div class="scene" style="flex-direction:column;gap:26px;justify-content:center">
      <div class="h2 te" style="font-size:60px">${s.title}</div>
      ${rows.map((r) => `<div class="wrow ${r.id}" style="display:grid;grid-template-columns:330px 1fr;align-items:center;gap:30px">
        <div><div style="font-size:34px;font-weight:800" class="${r.c}">${r.label}</div><div class="te" style="font-size:30px;color:var(--ink-dim)">${r.te}</div></div>
        <svg width="1300" height="${H}" viewBox="0 0 ${W} ${H}" preserveAspectRatio="none"><path d="${wave(r.f, r.A, 900)}" fill="none" stroke="var(--${r.c})" stroke-width="5"/></svg></div>`).join("")}</div>`;
    inn(tl, el.querySelector(".h2"), t + 0.1);
    const rs = el.querySelectorAll(".wrow");
    rs.forEach((r, i) => inn(tl, r, t + (s.at ? s.at[i] : 0.6 + i * 1.6), { x: -40 }));
    // Highlight shifts from beta to theta: the mind settles
    const k = t + (s.settleAt || s.dur * 0.6);
    tl.to(rs[0], { opacity: 0.3, duration: 0.8 }, k);
    tl.to(rs[1], { opacity: 0.55, duration: 0.8 }, k + 0.3);
    tl.fromTo(rs[2], { scale: 1 }, { scale: 1.03, duration: 0.8, ease: E, immediateRender: false }, k + 0.3);
    rs.forEach((r) => tl.fromTo(r.querySelector("path"), { x: 0 }, { x: -60, duration: s.dur, ease: "none", immediateRender: false }, t));
  };

  // ------------------------------------------------------------ term: keyword callout
  B.term = (el, s, tl, t) => {
    el.innerHTML = `<div class="scene" style="flex-direction:column;justify-content:center;align-items:center;text-align:center;gap:26px">
      ${s.eyebrow ? `<div class="eyebrow ${s.color || ""}">${s.eyebrow}</div>` : ""}
      <div class="te tw" style="font-size:${s.size || 150}px;font-weight:800;line-height:1.2;color:var(--${s.color || "gold"})">${s.te}</div>
      ${s.en ? `<div style="font-size:54px;font-weight:700;letter-spacing:.06em">${s.en}</div>` : ""}
      <div class="line" style="width:420px;height:3px;background:var(--${s.color || "gold"});opacity:.6"></div>
      ${s.def ? `<p class="sub te" style="max-width:1300px;font-size:40px">${s.def}</p>` : ""}</div>`;
    const sc = el.querySelector(".scene");
    [...sc.children].forEach((c, i) => inn(tl, c, t + 0.1 + i * 0.35, c.classList.contains("tw") ? { scale: 0.9 } : { y: 24 }));
    tl.fromTo(el.querySelector(".line"), { scaleX: 0 }, { scaleX: 1, duration: 0.9, ease: E, immediateRender: false }, t + 0.6);
    drift(tl, sc, t, s.dur, 1.04);
  };

  // ------------------------------------------------------------ stat: one big number
  B.stat = (el, s, tl, t) => {
    el.innerHTML = `<div class="scene" style="flex-direction:column;justify-content:center;gap:24px;${s.center === false ? "" : "align-items:center;text-align:center;"}">
      ${s.eyebrow ? `<div class="eyebrow">${s.eyebrow}</div>` : ""}
      <div class="big num" style="font-size:${s.size || 280}px;font-weight:800;line-height:1;letter-spacing:-0.03em;color:var(--${s.color || "o2"})">${s.big}</div>
      <div class="h2 te" style="font-size:60px;max-width:1500px">${s.label}</div>
      ${s.sub ? `<p class="sub te" style="max-width:1400px">${s.sub}</p>` : ""}
      ${s.tag ? `<div><span class="tag ${s.tagClass || "calm"}">${s.tag}</span></div>` : ""}</div>`;
    const sc = el.querySelector(".scene");
    [...sc.children].forEach((c, i) => inn(tl, c, t + 0.1 + i * 0.4, c.classList.contains("big") ? { scale: 0.8 } : { y: 24 }));
    drift(tl, sc, t, s.dur, 1.03);
  };

  // ------------------------------------------------------------ bullets: title + items revealed on cue
  B.bullets = (el, s, tl, t) => {
    el.innerHTML = `<div class="scene" style="flex-direction:column;justify-content:center;gap:36px">
      ${s.eyebrow ? `<div class="eyebrow">${s.eyebrow}</div>` : ""}
      <div class="h2 te" style="font-size:64px;max-width:1600px">${s.title}</div>
      <div class="items" style="display:flex;flex-direction:column;gap:24px">${s.items.map((it) => `<div class="it glass te" style="display:flex;align-items:center;gap:28px;padding:26px 40px;font-size:44px;font-weight:700;max-width:1500px">
        <span style="width:18px;height:18px;border-radius:50%;flex:none;background:var(--${s.color || "o2"})"></span>${it}</div>`).join("")}</div></div>`;
    const sc = el.querySelector(".scene");
    [...sc.children].slice(0, -1).forEach((c, i) => inn(tl, c, t + 0.1 + i * 0.35));
    el.querySelectorAll(".it").forEach((c, i) => inn(tl, c, t + (s.at ? s.at[i] : 0.9 + i * 1.3), { x: -50 }));
  };

  // ------------------------------------------------------------ compare: two panels side by side
  B.compare = (el, s, tl, t) => {
    const panel = (p, c) => `<div class="pn glass" style="flex:1;padding:50px 54px;display:flex;flex-direction:column;gap:24px;border-color:var(--${c})">
      <div class="eyebrow" style="color:var(--${c})">${p.eyebrow || ""}</div><div class="h2 te" style="font-size:58px">${p.title}</div>
      ${p.big ? `<div class="num" style="font-size:120px;font-weight:800;color:var(--${c})">${p.big}</div>` : ""}
      <p class="sub te" style="font-size:36px">${p.sub || ""}</p></div>`;
    el.innerHTML = `<div class="scene" style="flex-direction:column;gap:40px;justify-content:center">
      ${s.title ? `<div class="h2 te ttl" style="font-size:60px">${s.title}</div>` : ""}
      <div style="display:flex;gap:46px">${panel(s.a, s.a.color || "co2")}${panel(s.b, s.b.color || "o2")}</div></div>`;
    if (s.title) inn(tl, el.querySelector(".ttl"), t + 0.1);
    el.querySelectorAll(".pn").forEach((p, i) => inn(tl, p, t + (s.at ? s.at[i] : 0.5 + i * 1.6), { y: 40 }));
  };

  // ------------------------------------------------------------ history: dated archival card
  B.history = (el, s, tl, t) => {
    el.innerHTML = `<div class="scene" style="align-items:center;justify-content:center">
      <div class="card" style="position:relative;width:1500px;padding:70px 90px;border-radius:12px;background:linear-gradient(160deg,#2a2216,#17120b);border:2px solid rgba(232,194,122,0.45);box-shadow:0 40px 120px rgba(0,0,0,.6)">
        <div style="position:absolute;inset:18px;border:1px solid rgba(232,194,122,0.25);border-radius:8px"></div>
        <div style="display:flex;align-items:baseline;gap:40px"><div class="yr num gold" style="font-size:150px;font-weight:800;line-height:1">${s.year}</div>
          <div class="te" style="font-size:44px;font-weight:700;color:#f1e3c4">${s.place}</div></div>
        <div class="h2 te ht" style="font-size:64px;margin:30px 0 26px;color:#fff4dc">${s.title}</div>
        <div class="lines" style="display:flex;flex-direction:column;gap:18px">${s.lines.map((l) => `<div class="te ln" style="font-size:38px;color:#e6d6b5;line-height:1.35">— ${l}</div>`).join("")}</div>
        ${s.cite ? `<div class="srcl" style="margin-top:30px;font-size:26px;color:#b9a682">${s.cite}</div>` : ""}</div></div>`;
    inn(tl, el.querySelector(".card"), t + 0.1, { y: 40, rotation: -1.5 }, 0.9);
    inn(tl, el.querySelector(".yr"), t + 0.5, { scale: 0.85 });
    inn(tl, el.querySelector(".ht"), t + 0.9);
    el.querySelectorAll(".ln").forEach((c, i) => inn(tl, c, t + (s.at ? s.at[i] : 1.6 + i * 1.6), { x: -30 }));
    if (s.cite) inn(tl, el.querySelector(".srcl"), t + 1.2);
    drift(tl, el.querySelector(".card"), t, s.dur, 1.03);
  };

  // ------------------------------------------------------------ quote: big quote card
  B.quote = (el, s, tl, t) => {
    el.innerHTML = `<div class="scene" style="flex-direction:column;justify-content:center;align-items:center;text-align:center;gap:36px">
      <div style="font-size:220px;line-height:.5;color:var(--gold);font-weight:800;height:110px">“</div>
      <div class="te q" style="font-size:${s.size || 92}px;font-weight:800;line-height:1.25;max-width:1550px">${s.te}</div>
      ${s.en ? `<div class="en" style="font-size:40px;color:var(--ink-dim);font-style:italic;max-width:1400px">${s.en}</div>` : ""}
      ${s.who ? `<div class="who" style="font-size:34px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--gold)">${s.who}</div>` : ""}</div>`;
    const sc = el.querySelector(".scene");
    [...sc.children].forEach((c, i) => inn(tl, c, t + 0.1 + i * 0.5));
    drift(tl, sc, t, s.dur, 1.04);
  };

  // ------------------------------------------------------------ hold: the dramatic still (frozen clock, near-black)
  B.hold = (el, s, tl, t) => {
    el.innerHTML = `<div class="scene" style="background:#020306;flex-direction:column;justify-content:center;align-items:center;gap:30px;padding-bottom:110px">
      <div class="clk num" style="font-size:240px;font-weight:800;letter-spacing:-0.02em">${s.clock || "16:00"}</div>
      <div class="te lbl" style="font-size:46px;color:var(--ink-dim)">${s.label || ""}</div>
      <div class="ring" style="width:30px;height:30px;border-radius:50%;background:var(--alarm)"></div></div>`;
    inn(tl, el.querySelector(".clk"), t + 0.2, { scale: 0.92 }, 1.0);
    inn(tl, el.querySelector(".lbl"), t + 0.9);
    const reps = Math.max(1, Math.floor((s.dur - 0.5) / 1.0));
    tl.fromTo(el.querySelector(".ring"), { opacity: 0.2 }, { opacity: 1, duration: 0.5, yoyo: true, repeat: reps * 2 - 1, ease: "sine.inOut", immediateRender: false }, t + 0.3);
  };

  // ------------------------------------------------------------ endscreen: subscribe + two card slots
  B.endscreen = (el, s, tl, t) => {
    el.innerHTML = `<div class="scene" style="flex-direction:column;justify-content:center;gap:50px">
      <div class="h2 te ttl" style="font-size:72px">${s.title}</div>
      <div style="display:flex;gap:60px;align-items:center">
        <div class="slot glass" style="width:620px;height:350px;display:grid;place-items:center;font-size:30px;color:var(--ink-dim)">${s.slotA || ""}</div>
        <div class="slot glass" style="width:620px;height:350px;display:grid;place-items:center;font-size:30px;color:var(--ink-dim)">${s.slotB || ""}</div>
        <div class="sub-btn" style="display:flex;flex-direction:column;align-items:center;gap:20px">
          <div style="width:220px;height:220px;border-radius:50%;border:4px dashed rgba(255,255,255,.3)"></div>
          <div class="sbtn te" style="font-size:40px;font-weight:800;padding:20px 44px;border-radius:14px;background:#ff2b3d;color:#fff">${s.btn || "SUBSCRIBE"}</div></div></div>
      ${s.sub ? `<p class="sub te">${s.sub}</p>` : ""}</div>`;
    const sc = el.querySelector(".scene");
    inn(tl, el.querySelector(".ttl"), t + 0.1);
    el.querySelectorAll(".slot, .sub-btn").forEach((c, i) => inn(tl, c, t + 0.4 + i * 0.3, { y: 40 }));
    if (s.sub) inn(tl, sc.lastElementChild, t + 1.4);
    const reps = Math.max(1, Math.floor((s.dur - 2.5) / 1.2));
    tl.fromTo(el.querySelector(".sbtn"), { scale: 1 }, { scale: 1.07, duration: 0.6, yoyo: true, repeat: reps * 2 - 1, ease: "sine.inOut", immediateRender: false }, t + 2);
  };

  // ------------------------------------------------------------ kalari: practice-years timeline
  B.years = (el, s, tl, t) => {
    const n = s.marks.length;
    el.innerHTML = `<div class="scene" style="flex-direction:column;justify-content:center;gap:70px">
      <div class="h2 te ttl" style="font-size:64px">${s.title}</div>
      <div style="position:relative;width:1640px;height:300px">
        <div class="track" style="position:absolute;left:0;right:0;top:85px;height:10px;border-radius:6px;background:var(--gold);transform-origin:left"></div>
        ${s.marks.map((m, i) => `<div class="mk" style="position:absolute;left:${10 + (i / (n - 1)) * 80}%;top:0;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;gap:16px;width:360px;text-align:center">
          <div class="num" style="font-size:56px;font-weight:800;color:var(--gold)">${m.k}</div>
          <div style="width:30px;height:30px;border-radius:50%;background:var(--gold);border:6px solid #06090f"></div>
          <div class="te" style="font-size:40px;font-weight:700;line-height:1.3">${m.v}</div></div>`).join("")}</div>
      ${s.sub ? `<p class="sub te">${s.sub}</p>` : ""}</div>`;
    inn(tl, el.querySelector(".ttl"), t + 0.1);
    tl.fromTo(el.querySelector(".track"), { scaleX: 0 }, { scaleX: 1, duration: Math.min(4, s.dur - 1), ease: "power1.inOut", immediateRender: false }, t + 0.5);
    el.querySelectorAll(".mk").forEach((c, i) => inn(tl, c, t + (s.at ? s.at[i] : 0.6 + i * 1.1), { y: 20 }));
    if (s.sub) inn(tl, el.querySelector(".scene").lastElementChild, t + (s.subAt || 3));
  };

  // ------------------------------------------------------------ vigil: the live hold, clock synced to spoken minute marks
  // s.keys: [[offset, clockSeconds], ...]; s.log: [{at, t, te, color}]; all times relative to scene start
  B.vigil = (el, s, tl, t) => {
    const R = 250, C = 2 * Math.PI * R;
    el.innerHTML = `<div class="scene" style="gap:90px;align-items:center">
      <div class="left" style="display:flex;flex-direction:column;align-items:center;gap:30px">
        <svg width="600" height="600" viewBox="0 0 600 600" class="ring">
          <circle cx="300" cy="300" r="${R}" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="22"/>
          <circle class="arc" cx="300" cy="300" r="${R}" fill="none" stroke="var(--o2)" stroke-width="22" stroke-linecap="round"
            transform="rotate(-90 300 300)" stroke-dasharray="${C}" stroke-dashoffset="${C}"/>
          <text class="tval num" x="300" y="335" text-anchor="middle" fill="var(--ink)" font-size="118" font-weight="800" font-family="Inter">00:00</text>
          <text x="300" y="400" text-anchor="middle" fill="var(--ink-dim)" font-size="28" font-weight="600" font-family="Inter" letter-spacing="5">BREATH HOLD</text>
        </svg>
        <div class="glass resp" style="width:600px;padding:22px 30px;display:flex;flex-direction:column;gap:10px">
          <div style="display:flex;justify-content:space-between;font-size:26px;font-weight:700;color:var(--ink-dim)"><span>${s.respLabel || "Chest movement"}</span><span class="o2">${s.respVal || "—"}</span></div>
          <svg width="540" height="70" viewBox="0 0 540 70"><path class="rp" d="M0 35 C30 10 60 10 90 35 C120 60 150 60 180 35 L540 35" fill="none" stroke="var(--o2)" stroke-width="4"/></svg></div>
      </div>
      <div class="log" style="flex:1;display:flex;flex-direction:column;gap:18px">
        ${s.eyebrow ? `<div class="eyebrow">${s.eyebrow}</div>` : ""}
        ${s.log.map((e) => `<div class="ev glass" style="display:grid;grid-template-columns:150px 1fr;gap:26px;align-items:center;padding:20px 32px;border-left:8px solid var(--${e.color || "o2"})">
          <div class="num" style="font-size:44px;font-weight:800;color:var(--${e.color || "o2"})">${e.t}</div><div class="te" style="font-size:38px;font-weight:700;line-height:1.3">${e.te}</div></div>`).join("")}</div></div>`;
    inn(tl, el.querySelector(".ring"), t + 0.1, { scale: 0.9 }, 0.8);
    inn(tl, el.querySelector(".resp"), t + 0.5);
    if (s.eyebrow) inn(tl, el.querySelector(".log .eyebrow"), t + 0.3);
    const arc = el.querySelector(".arc"), tv = el.querySelector(".tval");
    const keys = s.keys.map(([a, c]) => [t + a, c]);
    for (let i = 0; i < keys.length - 1; i++) {
      const [a0, c0] = keys[i], [a1, c1] = keys[i + 1];
      tl.fromTo(arc, { attr: { "stroke-dashoffset": C * (1 - c0 / 960) } }, { attr: { "stroke-dashoffset": C * (1 - c1 / 960) }, duration: a1 - a0, ease: "none", immediateRender: false }, a0);
      counter(tl, tv, c0, c1, a0, a1 - a0, mmss);
    }
    // the breathing trace flattens: one breath, then a flat line
    const rp = el.querySelector(".rp");
    rp.setAttribute("stroke-dasharray", 700);
    tl.fromTo(rp, { attr: { "stroke-dashoffset": 700 } }, { attr: { "stroke-dashoffset": 0 }, duration: 3, ease: "none", immediateRender: false }, t + 0.8);
    // log entries: show the newest ones, older ones dim; keep at most s.window visible
    const evs = el.querySelectorAll(".ev");
    const win = s.window || 5;
    s.log.forEach((e, i) => {
      const at = t + e.at;
      inn(tl, evs[i], at, { x: 50 }, 0.5);
      if (i >= win) tl.to(evs[i - win], { opacity: 0, height: 0, paddingTop: 0, paddingBottom: 0, marginTop: -18, duration: 0.4 }, at - 0.45);
      if (i > 0) tl.to(evs[i - 1], { opacity: 0.45, duration: 0.4 }, at);
    });
    // shiver: tiny finite jitter of the whole scene
    if (s.shiverAt) {
      const n = Math.floor((s.shiverEnd - s.shiverAt) / 0.08);
      tl.fromTo(el.querySelector(".scene"), { x: 0 }, { x: 3, duration: 0.04, yoyo: true, repeat: n * 2 - 1, ease: "none", immediateRender: false }, t + s.shiverAt);
      tl.to(arc, { stroke: "#ff5d6c", duration: 0.6 }, t + s.shiverAt);
    }
  };

  // ------------------------------------------------------------ scenes builder
  window.HF_build = function (tl, scenes, opts) {
    const stage = document.getElementById("stage");
    scenes.forEach((s, i) => {
      const el = document.createElement("section");
      el.className = "clip";
      el.id = "sc" + i;
      el.dataset.start = String(s.start);
      el.dataset.duration = String(s.dur);
      el.dataset.trackIndex = "1";
      stage.appendChild(el);
      B[s.type](el, s, tl, s.start);
      // Scene fade-out unless the next scene starts later (crossfade 0.35 s)
      tl.to(el, { opacity: 0, duration: 0.35, ease: "power1.in" }, s.start + s.dur - 0.35);
      if (s.src) {
        const src = h(`<div class="src">${s.src}</div>`);
        el.appendChild(src);
        inn(tl, src, s.start + 0.8, { y: 10 });
      }
    });
    // Chapter strip + hold clock HUD (optional)
    if (opts && opts.chapter) {
      const c = h(`<div class="chapter"><b>${opts.chapter.n}</b><span class="te">${opts.chapter.name}</span></div>`);
      document.getElementById("root").appendChild(c);
      inn(tl, c, 0.3, { x: -20 });
    }
  };
})();
