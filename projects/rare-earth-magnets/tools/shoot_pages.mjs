// Screenshot real source pages (news headlines, PIB releases) for document push-ins.
// node projects/rare-earth-magnets/tools/shoot_pages.mjs  -> assets/docs/<name>.png (1920x1080 viewport, top of page)
import puppeteer from "puppeteer-core";
const OUT = new URL("../assets/docs/", import.meta.url).pathname;
const pages = {
  autocar_chetak_july: "https://www.autocarindia.com/industry-amp/bajaj-chetak-production-slumps-in-july-amid-rare-earth-magnet-crunch-436723",
  pmindia_cabinet_repm: "https://www.pmindia.gov.in/en/news_updates/cabinet-approves-rs-7280-crore-scheme-to-promote-manufacturing-of-sintered-rare-earth-permanent-magnets-repm/",
  pib_2147282: "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2147282",
  pib_2248182: "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2248182",
  pib_2238892: "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2238892",
  pib_2220295: "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2220295",
  ddindia_20_bids: "https://ddindia.co.in/2026/08/government-receives-20-bids-for-rare-earth-permanent-magnet-manufacturing-scheme/",
  miningtech_japan: "https://www.mining-technology.com/news/india-rare-earths-halt-japan-exports",
  cnbctv18_rajiv: "https://www.cnbctv18.com/business/india-ev-industry-china-rare-earth-magnet-exports-rajiv-bajaj-19595743.htm",
  iea_exec_summary: "https://www.iea.org/reports/rare-earth-elements/executive-summary",
  technology_org_nov10: "https://www.technology.org/2026/10/19/china-rare-earth-export-pause-november-10",
  fe_bajaj_ather_tvs: "https://www.financialexpress.com/auto/electric-vehicles/rare-earth-magnet-shortage-from-china-bajaj-ather-and-tvs-slashing-ev-output/3905951",
  ians_licences: "https://ianslive.in/indian-firms-get-licenses-to-import-rare-earth-magnets-from-china--20251030172703",
};
const b = await puppeteer.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args: ["--no-sandbox"] });
for (const [name, url] of Object.entries(pages)) {
  const p = await b.newPage();
  await p.setViewport({ width: 1920, height: 1080 });
  await p.setUserAgent("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36");
  try {
    await p.goto(url, { waitUntil: "networkidle2", timeout: 45000 });
    await new Promise(r => setTimeout(r, 2500));
    await p.screenshot({ path: OUT + name + ".png" });
    console.log("ok", name, await p.title());
  } catch (e) { console.log("fail", name, e.message.slice(0, 80)); }
  await p.close();
}
await b.close();
