/* Windscreen view in dense fog (B3/B4): rails at Indian broad gauge (1.676 m), sleepers, overhead-line masts and a
   three-aspect signal drawn in true perspective; each object is blended into the fog by its distance, so a signal only
   resolves near the visibility limit. Pure function of the state passed to draw() (ILLUSTRATION). */
window.FogView = function (canvas, fogImg) {
  const ctx = canvas.getContext("2d"), W = canvas.width, H = canvas.height;
  const CX = W / 2, HY = H * 0.43, F = 760, CAM_H = 3.2;          // focal length px, eye height m
  const FOG = [206, 213, 222];
  const fogK = (z) => 1 - Math.exp(-z / 16);                         // 0 near, ~0.96 at 50 m
  const mix = (rgb, z) => { const k = fogK(z); return `rgb(${rgb.map((c, i) => Math.round(c + (FOG[i] - c) * k)).join(",")})`; };
  const P = (X, Y, z) => [CX + F * X / z, HY + F * (CAM_H - Y) / z];   // world (lateral, height, distance) -> screen
  function draw(s) {
    // sky and ground, both swallowed by fog
    let g = ctx.createLinearGradient(0, 0, 0, H);
    g.addColorStop(0, "rgb(182,190,201)"); g.addColorStop(0.42, "rgb(206,213,222)"); g.addColorStop(0.5, "rgb(176,182,189)"); g.addColorStop(1, "rgb(58,60,62)");
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
    // ballast bed (trapezoid)
    ctx.beginPath(); let a = P(-2.4, 0, 1.2), b = P(2.4, 0, 1.2), c = P(2.4, 0, 400), d = P(-2.4, 0, 400);
    ctx.moveTo(...a); ctx.lineTo(...b); ctx.lineTo(...c); ctx.lineTo(...d); ctx.closePath();
    g = ctx.createLinearGradient(0, H, 0, HY); g.addColorStop(0, "rgb(52,50,48)"); g.addColorStop(0.55, "rgb(150,152,156)"); g.addColorStop(1, "rgb(200,206,214)");
    ctx.fillStyle = g; ctx.fill();
    // sleepers every 0.6 m, scrolling with distance travelled
    const ph = s.travel % 0.6;
    for (let k = 140; k >= 0; k--) {
      const z = 1.3 + k * 0.6 - ph; if (z < 1.3) continue;
      const [x1, y1] = P(-1.35, 0, z), [x2] = P(1.35, 0, z), [, y2] = P(0, 0, z + 0.25);
      ctx.fillStyle = mix([70, 64, 58], z); ctx.fillRect(x1, y2, x2 - x1, Math.max(1, y1 - y2));
    }
    // rails
    for (const X of [-0.838, 0.838]) {
      ctx.beginPath(); const [ax, ay] = P(X, 0.17, 1.3), [bx, by] = P(X, 0.17, 300);
      ctx.moveTo(ax, ay); ctx.lineTo(bx, by);
      const gr = ctx.createLinearGradient(ax, ay, bx, by); gr.addColorStop(0, "rgb(170,176,184)"); gr.addColorStop(0.25, mix([150, 156, 164], 30)); gr.addColorStop(1, `rgb(${FOG})`);
      ctx.strokeStyle = gr; ctx.lineWidth = 7; ctx.stroke();
    }
    // overhead-line masts every 60 m on the left
    const mph = s.travel % 60;
    for (let k = 4; k >= 0; k--) {
      const z = 8 + k * 60 - mph; if (z < 2) continue;
      const [bx, by] = P(-3.4, 0, z), [tx, ty] = P(-3.4, 7.2, z), [ax2] = P(0.2, 7.0, z);
      ctx.strokeStyle = mix([40, 44, 50], z); ctx.lineWidth = Math.max(1, 120 / z);
      ctx.beginPath(); ctx.moveTo(bx, by); ctx.lineTo(tx, ty); ctx.lineTo(ax2, ty); ctx.stroke();
    }
    // contact wire
    ctx.strokeStyle = "rgba(60,64,70,0.5)"; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(...P(0.1, 5.6, 1.5)); ctx.lineTo(...P(0.1, 5.6, 300)); ctx.stroke();
    // the signal (post right of the track); red aspect lit
    if (s.zsig > 0.9 && s.zsig < 150) {
      const z = s.zsig, [px, py] = P(2.3, 0, z), [hx, hy] = P(2.3, 5.2, z), sc = F / z;
      ctx.strokeStyle = mix([46, 50, 56], z); ctx.lineWidth = Math.max(1.5, 0.18 * sc); ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(hx, hy); ctx.stroke();
      const w = 0.55 * sc, h = 1.4 * sc;
      ctx.fillStyle = mix([18, 20, 26], z); ctx.fillRect(hx - w / 2, hy - h, w, h);
      const lr = 0.16 * sc, ly = hy - h + 0.25 * sc, vis = 1 - fogK(z) * 0.9;
      const glow = ctx.createRadialGradient(hx, ly, 0, hx, ly, lr * 6); glow.addColorStop(0, `rgba(255,70,60,${0.9 * vis})`); glow.addColorStop(1, "rgba(255,70,60,0)");
      ctx.fillStyle = glow; ctx.beginPath(); ctx.arc(hx, ly, lr * 6, 0, 7); ctx.fill();
      ctx.fillStyle = `rgba(255,110,100,${vis})`; ctx.beginPath(); ctx.arc(hx, ly, lr, 0, 7); ctx.fill();
    }
    // drifting fog banks (tileable texture), two layers at different speeds
    if (fogImg && fogImg.complete) {
      for (const [sp, al, sy] of [[18, 0.55, 0.0], [34, 0.42, 0.18]]) {
        const off = ((s.t * sp) % fogImg.width + fogImg.width) % fogImg.width;
        ctx.globalAlpha = al;
        for (let x = -off; x < W; x += fogImg.width * 1.6) ctx.drawImage(fogImg, x, H * sy, fogImg.width * 1.6, H * 0.9);
        ctx.globalAlpha = 1;
      }
    }
    // cab window frame
    ctx.strokeStyle = "rgb(10,12,16)"; ctx.lineWidth = 70; ctx.strokeRect(0, 0, W, H);
    const vg = ctx.createRadialGradient(CX, H * 0.48, H * 0.25, CX, H * 0.5, H * 0.8); vg.addColorStop(0, "rgba(0,0,0,0)"); vg.addColorStop(1, "rgba(0,0,0,0.55)");
    ctx.fillStyle = vg; ctx.fillRect(0, 0, W, H);
  }
  return { draw, P };
};
