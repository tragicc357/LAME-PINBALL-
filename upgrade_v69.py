from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old=s

s=s.replace('LAME — Howie Lucas Pinball v68','LAME — Howie Lucas Pinball v69')
share='https://tragicc357.github.io/LAME-PINBALL-/Lame%20box.png'
import re
s=re.sub(r'<meta property="og:image" content="[^"]+">',f'<meta property="og:image" content="{share}">',s,count=1)
s=re.sub(r'<meta property="og:image:secure_url" content="[^"]+">',f'<meta property="og:image:secure_url" content="{share}">',s,count=1)
s=re.sub(r'<meta name="twitter:image" content="[^"]+">',f'<meta name="twitter:image" content="{share}">',s,count=1)
s=s.replace('LAME — Howie Lucas Pinball global leaderboard preview','LAME — Howie Lucas Pinball artwork')

marker='<script>\nconst W=600,VIEW_H=900,WORLD_H=1300,LEVEL_GOAL=3000000,FLAP_GOAL=20000,MAX_LEVEL=5;'
insert='<script>\nconst tableArt=new Image();tableArt.src="Lame%20box.png";\nconst W=600,VIEW_H=900,WORLD_H=1300,LEVEL_GOAL=3000000,FLAP_GOAL=20000,MAX_LEVEL=5;'
if marker not in s:
    raise SystemExit('script marker not found')
s=s.replace(marker,insert,1)

draw_marker='ctx.fillStyle=pf;ctx.fillRect(0,0,W,WORLD_H);drawPlayfieldLighting();'
draw_insert='ctx.fillStyle=pf;ctx.fillRect(0,0,W,WORLD_H);if(tableArt.complete&&tableArt.naturalWidth){const iw=tableArt.naturalWidth,ih=tableArt.naturalHeight,scale=Math.max(W/iw,WORLD_H/ih),dw=iw*scale,dh=ih*scale,dx=(W-dw)/2,dy=(WORLD_H-dh)/2;ctx.save();ctx.globalAlpha=.34;ctx.drawImage(tableArt,dx,dy,dw,dh);ctx.globalAlpha=1;ctx.fillStyle="rgba(0,0,0,.34)";ctx.fillRect(0,0,W,WORLD_H);ctx.restore()}drawPlayfieldLighting();'
if draw_marker not in s:
    raise SystemExit('draw marker not found')
s=s.replace(draw_marker,draw_insert,1)

s=s.replace('<img src="pinball-table.jpg" alt="Howie Lucas outside the box">','<img src="Lame%20box.png" alt="Howie Lucas outside the box">',1)

if s==old:
    raise SystemExit('no changes made')
p.write_text(s,encoding='utf-8')
print('v69 upgrade applied')
# trigger v69 after full-quality artwork upload
