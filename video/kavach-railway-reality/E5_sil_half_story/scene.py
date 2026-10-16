TITLE = "E5 SIL-4 is only half the story"
BG = "none"
LIBS = ["e.js"]
CSS = """
  #sweep { display: none; }
  #desk { position: absolute; inset: 0; background: radial-gradient(ellipse at 40% 40%, #1d2638, #0b1018 70%); }
  .page { position: absolute; left: 170px; top: 120px; width: 760px; height: 860px; background: #F4F1E8; border-radius: 6px; box-shadow: 0 30px 80px rgba(0,0,0,0.6);
    padding: 54px 58px; box-sizing: border-box; font-family: Inter, Arial, sans-serif; color: #2a2a2a; transform: rotate(-1.6deg); }
  .page .h { font: 800 26px Inter, Arial, sans-serif; letter-spacing: 0.08em; color: #1f2937; }
  .page .sh { font: 600 18px Inter, Arial, sans-serif; letter-spacing: 0.08em; color: #6b7280; margin: 8px 0 26px; }
  .page .ln { height: 11px; background: rgba(60,60,60,0.18); border-radius: 5px; margin: 14px 0; }
  .page table { width: 100%; border-collapse: collapse; margin: 30px 0 22px; font: 600 24px Inter, Arial, sans-serif; }
  .page th { text-align: left; font: 800 17px Inter, Arial, sans-serif; letter-spacing: 0.06em; color: #374151; border-bottom: 3px solid #374151; padding: 10px 8px; }
  .page td { padding: 16px 8px; border-bottom: 1px solid rgba(0,0,0,0.15); }
  .page tr.s4 td { background: rgba(56,189,248,0.0); }
  .page .ft { font: 600 15px Inter, Arial, sans-serif; color: #6b7280; letter-spacing: 0.04em; }
  #lens { position: absolute; left: 0; top: 0; width: 380px; height: 380px; margin: -190px 0 0 -190px; border-radius: 50%; overflow: hidden; border: 8px solid #CBD5E1;
    box-shadow: 0 20px 60px rgba(0,0,0,0.6), inset 0 0 30px rgba(0,0,0,0.3); opacity: 0; }
  #lens .page { transform-origin: 0 0; }
  #sil { position: absolute; left: 1100px; top: 170px; font: 800 150px/1 Inter, Arial, sans-serif; color: #38BDF8; opacity: 0; text-shadow: 0 0 40px rgba(56,189,248,0.35); }
  #sil small { display: block; font: 800 30px Inter, Arial, sans-serif; letter-spacing: 0.16em; color: #E0F2FE; margin-top: 10px; }
  #chain { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; opacity: 0; }
  .stampx { font-size: 58px; text-align: center; line-height: 1.05; }
  #posts .fwd { padding-bottom: 170px; }
"""
ROWS = [("SIL 4", "10⁻⁹ ≤ THR < 10⁻⁸", "s4"), ("SIL 3", "10⁻⁸ ≤ THR < 10⁻⁷", ""), ("SIL 2", "10⁻⁷ ≤ THR < 10⁻⁶", ""), ("SIL 1", "10⁻⁶ ≤ THR < 10⁻⁵", "")]
PAGE = ('<div class="h">RAILWAY APPLICATIONS · SAFETY INTEGRITY</div><div class="sh">SAFETY INTEGRITY LEVELS (SIL) · ILLUSTRATIVE PAGE</div>'
  + "".join(f'<div class="ln" style="width:{w}%"></div>' for w in (96, 88, 93, 70))
  + '<table><tr><th>LEVEL</th><th>DANGEROUS FAILURES PER HOUR, PER FUNCTION</th></tr>'
  + "".join(f'<tr class="{c}"><td><b>{a}</b></td><td>{b}</td></tr>' for a, b, c in ROWS) + "</table>"
  + "".join(f'<div class="ln" style="width:{w}%"></div>' for w in (91, 84, 95, 62))
  + '<div class="ft" style="margin-top:28px">TOLERABLE HAZARD RATE (THR) BANDS AS IN THE EN 50129 SIL TABLE</div>')
BODY = f"""  <div id="desk"></div>
  <div class="page" id="pg">{PAGE}</div>
  <div class="pinl" id="lensp" style="position:absolute;left:0;top:0"><div id="lens"><div class="page" id="pg2">{PAGE}</div></div></div>
  <div id="sil">SIL-4<small>HIGHEST SAFETY LEVEL</small></div>
  <div id="posts"></div>
  <div class="stampx" id="st" style="left:1250px; top:500px; opacity:0">HALF THE<br>STORY</div>
  <svg id="chain" viewBox="0 0 1920 1080" data-layout-allow-overflow></svg>"""
