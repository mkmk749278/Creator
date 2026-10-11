// Capture PROOF screenshots: open the real page, highlight the quoted text, screenshot the viewport (1920×1080).
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
  const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1, userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36' });
  const pages = {};
  for (const s of SHOTS) {
    try {
      let p = pages[s.url];
      if (!p) { p = await ctx.newPage(); await p.goto(s.url, { waitUntil: 'domcontentloaded', timeout: 90000 }); await p.waitForTimeout(6000); pages[s.url] = p; }
      await p.evaluate(() => document.querySelectorAll('mark.wbmark').forEach(m => m.replaceWith(...m.childNodes)));
      const ok = await p.evaluate(({ find, also, headline }) => {
        // close cookie/popup layers that cover content
        document.querySelectorAll('[class*="cookie"],[id*="cookie"],[class*="popup"],[class*="modal"]').forEach(e => { if (getComputedStyle(e).position === 'fixed') e.remove(); });
        if (headline) { const h = document.querySelector('h1'); if (!h) return false; h.scrollIntoView({ block: 'center' }); h.style.background = 'rgba(255,230,0,.55)'; return true; }
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
      await p.screenshot({ path: `${OUT}/${s.id}.png` });
      console.log(s.id, ok ? 'ok' : 'TEXT NOT FOUND');
    } catch (e) { console.log(s.id, 'FAIL', e.message.slice(0, 120)); }
  }
  await b.close();
})();
