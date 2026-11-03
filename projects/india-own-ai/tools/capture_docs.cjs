// Screenshot the primary documents the film pushes into (1920x1080 at 2x for crisp push-ins).
// node tools/capture_docs.cjs  -> assets/docs/<name>.png
const { chromium } = require("playwright");
const pages = [
  ["deepseek_v3_abs", "https://arxiv.org/abs/2412.19437"],
  ["sarvam_105b_hf", "https://huggingface.co/sarvamai/sarvam-105b"],
  ["bharatgen_param2_hf", "https://huggingface.co/bharatgenai/Param2-17B-A2.4B-Thinking"],
  ["sarvam_blog", "https://www.sarvam.ai/blogs/sarvam-30b-105b"],
  ["bharatgen_blog", "https://bharatgen.com/blogs/param2-what-we-built"],
  ["pib_factsheet", "https://www.pib.gov.in/FactsheetDetails.aspx?Id=150860&reg=3&lang=3"],
  ["pib_jan2025", "https://pib.gov.in/PressReleasePage.aspx?PRID=2097709"],
  ["federal_register_rule", "https://www.federalregister.gov/documents/2025/01/15/2025-00636/framework-for-artificial-intelligence-diffusion"],
  ["commoncrawl_stats", "https://commoncrawl.github.io/cc-crawl-statistics/plots/languages"],
  ["aikosh", "https://aikosh.indiaai.gov.in/"],
  ["reuters_jan27", "https://www.reuters.com/markets/us/nasdaq-futures-tumble-chinas-ai-push-rattles-big-tech-2025-01-27"],
  ["techcrunch_go_free", "https://techcrunch.com/2025/10/27/openai-offers-free-chatgpt-go-for-one-year-to-all-users-in-india/"],
  ["techcrunch_indus", "https://techcrunch.com/2026/02/20/indias-sarvam-launches-indus-ai-chat-app-as-competition-heats-up/"],
];
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2,
    userAgent: "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36" });
  for (const [name, url] of pages) {
    const p = await ctx.newPage();
    try {
      const r = await p.goto(url, { waitUntil: "domcontentloaded", timeout: 45000 });
      await p.waitForTimeout(4000);
      await p.screenshot({ path: `assets/docs/${name}.png`, fullPage: false });
      await p.screenshot({ path: `assets/docs/${name}_full.png`, fullPage: true }).catch(() => {});
      console.log(name, r ? r.status() : "?", (await p.title()).slice(0, 70));
    } catch (e) { console.log(name, "FAIL", e.message.slice(0, 80)); }
    await p.close();
  }
  await b.close();
})();
