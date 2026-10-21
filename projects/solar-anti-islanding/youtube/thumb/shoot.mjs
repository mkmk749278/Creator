// Screenshot thumb.html at 2x (2560x1440 PNG) → thumbnail.jpg 1280x720 via ffmpeg.  node shoot.mjs
import puppeteer from "puppeteer-core";
import { execFileSync } from "child_process";
import path from "path";
const dir = path.dirname(new URL(import.meta.url).pathname);
const b = await puppeteer.launch({ executablePath: "/opt/pw-browsers/chromium", args: ["--no-sandbox", "--allow-file-access-from-files"] });
const p = await b.newPage(); await p.setViewport({ width: 1280, height: 720, deviceScaleFactor: 2 });
await p.goto("file://" + path.join(dir, "thumb.html")); await p.evaluate(() => document.fonts.ready); await new Promise(r => setTimeout(r, 400));
await p.screenshot({ path: "/tmp/thumbnail.png" }); await b.close();
execFileSync("ffmpeg", ["-v", "error", "-y", "-i", "/tmp/thumbnail.png", "-vf", "scale=1280:720", "-q:v", "2", path.join(dir, "../thumbnail.jpg")]);
console.log("thumbnail.jpg");
