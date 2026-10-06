// Anime-style chibi host duo (girl + boy), hand-authored vector art (no AI image generation).
// Usage: node scripts/make_duo.mjs  ->  video/assets/duo/duo.svg (+ duo-preview.html for PNG capture)
import { mkdirSync, writeFileSync } from "node:fs";

const LINE = "#3b2722";
const ol = `stroke="${LINE}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"`;
const thin = `stroke="${LINE}" stroke-width="3" stroke-linecap="round" fill="none"`;
const SKIN = "#ffe3cf";
const SKIN_SHADE = "#f6c6aa";

// Big anime eye: sclera, gradient iris, pupil, two highlights, heavy upper lash.
const eye = (x, y, flip, id, lash = 9) => {
  const s = flip ? -1 : 1; // mirror the outer-corner flick
  return `<g class="eye" transform="translate(${x} ${y}) scale(1.22) translate(${-x} ${-y})">
    <ellipse cx="${x}" cy="${y}" rx="28" ry="35" fill="#fff" ${ol}/>
    <ellipse cx="${x}" cy="${y + 4}" rx="24" ry="30" fill="url(#iris-${id})"/>
    <ellipse cx="${x}" cy="${y + 6}" rx="12" ry="16" fill="#2a1712"/>
    <path d="M${x - 20} ${y + 18} Q${x} ${y + 32} ${x + 20} ${y + 18}" stroke="#f2c58e" stroke-width="4" fill="none" opacity="0.8"/>
    <circle cx="${x - 9 * s}" cy="${y - 10}" r="10" fill="#fff"/>
    <circle cx="${x + 10 * s}" cy="${y + 14}" r="4.5" fill="#fff"/>
    <path d="M${x - 26 * s} ${y - 30} Q${x + 4 * s} ${y - 46} ${x + 32 * s} ${y - 12} L${x + 40 * s} ${y - 4}" fill="none" stroke="${LINE}" stroke-width="${lash}" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M${x - 12} ${y + 40} Q${x} ${y + 43} ${x + 12} ${y + 40}" ${thin}/>
  </g>`;
};

const blush = (x, y) => `<ellipse cx="${x}" cy="${y}" rx="24" ry="12" fill="#ff9fa6" opacity="0.55"/>
  <path d="M${x - 12} ${y + 5} l5 -10 M${x - 2} ${y + 5} l5 -10 M${x + 8} ${y + 5} l5 -10" stroke="#e86f7b" stroke-width="2.5" stroke-linecap="round" opacity="0.7"/>`;

// Anime fringe: alternating notch/tip points, each strand a rounded curve.
const fringe = (pts) =>
  pts
    .slice(1)
    .map(([px, py], i) => {
      const [ax, ay] = pts[i];
      const toTip = py > ay;
      return toTip ? `Q${ax} ${(ay + py) / 2 + 14} ${px} ${py}` : `Q${px} ${(ay + py) / 2 + 14} ${px} ${py}`;
    })
    .join(" ");

const shoe = (x, y) => `<path d="M${x - 30} ${y} Q${x - 32} ${y - 22} ${x - 6} ${y - 24} Q${x + 30} ${y - 22} ${x + 34} ${y} Z" fill="#6b3b26" ${ol}/>
  <path d="M${x - 18} ${y - 18} Q${x} ${y - 24} ${x + 16} ${y - 18}" stroke="#a0613f" stroke-width="4" fill="none" stroke-linecap="round"/>`;

