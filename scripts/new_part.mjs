// Scaffold one part of a multi-part video as a standalone HyperFrames project.
// Usage: node scripts/new_part.mjs <run-dir> <video-dir> <part-id>
//   e.g. node scripts/new_part.mjs runs/pixel-11 video/pixel11 p1
// Creates <video-dir>/<part-id>/ with: index.html skeleton (duration, voice
// audio, background, host bar wired to the voice timings), shared/ (theme,
// host bar, bg), media/ (vetted press images), voice.wav. Never overwrites an
// existing index.html.
import { cpSync, existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const [run, videoDir, part] = process.argv.slice(2);
if (!part) throw new Error("usage: new_part.mjs <run-dir> <video-dir> <part-id>");
const timings = JSON.parse(readFileSync(join(run, "voice", `${part}.timings.json`), "utf8"));
const dir = join(videoDir, part);
mkdirSync(dir, { recursive: true });
cpSync(join(videoDir, "_shared"), join(dir, "shared"), { recursive: true });
if (existsSync(join(videoDir, "_media"))) cpSync(join(videoDir, "_media"), join(dir, "media"), { recursive: true });
if (existsSync(join(videoDir, "_samples"))) cpSync(join(videoDir, "_samples"), join(dir, "samples"), { recursive: true });
cpSync(join(run, "voice", `${part}.wav`), join(dir, "voice.wav"));

const index = join(dir, "index.html");
if (!existsSync(index)) {
  const dur = timings.duration;
  writeFileSync(index, `<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>Pixel 11 consensus: ${part}</title>
    <script src="vendor/gsap.min.js"></script>
    <link rel="stylesheet" href="shared/theme.css" />
    <script src="shared/hostbar.js"></script>
    <style>
      @font-face { font-family: "Inter"; font-weight: 400; src: url("vendor/fonts/inter-latin-400-normal.woff2") format("woff2"); }
      @font-face { font-family: "Inter"; font-weight: 600; src: url("vendor/fonts/inter-latin-600-normal.woff2") format("woff2"); }
      @font-face { font-family: "Inter"; font-weight: 800; src: url("vendor/fonts/inter-latin-800-normal.woff2") format("woff2"); }
      /* Part-specific styles go here. */
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="${part}" data-start="0" data-width="1920" data-height="1080" data-duration="${dur}">
      <div class="bg"></div>
      <div class="bg-vignette"></div>

      <!-- SCENES: one <section class="clip" data-start data-duration> per beat, synced to voice timings -->

      <div id="hostbar"></div>
      <audio id="${part}-voice" src="voice.wav" data-start="0" data-duration="${dur}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      window.HF_TIMINGS = ${JSON.stringify(timings)};
      const tl = gsap.timeline({ paused: true });
      HF_hostbar(tl, window.HF_TIMINGS);

      // Scene tweens go here (absolute times in seconds, from HF_TIMINGS line starts).

      window.__timelines["${part}"] = tl;
    </script>
  </body>
</html>
`);
}
console.log(`scaffolded ${dir} (${timings.duration}s, ${timings.lines.length} lines)`);
