import puppeteer from "puppeteer-core";
const [,, html, out] = process.argv;
const b = await puppeteer.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args: ["--no-sandbox", "--allow-file-access-from-files"] });
const p = await b.newPage(); await p.setViewport({ width: 1280, height: 720 });
await p.goto("file://" + html, { waitUntil: "networkidle0" }); await p.evaluate(() => document.fonts.ready);
await p.screenshot({ path: out, type: "jpeg", quality: 92 }); await b.close();
