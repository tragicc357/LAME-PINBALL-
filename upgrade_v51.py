from pathlib import Path
p=Path('index.html')
s=p.read_text()

s=s.replace('LAME — Howie Lucas Pinball v49','LAME — Howie Lucas Pinball v51',1)

# Start-screen ball-count selector.
needle='''<div class="nicknameBox"><label>ENTER YOUR NICKNAME</label><input id="nicknameInput" maxlength="18" placeholder="Your nickname"></div>'''
insert='''<div class="nicknameBox"><label>ENTER YOUR NICKNAME</label><input id="nicknameInput" maxlength="18" placeholder="Your nickname"></div><div class="ballChoice"><label>HOW MANY BALLS CAN BE ACTIVE AT ONCE?</label><select id="ballCountSelect"><option value="1">1 BALL — CLASSIC</option><option value="2">2 BALLS — MULTIBALL</option><option value="3">3 BALLS — TRIPLE MULTIBALL</option></select><small>Each ball must be launched separately. Press LAUNCH again for Ball 2 and Ball 3.</small></div><div class="replaySummary"><b>🏆 ACHIEVEMENTS</b><span id="achievementCount">0/6 UNLOCKED</span></div>'''
if needle not in s: raise SystemExit('nickname target not found')
s=s.replace(needle,insert,1)

# Mission strip under level strip.
needle='''</div><div class="stats"><div><b id="playsStat">0</b><span>GLOBAL PLAYS</span>'''
insert='''</div><div class="missionStrip" id="missionStrip"><div><span>LEVEL MISSION</span><b id="missionTitle">FREE HOWIE</b></div><div class="missionProgress" id="missionProgress">0 / 4 FLAPS</div><div class="jackpotLamp" id="jackpotLamp">SUPER JACKPOT</div></div><div class="stats"><div><b id="playsStat">0</b><span>GLOBAL PLAYS</span>'''
if needle not in s: raise SystemExit('stats target not found')
s=s.replace(needle,insert,1)

# Replay-system styling.
needle='.boxStatus{margin:7px 0;background:#0b0f13;border:2px solid #5a4210;border-radius:10px;padding:7px}'
css='''.ballChoice{background:#090d11;border:2px solid #36516a;border-radius:12px;padding:9px;margin:10px 0}.ballChoice label{display:block;font-size:10px;color:#ffd21f;font-weight:900;margin-bottom:6px}.ballChoice select{width:100%;padding:11px;border-radius:9px;border:2px solid #555;background:#050708;color:#fff;font-size:14px;font-weight:900}.ballChoice small{display:block;color:#9fb0bd;font-size:9px;margin-top:6px}.replaySummary{display:flex;justify-content:space-between;align-items:center;background:#0b1116;border:1px solid #36516a;border-radius:9px;padding:7px 10px;margin:8px 0;color:#70d7ff;font-size:10px}.missionStrip{display:grid;grid-template-columns:1fr auto auto;gap:7px;align-items:center;background:linear-gradient(#111923,#070b0f);border:2px solid #385d79;border-radius:11px;padding:8px 9px;margin:6px 0}.missionStrip span{display:block;color:#87dfff;font-size:8px;font-weight:900;letter-spacing:1px}.missionStrip b{color:#fff;font-size:12px}.missionProgress{color:#ffd21f;font-size:11px;font-weight:1000;text-align:right}.jackpotLamp{border:2px solid #5d4210;border-radius:9px;padding:7px 8px;color:#725d27;background:#17120a;font-size:9px;font-weight:1000;text-align:center}.jackpotLamp.lit{color:#111;background:#ffd21f;border-color:#fff3a0;box-shadow:0 0 22px #ffd21f;animation:flash .35s infinite alternate}.achievementToast{position:fixed;left:50%;top:16%;transform:translateX(-50%);z-index:99999;width:min(88vw,430px);background:linear-gradient(#1b2630,#070a0d);border:3px solid #ffd21f;border-radius:16px;padding:15px;text-align:center;box-shadow:0 0 35px #ffd21f99;color:#fff;font-weight:900;pointer-events:none;opacity:0}.achievementToast.show{animation:achievementPop 2.6s ease both}.achievementToast b{display:block;color:#ffd21f;font-size:22px;font-family:Impact,Arial Black,sans-serif;letter-spacing:1px}@keyframes achievementPop{0%{opacity:0;transform:translate(-50%,-18px) scale(.9)}12%,78%{opacity:1;transform:translate(-50%,0) scale(1)}100%{opacity:0;transform:translate(-50%,-12px) scale(.96)}}'''+needle
if needle not in s: raise SystemExit('box status css target not found')
s=s.replace(needle,css,1)

