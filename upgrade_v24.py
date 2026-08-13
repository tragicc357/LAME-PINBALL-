from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
s=re.sub(r'<title>.*?</title>','<title>LAME — Howie Lucas Pinball v24</title>',s,count=1)

# HUD: add LEVEL and make room for six cells.
s=s.replace('grid-template-columns:1.15fr .65fr .78fr .78fr 1.05fr','grid-template-columns:1.05fr .62fr .62fr .75fr .75fr 1.05fr',1)
s=s.replace('<div class="hud"><div><b id="score">0</b><span>SCORE</span></div><div><b id="ballText">1/3</b><span>BALL</span></div>', '<div class="hud"><div><b id="score">0</b><span>SCORE</span></div><div><b id="ballText">1/3</b><span>BALL</span></div><div><b id="levelText">1/5</b><span>LEVEL</span></div>',1)

css='''\n.levelTransition{position:fixed;inset:0;z-index:8000;background:rgba(0,0,0,.92);display:flex;align-items:center;justify-content:center;text-align:center;padding:24px}.levelTransition.hide{display:none}.levelCard{width:min(92vw,520px);border:4px solid #ffd21f;border-radius:24px;padding:28px;background:#090909;box-shadow:0 0 50px #ffcc0066}.levelCard h3{font-family:Impact,Arial Black,sans-serif;font-size:64px;color:#ffd21f;margin:0}.levelCard .next{font-size:24px;font-weight:900;margin-top:12px}.levelCard .speed{font-size:34px;font-weight:1000;color:#70d7ff;margin-top:10px}.victoryScreen{position:fixed;inset:0;z-index:9999;background:#000;display:flex;align-items:center;justify-content:center;overflow:hidden}.victoryScreen.hide{display:none}.victoryScreen img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;background:#000}.victoryShade{position:absolute;inset:0;background:linear-gradient(transparent 45%,rgba(0,0,0,.78) 78%,rgba(0,0,0,.94))}.victoryCopy{position:absolute;left:4%;right:4%;bottom:5%;text-align:center}.victoryCopy h2{font-family:Impact,Arial Black,sans-serif;font-size:clamp(38px,9vw,92px);line-height:.95;margin:0;color:#fff;text-shadow:0 0 18px #ff0000,4px 5px #000;animation:victoryFlash .55s infinite alternate}.victoryCopy p{font-size:clamp(18px,4vw,34px);font-weight:1000;color:#ffd21f;margin:12px 0}.victoryCopy button{border:0;border-radius:14px;padding:14px 22px;margin:6px;background:#ffd21f;color:#111;font-weight:1000;font-size:18px}.victoryCopy .fbWin{background:#1877f2;color:#fff}@keyframes victoryFlash{0%{opacity:.35;transform:scale(.98);filter:drop-shadow(0 0 4px #f00)}100%{opacity:1;transform:scale(1.03);filter:drop-shadow(0 0 22px #f00)}}\n'''
s=s.replace('</style>',css+'</style>',1)
s=s.replace('<span>50,000 PTS = OPEN 1</span>','<span>12,000,000 PTS = NEXT LEVEL</span>',1)
start_old=re.search(r'<div class="howto">.*?</div><button id="startBtn">',s,re.S)
if start_old:
    start_new='''<div class="howto">1️⃣ Hold <b>LAUNCH</b> and release to fire<br>2️⃣ Every <b>12,000,000 points</b> clears a level<br>3️⃣ The table pauses and resets before each new level<br>4️⃣ Ball speed increases every level — up to Level 5<br>5️⃣ Beat all 5 levels and <b>HOWIE IS OUT THE BOX!</b><br>6️⃣ Share your score to Facebook so friends can try to beat it<br>7️⃣ Your nickname can still earn a global Top 5 score</div><button id="startBtn">'''
    s=s[:start_old.start()]+start_new+s[start_old.end():]
