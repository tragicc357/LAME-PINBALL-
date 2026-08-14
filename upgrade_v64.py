from pathlib import Path
p=Path('index.html')
s=p.read_text()
orig=s
s=s.replace('LAME — Howie Lucas Pinball v63','LAME — Howie Lucas Pinball v64',1)

# Every normal capture hole relocates after every completed eject.
old="if(used&&used.hits>=3)relocateCaptureHole(usedHoleId);else setStatus('BOX EJECT COMPLETE • BALL BACK IN PLAY')"
new="if(used)relocateCaptureHole(usedHoleId);else setStatus('BOX EJECT COMPLETE • BALL BACK IN PLAY')"
if old not in s: raise SystemExit('relocation threshold target missing')
s=s.replace(old,new,1)

# The hit count is no longer a threshold; keep it reset by relocation but make the UI explain movement.
old="ctx.fillText('50K',h.x,h.y+1);ctx.fillStyle='#9beaff';ctx.font='900 9px Arial';ctx.fillText((3-(h.hits||0))+' LEFT',h.x,h.y+15)"
new="ctx.fillText('50K',h.x,h.y+1);ctx.fillStyle='#9beaff';ctx.font='900 9px Arial';ctx.fillText('MOVES',h.x,h.y+15)"
if old not in s: raise SystemExit('hole UI target missing')
s=s.replace(old,new,1)

# Update relocation status to make the repeat-every-capture rule clear.
old="setStatus('🕳️ HOLE MOVED! OLD SPOT SEALED • NEW HOLE OPENED')"
new="setStatus('🕳️ HOLE MOVED! OLD SPOT SEALED • NEW HOLE OPENED — EVERY CAPTURE RELOCATES IT')"
if old not in s: raise SystemExit('relocation status target missing')
s=s.replace(old,new,1)

# Update instructions.
old='12. Each level has <b>3 capture holes</b>. Use the same hole 3 times and, after the third box eject, that hole <b>seals and relocates</b> to a new open spot. Two exterior rescue vortexes trigger <b>2 BONUS BALLS</b> for 3-ball multiball<br>13. Beat Level 5 to win'
new='12. Each level has <b>3 moving capture holes</b>. Every time a ball enters a normal hole, the ball ejects from the box and that hole <b>immediately seals and respawns somewhere else</b>. Ramp holes stay fixed. Two exterior rescue vortexes trigger <b>2 BONUS BALLS</b> for 3-ball multiball<br>13. Beat Level 5 to win'
if old in s:s=s.replace(old,new,1)

if s==orig: raise SystemExit('no changes applied')
p.write_text(s)
print('v64 every-capture relocation applied')
# trigger v64 workflow
