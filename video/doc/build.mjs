// Documentary engine build: EDL (edl.mjs) + asset registry (registry.json) -> N HyperFrames parts.
// Every frame is a full-screen photo or video. Owner footage in ./assets/ always wins over the
// licensed fallbacks; drop a file in and rebuild.
// Usage: node video/doc/build.mjs            (writes video/doc/p*/, runs/breath-hold/doc/*)
import { cpSync, existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { basename, dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { beats, lowerThirds, timer, parts, voice, outDir } from "./edl.mjs";

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, "../..");
const out = join(root, outDir || "runs/breath-hold/doc");
mkdirSync(out, { recursive: true });
const r3 = (x) => Math.round(x * 1000) / 1000;
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/"/g, "&quot;");

// ---------- pauses -> voice track with gaps (scripts/mix_master.py)
const pauses = beats.filter((b) => b.pause != null).map((b) => ({ at: b.pause, len: b.len, why: b.live ? "live audio" : "hold" }));
writeFileSync(join(out, "pauses.json"), JSON.stringify(pauses, null, 1));
execFileSync(join(root, ".venv/bin/python"), [join(root, "scripts/mix_master.py"), join(root, voice || "runs/breath-hold/voice/voiceover.mp3"), join(out, "pauses.json"), out]);
const pmap = JSON.parse(readFileSync(join(out, "pause_map.json"), "utf8"));
const shS = (t) => t + pauses.filter((p) => p.at <= t).reduce((a, p) => a + p.len, 0);  // start of a normal segment
const shE = (t) => t + pauses.filter((p) => p.at < t).reduce((a, p) => a + p.len, 0);   // end of a segment / pause start
const total = pmap.video_duration;

// ---------- registry: logical name -> available files (owner assets first)
const reg = JSON.parse(readFileSync(join(here, "registry.json"), "utf8"));
const probe = (f) => Number(execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).toString().trim());
const hasAudio = (f) => execFileSync("ffprobe", ["-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", f]).toString().trim() !== "";
const avail = {};
const resolve = (name, seen = new Set()) => {
  if (avail[name]) return avail[name];
  if (seen.has(name)) return [];
  seen.add(name);
  const e = reg.assets[name];
  if (!e) throw new Error(`registry: unknown asset ${name}`);
  let list = [];
  for (const c of e.files) {
    const abs = join(root, c.file);
    if (!existsSync(abs)) continue;
    const isVid = /\.(mp4|mov|webm|mkv)$/i.test(c.file);
    list.push({ ...c, abs, isVid, dur: isVid ? probe(abs) : 0, owner: c.file.startsWith("assets/") });
  }
  // Owner footage present -> use only that. Otherwise licensed files, then fallback names.
  if (list.some((x) => x.owner)) list = list.filter((x) => x.owner);
  // No owner file: own licensed files + every fallback name, interleaved for variety.
  else {
    const pools = [list, ...(e.fallback || []).map((f) => resolve(f, seen))].filter((p) => p.length);
    list = [];
    for (let i = 0; pools.some((p) => i < p.length); i++) for (const p of pools) if (i < p.length && !list.includes(p[i])) list.push(p[i]);
  }
  return (avail[name] = list);
};

// ---------- shots
const PATTERN = [3.1, 2.7, 3.3, 2.9, 3.4, 2.6, 3.0];
const MOVES = ["in", "left", "out", "right", "up", "in", "out"];
const VMOVES = ["push", "face", "left", "push", "right"];  // video: alternate wide / tight / drift
const useCount = {}, cursor = {};
let pi = 0;
const shots = [];
const pick = (name) => {
  const list = resolve(name);
  if (!list.length) throw new Error(`no media available for "${name}" (and no fallback)`);
  const k = (useCount[name] = (useCount[name] ?? -1) + 1);
  return list[k % list.length];
};
const segs = beats.map((b) => b.pause != null
  ? { ...b, a: shE(b.pause), b: shE(b.pause) + b.len }
  : { ...b, a: shS(b.from), b: shE(b.to) });
