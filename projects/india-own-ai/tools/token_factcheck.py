"""Fact-check measurements for the token test (2026-11-03). Re-runnable.

Usage: python3 -I token_factcheck.py <TOK> <EXTRA> > ../research/token_factcheck.txt
  <TOK>   the folder token_test.py uses (flores200_dataset/, sarvamai_sarvam-30b.json,
          deepseek-ai_DeepSeek-V3.json, bharatgenai_Param2-17B-A2.4B-Thinking.json)
  <EXTRA> one sub-folder per Hugging Face repo, '/' replaced by '_', each holding that repo's tokenizer.json:
          curl -L -o <EXTRA>/<org>_<name>/tokenizer.json https://huggingface.co/<org>/<name>/resolve/main/tokenizer.json
          for deepseek-ai/DeepSeek-V3.1, deepseek-ai/DeepSeek-R1-0528, deepseek-ai/DeepSeek-V3.2,
          deepseek-ai/DeepSeek-V4-Pro, deepseek-ai/DeepSeek-V4.1-Flash, sarvamai/sarvam-1,
          bharatgenai/Param-1-2.9B-Instruct, krutrim-ai-labs/Krutrim-1-instruct, unsloth/gemma-3-27b-it
          (google/gemma-3-27b-it is gated; the unsloth copy has the same size, 33,384,568 bytes)

Checks: 1) DeepSeek's chopper is unchanged from V3 to V4.1; 2) earlier Indian choppers and Google's Gemma 3 on the
same FLORES-200 devtest sentences; 3) how much of Sarvam's vocabulary is Gemma 3's; 4) other natural Telugu and
Chinese translations of the example question; 5) which Telugu letters DeepSeek splits across two pieces.
"""
import sys
import unicodedata
from collections import Counter

import tiktoken
from tokenizers import Tokenizer

TOK, EXTRA = sys.argv[1], sys.argv[2]
LANGS = ['eng_Latn', 'hin_Deva', 'tel_Telu', 'tam_Taml', 'kan_Knda', 'mal_Mlym', 'ben_Beng', 'ory_Orya', 'zho_Hans']
FLORES = {l: open(f'{TOK}/flores200_dataset/devtest/{l}.devtest', encoding='utf8').read().strip().split('\n')
          for l in LANGS}
EX = {'en': 'Will it rain in my village tomorrow?', 'te': 'రేపు మా ఊరిలో వర్షం పడుతుందా?', 'zh': '明天我们村会下雨吗？'}


def hf(path):
    t = Tokenizer.from_file(path)
    return t, (lambda s: t.encode(s, add_special_tokens=False).ids)


def table(name, enc):
    c = {l: sum(len(enc(s)) for s in FLORES[l]) for l in LANGS}
    cells = ' '.join(f"{l[:3]} {c[l]} ({c[l] / c['eng_Latn']:.2f})" for l in LANGS)
    ex = ' '.join(f'{k} {len(enc(v))}' for k, v in EX.items())
    print(f'{name:38s} example: {ex} | FLORES: {cells}')


print('== 1. DeepSeek chopper across versions (same counts = same chopper)')
for n in ['V3 (used in token_test.py)', 'DeepSeek-V3.1', 'DeepSeek-R1-0528', 'DeepSeek-V3.2', 'DeepSeek-V4-Pro',
          'DeepSeek-V4.1-Flash']:
    p = f'{TOK}/deepseek-ai_DeepSeek-V3.json' if n.startswith('V3 ') else f'{EXTRA}/deepseek-ai_{n}/tokenizer.json'
    table(n, hf(p)[1])

