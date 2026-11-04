import sys, tiktoken
from tokenizers import Tokenizer
D=sys.argv[1]
T={'chatgpt_o200k':(lambda e: lambda s:[e.decode([i]) for i in e.encode(s)])(tiktoken.get_encoding('o200k_base'))}
for n,f in [('sarvam','sarvamai_sarvam-30b'),('deepseekV3','deepseek-ai_DeepSeek-V3'),('bharatgen','bharatgenai_Param2-17B-A2.4B-Thinking')]:
    t=Tokenizer.from_file(f'{D}/{f}.json'); T[n]=(lambda t: lambda s:[t.decode([i]) for i in t.encode(s,add_special_tokens=False).ids])(t)
S={'en':'Will it rain in my village tomorrow?','te':'రేపు మా ఊరిలో వర్షం పడుతుందా?','hi':'क्या कल मेरे गाँव में बारिश होगी?','ta':'நாளை என் ஊரில் மழை பெய்யுமா?','zh':'明天我们村会下雨吗？'}
for n,f in T.items():
    print('==',n)
    for l,s in S.items():
        p=f(s); print(l,len(p),p)
