// node shoot.cjs <html> <out.jpg>   (Playwright's preinstalled Chromium, 1280x720, JPEG q92)
const { chromium } = require("playwright");
(async () => {
  const [html, out] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
  await p.goto("file://" + require("path").resolve(html)); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
  await p.screenshot({ path: out, type: "jpeg", quality: 92 }); await b.close();
})();
