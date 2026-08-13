from pathlib import Path
p=Path('index.html')
s=p.read_text()

def rep(a,b):
    global s
    if a not in s:
        raise SystemExit('missing target: '+a[:140])
    s=s.replace(a,b,1)

rep('LAME — Howie Lucas Pinball v35','LAME — Howie Lucas Pinball v36')

# Trick-shot state
rep('let score=0,currentBall=1,level=1,playing=false,waiting=true,left=false,right=false,combo=1,lastHit=0,cameraY=400,inShooter=true,boxOpen=0,nextFlapScore=FLAP_GOAL,transitioning=false,won=false,drainCommitted=false,autoPlay=false,computerLaunchAt=0,computerFlipAt=0,computerLastDecision=null,computerLastHitAt=0,howieOutPoints=0;',
    'let score=0,currentBall=1,level=1,playing=false,waiting=true,left=false,right=false,combo=1,lastHit=0,cameraY=400,inShooter=true,boxOpen=0,nextFlapScore=FLAP_GOAL,transitioning=false,won=false,drainCommitted=false,autoPlay=false,computerLaunchAt=0,computerFlipAt=0,computerLastDecision=null,computerLastHitAt=0,howieOutPoints=0,trickMode=null,trickStart=0,trickCooldown=0,trickCombo=0,lastTrickAt=0,spinnerAngle=0,trickTargetHits=[0,0,0];')

