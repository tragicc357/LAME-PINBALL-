from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
s=s.replace('LAME — Howie Lucas Pinball v52','LAME — Howie Lucas Pinball v53',1)
# Make the opening overlay scrollable instead of clipping tall content on phones.
css='''\n/* v53: keep start/watch controls visible on every screen size */\n#startScreen{align-items:flex-start!important;justify-content:center!important;overflow-y:auto!important;overflow-x:hidden!important;padding:12px!important;-webkit-overflow-scrolling:touch}\n#startScreen .panel{width:min(100%,430px)!important;max-height:none!important;margin:auto!important;position:relative!important;z-index:30!important;padding:16px!important}\n.modeButtons{display:grid;grid-template-columns:1fr;gap:9px;margin:10px 0 12px;position:relative;z-index:60}\n.modeButtons button{display:block!important;visibility:visible!important;opacity:1!important;position:relative!important;z-index:61!important;min-height:56px!important;font-size:16px!important}\n#watchComputer{background:linear-gradient(#2196f3,#0d5ba8)!important;color:#fff!important;border:3px solid #8ed6ff!important;box-shadow:0 0 20px #2196f388!important}\n#startBtn{background:linear-gradient(#ffd84a,#e8a900)!important;color:#111!important;border:2px solid #fff0a0!important}\n@media(max-height:760px){#startScreen .panel h3{font-size:38px!important}.nicknameBox,.ballChoice{margin:6px 0!important}.howto{font-size:10px!important;line-height:1.3!important}.modeButtons button{min-height:50px!important}}\n'''
if '</style>' not in s: raise SystemExit('style end not found')
s=s.replace('</style>',css+'</style>',1)
# Pull the two mode buttons out of the bottom of the long instruction block and place them high on the panel.
s=re.sub(r'<button id="startBtn">START GAME</button>','',s,count=1)
s=re.sub(r'<button id="watchComputer">[^<]*</button>','',s,count=1)
anchor='<div class="replaySummary"><b>🏆 ACHIEVEMENTS</b><span id="achievementCount">0/6 UNLOCKED</span></div>'
buttons='<div class="modeButtons"><button id="startBtn">🎮 START GAME</button><button id="watchComputer">🤖 WATCH COMPUTER PLAY — SMART AUTO MODE</button></div>'
if anchor not in s: raise SystemExit('replay summary anchor not found')
s=s.replace(anchor,anchor+buttons,1)
# Verify exactly one visible button for each mode and the handler is still present.
for token in ['LAME — Howie Lucas Pinball v53','id="startBtn"','id="watchComputer"','WATCH COMPUTER PLAY — SMART AUTO MODE','document.getElementById("watchComputer").onclick']:
    if token not in s: raise SystemExit('missing '+token)
if s.count('id="watchComputer"')!=1: raise SystemExit('watch button duplicate')
if s.count('id="startBtn"')!=1: raise SystemExit('start button duplicate')
p.write_text(s)
