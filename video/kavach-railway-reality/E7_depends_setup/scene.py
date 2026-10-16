TITLE = "E7 Fifteen km/h depends on the set-up"
BG = "none"
LIBS = ["e.js"]
CSS = """
  #sweep { display: none; }
  #desk { position: absolute; inset: 0; background: radial-gradient(ellipse at 60% 45%, #1a2436, #0a0f18 70%); }
  #dial { position: absolute; left: 1060px; top: 150px; width: 700px; height: 700px; opacity: 0; }
  #rule { position: absolute; left: 1080px; top: 860px; width: 660px; padding: 16px 22px; border-radius: 12px; background: rgba(15,23,42,0.92); border: 2px solid #F59E0B;
    font: 800 32px/1.2 Inter, Arial, sans-serif; color: #F8FAFC; opacity: 0; box-sizing: border-box; }
  #rule small { display: block; font: 800 22px Inter, Arial, sans-serif; letter-spacing: 0.12em; color: #FCD34D; margin-bottom: 6px; }
  #strike { position: absolute; height: 8px; background: #DC2626; border-radius: 4px; transform-origin: 0 50%; transform: scaleX(0); }
  .stampx { font-size: 60px; }
"""
BODY = """  <div id="desk"></div><div id="cards"></div>
  <svg id="dial" viewBox="0 0 700 700"></svg>
  <div id="rule"><small>THE RULE AT A FAILED SIGNAL</small>Loco pilots go at most 15 km/h</div>
  <div class="stampx dark" id="st" style="left:170px; top:690px; opacity:0">DEPENDS ON SET-UP</div>"""
JS = """
  const t0 = at("V052", "And what about"), t15 = at("V052", "exactly fifteen"), tR = at("V052", "Fifteen is the speed"), tK = at("V052", "what Kavach enforces"),
        tD = at("V052", "depends on its data"), tN = at("V052", "don't take that number");
  const card = E.fwd(document.getElementById("cards"), { x: 140, y: 330, title: "KAVACH ALWAYS LOCKS 15 KM/H", body: "Even if the driver forgets. Fixed by law!!", rot: -2 });
  // speedometer 0..40 km/h (so 15 reads clearly), 240 degrees, needle as a pure function of a tweened value
  const NS = "http://www.w3.org/2000/svg", dl = document.getElementById("dial"), cx = 350, cy = 360, R = 260, a0 = -120, sp = 240, MX = 40;
  const P = (v, r) => { const a = (a0 + sp * v / MX) * Math.PI / 180; return [cx + r * Math.sin(a), cy - r * Math.cos(a)]; };
  let h = `<circle cx="${cx}" cy="${cy}" r="${R + 40}" fill="#0B1220" stroke="#334155" stroke-width="6"/>`;
  for (let v = 0; v <= MX; v += 2) { const [x1, y1] = P(v, R), [x2, y2] = P(v, v % 10 ? R - 18 : R - 34); h += `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="#E5E7EB" stroke-width="${v % 10 ? 3 : 6}"/>`;
    if (v % 10 === 0) { const [lx, ly] = P(v, R - 70); h += `<text x="${lx}" y="${ly + 13}" text-anchor="middle" style="font: 800 38px Inter, Arial, sans-serif; fill: #CBD5E1">${v}</text>`; } }
  h += `<path id="arc" fill="none" stroke="#F59E0B" stroke-width="16"/><line id="ndl" x1="${cx}" y1="${cy}" x2="${cx}" y2="${cy - 220}" stroke="#F8FAFC" stroke-width="10" stroke-linecap="round"/>
    <circle cx="${cx}" cy="${cy}" r="58" fill="#F8FAFC"/><text id="dv" x="${cx}" y="${cy + 18}" text-anchor="middle" style="font: 800 52px Inter, Arial, sans-serif; fill: #0B1220">0</text>
    <text x="${cx}" y="${cy + 150}" text-anchor="middle" style="font: 800 28px Inter, Arial, sans-serif; letter-spacing: 0.16em; fill: #94A3B8">KM/H</text>`;
  dl.innerHTML = h;
  const st = { v: 0 }, set = () => { const [x, y] = P(st.v, 220); const n = document.getElementById("ndl"); n.setAttribute("x2", x); n.setAttribute("y2", y); document.getElementById("dv").textContent = Math.round(st.v);
    const [ax, ay] = P(0, R + 18), [bx, by] = P(Math.max(0.5, st.v), R + 18); document.getElementById("arc").setAttribute("d", `M ${ax} ${ay} A ${R + 18} ${R + 18} 0 ${st.v / MX * sp > 180 ? 1 : 0} 1 ${bx} ${by}`); };
  set();
  tl.fromTo(card, { opacity: 0, x: -120 }, { opacity: 1, x: 0, duration: 0.6, ease: "power3.out" }, t0);
  tl.to(card, { y: -14, duration: D - t0 - 0.6, ease: "sine.inOut" }, t0 + 0.6);
  tl.fromTo("#dial", { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.5 }, t15 - 0.6);
  tl.to(st, { v: 15, duration: 0.9, ease: "power2.out", onUpdate: set }, t15);
  tl.fromTo("#rule", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.5 }, tR);
  // what Kavach enforces comes from its data and settings: the target swings, then settles back
  tl.to(st, { v: 30, duration: 0.7, ease: "sine.inOut", onUpdate: set }, tK);
  tl.to(st, { v: 10, duration: 0.7, ease: "sine.inOut", onUpdate: set }, tK + 0.7);
  tl.to(st, { v: 15, duration: 0.6, ease: "sine.inOut", onUpdate: set }, tK + 1.4);
  tl.fromTo("#st", { opacity: 0, scale: 1.7, rotation: -16 }, { opacity: 0.95, scale: 1, rotation: -8, duration: 0.24, ease: "power4.in" }, tD + 0.2);
  tl.fromTo("#dial", { x: 0 }, { x: 5, duration: 0.05, yoyo: true, repeat: 3 }, tD + 0.44);
  // "don't take that number as a promise": the word ALWAYS on the card is struck through
  const h3 = card.querySelector("h3");
  h3.innerHTML = h3.innerHTML.replace("ALWAYS", '<span style="position:relative">ALWAYS<i id="alw" style="position:absolute;left:-6px;right:-6px;top:50%;height:8px;margin-top:-4px;background:#DC2626;border-radius:4px;transform:scaleX(0);transform-origin:0 50%"></i></span>');
  tl.to("#alw", { scaleX: 1, duration: 0.35, ease: "power2.in" }, tN + 0.2);
"""