for (const s of segs) {
  const len = s.b - s.a;
  const n = s.single ? 1 : Math.max(1, Math.round(len / (s.split ? 3.6 : 3.0)));
  const raw = Array.from({ length: n }, () => PATTERN[pi++ % PATTERN.length]);
  const k = len / raw.reduce((x, y) => x + y, 0);
  let t = s.a;
  raw.forEach((r, i) => {
    const d = i === n - 1 ? s.b - t : r3(r * k);
    const shot = { start: r3(t), dur: r3(d), end: !!s.end };
    const mk = (name) => {
      if (typeof name === "object" && name.anim) return { isAnim: true, anim: name.anim, opts: name.opts || {}, name: "anim:" + name.anim };
      const m = pick(name);
      const o = { ...m, name };
      if (m.isVid) {
        const span = Math.max(0.1, m.dur - d - 0.2);
        const c = (cursor[m.abs] = ((cursor[m.abs] ?? (m.start || 0)) ));
        o.mediaStart = s.mediaStart != null ? s.mediaStart : r3(c % span);
        cursor[m.abs] = c + d + 1.7;
      }
      o.move = s.move || m.move || (m.isVid ? VMOVES : MOVES)[(shots.length + i) % (m.isVid ? VMOVES.length : MOVES.length)];
      return o;
    };
    if (s.split) { shot.split = s.split.map(mk); shot.tags = s.tags; }
    else shot.media = mk(s.pool[i % s.pool.length]);
    if (s.live && i === 0) shot.live = s.live;
    shots.push(shot);
    t += d;
  });
}

// ---------- live audio track (owner footage only: real sound, never synthesised)
const live = [];
for (const s of segs.filter((x) => x.live)) {
  const m = resolve(s.live).find((x) => !s.liveFile || x.abs.endsWith(s.liveFile)) || resolve(s.live)[0];
  if (m && (m.owner || m.liveAudio) && m.isVid && hasAudio(m.abs)) live.push({ file: m.abs, at: r3(s.a), mediaStart: s.mediaStart ?? m.liveStart ?? Math.max(0, Math.min(0.3, m.dur - s.len)), len: s.len, gain: s.liveGain ?? 0 });
}
if (live.length) {
  const args = ["-y", "-loglevel", "error", "-f", "lavfi", "-t", String(total), "-i", "anullsrc=r=48000:cl=stereo"];
  let fc = "";
  live.forEach((l, i) => {
    args.push("-ss", String(l.mediaStart), "-t", String(l.len), "-i", l.file);
    fc += `[${i + 1}:a]aresample=48000,aformat=channel_layouts=stereo,volume=${l.gain}dB,afade=t=in:d=0.08,afade=t=out:st=${l.len - 0.4}:d=0.4,adelay=${Math.round(l.at * 1000)}|${Math.round(l.at * 1000)}[l${i}];`;
  });
  fc += `[0:a]${live.map((_, i) => `[l${i}]`).join("")}amix=inputs=${live.length + 1}:normalize=0:duration=first[o]`;
  execFileSync("ffmpeg", [...args, "-filter_complex", fc, "-map", "[o]", join(out, "live.wav")]);
} else if (existsSync(join(out, "live.wav"))) rmSync(join(out, "live.wav"));

// ---------- overlays in video time
const l3s = lowerThirds.map((l) => ({ ...l, start: r3(l.pause ? shE(l.at) : shS(l.at)) }));
const tkeys = timer.keys.map(([t, c]) => [r3(shS(t)), c]);
const twins = timer.windows.map(([a, b]) => [r3(shS(a)), r3(shE(b))]);
const talarm = timer.alarm.map(([a, b]) => [r3(shS(a)), r3(shE(b))]);
const endStart = shots.find((s) => s.end)?.start ?? total;

// ---------- emit parts
const fontFace = [400, 600, 800].map((w) =>
  `@font-face { font-family: "Inter"; font-weight: ${w}; src: url("vendor/fonts/inter-latin-${w}-normal.woff2") format("woff2"); }\n` +
  `      @font-face { font-family: "Noto Sans Telugu"; font-weight: ${w}; src: url("vendor/fonts/noto-sans-telugu-telugu-${w}-normal.woff2") format("woff2"); }`).join("\n      ");
