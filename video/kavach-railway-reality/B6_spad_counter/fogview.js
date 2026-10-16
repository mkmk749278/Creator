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
    // overhead-line masts every 60 m on the right (the signal stands on the left, as on Indian Railways)
    const mph = s.travel % 60;
    for (let k = 4; k >= 0; k--) {
      const z = 8 + k * 60 - mph; if (z < 2) continue;
      const [bx, by] = P(3.4, 0, z), [tx, ty] = P(3.4, 7.2, z), [ax2] = P(-0.2, 7.0, z);
      ctx.strokeStyle = mix([40, 44, 50], z); ctx.lineWidth = Math.max(1, 120 / z);
      ctx.beginPath(); ctx.moveTo(bx, by); ctx.lineTo(tx, ty); ctx.lineTo(ax2, ty); ctx.stroke();
    }
    // contact wire
    ctx.strokeStyle = "rgba(60,64,70,0.5)"; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(...P(0.1, 5.6, 1.5)); ctx.lineTo(...P(0.1, 5.6, 300)); ctx.stroke();
    // the signal (Indian colour-light, after Commons photos): white post, black backplate, four hooded lamps, red lit
    if (s.zsig > 0.9 && s.zsig < 150) {
      const z = s.zsig, [px, py] = P(-2.3, 0, z), [hx, hy] = P(-2.3, 5.6, z), sc = F / z;
      ctx.strokeStyle = mix([214, 218, 222], z * 0.7); ctx.lineWidth = Math.max(1.5, 0.16 * sc); ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(hx, hy); ctx.stroke();
      const w = 0.5 * sc, h = 1.9 * sc;
      ctx.fillStyle = mix([14, 15, 18], z * 0.7); ctx.fillRect(hx - w / 2, hy - h, w, h);
      ctx.fillStyle = mix([240, 240, 240], z * 0.7); ctx.fillRect(hx - w * 0.3, hy + 0.1 * sc, w * 0.6, 0.28 * sc);     // number plate
      const lr = 0.13 * sc, vis = Math.min(1, Math.max(0, (64 - z) / 16));  // a lit lamp cuts through fog: it resolves at about 50-60 m
      for (let i = 0; i < 4; i++) { const ly = hy - h + (0.3 + i * 0.43) * sc;
        ctx.fillStyle = mix(i === 3 ? [40, 12, 12] : [22, 22, 24], z * 0.7); ctx.beginPath(); ctx.arc(hx, ly, lr, 0, 7); ctx.fill();
        ctx.strokeStyle = mix([8, 8, 9], z * 0.7); ctx.lineWidth = Math.max(1, 0.06 * sc); ctx.beginPath(); ctx.arc(hx, ly, lr * 1.25, Math.PI * 1.05, Math.PI * 1.95); ctx.stroke(); }
      const ly = hy - h + (0.3 + 3 * 0.43) * sc;
      const glow = ctx.createRadialGradient(hx, ly, 0, hx, ly, lr * 16); glow.addColorStop(0, `rgba(255,70,60,${0.9 * vis})`); glow.addColorStop(1, "rgba(255,70,60,0)");
      ctx.fillStyle = glow; ctx.beginPath(); ctx.arc(hx, ly, lr * 16, 0, 7); ctx.fill();
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
    // cab: grey window frame with vertical protective bars and the console below (after the PIB cab photo)
    if (s.cab) {
      ctx.fillStyle = "rgba(60,66,74,0.92)";
      for (const f of [0.15, 0.32, 0.68, 0.85]) { const x = W * f; ctx.fillRect(x - 7, 0, 14, H); }
      let gg = ctx.createLinearGradient(0, 0, 0, 90); gg.addColorStop(0, "#2B3036"); gg.addColorStop(1, "#4B525B");
      ctx.fillStyle = gg; ctx.fillRect(0, 0, W, 70);
      gg = ctx.createLinearGradient(0, H - 230, 0, H); gg.addColorStop(0, "#6B7380"); gg.addColorStop(0.08, "#565D67"); gg.addColorStop(1, "#2C3036");
      ctx.fillStyle = gg; ctx.beginPath(); ctx.moveTo(0, H - 200); ctx.lineTo(W, H - 230); ctx.lineTo(W, H); ctx.lineTo(0, H); ctx.fill();
      ctx.fillStyle = "#3A4048"; ctx.fillRect(0, 0, 46, H); ctx.fillRect(W - 46, 0, 46, H);
      for (let i = 0; i < 4; i++) { const gx = 170 + i * 120, gy = H - 110; ctx.fillStyle = "#1A1D21"; ctx.beginPath(); ctx.arc(gx, gy, 44, 0, 7); ctx.fill();
        ctx.strokeStyle = "#C9CED6"; ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(gx, gy, 38, 0, 7); ctx.stroke();
        ctx.strokeStyle = "#F3F4F6"; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(gx, gy); ctx.lineTo(gx + 26 * Math.cos(-2.2 + i * 0.5), gy + 26 * Math.sin(-2.2 + i * 0.5)); ctx.stroke();
        ctx.lineWidth = 2; for (let k = 0; k <= 10; k++) { const a = Math.PI * (0.75 + 1.5 * k / 10); ctx.beginPath(); ctx.moveTo(gx + 31 * Math.cos(a), gy + 31 * Math.sin(a)); ctx.lineTo(gx + 37 * Math.cos(a), gy + 37 * Math.sin(a)); ctx.stroke(); }
        ctx.fillStyle = i === 1 ? "#DC2626" : "#E5E7EB"; ctx.beginPath(); ctx.arc(gx, gy, 5, 0, 7); ctx.fill(); }
      // hand wheel (master controller), brake handle, switch panel with indicator lamps
      const wx = 760, wy = H - 92; ctx.strokeStyle = "#1A1D21"; ctx.lineWidth = 14; ctx.beginPath(); ctx.arc(wx, wy, 64, 0, 7); ctx.stroke();
      ctx.strokeStyle = "#8C939C"; ctx.lineWidth = 4; ctx.beginPath(); ctx.arc(wx, wy, 64, 0, 7); ctx.stroke();
      ctx.strokeStyle = "#2A2E33"; ctx.lineWidth = 9; for (let k = 0; k < 3; k++) { const a = 0.4 + k * 2.094; ctx.beginPath(); ctx.moveTo(wx, wy); ctx.lineTo(wx + 60 * Math.cos(a), wy + 60 * Math.sin(a)); ctx.stroke(); }
      ctx.fillStyle = "#C9CED6"; ctx.beginPath(); ctx.arc(wx, wy, 13, 0, 7); ctx.fill();
      ctx.fillStyle = "#1A1D21"; ctx.beginPath(); ctx.roundRect(905, H - 175, 30, 120, 10); ctx.fill(); ctx.fillStyle = "#B91C1C"; ctx.beginPath(); ctx.arc(920, H - 180, 20, 0, 7); ctx.fill();
      ctx.fillStyle = "#2C3137"; ctx.beginPath(); ctx.roundRect(990, H - 170, 190, 110, 8); ctx.fill();
      for (let k = 0; k < 8; k++) { const sx = 1010 + (k % 4) * 44, sy = H - 145 + Math.floor(k / 4) * 50; ctx.fillStyle = "#4B5563"; ctx.fillRect(sx, sy, 18, 30); ctx.fillStyle = ["#22C55E", "#F59E0B", "#9CA3AF", "#22C55E"][k % 4]; ctx.beginPath(); ctx.arc(sx + 30, sy + 6, 5, 0, 7); ctx.fill(); }
    } else { ctx.strokeStyle = "rgb(10,12,16)"; ctx.lineWidth = 70; ctx.strokeRect(0, 0, W, H); }
    const vg = ctx.createRadialGradient(CX, H * 0.48, H * 0.25, CX, H * 0.5, H * 0.8); vg.addColorStop(0, "rgba(0,0,0,0)"); vg.addColorStop(1, "rgba(0,0,0,0.55)");
    ctx.fillStyle = vg; ctx.fillRect(0, 0, W, H);
  }
  return { draw, P };
};
