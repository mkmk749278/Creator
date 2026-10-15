// Full-page screenshots of the two complaint portals for the browser-clip scenes (1440 px wide, 2x).
const { chromium } = require('/opt/node-tools/node_modules/playwright-core');
const OUT = process.argv[2];
const SITES = [['bima', 'https://bimabharosa.irdai.gov.in/'], ['cio', 'https://cioins.co.in/'], ['cio_complaint', 'https://cioins.co.in/Complaint'], ['cio_offices', 'https://cioins.co.in/Ombudsman']];
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
  const ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2,
    userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36' });
  for (const [id, url] of SITES) {
    const p = await ctx.newPage();
    try { await p.goto(url, { waitUntil: 'networkidle', timeout: 90000 }); } catch (e) { console.log(id, 'goto', e.message.slice(0, 80)); }
    await p.waitForTimeout(5000);
    // close announcement pop-ups (OK buttons, modals, backdrops) so the page itself is visible
    for (const sel of ['text=OK', 'button.close', '.modal .close', '[data-dismiss=modal]', 'text=×']) { try { await p.click(sel, { timeout: 1500 }); await p.waitForTimeout(600); } catch (e) {} }
    await p.keyboard.press('Escape').catch(() => {});
    if (id.startsWith('cio')) await p.evaluate(() => document.querySelectorAll('.modal, .modal-backdrop').forEach((e) => e.remove()));
    await p.evaluate(() => { document.body.classList.remove('modal-open'); document.body.style.overflow = 'auto'; });
    await p.waitForTimeout(800);
    await p.evaluate(() => document.querySelectorAll('body *').forEach((e) => { const s = getComputedStyle(e).position; if (s === 'fixed' || s === 'sticky') e.style.position = 'absolute'; }));
    const h = await p.evaluate(() => document.documentElement.scrollHeight);
    await p.screenshot({ path: `${OUT}/${id}_full.png`, fullPage: true });
    console.log(id, 'height', h);
  }
  await b.close();
})();
