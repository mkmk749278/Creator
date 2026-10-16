// Capture PROOF screenshots: open the real page, highlight the quoted text, screenshot the viewport (1920×1080 CSS px at
// 2× = 3840×2160, so the edit can zoom 2–3× into the highlight and stay sharp). Fixed/sticky layers (pop-ups, cookie
// bars, sticky headers) and ad slots are removed. <id>.json holds the highlight's box (fractions of the frame) for the zoom.
// Usage: node proof_shots.js <playwright-core dir> <out dir> [id,id,…]
const { chromium } = require(process.argv[2] + '/node_modules/playwright-core');
const OUT = process.argv[3];
const ONLY = process.argv[4] ? process.argv[4].split(',') : null;
const SHOTS = [
  { id: 'pib_2633', url: 'https://www.pib.gov.in/PressReleasePage.aspx?PRID=2294805&lang=1&reg=1', find: 'Kavach Version 4.0 has been successfully commissioned on 2,633 Route Kilometres' },
  { id: 'pib_7726', url: 'https://www.pib.gov.in/PressReleasePage.aspx?PRID=2294805&lang=1&reg=1', find: '7,726', also: ['6,290'] },
  { id: 'pib_21794', url: 'https://www.pib.gov.in/PressReleasePage.aspx?PRID=2294805&lang=1&reg=1', find: '21,794 RKM' },
  { id: 'pib_1465', url: 'https://www.pib.gov.in/PressReleasePage.aspx?PRID=2294805&lang=1&reg=1', find: 'Kavach version 3.2 on 1,465 RKm' },
  { id: 'pib_autobrake', url: 'https://www.pib.gov.in/PressReleasePage.aspx?PRID=2294805&lang=1&reg=1', find: 'automatic application of brakes in case Loco Pilot fails to do so' },
  { id: 'pib_headline', url: 'https://www.pib.gov.in/PressReleasePage.aspx?PRID=2294805&lang=1&reg=1', find: 'x', headline: true },
  { id: 'pib_trial_2022', url: 'https://www.pib.gov.in/PressReleasePage.aspx?PRID=1802968', find: 'halted the locomotives 380 metres apart' },
  { id: 'pib_indigenous', url: 'https://www.pib.gov.in/PressReleasePage.aspx?PRID=1802968', find: 'indigenously developed ATP system' },
];
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', headless: false, args: ['--no-sandbox', '--headless=new'] });
  const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2, userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36' });
  const pages = {};
  for (const s of SHOTS.filter(x => !ONLY || ONLY.includes(x.id))) {
    try {
      let p = pages[s.url];
      if (!p) { p = await ctx.newPage(); await p.goto(s.url, { waitUntil: 'domcontentloaded', timeout: 90000 }); await p.waitForTimeout(6000); pages[s.url] = p; }
      await p.evaluate(() => document.querySelectorAll('mark.wbmark').forEach(m => m.replaceWith(...m.childNodes)));
      const ok = await p.evaluate(({ find, also, headline }) => {
        // close cookie/popup layers that cover content
        document.querySelectorAll('body *').forEach(e => { const p = getComputedStyle(e).position; if (p === 'fixed' || p === 'sticky') e.remove(); });
        document.querySelectorAll('iframe,ins,[id^="div-gpt"],[class*="advert"],[class*="adBox"],[class*="ad_"],[id*="google_ads"]').forEach(e => e.style.visibility = 'hidden');
        if (headline) { const h = document.querySelector('h1'); if (!h) return false; h.scrollIntoView({ block: 'center' });
          h.innerHTML = `<mark class="wbmark" style="background:rgba(255,230,0,.75);color:inherit">${h.innerHTML}</mark>`; return true; }
        const mark = (needle) => {
          const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
          let n; while ((n = w.nextNode())) { const i = n.nodeValue.indexOf(needle); if (i < 0) continue;
            const r = document.createRange(); r.setStart(n, i); r.setEnd(n, i + needle.length);
            const m = document.createElement('mark'); m.className = 'wbmark'; m.style.cssText = 'background:rgba(255,230,0,.75);color:inherit;padding:0 2px;border-radius:3px';
            r.surroundContents(m); return m; }
          return null; };
        const m = mark(find); if (!m) return false;
        (also || []).forEach(mark);
        m.scrollIntoView({ block: 'center' }); return true;
      }, { find: s.find, also: s.also || [], headline: !!s.headline });
      await p.waitForTimeout(800);
      const box = await p.evaluate(() => { let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
        document.querySelectorAll('mark.wbmark').forEach(m => { const r = m.getBoundingClientRect(); if (r.width < 1 || r.bottom < 0 || r.top > innerHeight) return;
          x0 = Math.min(x0, r.left); y0 = Math.min(y0, r.top); x1 = Math.max(x1, r.right); y1 = Math.max(y1, r.bottom); });
        const W = innerWidth, H = innerHeight; return x1 < 0 ? null : { x0: x0 / W, y0: y0 / H, x1: x1 / W, y1: y1 / H }; });
      require('fs').writeFileSync(`${OUT}/${s.id}.json`, JSON.stringify(box));
      await p.screenshot({ path: `${OUT}/${s.id}.png` });
      console.log(s.id, ok ? 'ok' : 'TEXT NOT FOUND');
    } catch (e) { console.log(s.id, 'FAIL', e.message.slice(0, 120)); }
  }
  await b.close();
})();
