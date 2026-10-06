// Generates the chibi channel mascot ("Consensus Kid") as vector SVGs, one per expression.
// Hand-authored vector art (no AI image generation). Colours come from config/brand.yaml.
// Usage: node scripts/make_mascot.mjs  ->  video/assets/mascot/mascot-<mood>.svg
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";

const brandYaml = readFileSync(new URL("../config/brand.yaml", import.meta.url), "utf8");
const brand = Object.fromEntries(
  [...brandYaml.matchAll(/^\s+(\w+):\s*"(#[0-9a-fA-F]{6})"/gm)].map((m) => [m[1], m[2]]),
);

const C = {
  skin: "#ffdcc4",
  skinShade: "#f5c3a6",
  hair: "#1d2440",
  hairHi: "#2f3a63",
  hoodie: brand.accent,
  hoodieShade: "#3fbfa2",
  pants: "#3a4566",
  ink: "#1a1d29",
  blush: "#ff9aa8",
  phones: brand.accent_2,
  white: "#ffffff",
};

const MOODS = {
  happy: { badge: brand.accent, badgeGlyph: "check" },
  thinking: { badge: brand.accent_2, badgeGlyph: "dots" },
  wow: { badge: brand.warn, badgeGlyph: "bang" },
  meh: { badge: brand.bad, badgeGlyph: "cross" },
  hello: { badge: brand.accent, badgeGlyph: "check" }, // open eyes + raised hand, used by the wave animation
};

const eye = (cx, mood) => {
  if (mood === "happy") {
    // closed ^ ^ smiling eyes
    return `<path d="M${cx - 20} 222 Q${cx} 196 ${cx + 20} 222" fill="none" stroke="${C.ink}" stroke-width="7" stroke-linecap="round"/>`;
  }
  const ry = mood === "wow" ? 31 : mood === "meh" ? 18 : 28;
  const cy = mood === "meh" ? 224 : 218;
  const look = mood === "thinking" ? 6 : 0;
  return `
    <ellipse cx="${cx}" cy="${cy}" rx="22" ry="${ry}" fill="${C.ink}"/>
    <ellipse cx="${cx + look}" cy="${cy + ry * 0.3}" rx="15" ry="${ry * 0.55}" fill="url(#iris)"/>
    <circle cx="${cx - 8 + look}" cy="${cy - ry * 0.4}" r="${mood === "wow" ? 9 : 8}" fill="${C.white}"/>
    <circle cx="${cx + 9 + look}" cy="${cy + ry * 0.35}" r="4" fill="${C.white}" opacity="0.9"/>
    ${mood === "meh" ? `<path d="M${cx - 26} ${cy - 14} H${cx + 26}" stroke="${C.skin}" stroke-width="16"/>
      <path d="M${cx - 24} ${cy - 7} H${cx + 24}" stroke="${C.ink}" stroke-width="6" stroke-linecap="round"/>` : ""}`;
};

const brows = (mood) => {
  const s = `fill="none" stroke="${C.hair}" stroke-width="6" stroke-linecap="round"`;
  if (mood === "thinking") return `<path d="M136 178 Q155 166 174 176" ${s}/><path d="M226 170 Q246 160 266 166" ${s}/>`;
  if (mood === "wow") return `<path d="M136 170 Q155 158 174 168" ${s}/><path d="M226 168 Q245 158 264 170" ${s}/>`;
  if (mood === "meh") return `<path d="M136 192 Q155 186 174 194" ${s}/><path d="M226 194 Q245 186 264 192" ${s}/>`;
  return `<path d="M138 180 Q155 172 172 180" ${s}/><path d="M228 180 Q245 172 262 180" ${s}/>`;
};

const mouth = (mood) => {
  if (mood === "happy" || mood === "hello")
    return `<path d="M182 258 Q200 284 218 258 Z" fill="#c2414f" stroke="${C.ink}" stroke-width="4" stroke-linejoin="round"/>
      <path d="M190 268 Q200 278 210 268" fill="#ff8a96"/>`;
  if (mood === "wow") return `<ellipse cx="200" cy="268" rx="11" ry="14" fill="#c2414f" stroke="${C.ink}" stroke-width="4"/>`;
  if (mood === "thinking") return `<path d="M188 266 Q198 260 212 264" fill="none" stroke="${C.ink}" stroke-width="5" stroke-linecap="round"/>`;
  return `<path d="M184 268 Q192 262 200 268 Q208 274 216 266" fill="none" stroke="${C.ink}" stroke-width="5" stroke-linecap="round"/>`;
};

