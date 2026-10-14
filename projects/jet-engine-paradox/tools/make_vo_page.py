#!/usr/bin/env python3
"""Build vo_blocks.html: the voice blocks as a phone page with one-tap Copy buttons (owner, 2026-10-13).

Reads bunty_blocks_clean.md (built by tools/build_script.py), so the page always matches the fact-checked script.
Run after build_script.py; publish the HTML as the "Jet Engine VO Blocks" artifact.
"""
import html
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
md = (HERE / "bunty_blocks_clean.md").read_text(encoding="utf-8")
blocks = re.findall(r"^## (Block \d+) · ([\d,]+) characters · lines (\S+)\n\n(.*?)(?=\n## |\Z)", md, re.S | re.M)

cards = []
for name, chars, lines, text in blocks:
    text = text.strip()
    n = name.split()[-1]
    paras = "".join(f"<p>{html.escape(p)}</p>" for p in text.split("\n\n"))
    cards.append(f"""
<section class="block" aria-labelledby="h{n}">
  <header>
    <div><h2 id="h{n}">{name}</h2><p class="meta">{len(text):,} characters · lines {html.escape(lines)} · save as <code>voice/block{n}.mp3</code></p></div>
    <button type="button" class="copy" data-target="t{n}" id="b{n}">Copy block {n}</button>
  </header>
  <div class="text" id="t{n}">{paras}</div>
  <textarea class="raw" id="r{n}" readonly aria-hidden="true" tabindex="-1">{html.escape(text)}</textarea>
</section>""")

urls = (HERE / "fetch_urls.txt").read_text().strip() if (HERE / "fetch_urls.txt").exists() else ""
fetch_card = "" if not urls else f"""
<section class="block" aria-labelledby="hf">
  <header>
    <div><h2 id="hf">Footage to fetch</h2><p class="meta">GitHub app → Actions → Fetch media for a video · slug <code>jet-engine-paradox</code> · max_height 1080 · runner self-hosted</p></div>
    <button type="button" class="copy" data-target="t9" id="b9">Copy URLs</button>
  </header>
  <div class="text" id="t9"><p class="urls">{html.escape(urls)}</p><p class="note">Ten short official clips: ISRO landing and launch, DRDO flying wing, Indian Air Force MiG-21 farewell, PIB and DD India Tejas, GE Aerospace engines. The list with what each one is for is in <code>fetch_list.md</code>.</p></div>
  <textarea class="raw" id="r9" readonly aria-hidden="true" tabindex="-1">{html.escape(urls)}</textarea>
</section>"""

termux = (HERE / "fetch_termux.sh").read_text().strip() if (HERE / "fetch_termux.sh").exists() else ""
if termux:
    fetch_card = f"""
<section class="block" aria-labelledby="ht">
  <header>
    <div><h2 id="ht">Footage: fetch on your phone</h2><p class="meta">Termux · one paste · files land in Download/jep</p></div>
    <button type="button" class="copy" data-target="t8" id="b8">Copy command</button>
  </header>
  <div class="text" id="t8"><p class="note">Open Termux on the phone (not the VPS), long-press, Paste, press Enter. It installs the tools, asks once for storage access (tap Allow), then downloads the ten official clips into <code>Download/jep</code>. When it finishes, open the Files or Drive app, select everything in <code>Download/jep</code> and upload it to Drive → <code>Creator/jet-engine-paradox/footage</code>. Then tell me.</p><p class="urls">{html.escape(termux)}</p></div>
  <textarea class="raw" id="r8" readonly aria-hidden="true" tabindex="-1">{html.escape(termux)}</textarea>
</section>""" + fetch_card

