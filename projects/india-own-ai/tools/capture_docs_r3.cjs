// Round-3 document captures (r2 review): the right model cards and releases on the right words.
// node tools/capture_docs_r3.cjs  -> assets/docs/<name>.png (+ _full.png)
const { chromium } = require("playwright");
const pages = [
  ["sarvam_m_hf", "https://huggingface.co/sarvamai/sarvam-m"],
  ["deepseek_v4_hf", "https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro"],
  ["uidai_sarvam", "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2112485"],
  ["aim_maharashtra", "https://analyticsindiamag.com/ai-news/sarvam-ai-rolls-out-indus-cowork-to-2500-maharashtra-govt-officials"],
  ["chatgpt_pricing", "https://chatgpt.com/pricing"],
  ["isro_navic", "https://www.isro.gov.in/IRNSS_Programme.html"],
  ["aikosh_datasets", "https://aikosh.indiaai.gov.in/home/datasets/all"],
];
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2,
    userAgent: "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36" });
  for (const [name, url] of pages) {
    const p = await ctx.newPage();
    try {
      const r = await p.goto(url, { waitUntil: "domcontentloaded", timeout: 45000 });
      await p.waitForTimeout(6000);
      await p.screenshot({ path: `assets/docs/${name}.png`, fullPage: false });
      await p.screenshot({ path: `assets/docs/${name}_full.png`, fullPage: true }).catch(() => {});
      console.log(name, r ? r.status() : "?", (await p.title()).slice(0, 70));
    } catch (e) { console.log(name, "FAIL", e.message.slice(0, 80)); }
    await p.close();
  }
  await b.close();
})();
