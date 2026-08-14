from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()

s=s.replace('LAME — Howie Lucas Pinball v39','LAME — Howie Lucas Pinball v40',1)

bad='function updateBallTrail();drawBallTrail();drawRealBall(){'
if bad in s:
    s=s.replace(bad,'function drawRealBall(){',1)

# Insert trail drawing only at the actual ball render call inside drawWorld.
# Find all bare drawRealBall() calls and skip the function declaration itself.
positions=[m.start() for m in re.finditer(r'drawRealBall\(\)',s)]
if len(positions)<2:
    raise SystemExit(f'Expected at least declaration + render call, found {len(positions)}')
# Replace the last occurrence, which is the render call in drawWorld.
pos=positions[-1]
s=s[:pos]+'updateBallTrail();drawBallTrail();drawRealBall()'+s[pos+len('drawRealBall()'):]

# Basic static sanity checks for the exact startup-breaking pattern.
if 'function updateBallTrail();' in s:
    raise SystemExit('Malformed function declaration still present')
if 'function drawRealBall(){' not in s:
    raise SystemExit('drawRealBall declaration missing')
if 'updateBallTrail();drawBallTrail();drawRealBall()' not in s:
    raise SystemExit('trail render hook missing')

p.write_text(s)
print('v40 patched: startup syntax fixed; v39 features preserved')
