TITLE = "E10 Title: The Kavach Railway Reality"
BG = "none"
CSS = """
  #gl { position: absolute; inset: 0; width: 1920px; height: 1080px; display: block; }
  #vig, #sweep { display: none; }
  #ttl { position: absolute; left: 0; right: 0; top: 380px; text-align: center; font: 800 132px/1 Inter, Arial, sans-serif; letter-spacing: 0.02em; color: #F8FAFC;
    text-shadow: 0 6px 40px rgba(0,0,0,0.85); clip-path: inset(100% 0 0 0); }
  #ttl small { display: block; margin-top: 26px; font: 800 30px Inter, Arial, sans-serif; letter-spacing: 0.5em; color: #7DD3FC; }
  #scan { position: absolute; left: 260px; right: 260px; top: 380px; height: 4px; background: linear-gradient(90deg, rgba(56,189,248,0), #7DD3FC, rgba(56,189,248,0)); box-shadow: 0 0 24px #38BDF8; opacity: 0; }
"""
BODY = """  <canvas id="gl" width="1920" height="1080"></canvas>
  <div id="ttl">THE KAVACH<br>RAILWAY REALITY</div>
  <div id="scan"></div>"""
JS = """
  // the title rises out of the track bed behind a cyan scan line
  tl.fromTo("#scan", { opacity: 0, y: 300 }, { opacity: 1, y: 0, duration: 0.9, ease: "power2.out" }, 0.15);
  tl.fromTo("#ttl", { clipPath: "inset(100% 0 0 0)", y: 40 }, { clipPath: "inset(0% 0 0 0)", y: 0, duration: 0.9, ease: "power2.out" }, 0.15);
  tl.to("#scan", { opacity: 0, duration: 0.5 }, 1.2);
  tl.fromTo("#ttl", { scale: 1.0 }, { scale: 1.03, duration: D, ease: "none", transformOrigin: "50% 50%" }, 0);
"""
MODULE = r"""
  import { THREE, createStage, seg, lerp, aim, camPath } from "./kav3d.js";
  import { nightTrack } from "./nighttrack.mjs";
  const st = createStage({ sky: "night", fov: 42, near: 0.03, bloom: { intensity: 1.2, threshold: 0.7, smoothing: 0.3 } });
  const D = st.DUR;
  st.run((st) => { const N = nightTrack(st, { tagZ: -6 });
    const cam = camPath([[0, [0.35, 0.55, N.zt + 6], [0, 0.0, N.zt - 10]], [D, [0.3, 0.42, N.zt + 3.6], [0, -0.05, N.zt - 10]]]);
    return { N, cam }; },
  (t, c) => { const { p, l } = c.cam(t); aim(st.camera, p, l); st.follow(0, 0, c.N.zt, 10);
    const g = Math.exp(-Math.pow((t - 1.1) / 0.35, 2)); c.N.glint.intensity = 6 * g; c.N.tag.userData.glow.material.opacity = 0.7 * g; });
"""