# Achievement toast markup.
needle='<div class="levelTransition hide" id="levelTransition">'
s=s.replace(needle,'<div class="achievementToast" id="achievementToast"><b>ACHIEVEMENT UNLOCKED!</b><span id="achievementToastText"></span></div>'+needle,1)

# Add replay state after existing howieOutPointsShown declaration.
needle='let howieOutPointsShown=0,scoreShown=0,spinnerGlowUntil=0,targetGlowUntil=0,celebrationUntil=0,comboLightUntil=0;'
repl=needle+'''\nlet selectedActiveBalls=1,extraBallsQueued=0,extraBalls=[],mainBallSuppressed=false,extraLaunchSerial=1,lastAutoExtraLaunch=0;\nlet missionLevelSeen=0,missionSpinnerHits=0,missionRampHits=0,missionHowieHits=0,missionDoneLevels=new Set(),superJackpotStep=0,superJackpotLit=false;\nconst ACH_KEY="lameAchievementsV51";let achievements=(()=>{try{return JSON.parse(localStorage.getItem(ACH_KEY)||"{}")||{}}catch(e){return{}}})();'''
if needle not in s: raise SystemExit('state target not found')
s=s.replace(needle,repl,1)

# Draw secondary balls with the main playfield.
needle='drawRealBall()}function draw(){'
repl='drawRealBall();drawExtraBalls()}function draw(){'
if needle not in s: raise SystemExit('drawWorld tail target not found')
s=s.replace(needle,repl,1)

# Hook trick events.
needle='''function trickAward(name,pts){const now=performance.now();if(now-lastTrickAt<2600)trickCombo++;else trickCombo=1;lastTrickAt=now;const bonus=pts*trickCombo;addScore(bonus,ball.x,ball.y);tone(720+trickCombo*90,.12,"triangle",.04,180);setStatus("🎯 "+name+" • "+bonus.toLocaleString()+" BONUS • COMBO x"+trickCombo)}'''
repl='''function trickAward(name,pts){const now=performance.now();if(now-lastTrickAt<2600)trickCombo++;else trickCombo=1;lastTrickAt=now;const bonus=pts*trickCombo;addScore(bonus,ball.x,ball.y);tone(720+trickCombo*90,.12,"triangle",.04,180);setStatus("🎯 "+name+" • "+bonus.toLocaleString()+" BONUS • COMBO x"+trickCombo);try{const L=trickLayout();if(name.includes(L.ramp.name))registerReplayEvent("ramp");else if(name.includes(L.spinner.name))registerReplayEvent("spinner")}catch(e){}}'''
if needle not in s: raise SystemExit('trickAward target not found')
s=s.replace(needle,repl,1)

# Hook primary Howie hits using timestamp change.
needle='''function hitHowie(){if(boxOpen<4||inShooter)return;'''
repl='''function hitHowie(){const __beforeHowieHit=howieHitAt;if(boxOpen<4||inShooter)return;'''
if needle not in s: raise SystemExit('hitHowie head not found')
s=s.replace(needle,repl,1)
needle='''setStatus("HOWIE BUMPER! +100,000 POINTS • BALL KICKED WITH HIS MOMENTUM")}}}function physics()'''
repl='''setStatus("HOWIE BUMPER! +100,000 POINTS • BALL KICKED WITH HIS MOMENTUM")}}if(howieHitAt!==__beforeHowieHit)registerReplayEvent("howie")}function physics()'''
if needle not in s: raise SystemExit('hitHowie tail not found')
s=s.replace(needle,repl,1)