s=s.replace('>SHARE SCORE</button>','>SHARE SCORE TO FACEBOOK</button>',1)
overlays='''<div class="levelTransition hide" id="levelTransition"><div class="levelCard"><h3 id="levelDone">LEVEL 1 COMPLETE!</h3><div class="next" id="levelNext">GET READY FOR LEVEL 2</div><div class="speed" id="levelSpeed">BALL SPEED 2X</div></div></div><div class="victoryScreen hide" id="victoryScreen"><img src="pinball-table.jpg" alt="Howie Lucas outside the box artwork"><div class="victoryShade"></div><div class="victoryCopy"><h2>CONGRATULATIONS<br>HOWIE IS OUTSIDE THE BOX!</h2><p id="victoryScore">YOU BEAT ALL 5 LEVELS</p><button class="fbWin" id="victoryShare">SHARE SCORE TO FACEBOOK</button><button id="victoryAgain">PLAY AGAIN</button></div></div>\n'''
s=s.replace('<script>',''+overlays+'<script>',1)
state_anchor='let score=0,currentBall=1,playing=false,waiting=true,left=false,right=false,combo=1,lastHit=0,shake=0,cameraY=400,charging=false,charge=0,chargeDir=1,chargeRAF=0,inShooter=true,boxOpen=0,nextFlapScore=50000,bottomStuckSince=0,outCelebrationUntil=0,outAccumMs=0,outStartedAt=0,wasFullyOpen=false;'
if state_anchor not in s: raise SystemExit('state anchor not found')
s=s.replace(state_anchor,state_anchor+'const LEVEL_GOAL=12000000,MAX_LEVEL=5;let level=1,levelTransitioning=false,gameWon=false;',1)
ref_anchor='const scoreEl=document.getElementById("score"),ballEl=document.getElementById("ballText"),multiEl=document.getElementById("multi"),bestEl=document.getElementById("best"),statusEl=document.getElementById("status"),powerFill=document.getElementById("powerFill"),powerPct=document.getElementById("powerPct");'
if ref_anchor in s:
    s=s.replace(ref_anchor,ref_anchor+'const levelTextEl=document.getElementById("levelText"),levelTransitionEl=document.getElementById("levelTransition"),victoryScreen=document.getElementById("victoryScreen");',1)
