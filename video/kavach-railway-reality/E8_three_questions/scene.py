TITLE = "E8 Three questions before you share"
BG = "none"
LIBS = ["e.js"]
CSS = """
  #vig { background: radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) 45%, rgba(0,0,0,0.6) 100%); }
  #sweep { display: none; }
  #rig { position: absolute; inset: 0; perspective: 1600px; }
  #ph { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; }
  .q { position: absolute; left: 1060px; padding: 18px 28px; border-radius: 16px; background: rgba(8,20,36,0.9); border: 3px solid #38BDF8; font: 800 44px Inter, Arial, sans-serif;
    color: #F8FAFC; white-space: nowrap; box-shadow: 0 18px 40px rgba(0,0,0,0.5); opacity: 0; }
  .q b { color: #7DD3FC; margin-right: 16px; }
  #q1 { top: 260px; } #q2 { top: 430px; } #q3 { top: 600px; }
  #step { position: absolute; left: 96px; bottom: 110px; width: 120px; height: 120px; border-radius: 60px; border: 6px solid #F59E0B; color: #F59E0B; font: 800 72px/108px Inter, Arial, sans-serif; text-align: center; opacity: 0; }
"""
BODY = """  <div id="bg"></div>
  <div id="rig"><div id="ph"></div></div>
  <div class="q" id="q1"><b>?</b>FITTED OR WORKING?</div>
  <div class="q" id="q2"><b>?</b>WHICH DATE?</div>
  <div class="q" id="q3"><b>?</b>HUMAN OR SIGNAL DATA?</div>
  <div id="step">1</div>"""
JS = """
  const T = E.table(document.getElementById("bg"));
  const P = E.phone(document.getElementById("ph"), { x: 420, y: 70, group: "Kumar Family", sub: "Amma, Ravi Bava, Chinni, Kiran, you", time: "12:58", av: "K" });
  P.addMsg({ who: "Chinni", color: "#BE185D", text: "Reached home safely" });
  P.addMsg({ who: "Kiran", color: "#047857", text: "Good. Dinner at 8?" });
  P.addMsg({ who: "Amma", color: "#B45309", text: "Ravi, is this true?" });
  const f = P.addMsg({ who: "Ravi Bava", color: "#1D4ED8", fwd: true, text: "<b>KAVACH ON 7,726 KM!!</b><br>Now every train is safe. Share fast!!" });
  f.style.display = "none";
  const t1 = at("V055", "One."), tF = at("V055", "When a Kavach forward"), t3 = at("V055", "ask three questions"), tA = at("V055", "is the number about fitted"), tB = at("V055", "which date"), tC = at("V055", "was the problem");
  tl.fromTo("#step", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, t1);
  tl.set(f, { display: "block" }, tF + 0.3); tl.fromTo(f, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3 }, tF + 0.3);
  for (const [id, t] of [["#q1", tA], ["#q2", tB], ["#q3", tC]]) tl.fromTo(id, { opacity: 0, x: 60, scale: 0.9 }, { opacity: 1, x: 0, scale: 1, duration: 0.4, ease: "back.out(1.8)" }, t);
  tl.to("#q1", { borderColor: "#94A3B8", duration: 0.3 }, tB); tl.to("#q2", { borderColor: "#94A3B8", duration: 0.3 }, tC);
  tl.fromTo("#ph", { rotationY: 10, rotationX: 6, x: -20, transformOrigin: "640px 540px" }, { rotationY: 4, rotationX: 3, x: 10, duration: D, ease: "sine.inOut" }, 0);
  T.bs.forEach((b, i) => tl.to(b, { x: (i % 2 ? 1 : -1) * 40, duration: D, ease: "sine.inOut" }, 0));
"""
