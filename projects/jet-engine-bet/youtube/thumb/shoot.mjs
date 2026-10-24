// node shoot.mjs <url> <out> <w> <h> [png]
import puppeteer from "puppeteer-core";
const [,, url, out, w, h, fmt] = process.argv;
const b = await puppeteer.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
  args: ["--no-sandbox", "--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--allow-file-access-from-files"] });
const p = await b.newPage(); await p.setViewport({ width: +w, height: +h });
p.on("console", m => console.log("page:", m.text())); p.on("pageerror", e => console.log("err:", e.message));
await p.goto(url, { waitUntil: "networkidle0" }); await p.evaluate(() => document.fonts.ready);
await p.waitForFunction("window.__done !== false", { timeout: 60000 }).catch(() => {});
await new Promise(r => setTimeout(r, 1500));
await p.screenshot({ path: out, type: fmt === "png" ? "png" : "jpeg", ...(fmt === "png" ? { omitBackground: true } : { quality: 92 }) });
await b.close();
