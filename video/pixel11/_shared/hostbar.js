// Host bar: builds speaker chips + per-line captions from voice timings and
// adds seek-safe tweens to the part's timeline. Call before registering tl:
//   HF_hostbar(tl, window.HF_TIMINGS);
// Requires <div id="hostbar"></div> inside the composition root.
(function () {
  const HOSTS = { maya: "Maya", leo: "Leo" };
  window.HF_hostbar = function (tl, timings) {
    const bar = document.getElementById("hostbar");
    bar.className = "hostbar";
    const hosts = document.createElement("div");
    hosts.className = "hosts";
    const rings = {}, dims = {};
    for (const [id, label] of Object.entries(HOSTS)) {
      const h = document.createElement("div");
      h.className = "host " + id;
      h.innerHTML = '<div class="avatar"><div class="ring"></div>' + label[0] + '</div><div class="name">' + label.toUpperCase() + '</div>';
      hosts.appendChild(h);
      rings[id] = h.querySelector(".ring");
      dims[id] = h.querySelector(".avatar");
    }
    const caps = document.createElement("div");
    caps.className = "captions";
    bar.append(hosts, caps);

    timings.lines.forEach((line, i) => {
      const c = document.createElement("div");
      c.className = "cap " + line.speaker;
      c.id = "cap-" + i;
      const who = document.createElement("span");
      who.className = "who";
      who.textContent = HOSTS[line.speaker];
      c.append(who, document.createTextNode(line.text));
      caps.appendChild(c);
      const s = line.start, e = line.end;
      tl.fromTo(c, { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.18, ease: "power2.out", immediateRender: false }, s - 0.05);
      tl.to(c, { opacity: 0, duration: 0.15, ease: "power1.in" }, e + 0.12);
      // Speaking ring pulses (finite repeat), the listener is dimmed.
      const other = line.speaker === "maya" ? "leo" : "maya";
      const pulses = Math.max(0, Math.floor((e - s) / 0.6) - 1);
      tl.fromTo(rings[line.speaker], { opacity: 0.9, scale: 1 }, { opacity: 0.35, scale: 1.08, duration: 0.3, ease: "sine.inOut",
        yoyo: true, repeat: pulses * 2 + 1, immediateRender: false }, s);
      tl.to(rings[line.speaker], { opacity: 0, scale: 1, duration: 0.15 }, e + 0.05);
      // Speaker grows slightly, the listener settles back.
      tl.to(dims[line.speaker], { scale: 1.06, duration: 0.2, ease: "power2.out" }, s - 0.05);
      tl.to(dims[other], { scale: 0.92, duration: 0.2, ease: "power2.out" }, s - 0.05);
    });
  };
})();
