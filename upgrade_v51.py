from pathlib import Path
p=Path('index.html')
s=p.read_text()
s=s.replace('LAME — Howie Lucas Pinball v51','LAME — Howie Lucas Pinball v52',1)
s=s.replace('🤖 WATCH COMPUTER PLAY</button>','🤖 WATCH COMPUTER PLAY — SMART AUTO MODE</button>',1)
new='''function computerPredictXFor(b){if(!b||b.vy<=.05)return b?b.x:300;const targetY=1068,frames=Math.max(0,Math.min(24,(targetY-b.y)/Math.max(.4,b.vy*.88)));let x=b.x+b.vx*frames*.88;while(x<24||x>576){if(x<24)x=48-x;if(x>576)x=1152-x}return x}function computerPredictX(){return computerPredictXFor(ball)}function computerControl(){if(!autoPlay||!playing||transitioning||won)return;const now=performance.now();if(waiting){if(mainBallSuppressed)return;if(computerLaunchAt&&now>=computerLaunchAt){computerLaunchAt=0;const p=.90+Math.random()*.09;setLaunchPower(p);launch(p);setStatus("🤖 COMPUTER LAUNCHED THE BALL") }return}if(extraBallsQueued>0&&now-lastAutoExtraLaunch>1300){lastAutoExtraLaunch=now;spawnExtraBall()}const candidates=[];if(!mainBallSuppressed&&!inShooter&&!drainCommitted)candidates.push(ball);for(const b of extraBalls){if(b.active&&!b.inShooter)candidates.push(b)}if(!candidates.length)return;let target=null,best=-1e9;for(const b of candidates){const danger=(b.vy>0?900:0)+b.y*1.25+Math.abs(b.x-300)*.35;if(b.y>760&&b.y<1160&&danger>best){best=danger;target=b}}if(!target||now<computerFlipAt)return;let predicted=computerPredictXFor(target)+computerBrain.centerBias;const urgency=Math.max(0,Math.min(1,(target.y-780)/320));const triggerY=940-Math.min(105,(computerBrain.lead-8.5)*18);if(target.y<triggerY&&urgency<.62)return;let side;if(predicted<285+computerBrain.leftOffset)side="L";else if(predicted>315+computerBrain.rightOffset)side="R";else side=target.vx<=0?"L":"R";const recent=computerBrain.recent.slice(-2);if(recent.length===2&&recent.every(r=>r.zone==="C"&&r.side===side))side=side==="L"?"R":"L";computerTap(side);computerFlipAt=now+Math.max(85,145-computerBrain.misses*2);setStatus("🤖 COMPUTER DEFENDING "+side+" FLIP • "+candidates.length+" BALL"+(candidates.length===1?"":"S")+" ACTIVE") }'''
start=s.find('function computerPredictX(){')
end=s.find('function loop(){',start)
if start<0 or end<0: raise SystemExit('computer block markers not found')
s=s[:start]+new+s[end:]
start=s.find('document.getElementById("watchComputer").onclick=')
end=s.find('document.getElementById("againBtn").onclick=',start)
if start<0 or end<0: raise SystemExit('watch handler markers not found')
rep='document.getElementById("watchComputer").onclick=()=>{autoPlay=true;nicknameInput.value="Computer";computerLastDecision=null;computerLaunchAt=performance.now()+450;startGame();setStatus("🤖 WATCH COMPUTER PLAY — SMART AUTO MODE")};'
s=s[:start]+rep+s[end:]
for token in ['LAME — Howie Lucas Pinball v52','SMART AUTO MODE','computerPredictXFor','mainBallSuppressed)return','candidates.push(b)']:
    if token not in s: raise SystemExit('missing '+token)
p.write_text(s)
print('v52 smart computer mode patched')
