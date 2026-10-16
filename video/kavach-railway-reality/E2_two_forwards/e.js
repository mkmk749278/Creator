/* Kavach E scenes: shared phone / chat / forward-card / stamp / crack kit. Generic UI only: no real app, outlet or
   person; the chat app is a plain green messenger, not WhatsApp branding. Everything is DOM + SVG driven by the scene's
   paused GSAP timeline (pure function of time). Injects its own CSS. */
(function () {
  const css = `
  .tbl { position: absolute; inset: 0; background:
      radial-gradient(ellipse at 30% 20%, rgba(255,214,160,0.22), rgba(0,0,0,0) 55%),
      repeating-linear-gradient(92deg, rgba(0,0,0,0.0) 0 38px, rgba(0,0,0,0.10) 38px 41px, rgba(255,255,255,0.03) 41px 70px),
      linear-gradient(180deg, #5b3b24 0%, #4a2f1c 55%, #2f1d11 100%); }
  .tbl .grainw { position: absolute; inset: -40px; opacity: 0.35; background:
      repeating-linear-gradient(88deg, rgba(255,230,200,0.05) 0 2px, rgba(0,0,0,0.06) 2px 5px, rgba(0,0,0,0) 5px 13px); filter: blur(1.2px); }
  .bokeh { position: absolute; border-radius: 50%; background: radial-gradient(circle, rgba(255,226,170,0.55), rgba(255,226,170,0) 70%); filter: blur(6px); }
  .phone { position: absolute; width: 440px; height: 940px; border-radius: 58px; background: #0b0c0f; box-shadow: 0 40px 90px rgba(0,0,0,0.55), 0 0 0 3px #2a2c31 inset, 0 0 0 1px #45484f;
    padding: 14px; box-sizing: border-box; }
  .phone .scr { position: relative; width: 100%; height: 100%; border-radius: 46px; overflow: hidden; background: #ECE6DD; font-family: Inter, Arial, sans-serif; }
  .phone .cam { position: absolute; left: 50%; top: 12px; width: 18px; height: 18px; margin-left: -9px; border-radius: 50%; background: #050608; z-index: 5; box-shadow: 0 0 0 2px #1b1d22; }
  .phone .sb { position: absolute; left: 0; right: 0; top: 0; height: 44px; display: flex; align-items: center; justify-content: space-between; padding: 0 28px; box-sizing: border-box;
    font: 600 17px Inter, Arial, sans-serif; color: #F8FAFC; z-index: 4; }
  .phone .sb i { display: inline-block; height: 12px; margin-left: 6px; background: #F8FAFC; border-radius: 2px; vertical-align: middle; }
  .phone .hdr { position: absolute; left: 0; right: 0; top: 0; height: 128px; background: #1F7A5A; z-index: 3; }
  .phone .hdr .ttl { position: absolute; left: 96px; top: 62px; font: 700 24px Inter, Arial, sans-serif; color: #fff; }
  .phone .hdr .sub { position: absolute; left: 96px; top: 94px; font: 500 15px Inter, Arial, sans-serif; color: rgba(255,255,255,0.8); }
  .phone .hdr .av { position: absolute; left: 32px; top: 62px; width: 52px; height: 52px; border-radius: 50%; background: #F3C26B; color: #3b2a0c; font: 800 22px/52px Inter, Arial, sans-serif; text-align: center; }
  .phone .feed { position: absolute; left: 0; right: 0; top: 128px; bottom: 76px; overflow: hidden; }
  .phone .stack { position: absolute; left: 0; right: 0; bottom: 8px; padding: 0 14px; }
  .phone .msg { position: relative; max-width: 82%; margin: 8px 0; padding: 10px 14px 22px; border-radius: 14px; background: #fff; color: #1f2328; font: 500 20px/1.3 Inter, Arial, sans-serif;
    box-shadow: 0 1px 1px rgba(0,0,0,0.12); }
  .phone .msg.me { margin-left: auto; background: #DCF3D5; }
  .phone .msg .who { display: block; font: 700 16px Inter, Arial, sans-serif; margin-bottom: 3px; }
  .phone .msg .tm { position: absolute; right: 10px; bottom: 5px; font: 500 13px Inter, Arial, sans-serif; color: #7b8088; }
  .phone .msg .fw { display: block; font: 600 italic 14px Inter, Arial, sans-serif; color: #7b8088; margin-bottom: 4px; }
  .phone .msg .fw:before { content: "\\21AA  "; font-style: normal; }
  .phone .bar { position: absolute; left: 12px; right: 12px; bottom: 12px; height: 54px; border-radius: 27px; background: #fff; font: 500 18px/54px Inter, Arial, sans-serif; color: #9aa0a6; padding-left: 22px; }
  .phone .unread { position: absolute; right: 24px; top: 70px; min-width: 40px; height: 40px; padding: 0 10px; box-sizing: border-box; border-radius: 20px; background: #25B36B; color: #fff;
    font: 800 20px/40px Inter, Arial, sans-serif; text-align: center; z-index: 4; }
  .phone .lock { position: absolute; inset: 0; background: linear-gradient(160deg, #1b2a48, #0c1424 60%, #070b14); z-index: 6; }
  .phone .lock .clk { position: absolute; left: 0; right: 0; top: 150px; text-align: center; font: 300 96px Inter, Arial, sans-serif; color: #F8FAFC; letter-spacing: -0.02em; }
  .phone .lock .dt { position: absolute; left: 0; right: 0; top: 270px; text-align: center; font: 500 20px Inter, Arial, sans-serif; color: rgba(248,250,252,0.8); }
  .phone .note { position: absolute; left: 14px; right: 14px; padding: 14px 16px; border-radius: 22px; background: rgba(240,244,250,0.94); color: #1f2328; font: 500 18px/1.3 Inter, Arial, sans-serif; z-index: 7;
    box-shadow: 0 8px 24px rgba(0,0,0,0.35); }
  .phone .note b { display: block; font: 700 15px Inter, Arial, sans-serif; color: #5f6670; margin-bottom: 4px; letter-spacing: 0.04em; }
  .fwd { position: absolute; width: 640px; padding: 26px 30px 44px; border-radius: 22px; background: #fff; color: #1f2328; box-shadow: 0 30px 70px rgba(0,0,0,0.5); font-family: Inter, Arial, sans-serif; box-sizing: border-box; }
  .fwd .fw { font: 600 italic 22px Inter, Arial, sans-serif; color: #7b8088; margin-bottom: 14px; }
  .fwd .fw:before { content: "\\21AA\\21AA  "; font-style: normal; }
  .fwd h3 { margin: 0 0 12px; font: 800 52px/1.05 Inter, Arial, sans-serif; letter-spacing: -0.01em; }
  .fwd p { margin: 0; font: 500 28px/1.35 Inter, Arial, sans-serif; color: #3a3f46; }
  .fwd .tm { position: absolute; right: 22px; bottom: 14px; font: 500 18px Inter, Arial, sans-serif; color: #8a9097; }
  .myth { position: absolute; font: 800 30px Inter, Arial, sans-serif; letter-spacing: 0.2em; color: #FCD34D; text-shadow: 0 2px 10px rgba(0,0,0,0.8); }
  .stampx { position: absolute; padding: 10px 26px; border: 7px double #DC2626; color: #DC2626; font: 800 60px/1 Inter, Arial, sans-serif; letter-spacing: 0.06em; text-transform: uppercase;
    background: rgba(255,255,255,0.0); white-space: nowrap; mix-blend-mode: multiply; }
  .stampx.dark { mix-blend-mode: normal; color: #F87171; border-color: #F87171; background: rgba(15,23,42,0.35); }
  `;
  const st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);
  const el = (tag, cls, parent, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; if (parent) parent.appendChild(e); return e; };
  window.E = {
    el,
    /** wooden kitchen table backdrop with warm window light and soft bokeh (seeded) */
    table(root, n = 9) {
      const t = el("div", "tbl", root); el("div", "grainw", t); const r = mulberry32(77), bs = [];
      for (let i = 0; i < n; i++) { const b = el("div", "bokeh", t); const s = 60 + r() * 140; Object.assign(b.style, { width: s + "px", height: s + "px", left: r() * 1920 + "px", top: r() * 500 - 60 + "px", opacity: 0.25 + r() * 0.4 }); bs.push(b); }
      return { t, bs };
    },
    /** generic Android phone with a green messenger chat; returns { root, scr, feed, stack, addMsg, unread, lock, note } */
    phone(parent, { x = 740, y = 70, group = "Family", sub = "Amma, Ravi Bava, Chinni, Kiran, you", time = "12:41", av = "F" } = {}) {
      const p = el("div", "phone", parent); p.style.left = x + "px"; p.style.top = y + "px";
      const s = el("div", "scr", p); el("div", "cam", s);
      el("div", "sb", s, `<span>${time}</span><span><i style="width:16px"></i><i style="width:14px"></i><i style="width:26px"></i></span>`);
      const h = el("div", "hdr", s); el("div", "av", h, av); el("div", "ttl", h, group); el("div", "sub", h, sub);
      const feed = el("div", "feed", s), stack = el("div", "stack", feed);
      el("div", "bar", s, "Message");
      const addMsg = ({ who = "", color = "#1F7A5A", text = "", fwd = false, me = false, tm = time }) => {
        const m = el("div", "msg" + (me ? " me" : ""), stack);
        m.innerHTML = `${who ? `<span class="who" style="color:${color}">${who}</span>` : ""}${fwd ? `<span class="fw">Forwarded many times</span>` : ""}${text}<span class="tm">${tm}</span>`;
        return m; };
      return { root: p, scr: s, feed, stack, addMsg };
    },
    /** a forwarded-message card (generic messenger look) */
    fwd(parent, { x, y, title, body, tm = "11:58", rot = 0, id }) {
      const c = el("div", "fwd", parent, `<div class="fw">Forwarded many times</div><h3>${title}</h3><p>${body}</p><span class="tm">${tm}</span>`);
      Object.assign(c.style, { left: x + "px", top: y + "px", transform: `rotate(${rot}deg)` }); if (id) c.id = id; return c;
    },
    /** seeded glass-crack paths radiating from (cx, cy) inside an svg; returns path elements (stroke-dash ready) */
    crack(svg, cx, cy, seed = 5, n = 11, R = 520, col = "rgba(255,255,255,0.92)") {
      const NS = "http://www.w3.org/2000/svg", r = mulberry32(seed), out = [];
      for (let i = 0; i < n; i++) { const a = (i / n) * 6.283 + r() * 0.4; let x = cx, y = cy, d = `M ${cx} ${cy}`;
        const L = R * (0.5 + r() * 0.6), steps = 7; for (let k = 1; k <= steps; k++) { const rr = (L * k) / steps; const aa = a + (r() - 0.5) * 0.5; x = cx + Math.cos(aa) * rr; y = cy + Math.sin(aa) * rr; d += ` L ${x.toFixed(1)} ${y.toFixed(1)}`; }
        const p = document.createElementNS(NS, "path"); p.setAttribute("d", d); p.setAttribute("fill", "none"); p.setAttribute("stroke", col); p.setAttribute("stroke-width", 2.5 + r() * 2);
        p.setAttribute("stroke-linecap", "round"); svg.appendChild(p); out.push(p); }
      for (let ring = 1; ring <= 3; ring++) { const p = document.createElementNS(NS, "path"); let d = ""; const rad = ring * R * 0.16;
        for (let k = 0; k <= 14; k++) { const a = (k / 14) * 6.283, rr = rad * (0.8 + r() * 0.4); d += `${k ? "L" : "M"} ${(cx + Math.cos(a) * rr).toFixed(1)} ${(cy + Math.sin(a) * rr).toFixed(1)} `; }
        p.setAttribute("d", d); p.setAttribute("fill", "none"); p.setAttribute("stroke", col); p.setAttribute("stroke-opacity", 0.75); p.setAttribute("stroke-width", 1.6); svg.appendChild(p); out.push(p); }
      out.forEach((p) => { const L = p.getTotalLength(); p.setAttribute("stroke-dasharray", L); p.setAttribute("stroke-dashoffset", L); p.dataset.len = L; });
      return out;
    },
  };
})();
/* the two myth forwards used in E2, E3, E6, E8 (same text everywhere) */
window.E.twoForwards = function (root) {
  const L = E.fwd(root, { x: 170, y: 360, title: "NO KAVACH? WHY?", body: "The government never bothered with safety. Wake up!!", rot: -2.5, id: "fL" });
  const R = E.fwd(root, { x: 1110, y: 390, title: "KAVACH = ZERO ACCIDENTS", body: "India already has Kavach. Crashes are impossible now.", rot: 2, id: "fR" });
  const m1 = E.el("div", "myth", root, "MYTH 1"); Object.assign(m1.style, { left: "190px", top: "290px" }); m1.id = "m1";
  const m2 = E.el("div", "myth", root, "MYTH 2"); Object.assign(m2.style, { left: "1130px", top: "320px" }); m2.id = "m2";
  return { L, R, m1, m2 };
};
