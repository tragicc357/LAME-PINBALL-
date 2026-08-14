from pathlib import Path
p=Path('index.html')
s=p.read_text()

s=s.replace('LAME — Howie Lucas Pinball v48','LAME — Howie Lucas Pinball v49',1)
s=s.replace('facebook-preview-v29.html','facebook-preview-v49.html')

old='''<div class="powerWrap"><div class="powerLabel"><span>LAUNCH MOMENTUM</span><span id="powerPct">0%</span></div><div class="powerTrack"><div class="powerFill" id="powerFill"></div></div></div>'''
new='''<div class="powerWrap" id="launchScorePanel"><div id="launchMeterView"><div class="powerLabel"><span>LAUNCH MOMENTUM</span><span id="powerPct">0%</span></div><div class="powerTrack"><div class="powerFill" id="powerFill"></div></div></div><div id="liveScoreView" class="liveScoreView hide"><div><span class="liveScoreLabel">TOTAL SCORE</span><b id="liveScoreNumber">0</b></div><div class="liveComboBox"><span>COMBO</span><b id="liveComboX">x1</b></div></div></div>'''
if old not in s: raise SystemExit('power panel target not found')
s=s.replace(old,new,1)

s=s.replace('.powerFill{height:100%;width:0%;background:linear-gradient(90deg,#28cf68 0%,#ffe12c 55%,#ff3b2f 100%)}', '''.powerFill{height:100%;width:0%;background:linear-gradient(90deg,#28cf68 0%,#ffe12c 55%,#ff3b2f 100%)}.liveScoreView{display:grid;grid-template-columns:1fr 110px;gap:8px;align-items:stretch}.liveScoreView.hide{display:none}.liveScoreView>div{background:linear-gradient(#151b21,#07090b);border:2px solid #b88a00;border-radius:10px;padding:7px 10px;text-align:center}.liveScoreLabel,.liveComboBox span{display:block;font-size:10px;font-weight:900;letter-spacing:1px;color:#aeb8c1}.liveScoreView #liveScoreNumber{display:block;font-family:Impact,Arial Black,sans-serif;font-size:clamp(30px,8vw,48px);line-height:1;color:#ffd21f;text-shadow:0 0 15px #ffbf00;margin-top:3px}.liveComboBox{display:flex!important;flex-direction:column;justify-content:center}.liveComboBox #liveComboX{font-family:Impact,Arial Black,sans-serif;font-size:34px;color:#70d7ff;text-shadow:0 0 12px #36bfff}''',1)

oldrefs='''const currentLevelEl=document.getElementById("currentLevelIndicator"),nextLevelEl=document.getElementById("nextLevelIndicator"),powerFill=document.getElementById("powerFill"),powerPct=document.getElementById("powerPct");'''
newrefs='''const currentLevelEl=document.getElementById("currentLevelIndicator"),nextLevelEl=document.getElementById("nextLevelIndicator"),powerFill=document.getElementById("powerFill"),powerPct=document.getElementById("powerPct"),launchMeterView=document.getElementById("launchMeterView"),liveScoreView=document.getElementById("liveScoreView"),liveScoreNumber=document.getElementById("liveScoreNumber"),liveComboX=document.getElementById("liveComboX");'''
if oldrefs not in s: raise SystemExit('refs target not found')
s=s.replace(oldrefs,newrefs,1)

s=s.replace('let howieOutPointsShown=0,spinnerGlowUntil=0,targetGlowUntil=0,celebrationUntil=0,comboLightUntil=0;', 'let howieOutPointsShown=0,scoreShown=0,spinnerGlowUntil=0,targetGlowUntil=0,celebrationUntil=0,comboLightUntil=0;',1)

