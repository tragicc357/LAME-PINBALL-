from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
# Accept either v52 or v53 as the starting point so this upgrade is safe if v53 is still queued.
s=s.replace('LAME — Howie Lucas Pinball v53','LAME — Howie Lucas Pinball v54',1)
s=s.replace('LAME — Howie Lucas Pinball v52','LAME — Howie Lucas Pinball v54',1)

# If the v53 visibility CSS has not landed yet, add it here too so WATCH COMPUTER PLAY stays visible.
if '#startScreen{align-items:flex-start!important' not in s:
    css='''\n/* v54: keep start/watch controls visible on every screen size */\n#startScreen{align-items:flex-start!important;justify-content:center!important;overflow-y:auto!important;overflow-x:hidden!important;padding:12px!important;-webkit-overflow-scrolling:touch}\n#startScreen .panel{width:min(100%,430px)!important;max-height:none!important;margin:auto!important;position:relative!important;z-index:30!important;padding:16px!important}\n.modeButtons{display:grid;grid-template-columns:1fr;gap:9px;margin:10px 0 12px;position:relative;z-index:60}\n.modeButtons button{display:block!important;visibility:visible!important;opacity:1!important;position:relative!important;z-index:61!important;min-height:56px!important;font-size:16px!important}\n#watchComputer{background:linear-gradient(#2196f3,#0d5ba8)!important;color:#fff!important;border:3px solid #8ed6ff!important;box-shadow:0 0 20px #2196f388!important}\n#startBtn{background:linear-gradient(#ffd84a,#e8a900)!important;color:#111!important;border:2px solid #fff0a0!important}\n'''
    s=s.replace('</style>',css+'</style>',1)
if 'class="modeButtons"' not in s:
    s=re.sub(r'<button id="startBtn">[^<]*</button>','',s,count=1)
    s=re.sub(r'<button id="watchComputer">[^<]*</button>','',s,count=1)
    anchor='<div class="replaySummary"><b>🏆 ACHIEVEMENTS</b><span id="achievementCount">0/6 UNLOCKED</span></div>'
    buttons='<div class="modeButtons"><button id="startBtn">🎮 START GAME</button><button id="watchComputer">🤖 WATCH COMPUTER PLAY — SMART AUTO MODE</button></div>'
    if anchor not in s: raise SystemExit('mode button anchor not found')
    s=s.replace(anchor,anchor+buttons,1)

# Smart multiball camera: prioritize the lowest active playfield ball, not shooter-lane balls.
marker='function loop(){computerControl();physics();updateExtraBalls();updateReplaySystems();'
if marker not in s: raise SystemExit('loop marker not found')
smart='''function updateSmartMultiballCamera(){if(!playing||transitioning||won)return;const balls=[];if(!mainBallSuppressed&&!waiting&&!inShooter&&!drainCommitted)balls.push(ball);for(const b of extraBalls){if(b.active&&!b.inShooter)balls.push(b)}if(!balls.length)return;let focus=balls[0];for(const b of balls){if(b.y>focus.y)focus=b}const multi=balls.length>1;const anchor=multi?VIEW_H*.70:VIEW_H*.52;const target=Math.max(0,Math.min(WORLD_H-VIEW_H,focus.y-anchor));cameraY+=(target-cameraY)*(multi?.27:.14)}\n'''
s=s.replace(marker,smart+'function loop(){computerControl();physics();updateExtraBalls();updateSmartMultiballCamera();updateReplaySystems();',1)

for token in ['LAME — Howie Lucas Pinball v54','updateSmartMultiballCamera','b.y>focus.y','!b.inShooter','WATCH COMPUTER PLAY — SMART AUTO MODE']:
    if token not in s: raise SystemExit('missing '+token)
p.write_text(s)
