TITLE = "E1 The family group chat on fire"
BG = "none"
LIBS = ["e.js"]
CSS = """
  #vig { background: radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) 45%, rgba(0,0,0,0.6) 100%); }
  #sweep { display: none; }
  #rig { position: absolute; inset: 0; perspective: 1600px; }
  #ph { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; transform-style: preserve-3d; }
  #shadow { position: absolute; left: 760px; top: 120px; width: 440px; height: 920px; border-radius: 60px; background: rgba(0,0,0,0.45); filter: blur(30px); }
  .unr { position: absolute; left: 1130px; top: 180px; min-width: 64px; height: 64px; padding: 0 16px; box-sizing: border-box; border-radius: 32px; background: #25B36B; color: #fff;
    font: 800 32px/64px Inter, Arial, sans-serif; text-align: center; box-shadow: 0 8px 24px rgba(0,0,0,0.4); opacity: 0; }
"""
BODY = """  <div id="bg"></div>
  <div id="rig"><div id="shadow"></div><div id="ph"></div></div>
  <div class="unr" id="unr">4</div>"""
JS = """
  const T = E.table(document.getElementById("bg"));
  const P = E.phone(document.getElementById("ph"), { x: 740, y: 70, group: "Kumar Family", sub: "Amma, Ravi Bava, Chinni, Kiran, you", time: "12:41", av: "K" });
  // lock screen with a generic news alert (no outlet), then the chat takes over at "by lunchtime"
  const lock = E.el("div", "lock", P.scr, `<div class="clk">8:12</div><div class="dt">Monday</div>`);
  const note = E.el("div", "note", P.scr, `<b>NEWS · NOW</b>Train accident reported this morning. Rescue work under way.`); note.style.top = "340px";
  const msgs = [
    { who: "Amma", color: "#B45309", text: "Did you all see the news? Train accident again." },
    { who: "Ravi Bava", color: "#1D4ED8", fwd: true, text: "Government NEVER bothered about safety!!" },
    { who: "Chinni", color: "#BE185D", text: "Is there no Kavach on that line??" },
    { who: "Kiran", color: "#047857", fwd: true, text: "India already has Kavach. How can this happen now?" },
    { who: "Amma", color: "#B45309", text: "Everyone travel carefully please" },
    { who: "Ravi Bava", color: "#1D4ED8", fwd: true, text: "Share this before it gets deleted!!!" },
    { who: "Chinni", color: "#BE185D", text: "Which one is true?" },
  ].map((m) => { const e = P.addMsg(m); e.style.display = "none"; return e; });
  const tN = at("V003", "news of a train crash"), tL = at("V003", "by lunchtime"), tF = at("V003", "is on fire");
  tl.fromTo(note, { y: -120, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: "back.out(1.6)" }, tN - 0.3);
  tl.to(lock, { y: -940, duration: 0.5, ease: "power2.in" }, tL - 0.2); tl.to(note, { y: -940, duration: 0.5, ease: "power2.in" }, tL - 0.2);
  // messages pile in faster and faster; each new one pushes the stack up (the stack is bottom-anchored)
  msgs.forEach((m, i) => { const t = tL + 0.35 + 2.3 * Math.sqrt(i / (msgs.length - 1)) ; tl.set(m, { display: "block" }, t); tl.fromTo(m, { opacity: 0, y: 30, scale: 0.96 }, { opacity: 1, y: 0, scale: 1, duration: 0.22, ease: "power2.out" }, t); });
  const u = { n: 4 }, U = document.getElementById("unr");
  tl.to("#unr", { opacity: 1, duration: 0.2 }, tL + 0.4);
  tl.to(u, { n: 120, duration: D - tL - 0.6, ease: "power2.in", onUpdate: () => { U.textContent = u.n >= 99 ? "99+" : Math.round(u.n); } }, tL + 0.4);
  tl.fromTo("#unr", { scale: 1 }, { scale: 1.18, duration: 0.15, yoyo: true, repeat: 7, ease: "sine.inOut" }, tF - 0.6);
  // camera: phone lies tilted on the table; slow push-in and a turn towards us
  tl.fromTo("#ph", { rotationX: 28, rotationZ: -7, scale: 0.92, y: 40, transformOrigin: "960px 540px" }, { rotationX: 10, rotationZ: -2, scale: 1.18, y: 30, duration: D, ease: "sine.inOut" }, 0);
  tl.fromTo("#shadow", { x: 30, y: 40, opacity: 0.8 }, { x: 14, y: 20, opacity: 0.6, duration: D, ease: "sine.inOut" }, 0);
  T.bs.forEach((b, i) => tl.to(b, { x: (i % 2 ? 1 : -1) * 40, y: 10, duration: D, ease: "sine.inOut" }, 0));
  grain(tl, "#bg .grainw", D);
"""
