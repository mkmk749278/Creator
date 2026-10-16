TITLE = "E2 Two forwards, two myths"
BG = "none"
LIBS = ["e.js"]
CSS = """
  #sweep { display: none; }
  #dim { position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 50%, rgba(8,12,20,0.35), rgba(8,12,20,0.8)); }
  .mk { background: linear-gradient(#FDE68A, #FDE68A) no-repeat 0 85% / 0% 45%; padding: 0 2px; }
  #cards .myth { font-size: 40px; }
  #bg { position: absolute; inset: -60px; filter: blur(7px); }
"""
BODY = """  <div id="bg"></div><div id="dim"></div><div id="cards"></div>"""
JS = """
  const T = E.table(document.getElementById("bg")), F = E.twoForwards(document.getElementById("cards"));
  const t1 = at("V004", "One forward"), t2 = at("V004", "and another says");
  // each forward slides up like a new message, then keeps drifting (never a still frame)
  tl.fromTo(F.L, { y: 140, opacity: 0, rotation: -6 }, { y: 0, opacity: 1, rotation: -2.5, duration: 0.6, ease: "back.out(1.4)" }, t1);
  tl.fromTo(F.m1, { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.4 }, t1 + 0.5);
  tl.fromTo(F.R, { y: 140, opacity: 0, rotation: 6 }, { y: 0, opacity: 1, rotation: 2, duration: 0.6, ease: "back.out(1.4)" }, t2);
  tl.fromTo(F.m2, { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.4 }, t2 + 0.5);
  tl.to(F.L, { y: -18, rotation: -1.5, duration: D - t1 - 0.6, ease: "sine.inOut" }, t1 + 0.6);
  tl.to(F.R, { y: -22, rotation: 1.2, duration: D - t2 - 0.6, ease: "sine.inOut" }, t2 + 0.6);
  // the camera leans into each forward as it is read, then pulls back to show both
  tl.fromTo("#cards", { scale: 1.06, x: 110, transformOrigin: "50% 50%" }, { scale: 1.09, x: 100, duration: t2 - 0.3, ease: "sine.inOut" }, 0);
  tl.to("#cards", { scale: 1.08, x: -100, duration: 0.8, ease: "power2.inOut" }, t2 - 0.3);
  tl.to("#cards", { scale: 1.02, x: 0, duration: 1.0, ease: "power2.inOut" }, at("V004", "impossible now") + 0.2);
  // a marker sweeps under the words as they are spoken
  const mark = (card, phrase) => { const pp = card.querySelector("p"); pp.innerHTML = pp.innerHTML.replace(phrase, `<span class="mk">${phrase}</span>`); return pp.querySelector(".mk"); };
  const k1 = mark(F.L, "never bothered with safety"), k2 = mark(F.R, "Crashes are impossible now");
  tl.to(k1, { backgroundSize: "100% 45%", duration: 0.6, ease: "power1.inOut" }, at("V004", "never bothered"));
  tl.to(k2, { backgroundSize: "100% 45%", duration: 0.6, ease: "power1.inOut" }, at("V004", "impossible now") - 0.5);
  T.bs.forEach((b, i) => tl.to(b, { x: (i % 2 ? 1 : -1) * 60, duration: D, ease: "sine.inOut" }, 0));
"""