const badge = ({ badge: color, badgeGlyph }) => {
  const g = {
    check: `<path d="M-11 0 L-3 8 L12 -8" fill="none" stroke="${C.white}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>`,
    cross: `<path d="M-8 -8 L8 8 M8 -8 L-8 8" stroke="${C.white}" stroke-width="6" stroke-linecap="round"/>`,
    bang: `<path d="M0 -12 V3" stroke="${C.white}" stroke-width="6" stroke-linecap="round"/><circle cx="0" cy="11" r="3.5" fill="${C.white}"/>`,
    dots: [-10, 0, 10].map((x) => `<circle cx="${x}" cy="0" r="4" fill="${C.white}"/>`).join(""),
  }[badgeGlyph];
  return `<g transform="translate(330 78)"><circle r="28" fill="${color}" stroke="${brand.bg}" stroke-width="5"/>${g}</g>`;
};

// Free hand: thinking = finger to chin, otherwise a relaxed wave/rest.
const freeArm = (mood) =>
  mood === "thinking"
    ? `<path d="M138 352 Q120 330 150 300" fill="none" stroke="${C.hoodie}" stroke-width="30" stroke-linecap="round"/>
       <circle cx="156" cy="296" r="16" fill="${C.skin}"/>`
    : mood === "hello"
      ? `<path d="M136 350 Q90 340 70 300" fill="none" stroke="${C.hoodie}" stroke-width="30" stroke-linecap="round"/>
         <circle cx="66" cy="288" r="17" fill="${C.skin}"/>
         <path d="M56 276 l-4 -12 M64 272 v-14 M73 274 l3 -12" stroke="${C.skin}" stroke-width="7" stroke-linecap="round"/>`
    : mood === "happy"
      ? `<path d="M136 350 Q100 330 92 290" fill="none" stroke="${C.hoodie}" stroke-width="30" stroke-linecap="round"/>
         <circle cx="90" cy="280" r="17" fill="${C.skin}"/>
         <path d="M84 266 v-12 M92 264 v-14 M100 268 v-10" stroke="${C.skin}" stroke-width="7" stroke-linecap="round"/>`
      : `<path d="M136 350 Q112 380 118 412" fill="none" stroke="${C.hoodie}" stroke-width="30" stroke-linecap="round"/>
         <circle cx="120" cy="420" r="16" fill="${C.skin}"/>`;

