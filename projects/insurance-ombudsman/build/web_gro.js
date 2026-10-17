// CIO "Grievance Redressal Officers" page for O030: officers' names and personal emails blurred in the page itself,
// the generic GRO role addresses kept readable (the VO: "the Ombudsman's website lists their email addresses too").
const { chromium } = require('/opt/node-tools/node_modules/playwright-core');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
  const ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 3 });
  const p = await ctx.newPage();
  await p.goto('https://cioins.co.in/GRONonLife', { waitUntil: 'networkidle', timeout: 90000 }).catch((e) => console.log(e.message));
  await p.waitForTimeout(3000);
  await p.evaluate(() => {
    document.querySelectorAll('.modal, .modal-backdrop').forEach((e) => e.remove());
    document.querySelectorAll('body *').forEach((e) => { const s = getComputedStyle(e).position; if (s === 'fixed' || s === 'sticky') e.style.position = 'absolute'; });
    // wrap "Name: ..." and "Email Id: ..." (not "GRO Email Id") lines and blur them
    const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
    const hits = [];
    while (walk.nextNode()) {
      const e = walk.currentNode, t = (e.innerText || '').trim();
      if (e.children.length <= 3 && (/^Name\s*:/.test(t) || /^Email Id\s*:/.test(t)) && t.length < 120) hits.push(e);
    }
    hits.forEach((e) => { e.style.filter = 'blur(7px)'; });
  });
  await p.waitForTimeout(800);
  await p.screenshot({ path: process.argv[2], clip: { x: 0, y: 0, width: 1440, height: 810 } });
  await b.close();
})();
