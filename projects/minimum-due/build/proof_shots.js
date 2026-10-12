// Capture PROOF screenshots: open the real page, highlight the quoted text, screenshot the viewport (1920×1080 CSS px at
// 2× = 3840×2160, so the edit can zoom 2–3× into the highlight and stay sharp). Fixed/sticky layers (pop-ups, cookie
// bars, sticky headers) and ad slots are removed. <id>.json holds the highlight's box (fractions of the frame) for the zoom.
// Usage: node proof_shots.js <playwright-core dir> <out dir>
const { chromium } = require(process.argv[2] + '/node_modules/playwright-core');
const OUT = process.argv[3];
const SHOTS = [
  { id: 'icici_page', url: 'https://www.icici.bank.in/personal-banking/blogs/card/credit-card/interest-rates', find: 'Interest free period is cancelled' },
  { id: 'icici_rate', url: 'https://www.icici.bank.in/personal-banking/blogs/card/credit-card/interest-rates', find: '3.75% per month' },
  { id: 'icici_bill', url: 'https://www.icici.bank.in/personal-banking/blogs/card/credit-card/interest-rates', find: '65,000.00' , also: ['69,688.00'] },
  { id: 'icici_interest', url: 'https://www.icici.bank.in/personal-banking/blogs/card/credit-card/interest-rates', find: '3,658.65', also: ['658.56'] },
  { id: 'icici_table', url: 'https://www.icici.bank.in/personal-banking/blogs/card/credit-card/interest-rates', find: '1,084.93', also: ['462.33', '34.68'] },
  { id: 'rbi_lost', url: 'https://taxguru.in/rbi/reserve-bank-india-commercial-banks-credit-cards-debit-cards-issuance-conduct-directions-2025.html', find: 'interest free credit period will be lost' },
  { id: 'rbi_warning', url: 'https://taxguru.in/rbi/reserve-bank-india-commercial-banks-credit-cards-debit-cards-issuance-conduct-directions-2025.html', find: 'Making only the minimum payment every month' },
  { id: 'news_rent', url: 'https://www.business-standard.com/finance/personal-finance/phonepe-paytm-cred-end-rent-service-as-rbi-tightens-payment-rules-125091800422_1.html', find: 'rent', headline: true },
];
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', headless: false, args: ['--no-sandbox', '--headless=new'] });
  const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2, userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36' });
  const pages = {};
  for (const s of SHOTS) {
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
