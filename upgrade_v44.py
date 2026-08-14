from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()

s=s.replace('LAME — Howie Lucas Pinball v43','LAME — Howie Lucas Pinball v44',1)

# Reduce ordinary playfield clutter and easy scoring: 4 bumpers, 2 lamps per level.
old_apply='''function applyLayout(){const q=layouts[level-1];bumpers=q.b.map((v,i)=>({x:v[0],y:v[1],r:v[2],label:labels[i],pts:pts[i],flash:0}));posts=q.p.map(v=>({x:v[0],y:v[1],r:17}));lamps=q.l.map((v,i)=>({x:v[0],y:v[1],label:["G","E","T","OUT"][i],on:false}))}'''
new_apply='''function applyLayout(){const q=layouts[level-1],keep=[0,2,4,5];bumpers=q.b.filter((_,i)=>keep.includes(i)).map((v,j)=>({x:v[0],y:v[1],r:v[2],label:["LAME","HOWIE","FREE","OUT"][j],pts:[650,850,1100,1400][j],flash:0}));posts=q.p.map(v=>({x:v[0],y:v[1],r:17}));lamps=q.l.filter((_,i)=>i===0||i===3).map((v,i)=>({x:v[0],y:v[1],label:i===0?"GET":"OUT",on:false}))}'''
if old_apply not in s:
    raise SystemExit('applyLayout target not found')
s=s.replace(old_apply,new_apply,1)

# Update the start-screen description to match the sparse feature philosophy.
s=s.replace('7. Hit the <b>FULL LOOP</b>, <b>SKY RAMP</b>, <b>SPINNER</b> and <b>TRICK BANK</b> for huge bonus points',
'''7. Each level has only <b>2 spaced-out feature shots</b>: a unique ramp and a unique spinner''',1)

# Remove the fixed Howie-out points panel over the box.
pat=r'if\(boxOpen===4\)\{ctx\.save\(\);ctx\.fillStyle="rgba\(0,0,0,\.90\)";.*?ctx\.restore\(\)\}\s*drawHowie\(\);'
s,n=re.subn(pat,'drawHowie();',s,count=1,flags=re.S)
if n!=1:
    raise SystemExit(f'fixed Howie panel removal failed: {n}')

# Make the Howie-out meter travel directly under Howie.
pat=r'function drawHowie\(\)\{.*?\}let howieOutPointsShown=0,spinnerGlowUntil=0,targetGlowUntil=0;'
new_howie=r'''function drawHowie(){if(boxOpen<4)return;const h=getHowie(),lit=performance.now()<howieFlashUntil;ctx.save();ctx.translate(h.x,h.y);if(lit){ctx.shadowBlur=38;ctx.shadowColor="#67c8ff";ctx.fillStyle="rgba(255,255,255,.28)";ctx.beginPath();ctx.arc(0,4,58,0,Math.PI*2);ctx.fill()}ctx.strokeStyle=lit?"#fff":"#111";ctx.fillStyle="#7b4826";ctx.lineWidth=lit?10:7;ctx.beginPath();ctx.arc(0,-48,17,0,Math.PI*2);ctx.fill();ctx.stroke();ctx.fillStyle="#111";ctx.fillRect(-20,-28,40,58);ctx.strokeStyle="#111";ctx.beginPath();ctx.moveTo(-15,-15);ctx.lineTo(-38,5);ctx.moveTo(15,-15);ctx.lineTo(38,5);ctx.moveTo(-10,30);ctx.lineTo(-28,62);ctx.moveTo(10,30);ctx.lineTo(28,62);ctx.stroke();ctx.shadowBlur=14;ctx.shadowColor="#55bfff";ctx.fillStyle="rgba(0,0,0,.88)";ctx.strokeStyle="#6ec8ff";ctx.lineWidth=3;ctx.fillRect(-105,76,210,66);ctx.strokeRect(-105,76,210,66);ctx.shadowBlur=0;ctx.textAlign="center";ctx.fillStyle="#fff";ctx.font="900 14px Impact,Arial Black,Arial";ctx.fillText("HOWIE OUT • DOUBLE POINTS",0,99,196);ctx.fillStyle="#ffd21f";ctx.font="900 22px Impact,Arial Black,Arial";ctx.fillText("+"+Math.floor(howieOutPointsShown).toLocaleString()+" PTS",0,128,196);ctx.restore()}let howieOutPointsShown=0,spinnerGlowUntil=0,targetGlowUntil=0;'''
s,n=re.subn(pat,new_howie,s,count=1,flags=re.S)
if n!=1:
    raise SystemExit(f'drawHowie replacement failed: {n}')