JS = """
  const t4 = at("V019", "S-I-L four"), tH = at("V019", "the highest safety"), tP = at("V019", "Some posts say"), tB = at("V019", "once in a billion"),
        tHalf = at("V019", "half the story"), tL = at("V019", "strict limit"), tN = at("V019", "not a promise");
  // magnifier: a scaled copy of the page inside a lens that glides onto the SIL 4 row (row y measured from the page)
  const pg = document.getElementById("pg"), pg2 = document.getElementById("pg2"), K = 1.9;
  const row = pg.querySelector("tr.s4"), R0 = document.getElementById("root").getBoundingClientRect(), rb = row.getBoundingClientRect();
  const rx = rb.left - R0.left + rb.width * 0.42, ry = rb.top - R0.top + rb.height / 2;
  pg2.style.left = "0px"; pg2.style.top = "0px";
  const lensAt = { x: 1250, y: 700 }, place = () => { document.getElementById("lensp").style.transform = `translate(${lensAt.x}px, ${lensAt.y}px)`;
    pg2.style.transform = `translate(${190 - (lensAt.x - pg.offsetLeft) * K}px, ${190 - (lensAt.y - pg.offsetTop) * K}px) scale(${K}) rotate(-1.6deg)`; };
  place();
  tl.fromTo("#pg", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.7, ease: "power3.out" }, 0.05);
  tl.to("#lens", { opacity: 1, duration: 0.4 }, t4 - 0.6);
  tl.to(lensAt, { x: rx, y: ry, duration: 1.0, ease: "power2.inOut", onUpdate: place }, t4 - 0.6);
  tl.to(lensAt, { x: rx + 60, duration: tP - t4 - 0.6, ease: "sine.inOut", onUpdate: place }, t4 + 0.4);
  tl.to(["#pg tr.s4 td", "#pg2 tr.s4 td"], { backgroundColor: "rgba(56,189,248,0.35)", duration: 0.4 }, t4 + 0.2);
  tl.fromTo("#sil", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(2)" }, tH);
  // the viral post, then the stamp
  const post = E.fwd(document.getElementById("posts"), { x: 1080, y: 330, title: "ONE FAILURE IN A BILLION HOURS", body: "So Kavach can never fail. 100% safe!!", rot: 2 });
  tl.to("#sil", { opacity: 0, y: -30, duration: 0.4 }, tP - 0.3);
  tl.to("#lens", { opacity: 0, duration: 0.3 }, tP - 0.3);
  tl.fromTo(post, { opacity: 0, x: 120 }, { opacity: 1, x: 0, duration: 0.6, ease: "power3.out" }, tP);
  tl.to(post, { y: -16, duration: tL - tP, ease: "sine.inOut" }, tP + 0.6);
  tl.fromTo("#st", { opacity: 0, scale: 1.7, rotation: -16 }, { opacity: 0.95, scale: 1, rotation: -8, duration: 0.24, ease: "power4.in" }, tHalf + 0.3);
  tl.fromTo("#posts", { x: 0 }, { x: 5, duration: 0.05, yoyo: true, repeat: 3 }, tHalf + 0.54);
  // the SIL target covers one safety function of the electronics, not the whole chain that keeps a train safe
  tl.to(["#pg", "#posts", "#st"], { opacity: 0, x: -60, duration: 0.5, ease: "power2.in" }, tL - 0.4);
  const NS = "http://www.w3.org/2000/svg", ch = document.getElementById("chain");
  const names = ["SIGNALLING DATA", "KAVACH ELECTRONICS", "BRAKES", "PEOPLE", "RULES"], W = 300, G = 40, X0 = (1920 - (5 * W + 4 * G)) / 2, Y = 470;
  names.forEach((n, i) => { const x = X0 + i * (W + G), lit = i === 1;
    const g = document.createElementNS(NS, "g"); g.setAttribute("id", "c" + i); ch.appendChild(g);
    g.innerHTML = `<rect x="${x}" y="${Y}" width="${W}" height="140" rx="16" fill="${lit ? "rgba(2,132,199,0.25)" : "rgba(30,41,59,0.8)"}" stroke="${lit ? "#38BDF8" : "#475569"}" stroke-width="${lit ? 5 : 3}"/>
      ${n.split(" ").map((w, k, a) => `<text x="${x + W / 2}" y="${Y + 80 + (k - (a.length - 1) / 2) * 38}" text-anchor="middle" style="font: 800 30px Inter, Arial, sans-serif; letter-spacing: 0.06em; fill: ${lit ? "#E0F2FE" : "#CBD5E1"}">${w}</text>`).join("")}`;
    if (i < 4) { const l = document.createElementNS(NS, "line"); Object.entries({ x1: x + W, y1: Y + 70, x2: x + W + G, y2: Y + 70.3, stroke: "#64748B", "stroke-width": 5 }).forEach(([k, v]) => l.setAttribute(k, v)); ch.appendChild(l); } });
  const tagG = document.createElementNS(NS, "g"); ch.appendChild(tagG); tagG.setAttribute("id", "sl4");
  tagG.innerHTML = `<text x="${X0 + W + G + W / 2}" y="${Y + 210}" text-anchor="middle" style="font: 800 30px Inter, Arial, sans-serif; letter-spacing: 0.1em; fill: #7DD3FC">SIL-4 TARGET</text>
    <text x="${X0 + W + G + W / 2}" y="${Y + 250}" text-anchor="middle" style="font: 800 22px Inter, Arial, sans-serif; letter-spacing: 0.1em; fill: #94A3B8">PER SAFETY FUNCTION</text>`;
  tl.to("#chain", { opacity: 1, duration: 0.4 }, tL);
  names.forEach((n, i) => tl.fromTo("#c" + i, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, tL + 0.1 + i * 0.12));
  tl.fromTo("#sl4", { opacity: 0 }, { opacity: 1, duration: 0.4 }, tL + 0.9);
  [0, 2, 3, 4].forEach((i, k) => tl.to(`#c${i} rect`, { attr: { stroke: "#F59E0B" }, duration: 0.25, yoyo: true, repeat: 1 }, tN + 0.3 + k * 0.15));
  tl.fromTo("#chain", { scale: 1.0, transformOrigin: "50% 50%" }, { scale: 1.04, duration: D - tL, ease: "sine.inOut" }, tL);
"""