const girl = (cx) => {
  const x = (d) => cx + d; // all girl coordinates are offsets from her centre line
  return `<g id="girl">
  <ellipse cx="${x(0)}" cy="905" rx="135" ry="16" fill="#000" opacity="0.18"/>
  <!-- legs, socks, shoes -->
  <path d="M${x(-48)} 780 V862 H${x(-18)} V780 Z M${x(18)} 780 V862 H${x(48)} V780 Z" fill="${SKIN}" ${ol}/>
  <path d="M${x(-50)} 840 H${x(-16)} V872 H${x(-50)} Z M${x(16)} 840 H${x(50)} V872 H${x(16)} Z" fill="#fff" ${ol}/>
  ${shoe(x(-36), 896)}${shoe(x(36), 896)}
  <!-- pleated skirt -->
  <path d="M${x(-92)} 700 H${x(92)} L${x(118)} 792 Q${x(0)} 808 ${x(-118)} 792 Z" fill="#33415f" ${ol}/>
  <path d="M${x(-50)} 704 L${x(-62)} 798 M${x(0)} 704 V804 M${x(50)} 704 L${x(62)} 798" stroke="#232e47" stroke-width="4" stroke-linecap="round"/>
  <!-- cardigan body -->
  <path d="M${x(-80)} 520 Q${x(0)} 498 ${x(80)} 520 Q${x(112)} 620 ${x(104)} 716 Q${x(0)} 734 ${x(-104)} 716 Q${x(-112)} 620 ${x(-80)} 520 Z" fill="#f2c062" ${ol}/>
  <path d="M${x(-104)} 690 Q${x(0)} 706 ${x(104)} 690" stroke="#d6a03f" stroke-width="5" fill="none"/>
  <path d="M${x(0)} 528 V712" ${thin}/>
  <circle cx="${x(8)}" cy="580" r="5" fill="#7a4a24"/><circle cx="${x(8)}" cy="630" r="5" fill="#7a4a24"/><circle cx="${x(8)}" cy="680" r="5" fill="#7a4a24"/>
  <path d="M${x(-34)} 510 L${x(0)} 548 L${x(-6)} 512 Z M${x(34)} 510 L${x(0)} 548 L${x(6)} 512 Z" fill="#fff" ${ol}/>
  <!-- resting arm (viewer right) -->
  <path d="M${x(78)} 532 Q${x(120)} 600 ${x(112)} 676 L${x(80)} 680 Q${x(84)} 610 ${x(62)} 560 Z" fill="#f2c062" ${ol}/>
  <circle cx="${x(97)}" cy="690" r="18" fill="${SKIN}" ${ol}/>
  <!-- head -->
  <g id="girl-head">
    <circle cx="${x(-92)}" cy="182" r="64" fill="#9a6440" ${ol}/>
    <path d="M${x(-120)} 160 Q${x(-92)} 140 ${x(-62)} 168 M${x(-130)} 190 Q${x(-92)} 168 ${x(-56)} 200" stroke="#7b4c2f" stroke-width="4" fill="none" stroke-linecap="round"/>
    <path d="M${x(-142)} 360 Q${x(-152)} 196 ${x(0)} 186 Q${x(152)} 196 ${x(142)} 360 Q${x(150)} 450 ${x(130)} 500 Q${x(116)} 460 ${x(112)} 420 L${x(-112)} 420 Q${x(-118)} 460 ${x(-134)} 500 Q${x(-150)} 450 ${x(-142)} 360 Z" fill="#9a6440" ${ol}/>
    <ellipse cx="${x(-62)}" cy="230" rx="28" ry="16" transform="rotate(-35 ${x(-62)} 230)" fill="#33415f" ${ol}/>
    <ellipse cx="${x(-136)}" cy="388" rx="20" ry="27" fill="${SKIN}" ${ol}/>
    <ellipse cx="${x(136)}" cy="388" rx="20" ry="27" fill="${SKIN}" ${ol}/>
    <ellipse cx="${x(0)}" cy="372" rx="136" ry="126" fill="${SKIN}" ${ol}/>
    <path d="M${x(-40)} 494 Q${x(0)} 506 ${x(40)} 494" stroke="${SKIN_SHADE}" stroke-width="10" fill="none" stroke-linecap="round"/>
    <!-- fringe with strand tips -->
    <path d="M${x(140)} 362 Q${x(148)} 206 ${x(0)} 198 Q${x(-148)} 206 ${x(-140)} 362 ${fringe([[-140, 362], [-116, 300], [-98, 352], [-74, 270], [-50, 338], [-22, 262], [4, 326], [30, 256], [56, 334], [84, 272], [104, 352], [120, 300], [140, 362]].map(([dx, y]) => [x(dx), y]))} Z" fill="#9a6440" ${ol}/>
    <path d="M${x(-136)} 330 Q${x(-150)} 430 ${x(-120)} 512 Q${x(-112)} 440 ${x(-110)} 340 Z M${x(136)} 330 Q${x(150)} 430 ${x(120)} 512 Q${x(112)} 440 ${x(110)} 340 Z" fill="#9a6440" ${ol}/>
    <path d="M${x(-70)} 222 Q${x(-20)} 206 ${x(30)} 214 M${x(50)} 222 Q${x(80)} 228 ${x(100)} 244" stroke="#c48b5e" stroke-width="7" fill="none" stroke-linecap="round"/>
    <path d="M${x(6)} 200 Q${x(8)} 140 ${x(58)} 130 Q${x(26)} 150 ${x(24)} 200" fill="#9a6440" ${ol}/>
    <!-- face -->
    <path d="M${x(-78)} 314 Q${x(-56)} 304 ${x(-34)} 312 M${x(34)} 312 Q${x(56)} 304 ${x(78)} 314" stroke="#7b4c2f" stroke-width="4" fill="none" stroke-linecap="round"/>
    <g id="girl-eyes">${eye(x(-54), 380, true, "girl")}${eye(x(54), 380, false, "girl")}</g>
    ${blush(x(-84), 432)}${blush(x(84), 432)}
    <circle cx="${x(0)}" cy="420" r="3" fill="${LINE}"/>
    <path d="M${x(-22)} 444 Q${x(0)} 446 ${x(22)} 444 Q${x(18)} 476 ${x(0)} 478 Q${x(-18)} 476 ${x(-22)} 444 Z" fill="#c4434f" ${ol}/>
    <path d="M${x(-12)} 468 Q${x(0)} 460 ${x(12)} 468 Q${x(6)} 476 ${x(0)} 476 Q${x(-6)} 476 ${x(-12)} 468 Z" fill="#ff8f99"/>
    <path d="M${x(-16)} 447 H${x(16)}" stroke="#fff" stroke-width="5" stroke-linecap="round"/>
  </g>
  <!-- waving arm (viewer left), drawn over the head so the hand stays visible -->
  <g id="girl-arm">
    <path d="M${x(-80)} 548 Q${x(-160)} 540 ${x(-186)} 470 L${x(-150)} 456 Q${x(-134)} 506 ${x(-66)} 516 Z" fill="#f2c062" ${ol}/>
    <path d="M${x(-190)} 474 Q${x(-206)} 436 ${x(-190)} 418 L${x(-200)} 392 Q${x(-194)} 382 ${x(-184)} 390 L${x(-174)} 412 L${x(-172)} 384 Q${x(-164)} 376 ${x(-158)} 386 L${x(-158)} 420 Q${x(-140)} 444 ${x(-148)} 462 Z" fill="${SKIN}" ${ol}/>
  </g>
</g>`;
};