const bounds = parts.map((p) => r3(shS(p))).concat([total]);
const credits = new Map();
let vid = 0, shotNo = 0;
for (let k = 0; k < bounds.length - 1; k++) {
  const id = `p${k + 1}`, t0 = bounds[k], t1 = bounds[k + 1], dur = r3(t1 - t0);
  const dir = join(here, id);
  rmSync(join(dir, "media"), { recursive: true, force: true });
  mkdirSync(join(dir, "media"), { recursive: true });
  cpSync(join(here, "_shared"), join(dir, "shared"), { recursive: true });
  cpSync(join(root, "assets/brand/logo_square.png"), join(dir, "media/logo_square.png"));
  execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-ss", String(t0), "-t", String(dur), "-i", join(out, "voice_paused.wav"), "-ar", "48000", "-ac", "1", join(dir, "voice.wav")]);
  const mine = shots.filter((s) => s.start >= t0 - 1e-6 && s.start < t1 - 1e-6);
  const local = (x) => r3(x - t0);
  const mediaTag = (m, st, d, extra = "") => {
    const fn = "media/" + basename(m.abs);
    if (!existsSync(join(dir, fn))) cpSync(m.abs, join(dir, fn));
    if (m.credit) credits.set(m.credit, true);
    const origin = m.origin ? ` data-origin="${m.origin}"` : "";
    if (m.isVid) return `<video id="v${++vid}" class="m" src="${fn}" muted playsinline data-move="${m.move}"${origin} data-start="${st}" data-duration="${d}" data-media-start="${m.mediaStart}" data-track-index="2" data-volume="0"${extra}></video>`;
    return `<img class="m" src="${fn}" alt="${esc(m.what || m.name)}" data-move="${m.move}"${origin}${extra} />`;
  };
  const overs = [];
  const html = mine.map((s) => {
    const st = local(s.start), d = s.dur;
    const tagOf = (m) => (!m.owner && m.archive ? `<div class="arch">${esc(m.archive)}</div>` : "") + (m.credit ? `<div class="cred">${esc(m.credit)}</div>` : "");
    if (s.split) {
      const [a, b] = s.split;
      const vids = a.isVid || b.isVid;
      const timing = vids ? `data-vs="${st}" data-vd="${d}" style="visibility:hidden"` : `data-start="${st}" data-duration="${d}" data-track-index="1"`;
      return `      <div id="${id}-s${++shotNo}" class="shot split${vids ? "" : " clip"}" ${timing}>
        <div class="half l">${mediaTag(a, st, d)}${a.archive ? `<div class="arch" style="right:auto;left:24px">${esc(a.archive)}</div>` : ""}<div class="tag">${esc(s.tags[0].big)}<small>${esc(s.tags[0].small)}</small></div></div>
        <div class="half r">${mediaTag(b, st, d)}${b.archive ? `<div class="arch">${esc(b.archive)}</div>` : ""}<div class="tag">${esc(s.tags[1].big)}<small>${esc(s.tags[1].small)}</small></div></div>
        <div class="grade"></div><div class="cred">${esc([a.credit, b.credit].filter(Boolean).join("  ·  "))}</div></div>`;
    }
    const m = s.media;
    if (m.isAnim) return `      <div id="${id}-s${++shotNo}" class="shot anim clip" data-start="${st}" data-duration="${d}" data-track-index="1" data-anim="${m.anim}" data-opts='${JSON.stringify(m.opts)}'><canvas class="cv" width="1920" height="1080"></canvas><div class="grade"></div></div>`;
    if (m.credit) credits.set(m.credit, true);
    const fit = m.fit === "contain" ? " contain" : "";
    const fill = fit && !m.isVid ? `<img class="fill" src="media/${basename(m.abs)}" alt="" />` : "";
    const timing = m.isVid ? `data-vs="${st}" data-vd="${d}" style="visibility:hidden"` : `data-start="${st}" data-duration="${d}" data-track-index="1"`;
    if (m.isVid && m.burned) return `      <div id="${id}-s${++shotNo}" class="shot" ${timing}>${mediaTag(m, st, d)}</div>`;
    if (m.isVid) {  // renderer paints video frames over siblings: overlays go in a later layer
      overs.push(`      <div class="vover" data-vs="${st}" data-vd="${d}" style="visibility:hidden"><div class="grade"></div>${tagOf(m)}</div>`);
      return `      <div id="${id}-s${++shotNo}" class="shot${fit}${s.end ? " end" : ""}" ${timing}>${mediaTag(m, st, d)}</div>`;
    }
    return `      <div id="${id}-s${++shotNo}" class="shot${fit}${s.end ? " end" : ""} clip" ${timing}>${fill}${mediaTag(m, st, d)}<div class="grade"></div>${tagOf(m)}</div>`;
  }).join("\n");
  const l3html = l3s.filter((l) => l.start >= t0 && l.start < t1).map((l) => {
    const words = esc(l.text).split(" | ").join('<span class="sep">|</span>');
    return `      <div id="${id}-l3-${String(local(l.start)).replace(".", "_")}" class="l3${l.wide ? " wide" : ""}" data-start="${local(l.start)}" data-duration="${l.dur}"><div class="bar"></div><div class="t"${l.wide ? ' style="text-transform:none;font-size:46px"' : ""}>${words}</div></div>`;
  }).join("\n");
  const clipKeys = (() => {   // only this part's timer segments, clipped to [0, dur] (negative positions shift GSAP timelines)
    const ks = tkeys.map(([t, c]) => [local(t), c]), out = [];
    for (let i = 0; i < ks.length - 1; i++) {
      const [a0, c0] = ks[i], [a1, c1] = ks[i + 1];
      if (a1 <= 0 || a0 >= dur) continue;
      const at = (x) => (a1 === a0 ? c0 : c0 + (c1 - c0) * (x - a0) / (a1 - a0));
      const s0 = Math.max(0, a0), s1 = Math.min(dur, a1);
      if (!out.length || out[out.length - 1][0] !== r3(s0)) out.push([r3(s0), Math.round(at(s0))]);
      out.push([r3(s1), Math.round(at(s1))]);
    }
    return out;
  })();
  const ptimer = { keys: clipKeys, windows: twins.filter(([a, b]) => b > t0 && a < t1).map(([a, b]) => [Math.max(0, local(a)), Math.min(dur, local(b))]),
    alarm: talarm.filter(([a, b]) => b > t0 && a < t1).map(([a, b]) => [Math.max(0, local(a)), Math.min(dur, local(b))]) };
  const end = endStart < t1 ? `      <div class="endcard" data-start="${local(Math.max(endStart, t0)) + 0.4}"><img class="logo" src="media/logo_square.png" alt="" /><div class="h">నచ్చితే Like · Share</div><div class="btn">SUBSCRIBE</div></div>` : "";
  writeFileSync(join(dir, "index.html"), `<!doctype html>
<html lang="te">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>16-minute breath hold: ${id}</title>
    <script src="vendor/gsap.min.js"></script>
    <link rel="stylesheet" href="shared/doc.css" />
    <script src="shared/anims.js"></script>
    <script src="shared/doc.js"></script>
    <style>
      ${fontFace}
    </style>
  </head>
  <body>
    <!-- Generated by video/doc/build.mjs from edl.mjs + registry.json. Edit those, not this file. -->
    <div id="root" data-composition-id="${id}" data-start="0" data-width="1920" data-height="1080" data-duration="${dur}">
${html}
${overs.join("\n")}
${l3html}
      <img class="bug" src="media/logo_square.png" alt="Be Practical with Kishore" />
      <div class="timer"><span class="dot"></span><span class="v">00:00</span><span class="k">BREATH HOLD</span></div>
${end}
      <audio id="${id}-voice" src="voice.wav" data-start="0" data-duration="${dur}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      const tl = gsap.timeline({ paused: true });
      DOC_animate(tl, ${JSON.stringify({ timer: ptimer })});
      window.__timelines["${id}"] = tl;
    </script>
  </body>
</html>
`);
  console.log(`${id}: ${t0.toFixed(2)}-${t1.toFixed(2)} (${dur.toFixed(2)}s, ${mine.length} shots)`);
}

