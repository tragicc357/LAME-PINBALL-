from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
s=s.replace('LAME — Howie Lucas Pinball v44','LAME — Howie Lucas Pinball v45',1)
pattern=r'function flipper\(side,held\)\{const pivot=side===\"L\"\?\{x:135,y:1085\}:\{x:465,y:1085\},len=128,angle='
repl='function flipper(side,held){const pivot=side===\"L\"?{x:135,y:1085}:{x:465,y:1085},len=155,angle='
s2,n=re.subn(pattern,repl,s,count=1)
if n!=1:
    raise SystemExit(f'flipper length target not found or ambiguous: {n}')
s=s2
# Safety checks
if 'len=155' not in s:
    raise SystemExit('longer flippers not installed')
if 'LAME — Howie Lucas Pinball v45' not in s:
    raise SystemExit('version title not updated')
p.write_text(s)
print('v45 patched: both flippers lengthened from 128 to 155 for a narrow center gap')
