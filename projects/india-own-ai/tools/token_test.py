import sys, json, tiktoken
from tokenizers import Tokenizer
D=sys.argv[1]
langs=['eng_Latn','hin_Deva','tel_Telu','tam_Taml','kan_Knda','mal_Mlym','ben_Beng','mar_Deva','guj_Gujr','ory_Orya','pan_Guru','zho_Hans','fra_Latn']
def load(l):
    return open(f'{D}/flores200_dataset/devtest/{l}.devtest',encoding='utf8').read().strip().split('\n')
toks={'gpt4o(o200k)':tiktoken.get_encoding('o200k_base').encode,'gpt4(cl100k)':tiktoken.get_encoding('cl100k_base').encode}
for n,f in [('sarvam','sarvamai_sarvam-30b'),('bharatgen','bharatgenai_Param2-17B-A2.4B-Thinking'),('deepseekV3','deepseek-ai_DeepSeek-V3'),('qwen3','Qwen_Qwen3-8B')]:
    t=Tokenizer.from_file(f'{D}/{f}.json'); toks[n]=(lambda t: lambda s: t.encode(s,add_special_tokens=False).ids)(t)
res={}
for l in langs:
    try: S=load(l)
    except Exception as e: print('skip',l,e); continue
    res[l]={n:sum(len(f(s)) for s in S) for n,f in toks.items()}
    res[l]['chars']=sum(len(s) for s in S); res[l]['n']=len(S)
eng=res['eng_Latn']
print('lang', *toks.keys(), sep='\t')
for l,r in res.items():
    print(l, *[f"{r[n]} ({r[n]/eng[n]:.2f}x)" for n in toks], sep='\t')
json.dump(res,open(sys.argv[2],'w'),indent=1)
