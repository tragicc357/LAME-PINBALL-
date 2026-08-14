from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
orig=s
s=s.replace('LAME — Howie Lucas Pinball v59','LAME — Howie Lucas Pinball v60',1)
# Add popup state/functions before drawWorld declaration.
needle='function drawWorld(){'
insert='''let pointPopups=[];\nfunction showPointPopup(points,x,y){\n  const n=Math.floor(Number(points)||0);\n  if(n<=0)return;\n  pointPopups.push({n,x:Number.isFinite(x)?x:ball.x,y:Number.isFinite(y)?y:ball.y,t:performance.now()});\n  if(pointPopups.length>18)pointPopups.splice(0,pointPopups.length-18);\n}\nfunction drawPointPopups(){\n  const now=performance.now();\n  pointPopups=pointPopups.filter(p=>now-p.t<1050);\n  ctx.save();ctx.textAlign='center';ctx.textBaseline='middle';\n  for(const p of pointPopups){\n    const age=(now-p.t)/1050, rise=18+age*62, alpha=Math.max(0,1-age);\n    const scale=1+Math.sin(Math.min(1,age/.18)*Math.PI)*.28;\n    ctx.save();ctx.translate(p.x,p.y-rise);ctx.scale(scale,scale);ctx.globalAlpha=alpha;\n    ctx.font='900 30px Impact,Arial Black,Arial';ctx.lineWidth=7;ctx.strokeStyle='rgba(0,0,0,.92)';ctx.shadowBlur=18;ctx.shadowColor='#ffd21f';\n    const txt='+'+p.n.toLocaleString();ctx.strokeText(txt,0,0);ctx.fillStyle='#fff36a';ctx.fillText(txt,0,0);ctx.restore();\n  }\n  ctx.restore();ctx.globalAlpha=1;\n}\n'''
if needle not in s: raise SystemExit('drawWorld target missing')
s=s.replace(needle,insert+needle,1)
# Main scoring path: show actual awarded total including combo/double points.
old='score+=n;if(boxOpen===4)howieOutPoints+=n;if(combo>=3)'
new='score+=n;showPointPopup(n,Number.isFinite(x)?x:ball.x,Number.isFinite(y)?y:ball.y);if(boxOpen===4)howieOutPoints+=n;if(combo>=3)'
if old not in s: raise SystemExit('addScore target missing')
s=s.replace(old,new,1)
# Main Howie bumper direct award.
s=s.replace('score+=100000;howieOutPoints+=100000;updateHud();openFlapsAndLevels();setStatus("HOWIE BUMPER!', 'score+=100000;showPointPopup(100000,ball.x,ball.y);howieOutPoints+=100000;updateHud();openFlapsAndLevels();setStatus("HOWIE BUMPER!',1)
# Extra-ball Howie direct award.
s=s.replace('score+=100000;howieOutPoints+=100000;updateHud();openFlapsAndLevels();howieFlashUntil=now+240;', 'score+=100000;showPointPopup(100000,b.x,b.y);howieOutPoints+=100000;updateHud();openFlapsAndLevels();howieFlashUntil=now+240;',1)
# Ramp eject-hole direct bonus.
s=s.replace('score+=bonus;if(boxOpen===4)howieOutPoints+=bonus;updateHud();openFlapsAndLevels();', 'score+=bonus;showPointPopup(bonus,ball.x,ball.y);if(boxOpen===4)howieOutPoints+=bonus;updateHud();openFlapsAndLevels();',1)
# Draw popups in world coordinates after all balls, so they appear above gameplay objects.
old_draw='drawRealBall();drawExtraBalls()}'
new_draw='drawRealBall();drawExtraBalls();drawPointPopups()}'
if old_draw not in s: raise SystemExit('draw popup target missing')
s=s.replace(old_draw,new_draw,1)
# Clear stale popups when a fresh game starts.
s=s.replace('score=0;scoreShown=0;howieOutPoints=0;', 'score=0;scoreShown=0;pointPopups=[];howieOutPoints=0;',1)
if s==orig: raise SystemExit('no changes')
p.write_text(s)
print('v60 upgrade applied')
# v60 trigger