# Replace loseBall so multiball continues until the last active ball drains.
needle='''async function loseBall(){if(autoPlay)learnComputerFromDrain();sfxDrain();boxOpen=0;updateFlaps();if(currentBall>=3){playing=false;await finishRecord();renderGameOver();document.getElementById("gameOver").classList.remove("hide")}else{currentBall++;resetBall()}}'''
repl='''async function loseBall(){if(activeExtraBallCount()>0){mainBallSuppressed=true;waiting=true;inShooter=true;drainCommitted=false;ball.x=535;ball.y=1265;ball.vx=ball.vy=0;sfxDrain();setStatus("MULTIBALL SAVE — KEEP PLAYING THE BALLS STILL ON THE TABLE!");return}return finishBallTurn()}async function finishBallTurn(){if(autoPlay)learnComputerFromDrain();sfxDrain();boxOpen=0;updateFlaps();extraBalls=[];extraBallsQueued=0;mainBallSuppressed=false;if(currentBall>=3){playing=false;await finishRecord();renderGameOver();document.getElementById("gameOver").classList.remove("hide")}else{currentBall++;resetBall()}}'''
if needle not in s: raise SystemExit('loseBall target not found')
s=s.replace(needle,repl,1)

# Reset replay state for a new game.
needle='score=0;scoreShown=0;howieOutPoints=0;howieOutPointsShown=0;'
repl='score=0;scoreShown=0;howieOutPoints=0;howieOutPointsShown=0;selectedActiveBalls=Math.max(1,Math.min(3,parseInt(document.getElementById("ballCountSelect")?.value||"1",10)||1));extraBallsQueued=selectedActiveBalls-1;extraBalls=[];mainBallSuppressed=false;missionLevelSeen=0;missionDoneLevels=new Set();superJackpotStep=0;superJackpotLit=false;'
if needle not in s: raise SystemExit('start reset target not found')
s=s.replace(needle,repl,1)