// ---------- reports
const owner = Object.keys(reg.assets).filter((n) => reg.assets[n].files.some((f) => f.file.startsWith("assets/")));
const status = owner.map((n) => `${resolve(n).some((x) => x.owner) ? "✓ using" : "✗ missing"}  ${reg.assets[n].files.find((f) => f.file.startsWith("assets/")).file}` +
  (resolve(n).some((x) => x.owner) ? "" : `  -> fallback: ${resolve(n).map((x) => basename(x.abs)).slice(0, 3).join(", ") || "none"}`));
writeFileSync(join(out, "asset_status.txt"), status.join("\n") + "\n");
writeFileSync(join(out, "credits.txt"), [...credits.keys()].join("\n") + "\n");
writeFileSync(join(out, "shots.json"), JSON.stringify(shots.map((s) => ({ start: s.start, dur: s.dur, media: s.media ? (s.media.isAnim ? s.media.name : basename(s.media.abs)) : s.split.map((m) => basename(m.abs)), live: s.live })), null, 0).replace(/\},\{/g, "},\n{"));
const lens = shots.map((s) => s.dur);
console.log(`${shots.length} shots, ${Math.min(...lens).toFixed(2)}–${Math.max(...lens).toFixed(2)} s; live audio: ${live.length ? "yes" : "none (no owner clip with audio)"}`);
console.log(status.join("\n"));