helpers=r'''function trickAward(name,pts){const now=performance.now();if(now-lastTrickAt<2600)trickCombo++;else trickCombo=1;lastTrickAt=now;const bonus=pts*trickCombo;addScore(bonus,ball.x,ball.y);tone(720+trickCombo*90,.12,"triangle",.04,180);setStatus("🎯 "+name+" • "+bonus.toLocaleString()+" BONUS • TRICK COMBO x"+trickCombo)}function startTrick(type){if(trickMode||performance.now()<trickCooldown||waiting||inShooter||drainCommitted)return false;trickMode=type;trickStart=performance.now();ball.vx=0;ball.vy=0;sfxHit(1.5);return true}function runTrickAnimation(){if(!trickMode)return false;const now=performance.now(),t=(now-trickStart);if(trickMode==="loop"){const d=900,p=Math.min(1,t/d),a=Math.PI*.5+Math.PI*2*p;ball.x=165+106*Math.cos(a);ball.y=410+106*Math.sin(a);cameraY=Math.max(0,Math.min(400,ball.y-430));if(p>=1){trickMode=null;trickCooldown=now+700;ball.x=165;ball.y=520;ball.vx=6.8;ball.vy=-5.5;trickAward("FULL LOOP",50000)}}else if(trickMode==="ramp"){const d=760,p=Math.min(1,t/d),u=1-p;ball.x=u*u*410+2*u*p*470+p*p*205;ball.y=u*u*770+2*u*p*445+p*p*300;cameraY=Math.max(0,Math.min(400,ball.y-430));if(p>=1){trickMode=null;trickCooldown=now+650;ball.x=205;ball.y=300;ball.vx=-5.8;ball.vy=5.2;trickAward("SKY RAMP",75000)}}return true}function handleTrickShots(){if(!playing||waiting||inShooter||drainCommitted||transitioning||won)return false;const now=performance.now();spinnerAngle+=.12;if(now>=trickCooldown&&ball.vy<-3.4&&ball.x>75&&ball.x<185&&ball.y>520&&ball.y<700){if(startTrick("loop"))return true}if(now>=trickCooldown&&ball.vy<-3.2&&ball.x>355&&ball.x<465&&ball.y>670&&ball.y<835){if(startTrick("ramp"))return true}const sx=302,sy=545,sd=Math.hypot(ball.x-sx,ball.y-sy);if(sd<ball.r+27&&now>trickCooldown){const nx=(ball.x-sx)/(sd||1),ny=(ball.y-sy)/(sd||1),dot=ball.vx*nx+ball.vy*ny;if(dot<0){ball.vx-=2.1*dot*nx;ball.vy-=2.1*dot*ny}ball.vx+=Math.cos(spinnerAngle)*2.2;ball.vy+=Math.sin(spinnerAngle)*2.2;ball.x=sx+nx*(ball.r+29);ball.y=sy+ny*(ball.r+29);trickCooldown=now+320;trickAward("SPINNER",7500)}const tx=[245,302,359],ty=655;for(let i=0;i<3;i++){const dx=ball.x-tx[i],dy=ball.y-ty;if(Math.abs(dx)<21&&Math.abs(dy)<26&&now-trickTargetHits[i]>700){trickTargetHits[i]=now;ball.vy=-Math.abs(ball.vy)-2.5;ball.vx+=dx>=0?1.8:-1.8;trickAward("TRICK TARGET "+(i+1),12000);if(trickTargetHits.every(v=>now-v<4500))trickAward("TARGET BANK COMPLETE",40000)}}return false}function drawTrickFeatures(){ctx.save();ctx.shadowBlur=12;ctx.shadowColor="#58c7ff66";ctx.strokeStyle="#252a2e";ctx.lineWidth=22;ctx.beginPath();ctx.arc(165,410,106,.48*Math.PI,2.48*Math.PI);ctx.stroke();ctx.strokeStyle=chromeGrad(65,300,260,520);ctx.lineWidth=12;ctx.stroke();ctx.fillStyle="#73d8ff";ctx.font="900 17px Impact";ctx.textAlign="center";ctx.shadowBlur=10;ctx.fillText("FULL LOOP +50K",165,282);ctx.shadowBlur=8;ctx.strokeStyle="#222";ctx.lineWidth=28;ctx.beginPath();ctx.moveTo(410,770);ctx.quadraticCurveTo(490,500,205,300);ctx.stroke();ctx.strokeStyle="#c7d7e2";ctx.lineWidth=18;ctx.stroke();ctx.strokeStyle="#64c9ff";ctx.lineWidth=4;ctx.stroke();ctx.fillStyle="#ffd21f";ctx.font="900 16px Impact";ctx.fillText("SKY RAMP +75K",408,735);ctx.save();ctx.translate(302,545);ctx.rotate(spinnerAngle);ctx.strokeStyle="#e9eef2";ctx.lineWidth=8;ctx.lineCap="round";ctx.beginPath();ctx.moveTo(-30,0);ctx.lineTo(30,0);ctx.stroke();ctx.strokeStyle="#ffd21f";ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(0,-24);ctx.lineTo(0,24);ctx.stroke();ctx.beginPath();ctx.arc(0,0,8,0,Math.PI*2);ctx.fillStyle="#fff";ctx.fill();ctx.restore();ctx.fillStyle="#70d7ff";ctx.font="900 12px Arial";ctx.fillText("SPINNER +7.5K",302,505);[245,302,359].forEach((x,i)=>{const g=ctx.createLinearGradient(x-18,630,x+18,682);g.addColorStop(0,"#f8fbff");g.addColorStop(.45,"#707c84");g.addColorStop(1,"#171b1e");ctx.fillStyle=g;ctx.strokeStyle="#ffd21f";ctx.lineWidth=3;ctx.fillRect(x-17,632,34,46);ctx.strokeRect(x-17,632,34,46);ctx.fillStyle="#111";ctx.font="900 16px Arial";ctx.fillText(String(i+1),x,661)});ctx.fillStyle="#ffd21f";ctx.font="900 12px Arial";ctx.fillText("TRICK BANK • COMPLETE ALL 3",302,704);ctx.restore()}'''

if 'function trickAward(' not in s:
    rep('function chromeGrad(',helpers+'function chromeGrad(')

# Draw the new physical-looking features with the rest of the playfield.
rep('bumpers.forEach(drawRealBumper);','drawTrickFeatures();bumpers.forEach(drawRealBumper);')

# Run the trick-shot controller before normal ball physics.
rep('function physics(){','function physics(){if(runTrickAnimation())return;if(handleTrickShots())return;')

# Reset trick state with every new ball/game.
rep('function resetBall(){','function resetBall(){trickMode=null;trickCooldown=performance.now()+350;')
rep('score=0;howieOutPoints=0;currentBall=1;level=1;combo=1;playing=true;','score=0;howieOutPoints=0;trickMode=null;trickCombo=0;lastTrickAt=0;trickTargetHits=[0,0,0];currentBall=1;level=1;combo=1;playing=true;')

p.write_text(s)
print('v36 patched: loop, ramp, spinner, trick target bank, combo bonus scoring')