# Add replay systems before computer brain declaration.
needle='const COMPUTER_BRAIN_KEY="lameComputerBrainV33";'
block=r'''
const MISSION_NAMES=["FREE HOWIE","SPIN TO WIN","RAMP RUN","HOWIE HUNTER","FINAL ESCAPE SEQUENCE"];
const MISSION_DESC=["OPEN ALL 4 BOX FLAPS","HIT THE LEVEL SPINNER 4 TIMES","COMPLETE THE RAMP 3 TIMES","HIT HOWIE 2 TIMES WHILE HE IS OUT","RAMP → SPINNER → HOWIE TO LIGHT SUPER JACKPOT"];
function saveAchievements(){try{localStorage.setItem(ACH_KEY,JSON.stringify(achievements))}catch(e){}}
function unlockAchievement(id,label){if(achievements[id])return;achievements[id]=Date.now();saveAchievements();const t=document.getElementById("achievementToast"),x=document.getElementById("achievementToastText");if(x)x.textContent=label;if(t){t.classList.remove("show");void t.offsetWidth;t.classList.add("show")}tone(880,.12,"triangle",.05,220);tone(1175,.18,"sine",.04,260,.11);updateAchievementCount()}
function updateAchievementCount(){const el=document.getElementById("achievementCount");if(el)el.textContent=Math.min(6,Object.keys(achievements).length)+"/6 UNLOCKED"}
function missionProgressText(){if(level===1)return boxOpen+" / 4 FLAPS";if(level===2)return missionSpinnerHits+" / 4 SPINS";if(level===3)return missionRampHits+" / 3 RAMPS";if(level===4)return missionHowieHits+" / 2 HOWIE HITS";return superJackpotLit?"JACKPOT LIT — HIT HOWIE!":(["RAMP","SPINNER","HOWIE"][superJackpotStep]||"HOWIE")+" NEXT"}
function refreshMissionUI(){const a=document.getElementById("missionTitle"),b=document.getElementById("missionProgress"),j=document.getElementById("jackpotLamp");if(a)a.textContent=MISSION_NAMES[level-1];if(b)b.textContent=missionDoneLevels.has(level)?"MISSION COMPLETE ✓":missionProgressText();if(j)j.classList.toggle("lit",superJackpotLit)}
function resetMissionForLevel(){missionLevelSeen=level;missionSpinnerHits=missionRampHits=missionHowieHits=0;superJackpotStep=0;superJackpotLit=false;refreshMissionUI();setStatus("LEVEL "+level+" MISSION: "+MISSION_DESC[level-1])}
function completeMission(){if(missionDoneLevels.has(level))return;missionDoneLevels.add(level);addScore(250000,300,160);celebrationUntil=performance.now()+1500;sfxBonus();setStatus("MISSION COMPLETE! +250,000 BONUS");if(missionDoneLevels.size>=5)unlockAchievement("missionMaster","MISSION MASTER — COMPLETE ALL 5 LEVEL MISSIONS");refreshMissionUI()}
function awardSuperJackpot(){if(!superJackpotLit)return;superJackpotLit=false;superJackpotStep=0;addScore(1000000,300,220);celebrationUntil=performance.now()+2200;sfxBonus();tone(1320,.25,"square",.05,300,.12);setStatus("🔥 SUPER JACKPOT! +1,000,000 🔥");unlockAchievement("jackpotKing","JACKPOT KING — COLLECT THE SUPER JACKPOT");completeMission();refreshMissionUI()}
function registerReplayEvent(type){if(missionLevelSeen!==level)resetMissionForLevel();if(type==="spinner")missionSpinnerHits++;if(type==="ramp")missionRampHits++;if(type==="howie")missionHowieHits++;if(level===2&&missionSpinnerHits>=4)completeMission();if(level===3&&missionRampHits>=3)completeMission();if(level===4&&missionHowieHits>=2){completeMission();unlockAchievement("howieHunter","HOWIE HUNTER — HIT HOWIE TWICE IN LEVEL 4")}
 if(level===5&&!missionDoneLevels.has(5)){if(type==="ramp"){superJackpotStep=1;setStatus("ESCAPE SEQUENCE: RAMP ✓ — HIT THE SPINNER") }else if(type==="spinner"&&superJackpotStep===1){superJackpotStep=2;setStatus("ESCAPE SEQUENCE: SPINNER ✓ — HIT HOWIE") }else if(type==="howie"&&superJackpotStep===2){superJackpotLit=true;superJackpotStep=3;setStatus("🔥 SUPER JACKPOT LIT! HIT HOWIE AGAIN! 🔥")}else if(type==="howie"&&superJackpotLit){awardSuperJackpot()}}
 refreshMissionUI()}
function activeExtraBallCount(){return extraBalls.reduce((n,b)=>n+(b.active?1:0),0)}
function totalBallsInPlay(){return (mainBallSuppressed||waiting?0:1)+activeExtraBallCount()}
function spawnExtraBall(){if(!playing||transitioning||won||extraBallsQueued<=0)return false;const n=selectedActiveBalls-extraBallsQueued+1;extraBalls.push({id:++extraLaunchSerial,x:535,y:1165,r:11,vx:0,vy:-24.5-level*.55,inShooter:true,active:true,trail:[]});extraBallsQueued--;momentumTrailUntil=performance.now()+650;sfxLaunch(.92);setStatus("MULTIBALL — BALL "+n+" LAUNCHED • "+extraBallsQueued+" STILL READY");if(selectedActiveBalls>=2)unlockAchievement("multiball","MULTIBALL MAYHEM — PLAY WITH MULTIPLE BALLS");if(selectedActiveBalls===3&&extraBallsQueued===0)unlockAchievement("triple","TRIPLE TROUBLE — GET 3 BALLS INTO PLAY");return true}
function extraCircleHit(b,o,boost,points){const dx=b.x-o.x,dy=b.y-o.y,d=Math.hypot(dx,dy),min=b.r+o.r;if(d<min){const nx=dx/(d||1),ny=dy/(d||1),dot=b.vx*nx+b.vy*ny;if(dot<0){b.vx=(b.vx-2*dot*nx)*boost;b.vy=(b.vy-2*dot*ny)*boost;sfxHit(Math.min(2,Math.abs(dot)/5))}b.x=o.x+nx*(min+1);b.y=o.y+ny*(min+1);o.flash=8;addScore(points,b.x,b.y)}}
function extraFlipperHit(b,side,held){const f=flipper(side,held),ax=f.pivot.x,ay=f.pivot.y,bx=f.tip.x,by=f.tip.y,vx=bx-ax,vy=by-ay,wx=b.x-ax,wy=b.y-ay,t=Math.max(0,Math.min(1,(wx*vx+wy*vy)/(vx*vx+vy*vy))),px=ax+t*vx,py=ay+t*vy,dx=b.x-px,dy=b.y-py,d=Math.hypot(dx,dy),min=b.r+24;if(d>=min)return;const nx=dx/(d||1),ny=dy/(d||1);b.x=px+nx*(min+1);b.y=py+ny*(min+1);if(performance.now()<=flipperMotionUntil[side]){sfxFlipper();const dot=b.vx*nx+b.vy*ny;if(dot<0){b.vx-=2.15*dot*nx;b.vy-=2.15*dot*ny}b.vy=Math.min(b.vy,-6)-(10.2+4.8*t);b.vx+=(side==="L"?1:-1)*(1.7+2.8*t)}else{b.vx=b.vx*.28+(side==="L"?1:-1)*(.7+.45*t);b.vy=Math.max(1.1,Math.abs(b.vy)*.2+.4)}}
function updateExtraBalls(){if(!playing||transitioning||won)return;const now=performance.now(),sf=speedFactor(),L=trickLayout();for(const b of extraBalls){if(!b.active)continue;b.vy+=.125*sf;b.x+=b.vx*.88*sf;b.y+=b.vy*.88*sf;b.vx*=.999;b.vy*=.999;if(b.inShooter){if(b.x<507){b.x=507;b.vx=Math.abs(b.vx)*.2}if(b.x>568){b.x=568;b.vx=-Math.abs(b.vx)*.2}if(b.y<135){b.inShooter=false;b.x=492;b.y=138;b.vx=-7.6-level*.3;b.vy=2.1;sfxHit(1.4)}continue}if(b.x<24){b.x=24;b.vx=Math.abs(b.vx)*.92;sfxHit()}if(b.x>576){b.x=576;b.vx=-Math.abs(b.vx)*.92;sfxHit()}if(b.y<25){b.y=25;b.vy=Math.abs(b.vy)*.92;sfxHit()}bumpers.forEach(o=>extraCircleHit(b,o,1.18,o.pts));posts.forEach(o=>extraCircleHit(b,o,1.08,45));extraFlipperHit(b,"L",left);extraFlipperHit(b,"R",right);
 const S=L.spinner,sd=Math.hypot(b.x-S.x,b.y-S.y);if(sd<b.r+S.r){const nx=(b.x-S.x)/(sd||1),ny=(b.y-S.y)/(sd||1),dot=b.vx*nx+b.vy*ny;if(dot<0){b.vx-=2*dot*nx;b.vy-=2*dot*ny}b.vx+=Math.cos(spinnerAngle)*2;b.vy+=Math.sin(spinnerAngle)*2;b.x=S.x+nx*(b.r+S.r+2);b.y=S.y+ny*(b.r+S.r+2);spinnerGlowUntil=now+700;addScore(S.pts,b.x,b.y);registerReplayEvent("spinner")}
 if(boxOpen===4){const h=getHowie(),hd=Math.hypot(b.x-h.x,b.y-h.y);if(hd<b.r+38){const nx=(b.x-h.x)/(hd||1),ny=(b.y-h.y)/(hd||1),dot=b.vx*nx+b.vy*ny;if(dot<0){b.vx-=2.1*dot*nx;b.vy-=2.1*dot*ny}const hm=Math.hypot(h.vx,h.vy)||1;b.vx+=h.vx/hm*5;b.vy+=h.vy/hm*5;b.x=h.x+nx*(b.r+41);b.y=h.y+ny*(b.r+41);score+=100000;howieOutPoints+=100000;updateHud();openFlapsAndLevels();howieFlashUntil=now+240;sfxHit(2.2);registerReplayEvent("howie")}}
 if(b.y>1220){b.active=false;sfxDrain();setStatus("MULTIBALL — ONE BALL DRAINED • "+Math.max(0,totalBallsInPlay()-1)+" STILL IN PLAY");if(mainBallSuppressed&&activeExtraBallCount()===0)finishBallTurn()}}
 if(autoPlay&&extraBallsQueued>0&&now-lastAutoExtraLaunch>1300&&!waiting){lastAutoExtraLaunch=now;spawnExtraBall()}}
function drawExtraBalls(){ctx.save();for(const b of extraBalls){if(!b.active)continue;ctx.shadowBlur=16;ctx.shadowColor="#7ddcff";const g=ctx.createRadialGradient(b.x-4,b.y-5,1,b.x+2,b.y+3,b.r+3);g.addColorStop(0,"#fff");g.addColorStop(.28,"#dff6ff");g.addColorStop(.58,"#7894a6");g.addColorStop(1,"#111820");ctx.fillStyle=g;ctx.beginPath();ctx.arc(b.x,b.y,b.r,0,Math.PI*2);ctx.fill();ctx.strokeStyle="#e8f6ff";ctx.lineWidth=1.4;ctx.stroke()}ctx.restore()}
function updateReplaySystems(){if(missionLevelSeen!==level)resetMissionForLevel();if(level===1&&boxOpen===4&&!missionDoneLevels.has(1)){completeMission();unlockAchievement("outBox","OUT THE BOX — FREE HOWIE") }if(perfectLaunchAwarded)unlockAchievement("perfectLaunch","PERFECT LAUNCH — HIT 100% POWER");updateAchievementCount();refreshMissionUI();const lbx=document.getElementById("launchBtn");if(lbx&&!waiting&&extraBallsQueued>0)lbx.innerHTML="LAUNCH<br>BALL "+(selectedActiveBalls-extraBallsQueued+1);else if(lbx&&!waiting&&selectedActiveBalls>1)lbx.innerHTML="MULTIBALL<br>ACTIVE";}
'''+needle
if needle not in s: raise SystemExit('computer brain marker not found')
s=s.replace(needle,block,1)