oldhud='''function updateHud(){scoreEl.textContent=score.toLocaleString();ballEl.textContent=currentBall+"/3";levelEl.textContent=level+"/5";multiEl.textContent="x"+combo;outEl.textContent=fmt(outMs());currentLevelEl.textContent=level;nextLevelEl.textContent=level<5?level+1:"FINAL";bestEl.textContent=stats.highScore.toLocaleString();playsEl.textContent=stats.plays.toLocaleString();highEl.textContent=stats.highScore.toLocaleString();longEl.textContent=fmt(stats.longestOutMs)}'''
newhud='''function updateHud(){scoreEl.textContent=score.toLocaleString();ballEl.textContent=currentBall+"/3";levelEl.textContent=level+"/5";multiEl.textContent="x"+combo;if(liveComboX)liveComboX.textContent="x"+combo;outEl.textContent=fmt(outMs());currentLevelEl.textContent=level;nextLevelEl.textContent=level<5?level+1:"FINAL";bestEl.textContent=stats.highScore.toLocaleString();playsEl.textContent=stats.plays.toLocaleString();highEl.textContent=stats.highScore.toLocaleString();longEl.textContent=fmt(stats.longestOutMs)}'''
if oldhud not in s: raise SystemExit('hud target not found')
s=s.replace(oldhud,newhud,1)

marker='''function setLaunchPower(v){charge=Math.max(.25,Math.min(1,v));if(powerFill)powerFill.style.width=Math.round(charge*100)+"%";if(powerPct)powerPct.textContent=Math.round(charge*100)+"%"}'''
helpers='''function showLaunchMeter(){if(launchMeterView)launchMeterView.style.display="block";if(liveScoreView)liveScoreView.classList.add("hide")}function showLiveScore(){if(launchMeterView)launchMeterView.style.display="none";if(liveScoreView)liveScoreView.classList.remove("hide");if(liveComboX)liveComboX.textContent="x"+combo}function updateLiveScoreCounter(){const d=score-scoreShown;if(Math.abs(d)<1)scoreShown=score;else scoreShown+=d*(Math.abs(d)>1000000?.055:Math.abs(d)>250000?.075:.12);if(liveScoreNumber)liveScoreNumber.textContent=Math.floor(scoreShown).toLocaleString();if(liveComboX)liveComboX.textContent="x"+combo}'''+marker
if marker not in s: raise SystemExit('launch power target not found')
s=s.replace(marker,helpers,1)

s=s.replace('if(powerFill)powerFill.style.width="0%";if(powerPct)powerPct.textContent="0%";updateHud();setStatus', 'if(powerFill)powerFill.style.width="0%";if(powerPct)powerPct.textContent="0%";showLaunchMeter();updateHud();setStatus',1)

s=s.replace('score=0;howieOutPoints=0;howieOutPointsShown=0;', 'score=0;scoreShown=0;howieOutPoints=0;howieOutPointsShown=0;',1)

oldlaunch='''function launch(power=.85){if(!playing||!waiting)return;initAudio();sfxLaunch(power);waiting=false;inShooter=true;drainCommitted=false;ball.x=535;ball.y=1165;ball.vx=0;ball.vy=-(18.5+power*10.5);setStatus(power>.88?"PERFECT LAUNCH!":"BALL LAUNCHED");setTimeout(()=>{if(powerFill)powerFill.style.width="0%";if(powerPct)powerPct.textContent="0%"},260)}'''
newlaunch='''function launch(power=.85){if(!playing||!waiting)return;initAudio();sfxLaunch(power);waiting=false;inShooter=true;drainCommitted=false;ball.x=535;ball.y=1165;ball.vx=0;ball.vy=-(18.5+power*10.5);showLiveScore();setStatus(power>.88?"PERFECT LAUNCH!":"BALL LAUNCHED");setTimeout(()=>{if(powerFill)powerFill.style.width="0%";if(powerPct)powerPct.textContent="0%"},260)}'''
if oldlaunch not in s: raise SystemExit('launch target not found')
s=s.replace(oldlaunch,newlaunch,1)

oldloop='''function loop(){computerControl();physics();draw();if(boxOpen===4&&playing)outEl.textContent=fmt(outMs());requestAnimationFrame(loop)}'''
newloop='''function loop(){computerControl();physics();updateLiveScoreCounter();draw();if(boxOpen===4&&playing)outEl.textContent=fmt(outMs());requestAnimationFrame(loop)}'''
if oldloop not in s: raise SystemExit('loop target not found')
s=s.replace(oldloop,newloop,1)

# sanity
for x in ['liveScoreNumber','showLiveScore()','updateLiveScoreCounter()','facebook-preview-v49.html']:
    if x not in s: raise SystemExit('missing '+x)
p.write_text(s)
print('v49 patched: launch meter swaps to animated total score + combo and new share preview URL')