const svg = (mood) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 520" width="400" height="520" role="img" aria-label="Phone Consensus mascot, ${mood}">
  <title>Consensus Kid (${mood})</title>
  <defs>
    <radialGradient id="iris" cx="0.5" cy="0.35" r="0.7">
      <stop offset="0" stop-color="${brand.accent}"/><stop offset="1" stop-color="${brand.accent_2}"/>
    </radialGradient>
    <linearGradient id="screen" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="${brand.bg_2}"/><stop offset="1" stop-color="${brand.bg}"/>
    </linearGradient>
  </defs>
  <ellipse cx="200" cy="500" rx="110" ry="12" fill="#000" opacity="0.28"/>
  <!-- legs -->
  <g id="body">
  <rect x="160" y="430" width="34" height="62" rx="14" fill="${C.pants}"/>
  <rect x="206" y="430" width="34" height="62" rx="14" fill="${C.pants}"/>
  <ellipse cx="174" cy="492" rx="26" ry="11" fill="${C.white}"/>
  <ellipse cx="226" cy="492" rx="26" ry="11" fill="${C.white}"/>
  <!-- body / hoodie -->
  <path d="M140 330 Q200 310 260 330 Q282 390 276 440 Q200 456 124 440 Q118 390 140 330 Z" fill="${C.hoodie}"/>
  <path d="M168 400 H232 Q236 426 228 432 H172 Q164 426 168 400 Z" fill="${C.hoodieShade}"/>
  <path d="M186 334 L182 372 M214 334 L218 372" stroke="${C.white}" stroke-width="4" stroke-linecap="round"/>
  <g id="free-arm">${freeArm(mood)}</g>
  <!-- phone hand (generic phone, not a real model) -->
  <path d="M262 352 Q296 372 290 404" fill="none" stroke="${C.hoodie}" stroke-width="30" stroke-linecap="round"/>
  <g transform="rotate(-12 300 380)">
    <rect x="276" y="336" width="50" height="90" rx="10" fill="${C.ink}"/>
    <rect x="281" y="342" width="40" height="78" rx="6" fill="url(#screen)"/>
    <rect x="287" y="352" width="28" height="5" rx="2.5" fill="${brand.accent}"/>
    <rect x="287" y="362" width="20" height="5" rx="2.5" fill="${brand.warn}"/>
    <rect x="287" y="372" width="24" height="5" rx="2.5" fill="${brand.accent_2}"/>
  </g>
  <circle cx="290" cy="404" r="16" fill="${C.skin}"/>
  <!-- head -->
  <g id="head">
  <ellipse cx="200" cy="300" rx="34" ry="14" fill="${C.skinShade}"/>
  <ellipse cx="200" cy="205" rx="128" ry="112" fill="${C.skin}"/>
  <!-- hair -->
  <path d="M74 214 Q60 98 168 82 Q252 70 306 112 Q342 146 328 216 Q316 170 290 150 Q282 176 256 172 Q262 150 248 140 Q228 172 196 170 Q206 150 196 136 Q170 172 132 168 Q140 150 138 140 Q100 160 74 214 Z" fill="${C.hair}"/>
  <path d="M150 96 Q200 80 250 92" fill="none" stroke="${C.hairHi}" stroke-width="10" stroke-linecap="round"/>
  <path d="M206 82 Q214 52 240 48 Q226 64 228 80 Z" fill="${C.hair}"/>
  <!-- headphones -->
  <path d="M70 200 Q66 64 200 60 Q334 64 330 200" fill="none" stroke="${C.phones}" stroke-width="14" stroke-linecap="round"/>
  <rect x="52" y="180" width="36" height="66" rx="16" fill="${C.phones}"/>
  <rect x="312" y="180" width="36" height="66" rx="16" fill="${C.phones}"/>
  <rect x="60" y="192" width="14" height="42" rx="7" fill="${brand.bg_2}"/>
  <rect x="326" y="192" width="14" height="42" rx="7" fill="${brand.bg_2}"/>
  <!-- face -->
  ${brows(mood)}
  <g id="eye-l" class="eye">${eye(155, mood)}</g>
  <g id="eye-r" class="eye">${eye(245, mood)}</g>
  <ellipse cx="130" cy="252" rx="18" ry="10" fill="${C.blush}" opacity="0.55"/>
  <ellipse cx="270" cy="252" rx="18" ry="10" fill="${C.blush}" opacity="0.55"/>
  ${mouth(mood)}
  ${badge(MOODS[mood])}
  </g>
  </g>
