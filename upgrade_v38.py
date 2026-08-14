from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()

s=s.replace('LAME — Howie Lucas Pinball v37','LAME — Howie Lucas Pinball v38',1)
s=s.replace('LEVEL_GOAL=1000000','LEVEL_GOAL=3000000',1)
s=s.replace('Every <b>1,000,000 points</b> clears a level','Every <b>3,000,000 points</b> clears a level',1)
s=s.replace('NEXT LEVEL: <b id="nextLevelIndicator">2</b>','NEXT LEVEL: <b id="nextLevelIndicator">2</b> • GOAL: <b>3,000,000</b>',1)

# Replace the complete trick-shot engine so every level gets a different, evenly-spaced layout.
start=s.find('function trickAward(')
end=s.find('function chromeGrad(',start)
if start<0 or end<0:
    raise SystemExit('Could not find trick-shot engine block')

block=r'''let howieOutPointsShown=0,spinnerGlowUntil=0,targetGlowUntil=0;
function trickLayout(){const layouts=[
{loop:{x:145,y:365,r:105,entry:[55,220,500,690]},ramp:{s:[435,880],c:[505,575],e:[300,270],entry:[345,505,720,930]},spinner:[315,535],targets:{xs:[225,300,375],y:690},gates:[[92,820],[506,820],[120,970],[480,965]]},
{loop:{x:445,y:385,r:102,entry:[365,545,500,700]},ramp:{s:[155,900],c:[70,590],e:[315,285],entry:[70,245,735,945]},spinner:[205,560],targets:{xs:[330,395,460],y:680},gates:[[95,760],[500,760],[165,1010],[435,1000]]},
{loop:{x:300,y:335,r:112,entry:[215,385,455,620]},ramp:{s:[455,900],c:[315,645],e:[120,365],entry:[365,530,735,945]},spinner:[420,585],targets:{xs:[130,195,260],y:700},gates:[[85,850],[515,850],[115,1030],[485,1030]]},
{loop:{x:155,y:455,r:98,entry:[65,230,575,760]},ramp:{s:[350,900],c:[520,660],e:[430,300],entry:[290,455,750,950]},spinner:[300,595],targets:{xs:[390,450,510],y:700},gates:[[100,780],[500,920],[155,1005],[445,1020]]},
{loop:{x:435,y:450,r:100,entry:[355,535,570,765]},ramp:{s:[170,905],c:[300,610],e:[475,315],entry:[85,260,755,955]},spinner:[155,585],targets:{xs:[265,330,395],y:710},gates:[[95,900],[505,800],[135,1025],[465,1015]]}
];return layouts[Math.max(0,Math.min(4,level-1))]}
function trickAward(name,pts){const now=performance.now();if(now-lastTrickAt<2600)trickCombo++;else trickCombo=1;lastTrickAt=now;const bonus=pts*trickCombo;addScore(bonus,ball.x,ball.y);tone(720+trickCombo*90,.12,"triangle",.04,180);setStatus("🎯 "+name+" • "+bonus.toLocaleString()+" BONUS • TRICK COMBO x"+trickCombo)}
function startTrick(type){if(trickMode||performance.now()<trickCooldown||waiting||inShooter||drainCommitted)return false;trickMode=type;trickStart=performance.now();ball.vx=0;ball.vy=0;sfxHit(1.5);return true}
function quadPoint(a,b,c,t){const u=1-t;return u*u*a+2*u*t*b+t*t*c}
function runTrickAnimation(){if(!trickMode)return false;const L=trickLayout(),now=performance.now(),t=now-trickStart;if(trickMode==="loop"){const p=Math.min(1,t/900),a=Math.PI*.5+Math.PI*2*p;ball.x=L.loop.x+L.loop.r*Math.cos(a);ball.y=L.loop.y+L.loop.r*Math.sin(a);cameraY=Math.max(0,Math.min(400,ball.y-430));if(p>=1){trickMode=null;trickCooldown=now+650;ball.x=L.loop.x;ball.y=L.loop.y+L.loop.r+18;ball.vx=(level%2?6.8:-6.8);ball.vy=-5.8;trickAward("FULL LOOP COMPLETE!",50000)}}else if(trickMode==="ramp"){const p=Math.min(1,t/780);ball.x=quadPoint(L.ramp.s[0],L.ramp.c[0],L.ramp.e[0],p);ball.y=quadPoint(L.ramp.s[1],L.ramp.c[1],L.ramp.e[1],p);cameraY=Math.max(0,Math.min(400,ball.y-430));if(p>=1){trickMode=null;trickCooldown=now+650;ball.x=L.ramp.e[0];ball.y=L.ramp.e[1];ball.vx=(L.ramp.e[0]<300?5.8:-5.8);ball.vy=5.2;trickAward("SKY RAMP COMPLETE!",75000)}}return true}
function inZone(z){return ball.x>z[0]&&ball.x<z[1]&&ball.y>z[2]&&ball.y<z[3]}
function handleTrickShots(){if(!playing||waiting||inShooter||drainCommitted||transitioning||won)return false;const L=trickLayout(),now=performance.now();spinnerAngle+=.12;if(now>=trickCooldown&&ball.vy<-3.2&&inZone(L.loop.entry)){if(startTrick("loop"))return true}if(now>=trickCooldown&&ball.vy<-3&&inZone(L.ramp.entry)){if(startTrick("ramp"))return true}const sx=L.spinner[0],sy=L.spinner[1],sd=Math.hypot(ball.x-sx,ball.y-sy);if(sd<ball.r+45&&now>trickCooldown){const nx=(ball.x-sx)/(sd||1),ny=(ball.y-sy)/(sd||1),dot=ball.vx*nx+ball.vy*ny;if(dot<0){ball.vx-=2.1*dot*nx;ball.vy-=2.1*dot*ny}ball.vx+=Math.cos(spinnerAngle)*2.4;ball.vy+=Math.sin(spinnerAngle)*2.4;ball.x=sx+nx*(ball.r+47);ball.y=sy+ny*(ball.r+47);trickCooldown=now+320;spinnerGlowUntil=now+700;trickAward("SPINNER",7500)}const ty=L.targets.y;for(let i=0;i<3;i++){const x=L.targets.xs[i],dx=ball.x-x,dy=ball.y-ty;if(Math.abs(dx)<24&&Math.abs(dy)<31&&now-trickTargetHits[i]>700){trickTargetHits[i]=now;targetGlowUntil=now+700;ball.vy=-Math.abs(ball.vy)-2.5;ball.vx+=dx>=0?1.8:-1.8;trickAward("TRICK TARGET "+(i+1),12000);if(trickTargetHits.every(v=>now-v<4500))trickAward("TARGET BANK COMPLETE",40000)}}return false}
function drawTrickFeatures(){const L=trickLayout(),now=performance.now(),pulse=.68+.32*Math.sin(now/130),loopHot=trickMode==="loop",rampHot=trickMode==="ramp",spinHot=now<spinnerGlowUntil,targetHot=now<targetGlowUntil;ctx.save();ctx.textAlign="center";
ctx.fillStyle="rgba(2,12,22,.9)";ctx.strokeStyle="#6fe3ff";ctx.lineWidth=4;ctx.shadowBlur=14;ctx.shadowColor="#31c9ff";ctx.fillRect(125,185,350,55);ctx.strokeRect(125,185,350,55);ctx.fillStyle="#fff";ctx.font="900 24px Impact,Arial Black";ctx.fillText("LEVEL "+level+" TRICK SHOTS",300,220);
ctx.shadowBlur=loopHot?38:16;ctx.shadowColor=loopHot?"#ffffff":"#2fc9ff";ctx.strokeStyle="#1d2226";ctx.lineWidth=30;ctx.beginPath();ctx.arc(L.loop.x,L.loop.y,L.loop.r,.42*Math.PI,2.52*Math.PI);ctx.stroke();ctx.strokeStyle=loopHot?"#ffffff":chromeGrad(L.loop.x-L.loop.r,L.loop.y-L.loop.r,L.loop.x+L.loop.r,L.loop.y+L.loop.r);ctx.lineWidth=18;ctx.stroke();ctx.strokeStyle=`rgba(60,210,255,${loopHot?1:pulse})`;ctx.lineWidth=6;ctx.stroke();ctx.fillStyle="#6fe3ff";ctx.font="900 16px Impact";ctx.fillText("FULL LOOP +50K",L.loop.x,L.loop.y-L.loop.r-18);
ctx.shadowBlur=rampHot?38:16;ctx.shadowColor=rampHot?"#ffffff":"#ffd21f";ctx.strokeStyle="#202428";ctx.lineWidth=42;ctx.beginPath();ctx.moveTo(...L.ramp.s);ctx.quadraticCurveTo(...L.ramp.c,...L.ramp.e);ctx.stroke();ctx.strokeStyle=rampHot?"#ffffff":chromeGrad(L.ramp.e[0],L.ramp.e[1],L.ramp.s[0],L.ramp.s[1]);ctx.lineWidth=30;ctx.stroke();ctx.strokeStyle="#ffd21f";ctx.lineWidth=5;ctx.stroke();ctx.fillStyle="#ffd21f";ctx.font="900 16px Impact";ctx.fillText("SKY RAMP +75K",L.ramp.s[0],L.ramp.s[1]-28);
ctx.save();ctx.translate(...L.spinner);ctx.shadowBlur=spinHot?38:20;ctx.shadowColor=spinHot?"#ffffff":"#ff5af7";ctx.rotate(spinnerAngle);ctx.strokeStyle=spinHot?"#fff":"#f7f7f7";ctx.lineWidth=11;ctx.lineCap="round";ctx.beginPath();ctx.moveTo(-43,0);ctx.lineTo(43,0);ctx.stroke();ctx.strokeStyle="#ff56ef";ctx.lineWidth=8;ctx.beginPath();ctx.moveTo(0,-37);ctx.lineTo(0,37);ctx.stroke();ctx.beginPath();ctx.arc(0,0,13,0,Math.PI*2);ctx.fillStyle="#fff";ctx.fill();ctx.restore();ctx.fillStyle="#ff70f2";ctx.font="900 15px Impact";ctx.fillText("SPINNER +7.5K",L.spinner[0],L.spinner[1]-54);
L.targets.xs.forEach((x,i)=>{const hit=now-trickTargetHits[i]<700;ctx.save();ctx.shadowBlur=(hit||targetHot)?32:12;ctx.shadowColor=(hit||targetHot)?"#fff":"#ff8b35";const g=ctx.createLinearGradient(x-22,L.targets.y-30,x+22,L.targets.y+35);g.addColorStop(0,hit?"#fff":"#e8edf1");g.addColorStop(.5,hit?"#ffd21f":"#87939b");g.addColorStop(1,"#171b1e");ctx.fillStyle=g;ctx.strokeStyle=hit?"#fff":"#ff8b35";ctx.lineWidth=4;ctx.fillRect(x-22,L.targets.y-30,44,62);ctx.strokeRect(x-22,L.targets.y-30,44,62);ctx.fillStyle="#111";ctx.font="900 22px Arial";ctx.fillText(String(i+1),x,L.targets.y+8);ctx.restore()});ctx.fillStyle="#ff9b4b";ctx.font="900 13px Impact";ctx.fillText("1 • 2 • 3 = +40K BANK BONUS",L.targets.xs[1],L.targets.y+55);
L.gates.forEach((q,i)=>{ctx.save();ctx.shadowBlur=14;ctx.shadowColor=i%2?"#ffd21f":"#6fe3ff";ctx.fillStyle=chromeGrad(q[0]-14,q[1]-14,q[0]+14,q[1]+14);ctx.strokeStyle=i%2?"#ffd21f":"#6fe3ff";ctx.lineWidth=3;ctx.beginPath();ctx.arc(q[0],q[1],14,0,Math.PI*2);ctx.fill();ctx.stroke();ctx.restore()});ctx.restore()}
'''
s=s[:start]+block+s[end:]

# Animated rolling/spinning-wheel style Howie-out point counter.
s=s.replace('function drawWorld(){','function drawWorld(){if(boxOpen===4){const d=howieOutPoints-howieOutPointsShown;if(Math.abs(d)<1)howieOutPointsShown=howieOutPoints;else howieOutPointsShown+=d*(Math.abs(d)>500000?.045:Math.abs(d)>100000?.06:.09)}',1)
s=s.replace('if(boxOpen===4){howieOutPoints=0;setStatus("HOWIE IS OUT THE BOX! DOUBLE POINTS!")}','if(boxOpen===4){howieOutPoints=0;howieOutPointsShown=0;setStatus("HOWIE IS OUT THE BOX! DOUBLE POINTS!")}',1)
s=s.replace('ctx.fillText("+"+howieOutPoints.toLocaleString()+" POINTS",300,713,410)','ctx.fillText("+"+Math.floor(howieOutPointsShown).toLocaleString()+" POINTS",300,713,410)',1)
s=s.replace('score=0;howieOutPoints=0;','score=0;howieOutPoints=0;howieOutPointsShown=0;',1)

p.write_text(s)
print('v38 patched: 5 unique trick layouts, active glows, 3M level goal, rolling Howie-out counter')
