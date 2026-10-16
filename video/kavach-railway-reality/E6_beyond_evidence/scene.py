TITLE = "E6 Both forwards go beyond the evidence"
BG = "none"
LIBS = ["e.js"]
CSS = """
  #sweep { display: none; }
  #dim { position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 50%, rgba(8,12,20,0.35), rgba(8,12,20,0.8)); }
  #bg { position: absolute; inset: -60px; filter: blur(7px); }
  .stampx { font-size: 56px; text-align: center; line-height: 1.05; }
  #cards .fwd { padding-bottom: 190px; }
"""
BODY = """  <div id="bg"></div><div id="dim"></div><div id="cards"></div>
  <div class="stampx" id="s1" style="left:270px; top:590px">BEYOND THE<br>EVIDENCE</div>
  <div class="stampx" id="s2" style="left:1210px; top:620px">BEYOND THE<br>EVIDENCE</div>"""
JS = """
  const T = E.table(document.getElementById("bg")), C = document.getElementById("cards");
  // the two Balasore forwards the narration names (same messenger look as the E2 myths)
  const L = E.fwd(C, { x: 170, y: 330, title: "KAVACH WOULD HAVE SAVED BALASORE", body: "100% sure. They just didn't install it!!", rot: -2.5 });
  const R = E.fwd(C, { x: 1110, y: 360, title: "KAVACH COULD NEVER STOP BALASORE", body: "It's useless. Don't believe the hype.", rot: 2 });
  const t1 = at("V047", "So the forward"), t2 = at("V047", "surely couldn't"), tB = at("V047", "are both going");
  tl.fromTo(L, { y: 140, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: "back.out(1.4)" }, t1);
  tl.fromTo(R, { y: 140, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: "back.out(1.4)" }, t2 - 0.6);
  tl.to(L, { y: -16, duration: D - t1 - 0.6, ease: "sine.inOut" }, t1 + 0.6); tl.to(R, { y: -16, duration: D - t2, ease: "sine.inOut" }, t2);
  for (const [s, t] of [["#s1", tB + 0.4], ["#s2", tB + 0.9]]) {
    tl.fromTo(s, { opacity: 0, scale: 1.7, rotation: -16 }, { opacity: 0.95, scale: 1, rotation: -8, duration: 0.24, ease: "power4.in" }, t);
    tl.fromTo("#cards", { x: 0 }, { x: 5, duration: 0.05, yoyo: true, repeat: 3 }, t + 0.24); }
  tl.fromTo("#cards", { scale: 1.0, transformOrigin: "50% 50%" }, { scale: 1.04, duration: D, ease: "sine.inOut" }, 0);
  T.bs.forEach((b, i) => tl.to(b, { x: (i % 2 ? 1 : -1) * 60, duration: D, ease: "sine.inOut" }, 0));
"""