pat=r'function checkFlapMilestones\(\)\{.*?\}\}\}function addScore'
m=re.search(pat,s,re.S)
if not m: raise SystemExit('milestone block not found')
new='''function levelSpeedFactor(){return Math.pow(2,Math.max(0,level-1))}function checkFlapMilestones(){if(levelTransitioning||gameWon)return;const goal=level*LEVEL_GOAL;if(score>=goal){if(level>=MAX_LEVEL){winGame()}else{advanceLevel()}}}function advanceLevel(){if(levelTransitioning||gameWon)return;levelTransitioning=true;playing=false;waiting=true;ball.vx=ball.vy=0;document.getElementById("levelDone").textContent="LEVEL "+level+" COMPLETE!";document.getElementById("levelNext").textContent="GET READY FOR LEVEL "+(level+1);document.getElementById("levelSpeed").textContent="BALL SPEED "+levelSpeedFactor()*2+"X";levelTransitionEl.classList.remove("hide");sfxBonus();setTimeout(()=>{level++;currentBall=1;combo=1;boxOpen=0;lamps.forEach(l=>l.on=false);updateFlaps();levelTransitionEl.classList.add("hide");playing=true;levelTransitioning=false;resetBall();updateHud();setStatus("LEVEL "+level+" — BALL SPEED "+levelSpeedFactor()+"X");sfxStart()},2300)}async function winGame(){if(gameWon)return;gameWon=true;levelTransitioning=true;playing=false;waiting=true;ball.vx=ball.vy=0;boxOpen=4;updateFlaps();startHowieSiren();sfxFlap(true);sfxBonus();document.getElementById("victoryScore").textContent=(playerName||"PLAYER")+" — "+score.toLocaleString()+" POINTS — ALL 5 LEVELS COMPLETE";victoryScreen.classList.remove("hide");await recordGameFinish(score,currentOutMs())}function addScore'''
s=s[:m.start()]+new+s[m.end():]
s=s.replace('function updateHud(){scoreEl.textContent=score.toLocaleString();ballEl.textContent=currentBall+"/3";', 'function updateHud(){scoreEl.textContent=score.toLocaleString();ballEl.textContent=currentBall+"/3";if(levelTextEl)levelTextEl.textContent=level+"/5";',1)
s=s.replace('score=0;currentBall=1;combo=1;playing=true;boxOpen=0;nextFlapScore=50000;', 'score=0;currentBall=1;combo=1;level=1;levelTransitioning=false;gameWon=false;playing=true;boxOpen=0;nextFlapScore=50000;victoryScreen?.classList.add("hide");levelTransitionEl?.classList.add("hide");',1)
s=s.replace('setStatus("Hold LAUNCH to build momentum");cameraY=400', 'setStatus("LEVEL "+level+" — Hold LAUNCH to build momentum");cameraY=400',1)
old_bg='function drawFittedGraphic(){ctx.save();ctx.fillStyle=boxOpen===4?"#ffffff":"#000000";ctx.fillRect(0,0,W,WORLD_H);ctx.restore()}'
new_bg='''function drawFittedGraphic(){ctx.save();ctx.fillStyle="#000";ctx.fillRect(0,0,W,WORLD_H);if(theme.complete&&theme.naturalWidth){const sc=Math.max(W/theme.naturalWidth,WORLD_H/theme.naturalHeight),dw=theme.naturalWidth*sc,dh=theme.naturalHeight*sc;ctx.globalAlpha=.58;ctx.drawImage(theme,(W-dw)/2,(WORLD_H-dh)/2,dw,dh);ctx.globalAlpha=1;ctx.fillStyle="rgba(0,0,0,.22)";ctx.fillRect(0,0,W,WORLD_H)}ctx.restore()}'''
if old_bg not in s: raise SystemExit('background function not found')
s=s.replace(old_bg,new_bg,1)
pat=r'function physics\(\)\{.*?cameraY\+=\(target-cameraY\)\*0\.09\}'
m=re.search(pat,s,re.S)
if not m: raise SystemExit('physics block not found')
physics='''function physics(){if(!playing||waiting||levelTransitioning)return;const speed=levelSpeedFactor(),steps=Math.max(1,Math.min(16,Math.ceil(speed)));for(let step=0;step<steps;step++){ball.vy+=0.125*speed/steps;capBallSpeed();ball.x+=ball.vx*0.88*speed/steps;ball.y+=ball.vy*0.88*speed/steps;ball.vx*=Math.pow(0.9988,1/steps);ball.vy*=Math.pow(0.9988,1/steps);if(!inShooter&&ball.x>135&&ball.x<465&&ball.y>1148)drainCommitted=true;if(drainCommitted){ball.vx*=0.78;ball.vy=Math.max(ball.vy+0.82,6.0);if(ball.y>1215){loseBall();return}continue}if(inShooter)shooterPhysics();else{if(ball.x<24){ball.x=24;ball.vx=Math.abs(ball.vx)*0.92;sfxContact("wall",Math.abs(ball.vx)/6)}if(ball.x>576){ball.x=576;ball.vx=-Math.abs(ball.vx)*0.92;sfxContact("wall",Math.abs(ball.vx)/6)}if(ball.y<25){ball.y=25;ball.vy=Math.abs(ball.vy)*0.92;sfxContact("metal",Math.abs(ball.vy)/6)}segHit(24,165,120,88,9,1.01,8);segHit(480,88,500,135,9,1.01,8);segHit(35,760,145,875,10,1.02,8);segHit(565,760,455,875,10,1.02,8);bumpers.forEach(b=>circleHit(b,1.14,b.pts));posts.forEach(p=>circleHit(p,1.04,45));capBallSpeed();hitFlipper("L",left);hitFlipper("R",right);if(gameWon)hitHowie();capBallSpeed();checkLamps();lowerSafety();stuckBallReset()}}const target=clamp(ball.y-VIEW_H*0.52,0,WORLD_H-VIEW_H);cameraY+=(target-cameraY)*0.16}'''
s=s[:m.start()]+physics+s[m.end():]
share_pat=r'document\.getElementById\("share"\)\.onclick=async\(\)=>\{.*?\};theme\.onload=draw;'
m=re.search(share_pat,s,re.S)
share_js='''function shareToFacebook(){const url="https://tragicc357.github.io/LAME-PINBALL-/";const text=`${playerName||"I"} scored ${score.toLocaleString()} points and reached Level ${level}/5 on LAME — Howie Lucas Pinball. Think you can beat it?`;const shareUrl="https://www.facebook.com/sharer/sharer.php?u="+encodeURIComponent(url)+"&quote="+encodeURIComponent(text);window.open(shareUrl,"facebook-share","width=680,height=760,noopener,noreferrer")}document.getElementById("share").onclick=shareToFacebook;document.getElementById("victoryShare").onclick=shareToFacebook;document.getElementById("victoryAgain").onclick=()=>{stopHowieSiren();victoryScreen.classList.add("hide");newGame()};theme.onload=draw;'''
if m:
    s=s[:m.start()]+share_js+s[m.end():]
else:
    s=s.replace('theme.onload=draw;',share_js,1)
p.write_text(s)
print('v24 applied')
# trigger
