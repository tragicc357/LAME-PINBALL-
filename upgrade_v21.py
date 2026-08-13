from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
s=re.sub(r'<title>.*?</title>','<title>LAME — Howie Lucas Pinball v21</title>',s,count=1)

# Replace the v20 flipper response. Paddles always collide physically.
# Resting paddle: catch/deflect softly and feed the ball inward/down toward the drain.
# Moving paddle: apply a strong upward impulse and momentum.
pat=r'function hitFlipper\(side,held\)\{.*?\}\}function checkLamps\(\)'
m=re.search(pat,s,re.S)
if not m: raise SystemExit('hitFlipper block not found')
new='''function hitFlipper(side,held){const f=flipper(side,held),ax=f.pivot.x,ay=f.pivot.y,bx=f.tip.x,by=f.tip.y,vx=bx-ax,vy=by-ay,wx=ball.x-ax,wy=ball.y-ay,len2=vx*vx+vy*vy,t=clamp((wx*vx+wy*vy)/len2,0,1),px=ax+t*vx,py=ay+t*vy,dx=ball.x-px,dy=ball.y-py,d=Math.hypot(dx,dy),thick=24,min=ball.r+thick;if(d>=min)return false;let nx=dx/(d||1),ny=dy/(d||1);if(d<.001){nx=0;ny=-1}ball.x=px+nx*(min+1);ball.y=py+ny*(min+1);const moving=performance.now()<=flipperMotionUntil[side];if(moving){const dot=ball.vx*nx+ball.vy*ny;if(dot<0){ball.vx-=1.95*dot*nx;ball.vy-=1.95*dot*ny}const tipPower=7.2+3.4*t;ball.vy=Math.min(ball.vy,-4.0)-tipPower;ball.vx+=(side==="L"?1:-1)*(1.5+2.7*t);const now=performance.now();if(now-flipperHitAt[side]>110){flipperHitAt[side]=now;addScore(35,px,py);spark(px,py,8)}}else{const inward=side==="L"?1:-1;ball.vx=ball.vx*.30+inward*(0.72+0.48*t);ball.vy=Math.max(1.05,Math.abs(ball.vy)*0.22+0.38);if(ball.y>1100)ball.vy=Math.max(ball.vy,1.55)}capBallSpeed();return true}function checkLamps()'''
s=s[:m.start()]+new+s[m.end():]

# Make sure the center drain cannot commit before a ball has had a fair chance to contact a resting paddle.
# Once it is clearly below paddle contact height, commit it to falling with no rescue/bounce.
s=s.replace('if(!inShooter&&ball.x>135&&ball.x<465&&ball.y>1120)drainCommitted=true;',
'''if(!inShooter&&ball.x>135&&ball.x<465&&ball.y>1148)drainCommitted=true;''',1)
s=s.replace('if(drainCommitted){ball.vx*=0.90;ball.vy=Math.max(ball.vy+0.65,5.2);if(ball.y>1215){loseBall();return}return}',
'''if(drainCommitted){ball.vx*=0.78;ball.vy=Math.max(ball.vy+0.82,6.0);if(ball.y>1215){loseBall();return}return}''',1)

# Update instructions so the intended paddle behavior is clear.
s=s.replace('5️⃣ Open all 4 to trigger <b>HOWIE\'S OUT THE BOX!</b>',
'''5️⃣ Resting paddles catch and feed the ball toward the drain; moving paddles hit hard<br>6️⃣ Open all 4 to trigger <b>HOWIE'S OUT THE BOX!</b>''',1)
s=s.replace('6️⃣ Your <b>nickname</b> can earn a spot in the global Top 5 score or Top 5 OUT TIME',
'''7️⃣ Your <b>nickname</b> can earn a spot in the global Top 5 score or Top 5 OUT TIME''',1)

p.write_text(s)
print('v21 applied')