# Replace the crowded four-feature trick system with exactly one unique ramp + one unique spinner per level.
start=s.find('function trickLayout(){const layouts=[')
end=s.find('function launchRailPoint(t){',start)
if start<0 or end<0:
    raise SystemExit('trick system boundaries not found')

sparse='''function trickLayout(){const levels=[
{ramp:{name:"SIDEWINDER RAIL",s:[88,965],c1:[52,790],c2:[70,510],e:[155,345],entry:[42,145,900,1015],pts:52000,color:"#38d7ff"},spinner:{name:"FOUR-BLADE",x:470,y:895,r:40,blades:4,pts:6500,color:"#ff60db"}},
{ramp:{name:"WAVE RUNNER",s:[485,965],c1:[548,800],c2:[535,500],e:[430,345],entry:[430,550,900,1015],pts:58000,color:"#ffd34d"},spinner:{name:"HALO WHEEL",x:115,y:885,r:42,blades:6,pts:7200,color:"#7aff8d"}},
{ramp:{name:"U-TURN RAIL",s:[92,950],c1:[42,730],c2:[175,540],e:[92,360],entry:[40,150,885,1010],pts:64000,color:"#a97cff"},spinner:{name:"TWIN BAR",x:475,y:880,r:44,blades:2,pts:8000,color:"#ff9250"}},
{ramp:{name:"SWITCHBACK",s:[482,950],c1:[545,760],c2:[410,540],e:[505,355],entry:[430,550,885,1010],pts:70000,color:"#4fffe5"},spinner:{name:"STAR SPINNER",x:115,y:875,r:44,blades:5,pts:9000,color:"#ffe95c"}},
{ramp:{name:"FINAL CORKSCREW",s:[92,955],c1:[35,740],c2:[210,520],e:[110,325],entry:[38,150,890,1015],pts:80000,color:"#ff5f76"},spinner:{name:"ROTOR SIX",x:475,y:875,r:46,blades:6,pts:11000,color:"#6db8ff"}}
];return levels[Math.max(0,Math.min(4,level-1))]}
function trickAward(name,pts){const now=performance.now();if(now-lastTrickAt<2600)trickCombo++;else trickCombo=1;lastTrickAt=now;const bonus=pts*trickCombo;addScore(bonus,ball.x,ball.y);tone(720+trickCombo*90,.12,"triangle",.04,180);setStatus("🎯 "+name+" • "+bonus.toLocaleString()+" BONUS • COMBO x"+trickCombo)}
function startTrick(type){if(trickMode||performance.now()<trickCooldown||waiting||inShooter||drainCommitted)return false;trickMode=type;trickStart=performance.now();ball.vx=0;ball.vy=0;sfxHit(1.5);return true}
function cubicPoint(a,b,c,d,t){const u=1-t;return u*u*u*a+3*u*u*t*b+3*u*t*t*c+t*t*t*d}
function runTrickAnimation(){if(!trickMode)return false;const L=trickLayout(),now=performance.now(),t=now-trickStart;if(trickMode==="ramp"){const p=Math.min(1,t/920),R=L.ramp;ball.x=cubicPoint(R.s[0],R.c1[0],R.c2[0],R.e[0],p);ball.y=cubicPoint(R.s[1],R.c1[1],R.c2[1],R.e[1],p);cameraY+=(Math.max(0,Math.min(400,ball.y-430))-cameraY)*.22;if(p>=1){trickMode=null;trickCooldown=now+850;ball.x=R.e[0];ball.y=R.e[1];ball.vx=R.e[0]<300?5.2:-5.2;ball.vy=4.8;momentumTrailUntil=now+650;trickAward(R.name+" COMPLETE!",R.pts)}}return true}
function inZone(z){return ball.x>z[0]&&ball.x<z[1]&&ball.y>z[2]&&ball.y<z[3]}
function handleTrickShots(){if(!playing||waiting||inShooter||drainCommitted||transitioning||won)return false;const L=trickLayout(),now=performance.now(),R=L.ramp,S=L.spinner;spinnerAngle+=.085;if(now>=trickCooldown&&ball.vy<-2.5&&inZone(R.entry)){if(startTrick("ramp"))return true}const dx=ball.x-S.x,dy=ball.y-S.y,sd=Math.hypot(dx,dy);if(sd<ball.r+S.r&&now>trickCooldown){const nx=dx/(sd||1),ny=dy/(sd||1),dot=ball.vx*nx+ball.vy*ny;if(dot<0){ball.vx-=2.0*dot*nx;ball.vy-=2.0*dot*ny}ball.vx+=Math.cos(spinnerAngle)*2.0;ball.vy+=Math.sin(spinnerAngle)*2.0;ball.x=S.x+nx*(ball.r+S.r+2);ball.y=S.y+ny*(ball.r+S.r+2);trickCooldown=now+520;spinnerGlowUntil=now+800;momentumTrailUntil=now+520;trickAward(S.name,S.pts)}return false}
function drawTrickFeatures(){const L=trickLayout(),R=L.ramp,S=L.spinner,now=performance.now(),rampHot=trickMode==="ramp",spinHot=now<spinnerGlowUntil;ctx.save();ctx.textAlign="center";
ctx.save();ctx.shadowBlur=rampHot?34:10;ctx.shadowColor=rampHot?"#fff":R.color;ctx.strokeStyle="#11161a";ctx.lineWidth=30;ctx.beginPath();ctx.moveTo(R.s[0],R.s[1]);ctx.bezierCurveTo(R.c1[0],R.c1[1],R.c2[0],R.c2[1],R.e[0],R.e[1]);ctx.stroke();ctx.strokeStyle=rampHot?"#fff":chromeGrad(R.s[0],R.s[1],R.e[0],R.e[1]);ctx.lineWidth=18;ctx.stroke();ctx.strokeStyle=R.color;ctx.lineWidth=4;ctx.stroke();ctx.fillStyle=R.color;ctx.font="900 14px Impact,Arial Black";ctx.fillText(R.name+" +"+(R.pts/1000)+"K",R.s[0]+(R.s[0]<300?70:-70),R.s[1]-32);ctx.restore();
ctx.save();ctx.translate(S.x,S.y);ctx.rotate(spinnerAngle);ctx.shadowBlur=spinHot?34:12;ctx.shadowColor=spinHot?"#fff":S.color;ctx.strokeStyle=spinHot?"#fff":S.color;ctx.lineWidth=9;ctx.lineCap="round";for(let i=0;i<S.blades;i++){const a=Math.PI*2*i/S.blades;ctx.beginPath();ctx.moveTo(Math.cos(a)*10,Math.sin(a)*10);ctx.lineTo(Math.cos(a)*S.r,Math.sin(a)*S.r);ctx.stroke()}ctx.beginPath();ctx.arc(0,0,13,0,Math.PI*2);ctx.fillStyle=spinHot?"#fff":"#e9eef2";ctx.fill();ctx.strokeStyle="#202428";ctx.lineWidth=3;ctx.stroke();ctx.restore();ctx.fillStyle=S.color;ctx.font="900 13px Impact,Arial Black";ctx.fillText(S.name+" +"+(S.pts/1000)+"K",S.x,S.y-S.r-20);ctx.restore()}
'''
s=s[:start]+sparse+s[end:]

# Safety checks: no old crowded feature names or target bank code should remain.
for bad in ['FULL LOOP +50K','SKY RAMP +75K','TRICK TARGET ','TARGET BANK COMPLETE']:
    if bad in s:
        raise SystemExit('old crowded feature still present: '+bad)
if 'HOWIE OUT • DOUBLE POINTS' not in s or 'howieOutPointsShown' not in s:
    raise SystemExit('moving Howie meter missing')
if 'SIDEWINDER RAIL' not in s or 'FINAL CORKSCREW' not in s:
    raise SystemExit('sparse level features missing')

p.write_text(s)
print('v44 patched: sparse two-feature boards + moving Howie-out meter')
