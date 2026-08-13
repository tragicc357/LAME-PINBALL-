from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
s=re.sub(r'<title>.*?</title>','<title>LAME — Howie Lucas Pinball v25</title>',s,count=1)
s=s.replace('const LEVEL_GOAL=12000000,MAX_LEVEL=5;let level=1,levelTransitioning=false,gameWon=false;','const LEVEL_GOAL=1000000,FLAP_GOAL=20000,MAX_LEVEL=5;let level=1,levelTransitioning=false,gameWon=false;',1)
s=s.replace('<span>12,000,000 PTS = NEXT LEVEL</span>','<span>20,000 PTS = OPEN 1 FLAP</span>',1)
s=s.replace('function drawFittedGraphic(){ctx.save();ctx.fillStyle="#000";ctx.fillRect(0,0,W,WORLD_H);if(theme.complete&&theme.naturalWidth){const sc=Math.max(W/theme.naturalWidth,WORLD_H/theme.naturalHeight),dw=theme.naturalWidth*sc,dh=theme.naturalHeight*sc;ctx.globalAlpha=.58;ctx.drawImage(theme,(W-dw)/2,(WORLD_H-dh)/2,dw,dh);ctx.globalAlpha=1;ctx.fillStyle="rgba(0,0,0,.22)";ctx.fillRect(0,0,W,WORLD_H)}ctx.restore()}','function drawFittedGraphic(){ctx.save();ctx.fillStyle="#000000";ctx.fillRect(0,0,W,WORLD_H);ctx.restore()}',1)
p.write_text(s)
print('v25 step1 applied')
