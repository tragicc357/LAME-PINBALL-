from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
s=re.sub(r'<title>.*?</title>','<title>LAME — Howie Lucas Pinball v18</title>',s,count=1)

# Widen the drain gap all the way to the flipper pivots, matching where each paddle begins.
# Physics floor gap.
s=s.replace('const gapL=244,gapR=356,floorY=1165;','const gapL=135,gapR=465,floorY=1165;',1)
# Drawn floor gap.
s=s.replace('const floorY=1165,gapL=244,gapR=356;','const floorY=1165,gapL=135,gapR=465;',1)

# Double every scoring event while Howie is fully outside the box.
old='const pts=base*combo;score+=pts;'
new='const pts=base*combo*(boxOpen===4?2:1);score+=pts;'
if old not in s: raise SystemExit('score block not found')
s=s.replace(old,new,1)

# Make the breakout state explicitly announce the scoring bonus.
s=s.replace('setStatus("HOWIE\'S OUT THE BOX!")','setStatus("HOWIE\'S OUT THE BOX! 2X POINTS ACTIVE!")',1)

# Add a visible 2X label to the free-state banner if present.
s=s.replace('ctx.fillText("HOWIE IS FREE!",0,90);','ctx.fillText("HOWIE IS FREE!  •  2X POINTS",0,90);',1)

p.write_text(s)
print('v18 applied')
