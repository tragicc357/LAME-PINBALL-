from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
s=s.replace('LAME — Howie Lucas Pinball v58','LAME — Howie Lucas Pinball v59',1)
pat=r'async function api\(method,body\)\{.*?\}function esc\(v\)'
repl='async function api(method,body){const o={method,headers:{"Authorization":"Bearer "+GAME_ANON_KEY,"apikey":GAME_ANON_KEY,"Content-Type":"application/json"}};if(body)o.body=JSON.stringify(body);const r=await fetch(GAME_API,o);if(!r.ok)throw new Error(r.status+" "+await r.text());return r.json()}function esc(v)'
s2,n=re.subn(pat,repl,s,count=1,flags=re.S)
if n!=1: raise SystemExit(f'api replacement count {n}')
p.write_text(s2)
print('v59 edge direct-db client restored')
