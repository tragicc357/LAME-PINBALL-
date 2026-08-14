from pathlib import Path
p=Path('index.html')
s=p.read_text()
orig=s
s=s.replace('LAME — Howie Lucas Pinball v62','LAME — Howie Lucas Pinball v63',1)

old="""function levelCaptureHoles(){return [
[{x:115,y:520,r:25},{x:300,y:405,r:25},{x:455,y:635,r:25}],
[{x:150,y:610,r:25},{x:330,y:500,r:25},{x:455,y:345,r:25}],
[{x:110,y:390,r:25},{x:300,y:560,r:25},{x:470,y:720,r:25}],
[{x:145,y:700,r:25},{x:330,y:390,r:25},{x:465,y:560,r:25}],
[{x:125,y:590,r:25},{x:300,y:430,r:25},{x:465,y:690,r:25}]
][Math.max(0,Math.min(4,level-1))]}"""
new="""let captureHoleLevel=0,captureHoleState=[];
const CAPTURE_HOLE_POOLS=[
[[115,520],[300,405],[455,635],[165,720],[390,535],[260,830],[445,455],[125,650]],
[[150,610],[330,500],[455,345],[115,720],[390,690],[250,390],[465,600],[175,455]],
[[110,390],[300,560],[470,720],[155,650],[390,430],[245,785],[455,520],[150,500]],
[[145,700],[330,390],[465,560],[115,510],[385,720],[255,590],[450,440],[175,820]],
[[125,590],[300,430],[465,690],[150,760],[390,540],[245,835],[455,455],[165,500]]
];
function resetCaptureHolesForLevel(){const pool=CAPTURE_HOLE_POOLS[Math.max(0,Math.min(4,level-1))];captureHoleLevel=level;captureHoleState=pool.slice(0,3).map((q,i)=>({id:i,x:q[0],y:q[1],r:25,hits:0,poolIndex:i}))}
function levelCaptureHoles(){if(captureHoleLevel!==level||captureHoleState.length!==3)resetCaptureHolesForLevel();return captureHoleState}
function relocateCaptureHole(id){const holes=levelCaptureHoles(),h=holes.find(q=>q.id===id);if(!h)return;const pool=CAPTURE_HOLE_POOLS[Math.max(0,Math.min(4,level-1))];let next=(h.poolIndex+3)%pool.length,tries=0;while(tries<pool.length){const q=pool[next],blocked=holes.some(o=>o.id!==h.id&&Math.hypot(o.x-q[0],o.y-q[1])<95);if(!blocked){h.x=q[0];h.y=q[1];h.poolIndex=next;h.hits=0;break}next=(next+1)%pool.length;tries++}celebrationUntil=performance.now()+900;actionFeedback('HOLE MOVED!','#73e5ff',700);sfxBonus();setStatus('🕳️ HOLE MOVED! OLD SPOT SEALED • NEW HOLE OPENED')}
"""
if old not in s: raise SystemExit('levelCaptureHoles target missing')
s=s.replace(old,new,1)

old="holeCapture={kind,x:h.x,y:h.y,start:performance.now(),bonus:captureAward(h.x,h.y,kind==='VORTEX'?'🌀 VORTEX HOLE!':'🕳️ TABLE HOLE!')};"
new="holeCapture={kind,x:h.x,y:h.y,holeId:kind==='HOLE'?h.id:null,start:performance.now(),bonus:captureAward(h.x,h.y,kind==='VORTEX'?'🌀 VORTEX HOLE!':'🕳️ TABLE HOLE!')};if(kind==='HOLE')h.hits=(h.hits||0)+1;"
if old not in s: raise SystemExit('holeCapture creation target missing')
s=s.replace(old,new,1)

old="""}else{const wasVortex=holeCapture.kind==='VORTEX';holeCapture=null;ball.x=level%2?220:380;ball.y=535;ball.vx=level%2?-6.0:6.0;ball.vy=-6.4;momentumTrailUntil=now+950;if(wasVortex)awardVortexBonusBalls();else setStatus('BOX EJECT COMPLETE • BALL BACK IN PLAY')}return true}"""
new="""}else{const wasVortex=holeCapture.kind==='VORTEX',usedHoleId=holeCapture.holeId;holeCapture=null;ball.x=level%2?220:380;ball.y=535;ball.vx=level%2?-6.0:6.0;ball.vy=-6.4;momentumTrailUntil=now+950;if(wasVortex)awardVortexBonusBalls();else{const used=levelCaptureHoles().find(q=>q.id===usedHoleId);if(used&&used.hits>=3)relocateCaptureHole(usedHoleId);else setStatus('BOX EJECT COMPLETE • BALL BACK IN PLAY')}}return true}"""
if old not in s: raise SystemExit('capture eject completion target missing')
s=s.replace(old,new,1)

# Show remaining uses visually so players understand the rule.
old="ctx.fillText('50K',h.x,h.y+4)"
new="ctx.fillText('50K',h.x,h.y+1);ctx.fillStyle='#9beaff';ctx.font='900 9px Arial';ctx.fillText((3-(h.hits||0))+' LEFT',h.x,h.y+15)"
if old not in s: raise SystemExit('hole label target missing')
s=s.replace(old,new,1)

# Reset dynamic hole layout on each new level and fresh game.
s=s.replace("level++;currentBall=1;combo=1;boxOpen=0;nextFlapScore=(level-1)*LEVEL_GOAL+FLAP_GOAL;applyLayout();", "level++;currentBall=1;combo=1;boxOpen=0;nextFlapScore=(level-1)*LEVEL_GOAL+FLAP_GOAL;resetCaptureHolesForLevel();applyLayout();",1)
s=s.replace("currentBall=1;level=1;combo=1;playing=true;", "currentBall=1;level=1;combo=1;captureHoleLevel=0;captureHoleState=[];resetCaptureHolesForLevel();playing=true;",1)

old='12. Each level has <b>3 capture holes</b>. Two <b>exterior rescue vortexes</b> sit outside the walls — upper-left and below the launcher. A vortex swallows a trapped ball, ejects it from the box, and triggers <b>2 BONUS BALLS</b> for 3-ball multiball<br>13. Beat Level 5 to win'
new='12. Each level has <b>3 capture holes</b>. Use the same hole 3 times and, after the third box eject, that hole <b>seals and relocates</b> to a new open spot. Two exterior rescue vortexes trigger <b>2 BONUS BALLS</b> for 3-ball multiball<br>13. Beat Level 5 to win'
if old in s:s=s.replace(old,new,1)

if s==orig: raise SystemExit('no changes applied')
p.write_text(s)
print('v63 relocating capture holes applied')
