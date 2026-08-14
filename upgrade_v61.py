from pathlib import Path
p=Path('index.html')
s=p.read_text()
orig=s
s=s.replace('LAME — Howie Lucas Pinball v60','LAME — Howie Lucas Pinball v61',1)

# Insert hole/vortex system before point popup system.
needle='let pointPopups=[];'
insert=r'''let holeCapture=null;
function levelCaptureHoles(){return [
[{x:115,y:520,r:25},{x:300,y:405,r:25},{x:455,y:635,r:25}],
[{x:150,y:610,r:25},{x:330,y:500,r:25},{x:455,y:345,r:25}],
[{x:110,y:390,r:25},{x:300,y:560,r:25},{x:470,y:720,r:25}],
[{x:145,y:700,r:25},{x:330,y:390,r:25},{x:465,y:560,r:25}],
[{x:125,y:590,r:25},{x:300,y:430,r:25},{x:465,y:690,r:25}]
][Math.max(0,Math.min(4,level-1))]}
function levelVortexHoles(){const ys=[[330,770],[430,690],[520,300],[620,430],[350,760]][Math.max(0,Math.min(4,level-1))];return[{x:42,y:ys[0],r:29,side:-1},{x:558,y:ys[1],r:29,side:1}]}
function captureAward(x,y,label){const bonus=50000*(boxOpen===4?2:1);score+=bonus;showPointPopup(bonus,x,y);if(boxOpen===4)howieOutPoints+=bonus;updateHud();openFlapsAndLevels();sfxBonus();tone(230,.16,'sine',.045,-120);setStatus(label+' +'+bonus.toLocaleString()+' • BALL SWALLOWED...');return bonus}
function beginHoleCapture(kind,h){if(holeCapture||waiting||inShooter||drainCommitted||transitioning||trickMode)return false;holeCapture={kind,x:h.x,y:h.y,start:performance.now(),bonus:captureAward(h.x,h.y,kind==='VORTEX'?'🌀 VORTEX HOLE!':'🕳️ TABLE HOLE!')};ball.vx=0;ball.vy=0;momentumTrailUntil=0;ballTrail=[];actionFeedback(kind==='VORTEX'?'VORTEX!':'HOLE!','#7ee8ff',520);return true}
function applyVortexAndHoleCapture(){if(holeCapture||waiting||inShooter||drainCommitted||transitioning||trickMode)return !!holeCapture;for(const h of levelCaptureHoles()){const d=Math.hypot(ball.x-h.x,ball.y-h.y);if(d<h.r+ball.r*.55){beginHoleCapture('HOLE',h);return true}}for(const v of levelVortexHoles()){const dx=v.x-ball.x,dy=v.y-ball.y,d=Math.hypot(dx,dy);if(d<105&&d>1){const pull=(1-d/105)*.48;ball.vx+=dx/d*pull;ball.vy+=dy/d*pull}if(d<v.r+ball.r*.45){beginHoleCapture('VORTEX',v);return true}}return false}
function runHoleCapture(){if(!holeCapture)return false;const now=performance.now(),t=now-holeCapture.start,h=holeCapture;if(t<720){const q=t/720,ang=q*Math.PI*5,r=(1-q)*34;ball.x=h.x+Math.cos(ang)*r;ball.y=h.y+Math.sin(ang)*r;cameraY+=(Math.max(0,Math.min(WORLD_H-VIEW_H,ball.y-430))-cameraY)*.24}else if(t<2050){ball.x=h.x;ball.y=h.y}else if(t<2780){if(t<2120){boxEjectFlashUntil=now+900;sfxLaunch(.72);tone(820,.13,'square',.05,230);setStatus('📦 BOX EJECT — BALL POPPING BACK INTO PLAY!')}const q=(t-2050)/730,u=1-q,sx=300,sy=760,ex=level%2?220:380,ey=535;ball.x=u*u*sx+2*u*q*300+q*q*ex;ball.y=u*u*sy+2*u*q*610+q*q*ey;cameraY+=(Math.max(0,Math.min(WORLD_H-VIEW_H,ball.y-430))-cameraY)*.30}else{holeCapture=null;ball.x=level%2?220:380;ball.y=535;ball.vx=level%2?-6.0:6.0;ball.vy=-6.4;momentumTrailUntil=now+950;setStatus('BOX EJECT COMPLETE • BALL BACK IN PLAY')}return true}
function drawCaptureHoles(){const now=performance.now();ctx.save();ctx.textAlign='center';for(const h of levelCaptureHoles()){const hot=holeCapture&&holeCapture.kind==='HOLE'&&Math.hypot(holeCapture.x-h.x,holeCapture.y-h.y)<2;ctx.shadowBlur=hot?34:12;ctx.shadowColor=hot?'#fff':'#55d9ff';ctx.beginPath();ctx.arc(h.x,h.y,h.r+6,0,Math.PI*2);ctx.fillStyle=chromeGrad(h.x-h.r,h.y-h.r,h.x+h.r,h.y+h.r);ctx.fill();ctx.beginPath();ctx.arc(h.x,h.y,h.r,0,Math.PI*2);const g=ctx.createRadialGradient(h.x-7,h.y-8,2,h.x,h.y,h.r);g.addColorStop(0,'#18222a');g.addColorStop(.45,'#030405');g.addColorStop(1,'#000');ctx.fillStyle=g;ctx.fill();ctx.strokeStyle=hot?'#fff':'#73e5ff';ctx.lineWidth=3;ctx.stroke();ctx.fillStyle='#ffd21f';ctx.font='900 11px Impact,Arial Black';ctx.fillText('50K',h.x,h.y+4)}for(const v of levelVortexHoles()){const a=now/180*(v.side||1),hot=holeCapture&&holeCapture.kind==='VORTEX'&&Math.hypot(holeCapture.x-v.x,holeCapture.y-v.y)<2;ctx.save();ctx.translate(v.x,v.y);ctx.shadowBlur=hot?42:24;ctx.shadowColor=hot?'#fff':'#7b5cff';for(let k=0;k<4;k++){ctx.beginPath();ctx.arc(0,0,v.r-k*6,a+k*.75,a+Math.PI*1.45+k*.75);ctx.strokeStyle=k%2?'#6de7ff':'#8f5cff';ctx.lineWidth=4;ctx.stroke()}ctx.beginPath();ctx.arc(0,0,10,0,Math.PI*2);ctx.fillStyle='#000';ctx.fill();ctx.restore();ctx.fillStyle='#9beaff';ctx.font='900 10px Impact,Arial Black';ctx.fillText('VORTEX',v.x,v.y-v.r-10)}ctx.restore()}
'''
if needle not in s: raise SystemExit('point popup insertion target missing')
s=s.replace(needle,insert+needle,1)

