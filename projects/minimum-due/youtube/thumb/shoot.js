// Screenshot thumb.html variants at 2x (2560x1440 PNG) for YouTube; JPG 1280x720 copies are made with ffmpeg.
// Usage: node shoot.js <playwright-core dir> <out dir>
const { chromium } = require(process.argv[2] + "/node_modules/playwright-core");
const path = require("path");
(async () => {
  const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium", headless: false, args: ["--no-sandbox", "--headless=new"] });
  const p = await b.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 2 });
  for (const v of ["A", "B"]) {
    await p.goto("file://" + path.join(__dirname, "thumb.html") + "#" + v);
    await p.reload();
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(400);
    await p.screenshot({ path: path.join(process.argv[3], `thumbnail_${v}.png`) });
    console.log("shot", v);
  }
  await b.close();
})();