print('\n== 2. Earlier choppers and Google Gemma 3 on the same 1,012 sentences')
o = tiktoken.get_encoding('o200k_base')
table('o200k_base (ChatGPT, GPT-4o to GPT-5.x)', o.encode)
for n, p in [('Sarvam 30B/105B (Feb 2026)', f'{TOK}/sarvamai_sarvam-30b.json'),
             ('Sarvam-1 (Oct 2024)', f'{EXTRA}/sarvamai_sarvam-1/tokenizer.json'),
             ('BharatGen Param-1 2.9B (Jun 2025)', f'{EXTRA}/bharatgenai_Param-1-2.9B-Instruct/tokenizer.json'),
             ('Krutrim-1 (2024)', f'{EXTRA}/krutrim-ai-labs_Krutrim-1-instruct/tokenizer.json'),
             ('Gemma 3 (Google, Mar 2025)', f'{EXTRA}/unsloth_gemma-3-27b-it/tokenizer.json')]:
    table(n, hf(p)[1])

print("\n== 3. Sarvam's vocabulary vs Gemma 3's")
sv = hf(f'{TOK}/sarvamai_sarvam-30b.json')[0].get_vocab()
gm = hf(f'{EXTRA}/unsloth_gemma-3-27b-it/tokenizer.json')[0].get_vocab()


def script(tok):
    for ch in tok:
        if ch.isalpha():
            return unicodedata.name(ch, '?').split()[0]
    return 'other'


same = sum(1 for k, v in sv.items() if gm.get(k) == v)
print(f'Sarvam vocab {len(sv)}, Gemma 3 vocab {len(gm)}, same piece at the same id: {same} ({100 * same / len(sv):.1f}%)')
print('only in Sarvam, by script:', Counter(script(k) for k in sv if k not in gm).most_common(10))
print('only in Gemma 3, by script:', Counter(script(k) for k in gm if k not in sv).most_common(10))
for s in ['TELUGU', 'TAMIL', 'ORIYA', 'DEVANAGARI', 'KANNADA']:
    print(f'  {s}: Sarvam {sum(script(k) == s for k in sv)} pieces, Gemma 3 {sum(script(k) == s for k in gm)}')

print('\n== 4. Other natural translations of the example (o200k / Sarvam / DeepSeek)')
sar, ds = hf(f'{TOK}/sarvamai_sarvam-30b.json')[1], hf(f'{TOK}/deepseek-ai_DeepSeek-V3.json')[1]
for s in ['Will it rain in my village tomorrow?', 'రేపు మా ఊరిలో వర్షం పడుతుందా?', 'రేపు మా గ్రామంలో వర్షం పడుతుందా?',
          'రేపు నా ఊరిలో వర్షం పడుతుందా?', 'రేపు మా ఊర్లో వర్షం పడుతుందా?', 'మా ఊళ్ళో రేపు వాన పడుతుందా?',
          'రేపు మా గ్రామంలో వర్షం కురుస్తుందా?', '明天我们村会下雨吗？', '我的村子明天会下雨吗？', '明天我村里会下雨吗？']:
    print(f'{len(o.encode(s)):3d} {len(sar(s)):3d} {len(ds(s)):3d}  {s}')

print('\n== 5. Telugu letters DeepSeek splits across two pieces (example question)')
ids = ds(EX['te'])
dtok = hf(f'{TOK}/deepseek-ai_DeepSeek-V3.json')[0]
bs = list(range(33, 127)) + list(range(161, 173)) + list(range(174, 256))
cs, n = bs[:], 0
for b in range(256):
    if b not in bs:
        bs.append(b)
        cs.append(256 + n)
        n += 1
byte_of = {chr(c): b for b, c in zip(bs, cs)}
owner = []
for k, i in enumerate(ids):
    owner += [k] * len(bytes(byte_of[ch] for ch in dtok.id_to_token(i)))
pos = 0
for ch in EX['te']:
    L = len(ch.encode('utf8'))
    if len(set(owner[pos:pos + L])) > 1:
        print(f'  {ch} {unicodedata.name(ch)}: {L} bytes split over pieces {sorted(set(owner[pos:pos + L]))}')
    pos += L
print(f'  total pieces: {len(ids)}')
