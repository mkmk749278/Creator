// Bakes library/geo/land_sdf_4k.png: a signed distance field of Natural Earth 1:50m LAND (merged landmasses, so no
// political borders anywhere; PLAYBOOK §15 Fire and Ice lesson) in equirectangular projection, 4096x2048.
// Grey value = 0.5 + d / (2 * RANGE) with d in texels (positive on land); the coastline is the 0.5 level set.
// Needs world-atlas@2.0.2, topojson-client@3.1.0, d3-geo@3.1.1 (install in a scratch dir, not in the repo) and puppeteer-core.
// Usage: node bake_land.mjs <dir with node_modules for the geo packages> <out.png>
import { createRequire } from "node:module";
import { readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
const [geoDir, out] = process.argv.slice(2);
const req = createRequire(join(geoDir, "package.json"));
const { geoEquirectangular, geoPath } = req("d3-geo");
const { feature } = req("topojson-client");
const puppeteer = createRequire(import.meta.url)("/home/user/Creator/node_modules/puppeteer-core");
const SS = 2, W = 4096 * SS, H = 2048 * SS, RANGE = 32 * SS;
const topo = JSON.parse(readFileSync(join(geoDir, "node_modules/world-atlas/land-50m.json"), "utf8"));
const proj = geoEquirectangular().scale(W / (2 * Math.PI)).translate([W / 2, H / 2]).precision(0.1);
const d = geoPath(proj).digits(2)(feature(topo, topo.objects.land));
const browser = await puppeteer.launch({ executablePath: "/opt/pw-browsers/chromium", args: ["--no-sandbox"] });
const page = await browser.newPage();
const png = await page.evaluate(async (d, W, H, RANGE, SS) => {
  const c = new OffscreenCanvas(W, H), g = c.getContext("2d");
  g.fillStyle = "#000"; g.fillRect(0, 0, W, H); g.fillStyle = "#fff"; g.fill(new Path2D(d), "evenodd");
  const px = g.getImageData(0, 0, W, H).data, N = W * H, inside = new Uint8Array(N);
  for (let i = 0; i < N; i++) inside[i] = px[i * 4] > 127 ? 1 : 0;
  // Felzenszwalb-Huttenlocher exact squared EDT (1D pass on columns then rows); x wraps around the antimeridian
  const INF = 1e20;
  function edt(isFeature) {
    const f = new Float64Array(N);
    for (let i = 0; i < N; i++) f[i] = isFeature(i) ? 0 : INF;
    const n = Math.max(W * 3, H), v = new Int32Array(n), z = new Float64Array(n + 1), tmp = new Float64Array(n), res = new Float64Array(n);
    const pass = (len) => { let k = 0; v[0] = 0; z[0] = -INF; z[1] = INF;
      for (let q = 1; q < len; q++) { let s;
        while (true) { const p = v[k]; s = ((tmp[q] + q * q) - (tmp[p] + p * p)) / (2 * q - 2 * p); if (s <= z[k]) { k--; if (k < 0) { k = 0; break; } } else break; }
        k++; v[k] = q; z[k] = s; z[k + 1] = INF; }
      k = 0; for (let q = 0; q < len; q++) { while (z[k + 1] < q) k++; const dq = q - v[k]; res[q] = dq * dq + tmp[v[k]]; } };
    for (let x = 0; x < W; x++) { for (let y = 0; y < H; y++) tmp[y] = f[y * W + x]; pass(H); for (let y = 0; y < H; y++) f[y * W + x] = res[y]; }
    for (let y = 0; y < H; y++) { // tile the row three times so distances wrap across +-180
      for (let r = 0; r < 3; r++) for (let x = 0; x < W; x++) tmp[r * W + x] = f[y * W + x];
      pass(W * 3); for (let x = 0; x < W; x++) f[y * W + x] = res[W + x]; }
    return f;
  }
  const dOut = edt((i) => inside[i] === 1), dIn = edt((i) => inside[i] === 0);
  const ow = W / SS, oh = H / SS, o = new OffscreenCanvas(ow, oh), og = o.getContext("2d"), im = og.createImageData(ow, oh);
  for (let y = 0; y < oh; y++) for (let x = 0; x < ow; x++) {
    let acc = 0; // average the signed distance over the SSxSS block (sub-texel accurate edge)
    for (let j = 0; j < SS; j++) for (let i = 0; i < SS; i++) { const k = (y * SS + j) * W + x * SS + i;
      acc += inside[k] ? Math.sqrt(dIn[k]) - 0.5 : -(Math.sqrt(dOut[k]) - 0.5); }
    const sd = acc / (SS * SS), v = Math.max(0, Math.min(255, Math.round(255 * (0.5 + sd / (2 * RANGE)))));
    const p = (y * ow + x) * 4; im.data[p] = im.data[p + 1] = im.data[p + 2] = v; im.data[p + 3] = 255;
  }
  og.putImageData(im, 0, 0);
  const blob = await o.convertToBlob({ type: "image/png" }), buf = new Uint8Array(await blob.arrayBuffer());
  let s = ""; for (let i = 0; i < buf.length; i += 0x8000) s += String.fromCharCode.apply(null, buf.subarray(i, i + 0x8000));
  return btoa(s);
}, d, W, H, RANGE, SS);
await browser.close();
writeFileSync(out, Buffer.from(png, "base64"));
console.log("wrote", out);
