from pathlib import Path
p=Path('index.html')
s=p.read_text()
s=s.replace('LAME — Howie Lucas Pinball v55','LAME — Howie Lucas Pinball v56',1)
# State for ramp capture/eject sequence.
old='let missionLevelSeen=0,missionSpinnerHits=0,missionRampHits=0,missionHowieHits=0,missionDoneLevels=new Set(),superJackpotStep=0,superJackpotLit=false;'
new=old+'let rampHoleScored=false,boxEjectFired=false,rampHoleFlashUntil=0,boxEjectFlashUntil=0;'
if old not in s: raise SystemExit('state anchor not found')
s=s.replace(old,new,1)
# Reset sequence when starting any ramp trick.
old='function startTrick(type){if(trickMode||performance.now()<trickCooldown||waiting||inShooter||drainCommitted)return false;trickMode=type;trickStart=performance.now();ball.vx=0;ball.vy=0;sfxHit(1.5);return true}'
new='function startTrick(type){if(trickMode||performance.now()<trickCooldown||waiting||inShooter||drainCommitted)return false;trickMode=type;trickStart=performance.now();if(type==="ramp"){rampHoleScored=false;boxEjectFired=false}ball.vx=0;ball.vy=0;sfxHit(1.5);return true}'
if old not in s: raise SystemExit('startTrick anchor not found')
s=s.replace(old,new,1)
# Replace ramp animation with ramp -> hole -> hold -> box eject.
start=s.find('function runTrickAnimation(){')
end=s.find('function inZone(z){',start)
if start<0 or end<0: raise SystemExit('runTrickAnimation markers not found')
newfun='''function runTrickAnimation(){if(!trickMode)return false;const L=trickLayout(),now=performance.now(),t=now-trickStart;if(trickMode==="ramp"){const R=L.ramp;if(t<920){const p=Math.min(1,t/920);ball.x=cubicPoint(R.s[0],R.c1[0],R.c2[0],R.e[0],p);ball.y=cubicPoint(R.s[1],R.c1[1],R.c2[1],R.e[1],p);cameraY+=(Math.max(0,Math.min(400,ball.y-430))-cameraY)*.22}else if(t<1180){const q=(t-920)/260;ball.x=R.e[0];ball.y=R.e[1]+q*10;if(!rampHoleScored){rampHoleScored=true;rampHoleFlashUntil=now+700;const bonus=50000*(boxOpen===4?2:1);score+=bonus;if(boxOpen===4)howieOutPoints+=bonus;updateHud();openFlapsAndLevels();registerReplayEvent("ramp");sfxBonus();tone(220,.16,"sine",.04,-110);setStatus("🕳️ RAMP HOLE! +"+bonus.toLocaleString()+" • BALL LOCKED...")}}else if(t<2600){ball.x=R.e[0];ball.y=R.e[1]+10;cameraY+=(Math.max(0,Math.min(400,700-430))-cameraY)*.10}else if(t<3260){if(!boxEjectFired){boxEjectFired=true;boxEjectFlashUntil=now+950;sfxLaunch(.72);tone(780,.14,"square",.055,260);setStatus("📦 BOX EJECT! BALL POPPING BACK INTO PLAY!")}const q=(t-2600)/660,u=1-q;const sx=300,sy=760,ex=level%2?205:395,ey=540;ball.x=u*u*sx+2*u*q*300+q*q*ex;ball.y=u*u*sy+2*u*q*610+q*q*ey;cameraY+=(Math.max(0,Math.min(400,ball.y-430))-cameraY)*.28}else{trickMode=null;trickCooldown=now+900;ball.x=level%2?205:395;ball.y=540;ball.vx=level%2?-5.8:5.8;ball.vy=-5.6;momentumTrailUntil=now+900;setStatus("RAMP EJECT COMPLETE • BALL BACK IN PLAY")}}return true}\n'''
s=s[:start]+newfun+s[end:]
# Add visible eject hole to each ramp end.
needle='ctx.save();ctx.translate(S.x,S.y);ctx.rotate(spinnerAngle);'
insert='''ctx.save();const holeHot=now<rampHoleFlashUntil;ctx.shadowBlur=holeHot?34:12;ctx.shadowColor=holeHot?"#fff":"#ff6b2f";ctx.beginPath();ctx.arc(R.e[0],R.e[1]+8,25,0,Math.PI*2);ctx.fillStyle="#050505";ctx.fill();ctx.strokeStyle=holeHot?"#fff":"#d0d7dc";ctx.lineWidth=7;ctx.stroke();ctx.beginPath();ctx.arc(R.e[0],R.e[1]+8,15,0,Math.PI*2);ctx.fillStyle="#000";ctx.fill();ctx.fillStyle=holeHot?"#fff36a":"#ff8a4c";ctx.font="900 11px Impact,Arial Black";ctx.fillText("EJECT HOLE",R.e[0],R.e[1]-26);ctx.restore();\n'''+needle
if needle not in s: raise SystemExit('draw spinner anchor not found')
s=s.replace(needle,insert,1)
# Box flashes during ejection.
s=s.replace('function drawRealBox(bx,by,bw,bh){const lit=boxLit;','function drawRealBox(bx,by,bw,bh){const lit=boxLit||performance.now()<boxEjectFlashUntil;',1)
# Hide captured ball while it is underground / inside the box, reveal during eject animation.
s=s.replace('function drawRealBall(){ctx.save();','function drawRealBall(){if(trickMode==="ramp"&&rampHoleScored&&(performance.now()-trickStart)<2600)return;ctx.save();',1)
# Verify feature presence.
for token in ['LAME — Howie Lucas Pinball v56','EJECT HOLE','RAMP HOLE!','BOX EJECT!','bonus=50000','rampHoleScored','boxEjectFlashUntil']:
    if token not in s: raise SystemExit('missing '+token)
p.write_text(s)
