from pathlib import Path
p=Path('index.html')
s=p.read_text()
orig=s
s=s.replace('LAME — Howie Lucas Pinball v61','LAME — Howie Lucas Pinball v62',1)

# Fixed exterior vortex positions: upper-left above the playfield and lower-right below launcher.
old="function levelVortexHoles(){const ys=[[330,770],[430,690],[520,300],[620,430],[350,760]][Math.max(0,Math.min(4,level-1))];return[{x:42,y:ys[0],r:29,side:-1},{x:558,y:ys[1],r:29,side:1}]}"
new="function levelVortexHoles(){return[{x:28,y:135,r:31,side:-1,label:'ESCAPE VORTEX'},{x:572,y:1258,r:31,side:1,label:'BONUS VORTEX'}]}"
if old not in s: raise SystemExit('old vortex layout target missing')
s=s.replace(old,new,1)

# Give exterior vortexes a stronger rescue pull so balls cannot remain trapped in dead exterior areas.
old="if(d<105&&d>1){const pull=(1-d/105)*.48;ball.vx+=dx/d*pull;ball.vy+=dy/d*pull}if(d<v.r+ball.r*.45){beginHoleCapture('VORTEX',v);return true}"
new="if(d<150&&d>1){const pull=(1-d/150)*.92+.10;ball.vx+=dx/d*pull;ball.vy+=dy/d*pull}if(d<v.r+ball.r*.72){beginHoleCapture('VORTEX',v);return true}"
if old not in s: raise SystemExit('vortex pull target missing')
s=s.replace(old,new,1)

# Add explicit rescue zones for the two known exterior stuck areas.
old="function applyVortexAndHoleCapture(){if(holeCapture||waiting||inShooter||drainCommitted||transitioning||trickMode)return !!holeCapture;for(const h of levelCaptureHoles())"
new="function applyVortexAndHoleCapture(){if(holeCapture||waiting||inShooter||drainCommitted||transitioning||trickMode)return !!holeCapture;const exterior=levelVortexHoles();if(ball.y<185&&ball.x<120){beginHoleCapture('VORTEX',exterior[0]);return true}if(ball.y>1185&&ball.x>485){beginHoleCapture('VORTEX',exterior[1]);return true}for(const h of levelCaptureHoles())"
if old not in s: raise SystemExit('vortex rescue zone target missing')
s=s.replace(old,new,1)

# Add a true 3-ball bonus multiball burst from the box after a vortex rescue.
needle="function runHoleCapture(){"
insert=r'''let bonusBallFlashUntil=0;
function awardVortexBonusBalls(){
  const activeNow=totalBallsInPlay();
  const add=Math.max(0,Math.min(2,3-activeNow));
  for(let i=0;i<add;i++){
    const dir=i===0?-1:1;
    extraBalls.push({id:++extraLaunchSerial,x:300+dir*18,y:735,r:11,vx:dir*(5.8+level*.25),vy:-8.8-level*.32,inShooter:false,active:true,trail:[]});
  }
  selectedActiveBalls=Math.max(selectedActiveBalls,3);
  extraBallsQueued=0;
  bonusBallFlashUntil=performance.now()+2600;
  celebrationUntil=performance.now()+1800;
  momentumTrailUntil=performance.now()+1000;
  unlockAchievement('multiball','MULTIBALL MAYHEM — PLAY WITH MULTIPLE BALLS');
  unlockAchievement('triple','TRIPLE TROUBLE — GET 3 BALLS INTO PLAY');
  sfxBonus();tone(1040,.14,'triangle',.055,330);setTimeout(()=>tone(1320,.16,'triangle',.05,280),90);
  setStatus('🔥 BONUS BALLS! NOW YOU’RE PLAYING WITH 3 BALLS AT ONCE! 🔥');
}
function drawBonusBallFlash(){
  const now=performance.now();if(now>=bonusBallFlashUntil)return;
  const pulse=.45+.55*Math.abs(Math.sin(now/90));
  ctx.save();ctx.globalAlpha=.10+.13*pulse;ctx.fillStyle=pulse>.65?'#ffffff':'#48b9ff';ctx.fillRect(0,cameraY,W,VIEW_H);ctx.globalAlpha=1;
  ctx.textAlign='center';ctx.shadowBlur=28;ctx.shadowColor='#48b9ff';ctx.fillStyle='#fff';ctx.font='900 38px Impact,Arial Black,Arial';ctx.fillText('BONUS BALLS!',W/2,cameraY+205);
  ctx.fillStyle='#ffd21f';ctx.font='900 24px Impact,Arial Black,Arial';ctx.fillText('NOW YOU’RE PLAYING WITH 3 BALLS!',W/2,cameraY+246);ctx.restore();
}
'''
if needle not in s: raise SystemExit('runHoleCapture insertion target missing')
s=s.replace(needle,insert+needle,1)

# Trigger bonus balls once, only for vortex captures, after the captured ball ejects.
old="}else{holeCapture=null;ball.x=level%2?220:380;ball.y=535;ball.vx=level%2?-6.0:6.0;ball.vy=-6.4;momentumTrailUntil=now+950;setStatus('BOX EJECT COMPLETE • BALL BACK IN PLAY')}return true}"
new="}else{const wasVortex=holeCapture.kind==='VORTEX';holeCapture=null;ball.x=level%2?220:380;ball.y=535;ball.vx=level%2?-6.0:6.0;ball.vy=-6.4;momentumTrailUntil=now+950;if(wasVortex)awardVortexBonusBalls();else setStatus('BOX EJECT COMPLETE • BALL BACK IN PLAY')}return true}"
if old not in s: raise SystemExit('hole capture eject target missing')
s=s.replace(old,new,1)

# Draw exterior vortexes with labels, without crowding the main playfield.
old="ctx.fillStyle='#9beaff';ctx.font='900 10px Impact,Arial Black';ctx.fillText('VORTEX',v.x,v.y-v.r-10)}ctx.restore()}"
new="ctx.fillStyle='#9beaff';ctx.font='900 10px Impact,Arial Black';ctx.fillText(v.label||'VORTEX',Math.max(56,Math.min(544,v.x)),v.y-v.r-10)}ctx.restore()}"
if old not in s: raise SystemExit('vortex label target missing')
s=s.replace(old,new,1)

# Flash the bonus-ball message in world coordinates above normal play objects.
old="drawRealBall();drawExtraBalls();drawPointPopups()}"
new="drawRealBall();drawExtraBalls();drawPointPopups();drawBonusBallFlash()}"
if old not in s: raise SystemExit('bonus flash draw target missing')
s=s.replace(old,new,1)

# Update the instructions for the revised exterior-vortex mechanic.
old='12. Each level has <b>3 capture holes</b> plus <b>edge vortex holes</b> — entering one awards 50K and ejects the ball from the box<br>13. Beat Level 5 to win'
new='12. Each level has <b>3 capture holes</b>. Two <b>exterior rescue vortexes</b> sit outside the walls — upper-left and below the launcher. A vortex swallows a trapped ball, ejects it from the box, and triggers <b>2 BONUS BALLS</b> for 3-ball multiball<br>13. Beat Level 5 to win'
if old in s:s=s.replace(old,new,1)

if s==orig: raise SystemExit('no changes applied')
p.write_text(s)
print('v62 exterior vortex rescue + bonus multiball applied')
# trigger