</svg>
`;

const outDir = new URL("../video/assets/mascot/", import.meta.url);
mkdirSync(outDir, { recursive: true });
for (const mood of Object.keys(MOODS)) writeFileSync(new URL(`mascot-${mood}.svg`, outDir), svg(mood));

// Phone-viewable contact sheet (render to PNG with headless Chromium).
const sheet = `<!doctype html><meta charset="utf-8"><style>
body{margin:0;background:${brand.bg};display:grid;grid-template-columns:repeat(${Object.keys(MOODS).length},1fr);gap:24px;padding:40px;width:1840px;height:1000px;align-items:center;font:600 34px sans-serif;color:${brand.ink}}
figure{margin:0;background:${brand.bg_2};border-radius:28px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:40px 0}
img{width:320px}figcaption{margin-top:12px}</style>
${Object.keys(MOODS).map((m) => `<figure><img src="mascot-${m}.svg"><figcaption>${m}</figcaption></figure>`).join("")}`;
writeFileSync(new URL("contact-sheet.html", outDir), sheet);
console.log(`wrote ${Object.keys(MOODS).length} moods to video/assets/mascot/`);

// HyperFrames composition: the "hello" mascot blinking and waving (6 s, loops cleanly).
const animDir = new URL("../video/mascot/", import.meta.url);
mkdirSync(animDir, { recursive: true });
const greeting = "Hi!"; // on-screen text; keep i18n-ready
const inlineSvg = svg("hello").replace('width="400" height="520"', 'id="mascot-svg"');
writeFileSync(
  new URL("index.html", animDir),
  `<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>Mascot: blink and wave</title>
    <!-- Generated by scripts/make_mascot.mjs; edit the generator, not this file. -->
    <script src="vendor/gsap.min.js"></script>
    <style>
      @font-face { font-family: "Inter"; font-weight: 800; src: url("vendor/fonts/inter-latin-800-normal.woff2") format("woff2"); }
      /* Brand tokens: mirror config/brand.yaml */
      :root {
${Object.entries(brand).map(([k, v]) => `        --${k.replace("_", "-")}: ${v};`).join("\n")}
      }
      * { box-sizing: border-box; }
      body { margin: 0; background: var(--bg); color: var(--ink); font-family: "Inter", sans-serif; }
      #root { position: relative; width: 1920px; height: 1080px; overflow: hidden; background: radial-gradient(90% 80% at 50% 40%, var(--bg-2) 0%, var(--bg) 70%); }
      #glow { position: absolute; left: 610px; top: 190px; width: 700px; height: 700px; border-radius: 50%; background: #134d48; filter: blur(140px); opacity: 0.6; }
      #mascot { position: absolute; left: 598px; top: 70px; width: 724px; height: 940px; }
      #mascot-svg { width: 100%; height: 100%; overflow: visible; }
      #bubble {
        position: absolute; left: 330px; top: 250px; padding: 22px 48px; border-radius: 48px;
        background: var(--ink); color: var(--bg); font-weight: 800; font-size: 96px; line-height: 1;
        box-shadow: 0 30px 80px rgba(0, 0, 0, 0.45);
      }
      #bubble::after {
        content: ""; position: absolute; right: -18px; bottom: 6px; border: 22px solid transparent;
        border-left-color: var(--ink); border-bottom-color: var(--ink); transform: rotate(-10deg);
      }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="mascot" data-start="0" data-width="1920" data-height="1080" data-duration="6">
      <div id="glow"></div>
      <div id="mascot">${inlineSvg}</div>
      <div id="bubble">${greeting}</div>
    </div>
    <script>
      const tl = gsap.timeline({ paused: true });
      // Pop in, then breathe (even repeat count so it settles back to rest).
      tl.from("#mascot", { y: 80, scale: 0.85, opacity: 0, duration: 0.6, ease: "back.out(1.7)", transformOrigin: "50% 100%" }, 0);
      tl.to("#body", { y: -6, duration: 0.75, ease: "sine.inOut", yoyo: true, repeat: 5 }, 0.6);
      // Wave: swing the raised arm around the shoulder, head tilts along.
      const wave = (t, swings) => {
        tl.to("#free-arm", { rotation: -18, duration: 0.18, ease: "sine.out", svgOrigin: "136 350" }, t);
        tl.to("#free-arm", { rotation: 8, duration: 0.24, ease: "sine.inOut", yoyo: true, repeat: swings * 2 - 1, svgOrigin: "136 350" }, t + 0.18);
        tl.to("#free-arm", { rotation: 0, duration: 0.2, ease: "sine.out", svgOrigin: "136 350" }, t + 0.18 + swings * 0.48);
        tl.to("#head", { rotation: -4, duration: 0.4, ease: "sine.inOut", svgOrigin: "200 300" }, t);
        tl.to("#head", { rotation: 0, duration: 0.4, ease: "sine.inOut", svgOrigin: "200 300" }, t + 0.18 + swings * 0.48);
      };
      wave(0.8, 3);
      wave(3.9, 2);
      // Blinks (one double blink).
      for (const t of [1.5, 3.1, 3.35, 5.4]) {
        tl.to(".eye", { scaleY: 0.1, transformOrigin: "50% 50%", duration: 0.07, ease: "power1.in" }, t);
        tl.to(".eye", { scaleY: 1, transformOrigin: "50% 50%", duration: 0.09, ease: "power1.out" }, t + 0.07);
      }
      // Speech bubble.
      tl.from("#bubble", { scale: 0, opacity: 0, transformOrigin: "100% 100%", duration: 0.45, ease: "back.out(2)" }, 0.9);
      tl.to("#bubble", { scale: 0.9, opacity: 0, transformOrigin: "100% 100%", duration: 0.3, ease: "power1.in" }, 5.5);
      tl.set({}, {}, 6);
      window.__timelines = window.__timelines || {};
      window.__timelines["mascot"] = tl;
    </script>
  </body>
</html>
`,
);
console.log("wrote video/mascot/index.html");
