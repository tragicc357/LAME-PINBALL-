from pathlib import Path
p=Path('index.html')
s=p.read_text()

s=s.replace('LAME — Howie Lucas Pinball v45','LAME — Howie Lucas Pinball v46',1)

# Add visual state vars without changing gameplay physics/scoring.
needle='let howieOutPointsShown=0,spinnerGlowUntil=0,targetGlowUntil=0;'
replacement='let howieOutPointsShown=0,spinnerGlowUntil=0,targetGlowUntil=0,celebrationUntil=0,comboLightUntil=0;'
if needle not in s: raise SystemExit('visual vars marker missing')
s=s.replace(needle,replacement,1)

# Trigger short light shows for flap opens and stronger combos.
s=s.replace('setStatus("BOX FLAP OPENED! "+boxOpen+"/4");', 'celebrationUntil=performance.now()+1100;setStatus("BOX FLAP OPENED! "+boxOpen+"/4");',1)
s=s.replace('score+=n;if(boxOpen===4)howieOutPoints+=n;updateHud();openFlapsAndLevels()', 'score+=n;if(boxOpen===4)howieOutPoints+=n;if(combo>=3)comboLightUntil=performance.now()+650;updateHud();openFlapsAndLevels()',1)

# Insert non-collision visual layer before drawWorld.
marker='function drawWorld(){'
if marker not in s: raise SystemExit('drawWorld marker missing')
visual=r'''function levelPalette(){return [
{a:'#27c7ff',b:'#ffd21f',c:'#ff3b6b'},
{a:'#8b5cff',b:'#35f2b0',c:'#ffd447'},
{a:'#ff6a35',b:'#64ddff',c:'#f3f3f3'},
{a:'#45a7ff',b:'#ff4edb',c:'#ffe36a'},
{a:'#ff304f',b:'#41f4ff',c:'#ffffff'}][Math.max(0,Math.min(4,level-1))]}
function drawPlayfieldLighting(){const now=performance.now(),P=levelPalette(),pulse=.55+.45*Math.sin(now/180),fast=.5+.5*Math.sin(now/70);ctx.save();
// subtle under-glass GI wash
const gi=ctx.createRadialGradient(300,620,80,300,620,620);gi.addColorStop(0,'rgba(255,255,255,.015)');gi.addColorStop(.58,P.a+'16');gi.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=gi;ctx.fillRect(0,0,W,WORLD_H);
// cabinet edge chase lights - visual only
const edgeY=[210,300,390,480,570,660,750,840,930,1020];edgeY.forEach((y,i)=>{const hot=((Math.floor(now/115)+i)%5)===0;for(const x of [38,478]){ctx.beginPath();ctx.arc(x,y,hot?7:5,0,Math.PI*2);ctx.fillStyle=hot?P.b:P.a;ctx.globalAlpha=hot?.95:.32;ctx.shadowBlur=hot?22:8;ctx.shadowColor=hot?P.b:P.a;ctx.fill()}});ctx.globalAlpha=1;ctx.shadowBlur=0;
// lane inserts positioned in open, non-scoring areas
const inserts=[[92,325],[465,335],[105,535],[455,545],[135,735],[440,755],[170,930],[420,925]];inserts.forEach((q,i)=>{const phase=.35+.65*Math.max(0,Math.sin(now/240+i*.8));ctx.save();ctx.translate(q[0],q[1]);ctx.rotate((i%2?1:-1)*.18);ctx.shadowBlur=10+14*phase;ctx.shadowColor=i%3===0?P.b:P.a;ctx.fillStyle=i%3===0?P.b:P.a;ctx.globalAlpha=.16+.44*phase;ctx.beginPath();ctx.moveTo(0,-10);ctx.lineTo(12,10);ctx.lineTo(-12,10);ctx.closePath();ctx.fill();ctx.restore()});ctx.globalAlpha=1;
// level beacon and small lamp bank at top
ctx.textAlign='center';ctx.font='900 13px Arial';ctx.fillStyle=P.b;ctx.shadowBlur=10+10*pulse;ctx.shadowColor=P.b;ctx.fillText('LEVEL '+level+' • FEATURE SHOTS LIVE',300,124);for(let i=0;i<7;i++){const x=180+i*40,hot=((Math.floor(now/140)+i)%7)<2;ctx.beginPath();ctx.arc(x,143,5.5,0,Math.PI*2);ctx.fillStyle=hot?P.c:'#2b2f33';ctx.shadowBlur=hot?18:3;ctx.shadowColor=P.c;ctx.fill()}
// active feature arrows point toward ramp + spinner without adding obstacles
try{const L=trickLayout();const rampHot=trickMode==='ramp',spinHot=now<spinnerGlowUntil;ctx.shadowBlur=18;ctx.lineWidth=4;ctx.strokeStyle=rampHot?'#fff':P.b;ctx.fillStyle=rampHot?'#fff':P.b;ctx.globalAlpha=rampHot?1:.66;const rx=L.ramp.s[0],ry=L.ramp.s[1]+48;ctx.beginPath();ctx.moveTo(rx,ry-28);ctx.lineTo(rx-12,ry-5);ctx.lineTo(rx-4,ry-7);ctx.lineTo(rx-4,ry+8);ctx.lineTo(rx+4,ry+8);ctx.lineTo(rx+4,ry-7);ctx.lineTo(rx+12,ry-5);ctx.closePath();ctx.fill();ctx.globalAlpha=spinHot?1:.62;ctx.fillStyle=spinHot?'#fff':P.a;ctx.shadowColor=spinHot?'#fff':P.a;ctx.beginPath();ctx.arc(L.spinner[0],L.spinner[1]+62,8+4*fast,0,Math.PI*2);ctx.fill();ctx.font='900 11px Arial';ctx.fillText('RAMP',rx,ry+28);ctx.fillText('SPIN',L.spinner[0],L.spinner[1]+90)}catch(e){}
// event light shows: flap open + combo streaks
if(now<celebrationUntil){const k=(celebrationUntil-now)/1100;ctx.globalAlpha=.12+.16*Math.abs(Math.sin(now/55));ctx.fillStyle=P.b;ctx.fillRect(0,cameraY,W,VIEW_H);ctx.globalAlpha=1;for(let i=0;i<10;i++){const a=now/140+i*.628,r=95+220*(1-k);ctx.beginPath();ctx.arc(300+Math.cos(a)*r,cameraY+420+Math.sin(a)*r,5+8*k,0,Math.PI*2);ctx.fillStyle=i%2?P.a:P.b;ctx.shadowBlur=25;ctx.shadowColor=ctx.fillStyle;ctx.fill()}}
if(now<comboLightUntil){ctx.globalAlpha=.12+.13*fast;ctx.fillStyle=P.c;ctx.fillRect(0,cameraY,W,VIEW_H);ctx.globalAlpha=1;ctx.fillStyle='#fff';ctx.font='900 24px Impact,Arial Black';ctx.shadowBlur=22;ctx.shadowColor=P.c;ctx.fillText('COMBO x'+combo,300,cameraY+190)}ctx.restore();ctx.globalAlpha=1;ctx.shadowBlur=0}
function drawRealisticHardware(){const P=levelPalette(),now=performance.now();ctx.save();
// brushed metal side rails and visible fasteners
for(const x of [18,486]){const g=ctx.createLinearGradient(x-7,0,x+10,0);g.addColorStop(0,'#171a1d');g.addColorStop(.35,'#e7edf0');g.addColorStop(.58,'#666f76');g.addColorStop(1,'#111416');ctx.fillStyle=g;ctx.fillRect(x,175,12,945)}
for(const x of [24,492])for(let y=215;y<1100;y+=120){ctx.beginPath();ctx.arc(x,y,4,0,Math.PI*2);ctx.fillStyle='#cfd5d9';ctx.fill();ctx.beginPath();ctx.moveTo(x-2.5,y);ctx.lineTo(x+2.5,y);ctx.strokeStyle='#555';ctx.lineWidth=1;ctx.stroke()}
// soft glass reflection streaks
ctx.globalAlpha=.055;ctx.strokeStyle='#fff';ctx.lineWidth=18;ctx.beginPath();ctx.moveTo(70,180);ctx.lineTo(240,720);ctx.stroke();ctx.beginPath();ctx.moveTo(390,250);ctx.lineTo(520,680);ctx.stroke();ctx.restore();ctx.globalAlpha=1}
'''
s=s.replace(marker,visual+marker,1)

