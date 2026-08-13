from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
s=re.sub(r'<title>.*?</title>','<title>LAME — Howie Lucas Pinball v14</title>',s,count=1)

# Slightly slower, more controllable launch.
s=s.replace('ball.vy=-(17.5+power*9.3)','ball.vy=-(14.8+power*6.4)',1)
# Slightly calmer shooter exit.
s=s.replace('ball.vx=-(5.8+Math.max(0,(-ball.vy-4))*0.12)','ball.vx=-(4.9+Math.max(0,(-ball.vy-4))*0.09)',1)

# Add a hard gameplay speed cap and flipper hit cooldowns.
s=s.replace('let score=0,currentBall=1,playing=false,waiting=true,left=false,right=false,combo=1,lastHit=0,shake=0,cameraY=400,charging=false,charge=0,chargeDir=1,chargeRAF=0,inShooter=true,boxOpen=0,nextFlapScore=50000,bottomStuckSince=0,outCelebrationUntil=0,outAccumMs=0,outStartedAt=0,wasFullyOpen=false;',
'''let score=0,currentBall=1,playing=false,waiting=true,left=false,right=false,combo=1,lastHit=0,shake=0,cameraY=400,charging=false,charge=0,chargeDir=1,chargeRAF=0,inShooter=true,boxOpen=0,nextFlapScore=50000,bottomStuckSince=0,outCelebrationUntil=0,outAccumMs=0,outStartedAt=0,wasFullyOpen=false;let flipperHitAt={L:0,R:0};''',1)

# Replace flipper contact with a thicker, always-resolving collider. Held flippers impart a reliable upward impulse.
old=re.search(r'function flipper\(side,held\)\{.*?\}function hitFlipper\(side,held\)\{.*?\}(?=function checkLamps)',s,re.S)
if not old: raise SystemExit('flipper block not found')
new='''function flipper(side,held){const pivot=side==="L"?{x:135,y:1085}:{x:465,y:1085},len=150;const angle=side==="L"?(held?-0.62:0.18):(held?Math.PI+0.62:Math.PI-0.18);return{pivot,tip:{x:pivot.x+Math.cos(angle)*len,y:pivot.y+Math.sin(angle)*len}}}
function hitFlipper(side,held){const f=flipper(side,held),ax=f.pivot.x,ay=f.pivot.y,bx=f.tip.x,by=f.tip.y,vx=bx-ax,vy=by-ay,wx=ball.x-ax,wy=ball.y-ay,len2=vx*vx+vy*vy,t=clamp((wx*vx+wy*vy)/len2,0,1),px=ax+t*vx,py=ay+t*vy,dx=ball.x-px,dy=ball.y-py,d=Math.hypot(dx,dy),thick=24,min=ball.r+thick;if(d<min){let nx=dx/(d||1),ny=dy/(d||1);if(Math.abs(d)<.001){nx=0;ny=-1}const dot=ball.vx*nx+ball.vy*ny;ball.x=px+nx*(min+1);ball.y=py+ny*(min+1);if(dot<0){ball.vx-=1.85*dot*nx;ball.vy-=1.85*dot*ny}if(held){const tipPower=5.7+2.7*t;ball.vy=Math.min(ball.vy,-3.2)-tipPower;ball.vx+=(side==="L"?1:-1)*(1.0+2.0*t);const now=performance.now();if(now-flipperHitAt[side]>120){flipperHitAt[side]=now;addScore(35,px,py);spark(px,py,8)}}else if(ball.vy>0){ball.vy=-Math.max(3.2,ball.vy*.72)}capBallSpeed()}}'''
s=s[:old.start()]+new+s[old.end():]

# Add speed cap helper before physics.
marker='function physics(){'
if marker not in s: raise SystemExit('physics not found')
helper='''function capBallSpeed(){const max=14.5,sp=Math.hypot(ball.vx,ball.vy);if(sp>max){const k=max/sp;ball.vx*=k;ball.vy*=k}}'''
s=s.replace(marker,helper+marker,1)

# Tune gravity and per-frame travel, and clamp velocity before and after collisions.
s=s.replace('function physics(){if(!playing||waiting)return;ball.vy+=0.145;ball.x+=ball.vx*0.94;ball.y+=ball.vy*0.94;ball.vx*=0.9995;ball.vy*=0.9995;',
'''function physics(){if(!playing||waiting)return;ball.vy+=0.125;capBallSpeed();ball.x+=ball.vx*0.88;ball.y+=ball.vy*0.88;ball.vx*=0.9988;ball.vy*=0.9988;''',1)
# Ensure bumpers cannot create runaway speed.
s=s.replace('posts.forEach(p=>circleHit(p,1.04,45));hitFlipper("L",left);hitFlipper("R",right);checkLamps();lowerSafety();stuckBallReset()',
'''posts.forEach(p=>circleHit(p,1.04,45));capBallSpeed();hitFlipper("L",left);hitFlipper("R",right);capBallSpeed();checkLamps();lowerSafety();stuckBallReset()''',1)

p.write_text(s)
print('v14 applied')
# trigger
