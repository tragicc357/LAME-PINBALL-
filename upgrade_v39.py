from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()

if 'LAME — Howie Lucas Pinball v38' not in s:
    raise SystemExit('Expected v38 title not found')
s=s.replace('LAME — Howie Lucas Pinball v38','LAME — Howie Lucas Pinball v39',1)

# Add launch-rail / perfect-launch / momentum-trail state to the existing trick state.
needle='trickTargetHits=[0,0,0];'
if needle not in s:
    raise SystemExit('trick state target not found')
s=s.replace(needle,'trickTargetHits=[0,0,0],launchRailActive=false,launchRailStart=0,perfectLaunchPending=false,perfectLaunchAwarded=false,momentumTrailUntil=0,ballTrail=[];',1)

helpers=r'''function launchRailPoint(t){const p=Math.max(0,Math.min(1,t));if(p<.38){const q=p/.38,a=Math.PI*.04-Math.PI*1.12*q;return{x:512+112*Math.cos(a),y:290+112*Math.sin(a)}}const q=(p-.38)/.62,u=1-q;return{x:u*u*405+2*u*q*315+q*q*205,y:u*u*188+2*u*q*120+q*q*235}}function beginLaunchRail(){if(launchRailActive||!inShooter)return;launchRailActive=true;launchRailStart=performance.now();ball.vx=0;ball.vy=0;sfxLaunch();if(perfectLaunchPending&&!perfectLaunchAwarded){perfectLaunchAwarded=true;addScore(20000,ball.x,ball.y);setStatus("💯 PERFECT LAUNCH! +20,000 BONUS");tone(980,.16,"triangle",.06,280)}}function runLaunchRail(){if(!launchRailActive)return false;const now=performance.now(),p=Math.min(1,(now-launchRailStart)/920),pt=launchRailPoint(p);ball.x=pt.x;ball.y=pt.y;cameraY=Math.max(0,Math.min(400,ball.y-430));if(p>=1){launchRailActive=false;inShooter=false;ball.x=205;ball.y=235;ball.vx=-6.8-level*.35;ball.vy=7.3+level*.25;momentumTrailUntil=now+850;sfxHit(1.2)}return true}function maybeEnterLaunchRail(){if(!launchRailActive&&inShooter&&!waiting&&ball.vy<-3&&ball.y<325)beginLaunchRail()}function drawLaunchLoopRail(){ctx.save();ctx.shadowBlur=16;ctx.shadowColor="#64d9ff";ctx.strokeStyle="#15191c";ctx.lineWidth=30;ctx.beginPath();for(let i=0;i<=36;i++){const p=i/36,pt=launchRailPoint(p);if(i===0)ctx.moveTo(pt.x,pt.y);else ctx.lineTo(pt.x,pt.y)}ctx.stroke();ctx.strokeStyle=chromeGrad(185,95,600,390);ctx.lineWidth=18;ctx.stroke();ctx.strokeStyle="#66dfff";ctx.lineWidth=4;ctx.stroke();ctx.setLineDash([13,10]);ctx.strokeStyle="rgba(255,255,255,.72)";ctx.lineWidth=3;ctx.stroke();ctx.setLineDash([]);ctx.fillStyle="#7ee8ff";ctx.font="900 15px Impact";ctx.textAlign="center";ctx.fillText("LOOP LAUNCH RAIL",410,105);ctx.restore()}function updateBallTrail(){const now=performance.now();if(now<momentumTrailUntil&&!waiting&&!inShooter){ballTrail.unshift({x:ball.x,y:ball.y,t:now});if(ballTrail.length>12)ballTrail.length=12}else if(ballTrail.length){ballTrail=ballTrail.filter(q=>now-q.t<420)}}function drawBallTrail(){const now=performance.now();ctx.save();for(let i=ballTrail.length-1;i>=0;i--){const q=ballTrail[i],age=(now-q.t)/420;if(age>=1)continue;const a=(1-age)*(.44-(i/Math.max(1,ballTrail.length))*.12),r=Math.max(2,ball.r*(1-age*.62));ctx.globalAlpha=Math.max(0,a);ctx.shadowBlur=10;ctx.shadowColor="#bfefff";const g=ctx.createRadialGradient(q.x-3,q.y-3,1,q.x,q.y,r);g.addColorStop(0,"#f8fdff");g.addColorStop(.45,"#8fdcff");g.addColorStop(1,"rgba(90,185,255,0)");ctx.fillStyle=g;ctx.beginPath();ctx.arc(q.x,q.y,r,0,Math.PI*2);ctx.fill()}ctx.restore();ctx.globalAlpha=1}function armPerfectLaunchBonus(){const el=document.getElementById("powerPct");const pct=parseInt((el&&el.textContent)||"0",10)||0;perfectLaunchPending=pct>=100;perfectLaunchAwarded=false}'''

anchor='function chromeGrad('
if anchor not in s:
    raise SystemExit('visual helper anchor not found')
s=s.replace(anchor,helpers+anchor,1)

# Let the rail become a real animated path before normal physics takes over.
old='function physics(){if(runTrickAnimation())return;if(handleTrickShots())return;'
new='function physics(){if(runLaunchRail())return;maybeEnterLaunchRail();if(runLaunchRail())return;if(runTrickAnimation())return;if(handleTrickShots())return;'
if old not in s:
    raise SystemExit('physics hook target not found')
s=s.replace(old,new,1)

# Draw the new loop rail and speed trail as part of the playfield.
if 'drawTrickFeatures();bumpers.forEach(drawRealBumper);' not in s:
    raise SystemExit('draw trick target not found')
s=s.replace('drawTrickFeatures();bumpers.forEach(drawRealBumper);','drawLaunchLoopRail();drawTrickFeatures();bumpers.forEach(drawRealBumper);',1)
if 'drawRealBall()' not in s:
    raise SystemExit('ball draw target not found')
s=s.replace('drawRealBall()','updateBallTrail();drawBallTrail();drawRealBall()',1)

# Reset rail/trail state with each ball.
s=s.replace('function resetBall(){trickMode=null;trickCooldown=performance.now()+350;','function resetBall(){launchRailActive=false;perfectLaunchPending=false;perfectLaunchAwarded=false;ballTrail=[];momentumTrailUntil=0;trickMode=null;trickCooldown=performance.now()+350;',1)

# Capture the visible meter at release BEFORE the existing release handler resets it.
insert='''\n["pointerup","pointercancel"].forEach(ev=>{document.getElementById("launchBtn")?.addEventListener(ev,armPerfectLaunchBonus,true)});window.addEventListener("keyup",e=>{if(e.code==="Space")armPerfectLaunchBonus()},true);\n// Any normal hit sound marks a fresh impact and briefly enables the fast-ball trail.\ntry{const __origSfxHit=sfxHit;sfxHit=function(...args){momentumTrailUntil=performance.now()+900;return __origSfxHit(...args)}}catch(e){}\n'''
if '</script>' not in s:
    raise SystemExit('script close not found')
s=s.replace('</script>',insert+'</script>',1)

# Tell players about the 100% launch bonus.
s=s.replace('1. Hold <b>LAUNCH</b> and release to fire','1. Hold <b>LAUNCH</b> and release to fire — hit <b>100%</b> for a <b>+20,000 PERFECT LAUNCH</b> bonus',1)

p.write_text(s)
print('v39 patched: looping launch rail, perfect 100% +20K, impact-only ball speed trail')