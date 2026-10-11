const { chromium } = require(process.argv[2] + '/node_modules/playwright-core');
(async () => { const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', headless: false, args: ['--no-sandbox','--headless=new'] });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  for (const f of ['sim_bill','sim_autopay_min','sim_autopay_full','sim_warning','sim_finance']) { await p.goto('file://' + __dirname + '/' + f + '.html'); await p.waitForTimeout(300); await p.screenshot({ path: process.argv[3] + '/' + f + '.png' }); console.log(f); }
  await b.close(); })();