# Draw lighting beneath mechanisms, hardware above base playfield but before main mechanisms.
old="ctx.fillStyle=pf;ctx.fillRect(0,0,W,WORLD_H);ctx.save();ctx.globalAlpha=.08;"
new="ctx.fillStyle=pf;ctx.fillRect(0,0,W,WORLD_H);drawPlayfieldLighting();drawRealisticHardware();ctx.save();ctx.globalAlpha=.08;"
if old not in s: raise SystemExit('playfield insertion marker missing')
s=s.replace(old,new,1)

# Add gentle pulse to real bumpers even when not hit, keeping same collisions/scoring.
oldb='function drawRealBumper(b){const flash=b.flash>0;ctx.save();ctx.shadowBlur=flash?30:12;ctx.shadowColor=flash?"#fff2a8":"#49b8ff55";'
newb='function drawRealBumper(b){const flash=b.flash>0,ambient=.5+.5*Math.sin(performance.now()/170+b.x*.02);ctx.save();ctx.shadowBlur=flash?34:10+10*ambient;ctx.shadowColor=flash?"#fff2a8":levelPalette().a;'
if oldb in s: s=s.replace(oldb,newb,1)

# More exciting table frame glow, no layout crowding.
s=s.replace('.table{position:relative;border-radius:18px;overflow:hidden;border:3px solid #252525;box-shadow:0 0 0 2px #a67b00,0 0 30px #e6a90030}', '.table{position:relative;border-radius:18px;overflow:hidden;border:3px solid #4a4f54;box-shadow:0 0 0 2px #d2a51b,0 0 34px #3bbcff55,inset 0 0 18px #000}',1)

# Safety checks.
if 'LAME — Howie Lucas Pinball v46' not in s: raise SystemExit('title update failed')
if 'function drawPlayfieldLighting()' not in s: raise SystemExit('lighting layer missing')
if 'drawPlayfieldLighting();drawRealisticHardware();' not in s: raise SystemExit('lighting call missing')

p.write_text(s)
print('v46 visual upgrade applied: realistic hardware, responsive RGB-style lighting, chase lamps, inserts, arrows, and event light shows')