page = f"""<title>Jet Engine VO Blocks</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;700;800&family=Source+Serif+4:opsz,wght@8..60,400;8..60,500&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: one narrow reading column; each voice block is a slab with a sticky copy bar, like a take sheet in a booth */
:root {{
  --bg: #f4f5f7; --panel: #ffffff; --ink: #141a24; --muted: #5b6474; --line: #d9dde4;
  --amber: #c2410c; --amber-ink: #ffffff; --ok: #15803d;
  --display: "Archivo", "Helvetica Neue", Arial, sans-serif;
  --body: "Source Serif 4", Georgia, "Times New Roman", serif;
  --mono: "IBM Plex Mono", ui-monospace, Menlo, monospace;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg: #0b0e14; --panel: #131925; --ink: #f1f4f8; --muted: #9aa4b5; --line: #263042;
  --amber: #f97316; --amber-ink: #160a02; --ok: #4ade80; color-scheme: dark; }} }}
:root[data-theme="dark"] {{
  --bg: #0b0e14; --panel: #131925; --ink: #f1f4f8; --muted: #9aa4b5; --line: #263042;
  --amber: #f97316; --amber-ink: #160a02; --ok: #4ade80; color-scheme: dark; }}
body {{ background: var(--bg); color: var(--ink); font-family: var(--body); }}
.wrap {{ max-width: 46rem; margin: 0 auto; padding-inline: 16px; padding-block: 28px 56px; display: grid; gap: 22px; }}
h1 {{ font-family: var(--display); font-weight: 800; font-size: clamp(1.6rem, 5vw, 2.3rem); line-height: 1.1; margin: 0; text-wrap: balance; letter-spacing: -0.01em; }}
.kicker {{ font-family: var(--mono); font-size: .75rem; letter-spacing: .12em; text-transform: uppercase; color: var(--amber); margin: 0 0 8px; }}
.lede {{ color: var(--muted); font-size: 1rem; line-height: 1.55; margin: 10px 0 0; }}
.settings {{ border: 1px solid var(--line); background: var(--panel); border-radius: 6px; padding: 14px 16px; display: grid; gap: 6px; font-family: var(--mono); font-size: .8rem; }}
.settings div {{ display: flex; gap: 10px; flex-wrap: wrap; }}
.settings dt {{ color: var(--muted); min-width: 7.5rem; }}
.settings dd {{ margin: 0; min-width: 0; }}
.block {{ background: var(--panel); border: 1px solid var(--line); border-radius: 6px; }}
.block header {{ position: sticky; top: env(safe-area-inset-top, 0px); z-index: 1; background: var(--panel); border-bottom: 1px solid var(--line); border-radius: 6px 6px 0 0;
  display: flex; gap: 12px; align-items: center; justify-content: space-between; flex-wrap: wrap; padding: 12px 16px; }}
h2 {{ font-family: var(--display); font-weight: 700; font-size: 1.15rem; margin: 0; }}
.meta {{ font-family: var(--mono); font-size: .72rem; color: var(--muted); margin: 3px 0 0; }}
code {{ font-family: var(--mono); }}
.copy {{ font-family: var(--display); font-weight: 700; font-size: .95rem; border: 0; border-radius: 4px; padding: 11px 18px; min-height: 44px;
  background: var(--amber); color: var(--amber-ink); cursor: pointer; }}
.copy:focus-visible {{ outline: 3px solid var(--ink); outline-offset: 2px; }}
.copy.done {{ background: var(--ok); }}
.text {{ padding: 6px 16px 14px; font-size: 1.02rem; line-height: 1.65; max-width: 65ch; }}
.text p {{ margin: 12px 0; }}
.raw {{ position: absolute; left: -9999px; width: 1px; height: 1px; }}
  .urls {{ font-family: var(--mono); font-size: .78rem; line-height: 1.5; word-break: break-all; }}
.note {{ font-size: .9rem; color: var(--muted); }}
.foot {{ font-size: .9rem; color: var(--muted); line-height: 1.55; }}
@media (prefers-reduced-motion: no-preference) {{ .copy {{ transition: background .15s; }} }}
</style>
<main class="wrap">
  <div>
    <p class="kicker">Be Practical with Kishore · voiceover</p>
    <h1>The Jet Engine Paradox</h1>
    <p class="lede">Fact-checked script v2, about ten minutes of speech. Tap a block's Copy button, paste it into ElevenLabs as one generation, and listen once. If a take skips or repeats words, generate that block again.</p>
  </div>
  <dl class="settings">
    <div><dt>Voice</dt><dd>Akash (your pick of the Akash voices)</dd></div>
    <div><dt>Model</dt><dd>Eleven Multilingual v2 (from your brief)</dd></div>
    <div><dt>Stability</dt><dd>0.60</dd></div>
    <div><dt>Similarity</dt><dd>0.85</dd></div>
    <div><dt>Style</dt><dd>0.15</dd></div>
    <div><dt>Speaker boost</dt><dd>On</dd></div>
  </dl>
  {''.join(cards)}
  {fetch_card}
  <p class="foot">Send the takes back as <code>block1.mp3</code> and <code>block2.mp3</code>: drop them in the Google Drive Creator folder or attach them in chat. The video is timed to the voice, so any pace is fine.</p>
</main>
<script>
document.querySelectorAll('.copy').forEach(function (btn) {{
  btn.addEventListener('click', function () {{
    var n = btn.dataset.target.slice(1), raw = document.getElementById('r' + n), label = btn.dataset.label || (btn.dataset.label = btn.textContent);
    function ok() {{ btn.textContent = 'Copied'; btn.classList.add('done'); setTimeout(function () {{ btn.textContent = label; btn.classList.remove('done'); }}, 2200); }}
    function fallback() {{
      var r = document.createRange(); r.selectNodeContents(document.getElementById('t' + n));
      var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
      btn.textContent = 'Selected: tap Copy';
    }}
    if (navigator.clipboard && navigator.clipboard.writeText) {{
      navigator.clipboard.writeText(raw.value).then(ok, fallback);
    }} else {{ fallback(); }}
  }});
}});
</script>
"""
(HERE / "vo_blocks.html").write_text(page, encoding="utf-8")
print(f"vo_blocks.html: {len(blocks)} blocks")