const boy = (cx) => {
  const x = (d) => cx + d;
  return `<g id="boy">
  <ellipse cx="${x(0)}" cy="905" rx="135" ry="16" fill="#000" opacity="0.18"/>
  <!-- jeans with rolled cuffs -->
  <path d="M${x(-86)} 700 H${x(86)} L${x(80)} 862 H${x(14)} L${x(4)} 760 L${x(-6)} 760 L${x(-16)} 862 H${x(-80)} Z" fill="#33415f" ${ol}/>
  <path d="M${x(-82)} 846 H${x(-14)} V870 H${x(-82)} Z M${x(14)} 846 H${x(82)} V870 H${x(14)} Z" fill="#4c5d86" ${ol}/>
  <path d="M${x(-40)} 720 Q${x(-46)} 790 ${x(-50)} 840" stroke="#232e47" stroke-width="4" fill="none" stroke-linecap="round"/>
  ${shoe(x(-46), 896)}${shoe(x(46), 896)}
  <!-- hoodie -->
  <path d="M${x(-86)} 520 Q${x(0)} 496 ${x(86)} 520 Q${x(118)} 620 ${x(108)} 722 Q${x(0)} 740 ${x(-108)} 722 Q${x(-118)} 620 ${x(-86)} 520 Z" fill="#6b7590" ${ol}/>
  <path d="M${x(-108)} 696 Q${x(0)} 714 ${x(108)} 696" stroke="#56607a" stroke-width="5" fill="none"/>
  <path d="M${x(0)} 540 V716" ${thin}/>
  <path d="M${x(-56)} 616 Q${x(0)} 606 ${x(56)} 616 L${x(66)} 676 Q${x(0)} 688 ${x(-66)} 676 Z" fill="#5d6780" ${ol}/>
  <path d="M${x(-50)} 512 Q${x(0)} 560 ${x(50)} 512 Q${x(0)} 534 ${x(-50)} 512 Z" fill="#56607a" ${ol}/>
  <path d="M${x(-16)} 540 V590 M${x(16)} 540 V590" stroke="#e8ecf5" stroke-width="4" stroke-linecap="round"/>
  <!-- arm in pocket (viewer left) -->
  <path d="M${x(-84)} 530 Q${x(-126)} 600 ${x(-112)} 670 L${x(-62)} 664 Q${x(-80)} 610 ${x(-64)} 566 Z" fill="#6b7590" ${ol}/>
  <!-- arm holding a phone (viewer right) -->
  <g id="boy-arm">
    <path d="M${x(82)} 530 Q${x(126)} 590 ${x(124)} 640 L${x(92)} 650 Q${x(90)} 600 ${x(64)} 566 Z" fill="#6b7590" ${ol}/>
    <rect x="${x(104)}" y="560" width="46" height="84" rx="9" fill="#1d2233" ${ol} transform="rotate(10 ${x(127)} 602)"/>
    <rect x="${x(110)}" y="568" width="34" height="68" rx="5" fill="#5ee1c2" transform="rotate(10 ${x(127)} 602)"/>
    <circle cx="${x(112)}" cy="640" r="18" fill="${SKIN}" ${ol}/>
  </g>
  <!-- head -->
  <g id="boy-head">
    <path d="M${x(-142)} 380 Q${x(-156)} 200 ${x(0)} 190 Q${x(156)} 200 ${x(142)} 380 Z" fill="#2b2b33" ${ol}/>
    <ellipse cx="${x(-136)}" cy="392" rx="20" ry="27" fill="${SKIN}" ${ol}/>
    <ellipse cx="${x(136)}" cy="392" rx="20" ry="27" fill="${SKIN}" ${ol}/>
    <path d="M${x(-140)} 392 q8 -6 10 6 M${x(140)} 392 q-8 -6 -10 6" ${thin}/>
    <ellipse cx="${x(0)}" cy="374" rx="136" ry="124" fill="${SKIN}" ${ol}/>
    <path d="M${x(-40)} 494 Q${x(0)} 504 ${x(40)} 494" stroke="${SKIN_SHADE}" stroke-width="10" fill="none" stroke-linecap="round"/>
    <!-- spiky top and fringe -->
    <path d="M${x(-150)} 300 L${x(-176)} 262 L${x(-130)} 250 L${x(-150)} 196 L${x(-90)} 214 L${x(-92)} 150 L${x(-36)} 196 L${x(-6)} 126 L${x(24)} 190 L${x(76)} 120 L${x(80)} 196 L${x(136)} 168 L${x(124)} 226 L${x(178)} 238 L${x(140)} 280 L${x(166)} 330 L${x(136)} 330 L${x(126)} 296 L${x(110)} 344 L${x(88)} 270 L${x(62)} 330 L${x(40)} 262 L${x(14)} 318 L${x(-12)} 256 L${x(-40)} 322 L${x(-64)} 262 L${x(-88)} 336 L${x(-106)} 288 L${x(-124)} 340 L${x(-136)} 304 L${x(-160)} 340 Z" fill="#2b2b33" ${ol}/>
    <path d="M${x(-70)} 222 L${x(-40)} 212 M${x(-10)} 206 L${x(30)} 200 M${x(60)} 214 L${x(96)} 222" stroke="#5a5a68" stroke-width="8" stroke-linecap="round"/>
    <!-- face -->
    <path d="M${x(-78)} 318 Q${x(-56)} 310 ${x(-34)} 318 M${x(34)} 318 Q${x(56)} 310 ${x(78)} 318" stroke="#2b2b33" stroke-width="5" fill="none" stroke-linecap="round"/>
    <g id="boy-eyes">${eye(x(-54), 384, true, "boy", 7)}${eye(x(54), 384, false, "boy", 7)}</g>
    ${blush(x(-86), 436)}${blush(x(86), 436)}
    <circle cx="${x(0)}" cy="424" r="3" fill="${LINE}"/>
    <path d="M${x(-20)} 452 Q${x(-10)} 462 ${x(0)} 452 Q${x(10)} 462 ${x(20)} 452" stroke="${LINE}" stroke-width="4" stroke-linecap="round" fill="none"/>
  </g>
</g>`;
};

const iris = (id, top, bottom) => `<linearGradient id="iris-${id}" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="${top}"/><stop offset="1" stop-color="${bottom}"/></linearGradient>`;

const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 940" width="1000" height="940" role="img" aria-label="Phone Consensus host duo">
  <title>Consensus hosts (anime chibi duo)</title>
  <defs>${iris("girl", "#5a3018", "#c98b4c")}${iris("boy", "#3d2a1c", "#b07a48")}</defs>
  ${girl(285)}
  ${boy(720)}
</svg>
`;

const outDir = new URL("../video/assets/duo/", import.meta.url);
mkdirSync(outDir, { recursive: true });
writeFileSync(new URL("duo.svg", outDir), svg);
writeFileSync(
  new URL("duo-preview.html", outDir),
  `<!doctype html><meta charset="utf-8"><style>body{margin:0;background:#f4efe6;display:flex;align-items:center;justify-content:center;width:1080px;height:1080px}img{width:1000px}</style><img src="duo.svg">`,
);
console.log("wrote video/assets/duo/duo.svg");
