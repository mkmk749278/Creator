#!/usr/bin/env python3
"""The village question as each chopper really cuts it, for the PIECE METER tiles (research/token_pieces.json).
Byte fragments of a letter (a piece that is not valid text on its own) are kept as raw bytes and marked bad=True;
on screen they are the red half-letter tiles. usage: token_pieces.py TOKENIZER_DIR"""
import json, sys, tiktoken
from tokenizers import Tokenizer
D = sys.argv[1]
S = {'en': 'Will it rain in my village tomorrow?', 'hi': 'क्या कल मेरे गाँव में बारिश होगी?',
     'mr': 'उद्या माझ्या गावात पाऊस पडेल का?', 'te': 'రేపు మా ఊరిలో వర్షం పడుతుందా?', 'zh': '明天我们村会下雨吗？'}
def pieces_bytes(byte_list):
    out = []
    for b in byte_list:
        try: out.append({'t': b.decode('utf-8'), 'bad': False})
        except UnicodeDecodeError: out.append({'t': b.hex(), 'bad': True})
    return out
res = {}
e = tiktoken.get_encoding('o200k_base')
res['chatgpt'] = {l: pieces_bytes([e.decode_single_token_bytes(i) for i in e.encode(s)]) for l, s in S.items()}
for n, f in [('sarvam', 'sarvamai_sarvam-30b'), ('deepseek', 'deepseek-ai_DeepSeek-V3')]:
    t = Tokenizer.from_file(f'{D}/{f}.json')
    def raw(tok):   # byte-level BPE tokens map back to bytes through the GPT-2 byte table
        bs = list(range(ord("!"), ord("~") + 1)) + list(range(ord("¡"), ord("¬") + 1)) + list(range(ord("®"), ord("ÿ") + 1))
        cs = bs[:]; n2 = 0
        for b in range(256):
            if b not in bs: bs.append(b); cs.append(256 + n2); n2 += 1
        dec = {chr(c): b for b, c in zip(bs, cs)}
        return bytes(dec[ch] for ch in tok)
    res[n] = {}
    for l, s in S.items():
        enc = t.encode(s, add_special_tokens=False)
        try: res[n][l] = pieces_bytes([raw(x) for x in enc.tokens])
        except KeyError:   # sentencepiece-style vocab (no byte table): decode ids one by one
            res[n][l] = [{'t': t.decode([i]), 'bad': '�' in t.decode([i])} for i in enc.ids]
for n in res:
    print(n, {l: (len(v), sum(p['bad'] for p in v)) for l, v in res[n].items()})
json.dump(res, open('research/token_pieces.json', 'w'), ensure_ascii=False, indent=1)