# Run extra-ball physics and replay UI every frame.
needle='''function loop(){computerControl();physics();updateLiveScoreCounter();draw();if(boxOpen===4&&playing)outEl.textContent=fmt(outMs());requestAnimationFrame(loop)}'''
repl='''function loop(){computerControl();physics();updateExtraBalls();updateReplaySystems();updateLiveScoreCounter();draw();if(boxOpen===4&&playing)outEl.textContent=fmt(outMs());requestAnimationFrame(loop)}'''
if needle not in s: raise SystemExit('loop target not found')
s=s.replace(needle,repl,1)

# Each additional press launches only one queued ball.
needle='''lb.onpointercancel=releaseCharge;'''
repl='''lb.onpointercancel=releaseCharge;lb.addEventListener("pointerup",()=>{if(playing&&!waiting&&extraBallsQueued>0)spawnExtraBall()});'''
if needle not in s: raise SystemExit('launch binding target not found')
s=s.replace(needle,repl,1)

# Start screen instructions mention new replay systems.
needle='''8. Beat Level 5 to win'''
repl='''8. Complete the unique mission on every level<br>9. Build the Level 5 escape sequence to light the <b>SUPER JACKPOT</b><br>10. Choose up to <b>3 active balls</b> — each additional ball needs another press of LAUNCH<br>11. Achievements stay unlocked on this device so you have something new to chase every game<br>12. Beat Level 5 to win'''
if needle not in s: raise SystemExit('howto target not found')
s=s.replace(needle,repl,1)

# Initial UI.
needle='nicknameInput.value=playerName;applyLayout();updateHud();loadStats();loop();'
repl='nicknameInput.value=playerName;updateAchievementCount();applyLayout();updateHud();refreshMissionUI();loadStats();loop();'
if needle not in s: raise SystemExit('startup target not found')
s=s.replace(needle,repl,1)

# Sanity checks.
for token in ['ballCountSelect','MISSION_NAMES','spawnExtraBall','SUPER JACKPOT','updateExtraBalls','achievementCount','LAME — Howie Lucas Pinball v51']:
    if token not in s: raise SystemExit('missing '+token)
p.write_text(s)
print('v51 replay update patched successfully')
