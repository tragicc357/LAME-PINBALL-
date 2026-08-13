from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
s=re.sub(r'<title>.*?</title>','<title>LAME — Howie Lucas Pinball v25</title>',s,count=1)
s=s.replace('const LEVEL_GOAL=12000000,MAX_LEVEL=5;let level=1,levelTransitioning=false,gameWon=false;','const LEVEL_GOAL=1000000,FLAP_GOAL=20000,MAX_LEVEL=5;let level=1,levelTransitioning=false,gameWon=false;',1)
s=s.replace('<span>12,000,000 PTS = NEXT LEVEL</span>','<span>20,000 PTS = OPEN 1 FLAP</span>',1)
s=s.replace('function drawFittedGraphic(){ctx.save();ctx.fillStyle="#000";ctx.fillRect(0,0,W,WORLD_H);if(theme.complete&&theme.naturalWidth){const sc=Math.max(W/theme.naturalWidth,WORLD_H/theme.naturalHeight),dw=theme.naturalWidth*sc,dh=theme.naturalHeight*sc;ctx.globalAlpha=.58;ctx.drawImage(theme,(W-dw)/2,(WORLD_H-dh)/2,dw,dh);ctx.globalAlpha=1;ctx.fillStyle="rgba(0,0,0,.22)";ctx.fillRect(0,0,W,WORLD_H)}ctx.restore()}','function drawFittedGraphic(){ctx.save();ctx.fillStyle="#000000";ctx.fillRect(0,0,W,WORLD_H);ctx.restore()}',1)
s=s.replace('<div class="levelTransition hide" id="levelTransition"><div class="levelCard">','<div class="levelTransition hide" id="levelTransition"><img src="pinball-table.jpg" style="position:absolute;inset:0;width:100%;height:100%;object-fit:contain;background:#000" alt="Howie artwork"><div class="levelCard" style="position:relative;z-index:2;background:rgba(0,0,0,.72)">',1)
s=s.replace('<div class="gameStats">','<div style="display:flex;justify-content:space-between;background:#070b0e;border:2px solid #36516a;border-radius:10px;padding:7px 10px;margin:0 0 7px;font-size:11px;font-weight:900;color:#70d7ff"><span>CURRENT LEVEL: <b id="currentLevelIndicator">1</b></span><span>NEXT LEVEL: <b id="nextLevelIndicator">2</b></span></div><div class="gameStats">',1)
m=re.search(r'<div class="howto">.*?</div><button id="startBtn">',s,re.S)
if m:
    t='<div class="howto">1. Hold <b>LAUNCH</b> and release to fire<br>2. Every <b>20,000 points</b> opens one box flap<br>3. Open all 4 flaps and Howie is free until you lose a ball or change levels<br>4. Every <b>1,000,000 points</b> clears a level<br>5. Between levels the game pauses and shows the Howie artwork full screen<br>6. Every new level loads a different board and the ball gets gradually faster<br>7. Beat Level 5 to finish the game</div><button id="startBtn">'
    s=s[:m.start()]+t+s[m.end():]
p.write_text(s)
print('v25 step2 applied')
