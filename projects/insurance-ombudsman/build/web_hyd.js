// CIO office directory with the HYDERABAD centre selected (the film follows a Hyderabad family), 3x for a 4K push-in.
const { chromium } = require('/opt/node-tools/node_modules/playwright-core');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
  const ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 3 });
  const p = await ctx.newPage();
  await p.goto('https://cioins.co.in/Ombudsman', { waitUntil: 'networkidle', timeout: 90000 }).catch(e => console.log(e.message));
  await p.waitForTimeout(3000);
  await p.evaluate(() => document.querySelectorAll('.modal, .modal-backdrop').forEach((e) => e.remove()));
  const els = await p.$$('text=/^\\s*HYDERABAD\\s*$/i'); console.log('matches', els.length);
  for (const e of els) { try { await e.click({ timeout: 2000 }); console.log('clicked'); break; } catch (x) { console.log('noclick'); } }
  await p.waitForTimeout(2500);
  await p.evaluate(() => document.querySelectorAll('body *').forEach((e) => { const s = getComputedStyle(e).position; if (s === 'fixed' || s === 'sticky') e.style.position = 'absolute'; }));
  const txt = await p.evaluate(() => document.body.innerText.match(/HYDERABAD[\s\S]{0,400}/g));
  console.log(JSON.stringify(txt && txt.slice(-2)));
  await p.screenshot({ path: process.argv[2], fullPage: true });
  await b.close();
})();