# Make hole capture run before other motion systems.
old='function physics(){if(runLaunchRail())return;'
new='function physics(){if(runHoleCapture())return;if(runLaunchRail())return;'
if old not in s: raise SystemExit('physics entry target missing')
s=s.replace(old,new,1)

# Test capture / vortex pull during normal physics integration.
old='capSpeed();if(level===4&&performance.now()<launchGraceUntil&&!inShooter){'
new='capSpeed();if(applyVortexAndHoleCapture())return;if(level===4&&performance.now()<launchGraceUntil&&!inShooter){'
if old not in s: raise SystemExit('physics integration target missing')
s=s.replace(old,new,1)

# Draw the three holes and the two edge vortexes on every level.
old='drawLaunchLoopRail();drawTrickFeatures();'
new='drawLaunchLoopRail();drawCaptureHoles();drawTrickFeatures();'
if old not in s: raise SystemExit('draw feature target missing')
s=s.replace(old,new,1)

# Keep the captured ball hidden during the hold portion, like the ramp eject hole.
old='function drawRealBall(){if(trickMode==="ramp"&&rampHoleScored&&(performance.now()-trickStart)<2600)return;'
new='function drawRealBall(){if(holeCapture&&(performance.now()-holeCapture.start)>=720&&(performance.now()-holeCapture.start)<2050)return;if(trickMode==="ramp"&&rampHoleScored&&(performance.now()-trickStart)<2600)return;'
if old not in s: raise SystemExit('drawRealBall target missing')
s=s.replace(old,new,1)

# Clear any capture state at new ball/game boundaries.
s=s.replace('launchRailActive=false;launchGraceUntil=0;', 'launchRailActive=false;holeCapture=null;launchGraceUntil=0;',1)
s=s.replace('score=0;scoreShown=0;pointPopups=[];', 'score=0;scoreShown=0;pointPopups=[];holeCapture=null;',1)

# Update instructions with the new mechanic.
s=s.replace('12. Beat Level 5 to win', '12. Each level has <b>3 capture holes</b> plus <b>edge vortex holes</b> — entering one awards 50K and ejects the ball from the box<br>13. Beat Level 5 to win',1)

if s==orig: raise SystemExit('no changes applied')
p.write_text(s)
print('v61 hole + vortex upgrade applied')
