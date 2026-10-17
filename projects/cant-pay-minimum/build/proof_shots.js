// Capture PROOF screenshots: open the real page, highlight the quoted text, screenshot the viewport (1920×1080 CSS px at
// 2× = 3840×2160, so the edit can zoom 2–3× into the highlight and stay sharp). Fixed/sticky layers (pop-ups, cookie
// bars, sticky headers) and ad slots are removed. <id>.json holds the highlight's box (fractions of the frame) for the zoom.
// Copied from projects/minimum-due/build/proof_shots.js. Changes: the matcher ignores whitespace and quote-mark
// differences and can span several text nodes (statute text is often split across <span>s); hidden accordion answers
// that hold the quote are opened; `only` runs a subset (comma-separated ids).
// PDFs (HDFC, PNB, OneCard, IndusInd, Supreme Court) are shot by proof_pdf.py: Chromium cannot highlight inside a PDF.
// Usage: node proof_shots.js <playwright-core dir> <out dir> [id,id,...]
// e.g.   node proof_shots.js /opt/node-tools ../assets/proof
const { chromium } = require(process.argv[2] + '/node_modules/playwright-core');
const OUT = process.argv[3];
const ONLY = process.argv[4] ? process.argv[4].split(',') : null;
const RBI_IRAC = 'https://www.rbi.org.in/Scripts/BS_ViewMasCirculardetails.aspx?id=12822';
const KANOON_SBI = 'https://indiankanoon.org/doc/68016726/';
const SBI_FAQ = 'https://www.sbicard.com/en/faq/card-blocking-unblocking.page';
const SHOTS = [
  { id: 'rbi_npa_90', url: RBI_IRAC, find: 'A credit card account will be treated as non-performing asset if the minimum amount due, as mentioned in the statement, is not paid fully within 90 days from the payment due date mentioned in the statement.' },
  { id: 'rbi_provision_25', url: RBI_IRAC, find: 'The ‘unsecured exposures’ which are identified as ‘substandard’ would attract additional provision of 10 per cent, i.e., a total of 25 per cent on the outstanding balance.' },
  { id: 'rbi_bureau_15days', url: 'https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12718', find: 'CICs and CIs shall keep the credit information collected/maintained by them updated regularly on a fortnightly basis (i.e., as on 15th and last day of the respective month)' },
  { id: 'kanoon_sbi_cibil', url: KANOON_SBI, find: 'On this account we conclude that the District Commission has rightly held the Company deficient in service i.e. by not properly intimating the respondent.' },
  { id: 'sbi_faq_block', url: SBI_FAQ, find: 'In case you have missed making payment of at least minimum amount due as of latest statement on your SBI Credit Card, your card may be blocked for further usage.' },
  { id: 'sbi_faq_writeoff', url: SBI_FAQ, fresh: true, find: 'More than 6 consecutive payments default', also: ['In case your account is written-off and you pay complete outstanding as per the agreement, we will process your request for CIBIL status clean-up'] },
  { id: 'kanoon_lok_adalat_indore', url: KANOON_SBI, find: 'In June 2019, the Company filed a pre-litigation in National Lok Adalat, Indore', also: ['dues of Rs.1,82,969/-'] },
  { id: 'livelaw_lok_adalat_decree', url: 'https://www.livelaw.in/amp/high-court/jammu-kashmir/jammu-and-kashmir-high-court-lok-adalat-awards-deemed-decrees-no-further-appeals-under-section-96-of-cpc-allowed-240513', find: 'every award issued by the Lok Adalat is deemed to be a decree of a Civil Court and is final and binding', hideText: ['Your free access to Live Law has expired'] },
  { id: 'bnb_76000_awards', url: 'https://www.barandbench.com/news/litigation/delhi-high-court-shocked-to-find-one-arbitrator-handled-axis-banks-4155-arbitrations-in-5-years', find: 'The bank also disclosed that 76,000 awards had been passed pan-India by sole arbitrators who were unilaterally appointed in disputes involving the bank.' },
  { id: 'drt_20_lakh', url: 'https://www.taxheal.com/?p=68695', find: 'the provisions of the said Act shall not apply where the amount of debt due to any bank or financial institution or to a consortium of banks or financial institutions is less than twenty lakh rupees.', hideText: ['File Taxes', 'Tax Heal Youtube Channel'] },
  { id: 'kanoon_ncdrc_setoff_53k', url: 'https://indiankanoon.org/doc/65053962/', find: 'In view of the aforesaid clause, the petitioner bank was entitled to set off the credit card dues at any point of time, without any notice to the complainant. Therefore, deduction of the amount of Rs.53,043.68 from the saving bank account of the complainant was in consonance with the above referred condition' },
  { id: 'kanoon_kerala_hold', url: 'https://indiankanoon.org/doc/98197117/', find: 'the action initiated by the respondents by freezing the account of the 1st petitioner is not an attachment, but according to the bank, it is in exercise of the right of adjustment or the right akin to set off' },
  { id: 'sc_2025_kukreja', url: 'https://www.caseciter.com/shrichand-rajaram-kukreja-vs-state-of-maharashtra-2025-insc-794-quashing-civil-disputes-criminal-cases/', find: 'It seems that the complainant has contrived to somehow or the other, involve the police machinery to act as recovery agents on his behalf.', also: ['The allegations, made in the complaint, present a dispute which is purely commercial and civil in nature.'] },
  { id: 'rbi_ombudsman_90days', url: 'https://www.rbi.org.in/Scripts/FAQView.aspx?Id=153', find: 'The complaint must be made to the RBI Ombudsman within 90 days from the date on which the above timeline expires or the date of the last communication from the concerned Regulated Entity, whichever is later.' },
  { id: 'rbi_faq_14448', url: 'https://www.rbi.org.in/Scripts/FAQView.aspx?Id=153', find: 'The IVRS facility on Toll Free No. 14448 is available 24x7.' },
  { id: 'rbi_faq_cms_address', url: 'https://www.rbi.org.in/Scripts/FAQView.aspx?Id=153', find: 'One centralised complaint lodging portal i.e., https://cms.rbi.org.in' },
  { id: 'rbi_cms_portal', url: 'https://cms.rbi.org.in/', find: '14448', optional: true },
  { id: 'ecourts_case_status', url: 'https://services.ecourts.gov.in/ecourtindia_v6/', none: true },
];
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', headless: false, args: ['--no-sandbox', '--headless=new'] });
  const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2, userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36' });
  const pages = {};
  for (const s of SHOTS) {
    if (ONLY && !ONLY.includes(s.id)) continue;
    try {
      let p = s.fresh ? null : pages[s.url];
      if (!p) { p = await ctx.newPage(); await p.goto(s.url, { waitUntil: 'domcontentloaded', timeout: 90000 }); await p.waitForTimeout(7000); if (!s.fresh) pages[s.url] = p; }
      await p.evaluate(() => { document.querySelectorAll('mark.wbmark').forEach(m => m.replaceWith(...m.childNodes)); document.body.normalize(); window.scrollTo(0, 0); });
      const ok = await p.evaluate(({ find, also, none, hideText }) => {
        // close cookie/popup layers that cover content
        document.querySelectorAll('html *').forEach(e => { const p = getComputedStyle(e).position; if (p === 'fixed' || p === 'sticky') e.remove(); });  // html, not body: Google's anno chip hangs off <html>
        document.querySelectorAll('iframe,ins,[id^="div-gpt"],[class*="advert"],[class*="adBox"],[class*="ad_"],[id*="google_ads"],[class*="adsbygoogle"],[class*="google-anno"],[class*="goog-rentry"],[id^="aswift"]').forEach(e => e.style.visibility = 'hidden');
        document.querySelectorAll('video').forEach(e => e.style.visibility = 'hidden');
        // hide a small box (paywall note, floating button) found by its text: climb while the parent stays under 260 px
        // and holds no highlight
        const hideBoxes = () => hideText.forEach(t => { const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
          while ((n = w.nextNode())) { if (!n.nodeValue.includes(t)) continue; let e = n.parentElement;
            while (e.parentElement && e.parentElement !== document.body && e.parentElement.getBoundingClientRect().height < 260 && !e.parentElement.querySelector('mark.wbmark')) e = e.parentElement;
            e.style.setProperty('visibility', 'hidden', 'important'); } });
        document.documentElement.style.overflow = 'auto'; document.body.style.overflow = 'auto';
        if (none) { hideBoxes(); return true; }
        const canon = c => (c === '‘' || c === '’' || c === '`') ? "'" : (c === '“' || c === '”') ? '"' : (c === '–' || c === '—') ? '-' : c;
        const norm = t => t.split('').map(canon).join('').replace(/\s+/g, '').toLowerCase();
        const mark = (needle) => {
          // flatten visible-or-hidden text nodes into one whitespace-free string, with a map back to (node, offset)
          const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, { acceptNode: n => /^(SCRIPT|STYLE|NOSCRIPT)$/.test(n.parentNode.nodeName) ? 2 : 1 });
          let n, flat = '', map = [];
          while ((n = w.nextNode())) { const v = n.nodeValue; for (let i = 0; i < v.length; i++) { if (/\s/.test(v[i])) continue; flat += canon(v[i]).toLowerCase(); map.push([n, i]); } }
          const k = flat.indexOf(norm(needle)); if (k < 0) return null;
          const end = k + norm(needle).length - 1;
          // group the hit by text node and wrap each piece
          const pieces = []; for (let j = k; j <= end; j++) { const [nd, off] = map[j]; const last = pieces[pieces.length - 1];
            if (last && last.n === nd) last.e = off + 1; else pieces.push({ n: nd, s: off, e: off + 1 }); }
          const marks = [];
          pieces.reverse().forEach(pc => { const r = document.createRange(); r.setStart(pc.n, pc.s); r.setEnd(pc.n, pc.e);
            const m = document.createElement('mark'); m.className = 'wbmark'; m.style.cssText = 'background:rgba(255,230,0,.75);color:inherit;padding:0 2px;border-radius:3px';
            r.surroundContents(m); marks.unshift(m); });
          // open collapsed accordions / hidden tabs holding the quote
          let e = marks[0].parentElement; while (e && e !== document.body) { const cs = getComputedStyle(e);
            if (cs.display === 'none') e.style.display = 'block';
            if (cs.visibility === 'hidden') e.style.visibility = 'visible';
            if (cs.overflow === 'hidden' && e.clientHeight < 5) { e.style.height = 'auto'; e.style.maxHeight = 'none'; }
            e = e.parentElement; }
          return marks[0]; };
        const m = mark(find); if (!m) return false;
        (also || []).forEach(mark);
        hideBoxes();
        m.scrollIntoView({ block: 'center' }); return true;
      }, { find: s.find || '', also: s.also || [], none: !!s.none, hideText: s.hideText || [] });
      await p.waitForTimeout(1000);
      // second sweep for layers injected after the first one (late pop-ups, ad chips); never touch the highlight
      await p.evaluate(() => document.querySelectorAll('html *').forEach(e => { const q = getComputedStyle(e).position;
        if ((q === 'fixed' || q === 'sticky') && !e.querySelector('mark.wbmark')) e.remove(); }));
      const box = s.none ? null : await p.evaluate(() => { let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
        document.querySelectorAll('mark.wbmark').forEach(m => { for (const r of m.getClientRects()) { if (r.width < 1 || r.bottom < 0 || r.top > innerHeight) continue;
          x0 = Math.min(x0, r.left); y0 = Math.min(y0, r.top); x1 = Math.max(x1, r.right); y1 = Math.max(y1, r.bottom); } });
        const W = innerWidth, H = innerHeight; return x1 < 0 ? null : { x0: x0 / W, y0: y0 / H, x1: x1 / W, y1: y1 / H }; });
      require('fs').writeFileSync(`${OUT}/${s.id}.json`, JSON.stringify(box));
      await p.screenshot({ path: `${OUT}/${s.id}.png` });
      console.log(s.id, ok ? 'ok' : 'TEXT NOT FOUND', JSON.stringify(box));
    } catch (e) { console.log(s.id, 'FAIL', e.message.slice(0, 160)); }
  }
  await b.close();
})();
