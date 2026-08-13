from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
s=re.sub(r'<title>.*?</title>','<title>LAME — Howie Lucas Pinball v16</title>',s,count=1)

# Speed rules: launch fastest, normal while Howie is boxed, faster while Howie is free.
s=s.replace('function capBallSpeed(){const max=inShooter?24:14.5,sp=Math.hypot(ball.vx,ball.vy);if(sp>max){const k=max/sp;ball.vx*=k;ball.vy*=k}}',
'''function capBallSpeed(){const max=inShooter?24:(boxOpen===4?18.5:14.5),sp=Math.hypot(ball.vx,ball.vy);if(sp>max){const k=max/sp;ball.vx*=k;ball.vy*=k}}''',1)

# Add a cooldown so one contact with Howie does not repeatedly trigger every frame.
s=s.replace('let flipperHitAt={L:0,R:0};','let flipperHitAt={L:0,R:0};let howieHitAt=0;',1)

# Give drawing and physics the exact same moving Howie position.
old=re.search(r'function drawHowieRunning\(\)\{.*?\}(?=\nfunction drawWorld)',s,re.S)
if not old: raise SystemExit('Howie drawing block not found')
new='''function getHowiePose(){const t=performance.now()/1000;const minY=cameraY+150,maxY=cameraY+VIEW_H-170;return{x:300+Math.sin(t*1.6)*175,y:clamp(cameraY+VIEW_H*.48+Math.cos(t*1.15)*125,minY,maxY),dir:Math.cos(t*1.6)>=0?1:-1,step:Math.sin(t*10)}}
function hitHowie(){if(boxOpen<4||inShooter)return;const h=getHowiePose(),dx=ball.x-h.x,dy=ball.y-h.y,d=Math.hypot(dx,dy),min=ball.r+42;if(d<min){const now=performance.now();let nx=dx/(d||1),ny=dy/(d||1);if(d<.001){nx=0;ny=-1}ball.x=h.x+nx*(min+2);ball.y=h.y+ny*(min+2);const dot=ball.vx*nx+ball.vy*ny;if(dot<0){ball.vx-=2.05*dot*nx;ball.vy-=2.05*dot*ny}else{ball.vx+=nx*2.2;ball.vy+=ny*2.2}ball.vx+=h.dir*1.8;ball.vy-=1.2;capBallSpeed();if(now-howieHitAt>220){howieHitAt=now;spark(h.x,h.y,18);shake=5;addScore(750,h.x,h.y-55);setStatus("HOWIE DEFLECTED THE BALL!")}}}
function drawHowieRunning(){if(boxOpen<4)return;const h=getHowiePose(),x=h.x,y=h.y,dir=h.dir,step=h.step;ctx.save();ctx.translate(x,y);ctx.scale(dir,1);ctx.lineCap="round";ctx.lineJoin="round";ctx.strokeStyle="#111";ctx.fillStyle="#7b4826";ctx.lineWidth=7;ctx.beginPath();ctx.arc(0,-58,19,0,Math.PI*2);ctx.fill();ctx.strokeStyle="#111";ctx.lineWidth=4;ctx.stroke();ctx.beginPath();ctx.moveTo(-16,-61);ctx.lineTo(-3,-61);ctx.moveTo(3,-61);ctx.lineTo(16,-61);ctx.moveTo(-3,-61);ctx.lineTo(3,-61);ctx.stroke();ctx.fillStyle="#111";ctx.beginPath();ctx.roundRect(-24,-38,48,64,10);ctx.fill();ctx.fillStyle="#fff";ctx.font="900 11px Arial";ctx.textAlign="center";ctx.fillText("HOWIE",0,-3);ctx.strokeStyle="#111";ctx.lineWidth=8;ctx.beginPath();ctx.moveTo(-18,-26);ctx.lineTo(-42,-6-step*10);ctx.moveTo(18,-26);ctx.lineTo(42,4+step*10);ctx.moveTo(-12,25);ctx.lineTo(-30,60+step*12);ctx.moveTo(12,25);ctx.lineTo(30,60-step*12);ctx.stroke();ctx.fillStyle="rgba(255,210,31,.96)";ctx.fillRect(-58,72,116,25);ctx.fillStyle="#111";ctx.font="900 13px Arial";ctx.fillText("HOWIE IS FREE!",0,90);ctx.restore()}'''
s=s[:old.start()]+new+s[old.end():]

# When Howie is out, process him as a moving physical obstacle after flippers.
s=s.replace('hitFlipper("L",left);hitFlipper("R",right);capBallSpeed();checkLamps();',
'''hitFlipper("L",left);hitFlipper("R",right);hitHowie();capBallSpeed();checkLamps();''',1)

p.write_text(s)
print('v16 applied')
