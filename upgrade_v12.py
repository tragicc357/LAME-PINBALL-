from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
site='https://tragicc357.github.io/LAME-PINBALL-/'
img=site+'pinball-table.jpg'
# title + Facebook/Open Graph preview
s=re.sub(r'<title>.*?</title>', '<title>LAME — Howie Lucas Pinball v12</title>', s, count=1)
# remove any old OG/Twitter tags this script owns, then insert fresh set
s=re.sub(r'\n?<meta property="og:[^"]+"[^>]*>', '', s)
s=re.sub(r'\n?<meta name="twitter:[^"]+"[^>]*>', '', s)
meta='''\n<meta property="og:title" content="LAME — Howie Lucas Pinball">\n<meta property="og:description" content="Break out the box, chase the global Top 5, and keep Howie out as long as you can.">\n<meta property="og:type" content="website">\n<meta property="og:url" content="'''+site+'''">\n<meta property="og:image" content="'''+img+'''">\n<meta property="og:image:secure_url" content="'''+img+'''">\n<meta property="og:image:type" content="image/jpeg">\n<meta property="og:image:width" content="120">\n<meta property="og:image:height" content="180">\n<meta property="og:image:alt" content="LAME — Howie Lucas Pinball table artwork">\n<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:title" content="LAME — Howie Lucas Pinball">\n<meta name="twitter:image" content="'''+img+'''">'''
s=s.replace('</title>', '</title>'+meta, 1)
# use uploaded pinball artwork as table art
s=re.sub(r'theme\.src="data:image/[^\"]+";', 'theme.src="pinball-table.jpg";', s, count=1)
# hard-lock camera to ball while it is actually in play
s=re.sub(r'const target=clamp\(ball\.y-VIEW_H\*0\.52,0,WORLD_H-VIEW_H\);\s*cameraY\+=\(target-cameraY\)\*0\.09;', 'if(playing&&!waiting){cameraY=clamp(ball.y-VIEW_H*0.50,0,WORLD_H-VIEW_H);}', s, count=1)
# fit the new tall pinball graphic as a full-table backdrop
s=re.sub(r'function drawFittedGraphic\(\)\{.*?\}(?=\nfunction drawHowieRunning)', '''function drawFittedGraphic(){if(!theme.complete||!theme.naturalWidth)return;const iw=theme.naturalWidth,ih=theme.naturalHeight;const scale=Math.max(W/iw,WORLD_H/ih);const dw=iw*scale,dh=ih*scale;const dx=(W-dw)/2,dy=(WORLD_H-dh)/2;ctx.globalAlpha=.93;ctx.drawImage(theme,dx,dy,dw,dh);ctx.globalAlpha=1}''', s, count=1, flags=re.S)
# keep Howie visibly moving INSIDE the current camera viewport the entire time all 4 flaps are open
runner='''function drawHowieRunning(){if(boxOpen<4||!theme.complete||!theme.naturalWidth)return;const t=performance.now()/1000;const minY=cameraY+145,maxY=cameraY+VIEW_H-175;const centerY=clamp(ball.y,minY+100,maxY-100);const x=300+Math.sin(t*1.65)*180;const y=clamp(centerY+Math.cos(t*1.20)*130,minY,maxY);const dir=Math.cos(t*1.65)>=0?1:-1;const bob=Math.sin(t*13)*5;const sx=theme.naturalWidth*.30,sy=theme.naturalHeight*.10,sw=theme.naturalWidth*.40,sh=theme.naturalHeight*.43;const h=150,w=105;ctx.save();ctx.translate(x,y+bob);ctx.scale(dir,1);ctx.beginPath();if(ctx.roundRect)ctx.roundRect(-w/2,-h/2,w,h,20);else ctx.rect(-w/2,-h/2,w,h);ctx.clip();ctx.shadowBlur=26;ctx.shadowColor="#ffd21f";ctx.drawImage(theme,sx,sy,sw,sh,-w/2,-h/2,w,h);ctx.restore();ctx.save();ctx.translate(x,y+bob);ctx.strokeStyle="#ffd21f";ctx.lineWidth=6;ctx.shadowBlur=20;ctx.shadowColor="#ffd21f";ctx.strokeRect(-w/2,-h/2,w,h);ctx.shadowBlur=0;ctx.fillStyle="rgba(0,0,0,.88)";ctx.fillRect(-65,h/2-22,130,25);ctx.fillStyle="#ffd21f";ctx.font="900 14px Arial";ctx.textAlign="center";ctx.fillText("HOWIE IS OUT!",0,h/2-5);ctx.restore()}'''
s=re.sub(r'function drawHowieRunning\(\)\{.*?\}(?=\nfunction drawWorld)', runner, s, count=1, flags=re.S)
# make the on-board art easier to see through the playfield overlay
s=s.replace('grad.addColorStop(.72,"rgba(2,6,9,.25)")','grad.addColorStop(.72,"rgba(2,6,9,.13)")')
s=s.replace('grad.addColorStop(1,"rgba(0,0,0,.60)")','grad.addColorStop(1,"rgba(0,0,0,.35)")')
# wording update for persistent runner behavior
s=s.replace('HOWIE\'S OUT THE BOX!','HOWIE\'S OUT THE BOX!')
p.write_text(s)
print('v12 applied')
