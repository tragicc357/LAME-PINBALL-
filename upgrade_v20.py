from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
s=re.sub(r'<title>.*?</title>','<title>LAME — Howie Lucas Pinball v20</title>',s,count=1)

# Track a short motion window whenever either paddle changes state.
s=s.replace('let flipperHitAt={L:0,R:0};let howieHitAt=0;let drainCommitted=false;',
'''let flipperHitAt={L:0,R:0};let flipperMotionUntil={L:0,R:0};let howieHitAt=0;let drainCommitted=false;''',1)

# A paddle only collides while it is actually moving (press or release transition).
old='function hitFlipper(side,held){const f=flipper(side,held),'
new='function hitFlipper(side,held){if(performance.now()>flipperMotionUntil[side])return;const f=flipper(side,held),'
if old not in s: raise SystemExit('hitFlipper block not found')
s=s.replace(old,new,1)

# Remove collision from the angled walls that connect into the paddle pivots.
old='''}segHit(25,930,110,1040,10,1.03,5);segHit(575,930,490,1040,10,1.03,5);segHit(110,1040,135,1085,8,1.02,3);segHit(490,1040,465,1085,8,1.02,3)}function howieOutStreakSeconds()'''
new='''}}function howieOutStreakSeconds()'''
if old not in s: raise SystemExit('lower paddle-wall collision block not found')
s=s.replace(old,new,1)

# Touch controls: only start a motion window when the paddle state actually changes.
old='function bindHold(id,side){const el=document.getElementById(id),set=v=>{if(side==="L")left=v;else right=v;el.classList.toggle("active",v)};'
new='''function bindHold(id,side){const el=document.getElementById(id),set=v=>{const was=side==="L"?left:right;if(was!==v)flipperMotionUntil[side]=performance.now()+170;if(side==="L")left=v;else right=v;el.classList.toggle("active",v)};'''
if old not in s: raise SystemExit('bindHold block not found')
s=s.replace(old,new,1)

# Keyboard controls get the same physical motion window.
s=s.replace('if(e.code==="ArrowLeft"||e.code==="KeyA")left=true;if(e.code==="ArrowRight"||e.code==="KeyD")right=true;',
'''if(e.code==="ArrowLeft"||e.code==="KeyA"){if(!left)flipperMotionUntil.L=performance.now()+170;left=true}if(e.code==="ArrowRight"||e.code==="KeyD"){if(!right)flipperMotionUntil.R=performance.now()+170;right=true};''',1)
s=s.replace('if(e.code==="ArrowLeft"||e.code==="KeyA")left=false;if(e.code==="ArrowRight"||e.code==="KeyD")right=false;',
'''if(e.code==="ArrowLeft"||e.code==="KeyA"){if(left)flipperMotionUntil.L=performance.now()+170;left=false}if(e.code==="ArrowRight"||e.code==="KeyD"){if(right)flipperMotionUntil.R=performance.now()+170;right=false};''',1)

# Make the double-points state explicit in both Howie captions.
s=s.replace('ctx.fillText("HOWIE IS FREE!  •  2X POINTS",0,90);','ctx.fillText("HOWIE IS FREE!  •  DOUBLE POINTS ‼️",0,90);',1)
s=s.replace('ctx.fillText("HOWIE\'S OUT THE BOX!",300,897);','ctx.fillText("HOWIE\'S OUT THE BOX! • DOUBLE POINTS ‼️",300,897);',1)
s=s.replace('setStatus("HOWIE\'S OUT THE BOX! 2X POINTS ACTIVE!")','setStatus("HOWIE\'S OUT THE BOX! DOUBLE POINTS ‼️")',1)

p.write_text(s)
print('v20 applied')
