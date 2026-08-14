from pathlib import Path
p=Path('index.html')
s=p.read_text()
orig=s
s=s.replace('LAME — Howie Lucas Pinball v65','LAME — Howie Lucas Pinball v66',1)

# Only one moving non-ramp capture hole per level.
s=s.replace("captureHoleState=pool.slice(0,2).map((q,i)=>({id:i,x:q[0],y:q[1],r:25,hits:0,poolIndex:i}))", "captureHoleState=pool.slice(0,1).map((q,i)=>({id:i,x:q[0],y:q[1],r:25,hits:0,poolIndex:i}))",1)
s=s.replace("captureHoleState.length!==2", "captureHoleState.length!==1",1)
s=s.replace("Each level has <b>2 moving capture holes</b>", "Each level has <b>1 moving capture hole</b>",1)

# Add universal 40K box-eject bonus and fireworks particle system before star state.
needle='let boxStars=[];'
insert=r'''let bonusFireworks=[];
function awardBoxEjectBonus(){
  const pts=40000;
  score+=pts;
  if(boxOpen===4)howieOutPoints+=pts;
  showPointPopup(pts,300,705);
  updateHud();openFlapsAndLevels();
  actionFeedback('+40,000 POINTS!','#ffd21f',850);
  setStatus('✨ BOX EJECT BONUS +40,000 POINTS! ✨');
}
function triggerBoxEjectCelebration(){spawnBoxStars();awardBoxEjectBonus()}
function spawnBonusFireworks(){
  const now=performance.now();
  const centers=[[150,cameraY+235],[450,cameraY+235],[300,cameraY+315]];
  for(const c of centers){for(let i=0;i<24;i++){const a=Math.PI*2*i/24+(Math.random()-.5)*.18,sp=2.8+Math.random()*5.4;bonusFireworks.push({x:c[0],y:c[1],vx:Math.cos(a)*sp,vy:Math.sin(a)*sp,t:now,life:900+Math.random()*550,r:2+Math.random()*2.8,h:(i*47+Math.random()*80)%360})}}
  if(bonusFireworks.length>120)bonusFireworks.splice(0,bonusFireworks.length-120);
}
function drawBonusFireworks(){
  const now=performance.now();bonusFireworks=bonusFireworks.filter(p=>now-p.t<p.life);ctx.save();
  for(const p of bonusFireworks){const q=(now-p.t)/p.life;p.x+=p.vx*.72;p.y+=p.vy*.72;p.vy+=.032;ctx.globalAlpha=Math.max(0,1-q);ctx.shadowBlur=16;ctx.shadowColor=`hsl(${p.h} 100% 65%)`;ctx.fillStyle=`hsl(${p.h} 100% 65%)`;ctx.beginPath();ctx.arc(p.x,p.y,p.r*(1-q*.25),0,Math.PI*2);ctx.fill()}
  ctx.restore();ctx.globalAlpha=1;
}
'''
if needle not in s: raise SystemExit('boxStars insertion target missing')
s=s.replace(needle,insert+needle,1)

# Every existing box eject already calls stars in v65. Replace that call with stars + real 40K award.
old='boxEjectFlashUntil=now+900;spawnBoxStars();'
new='boxEjectFlashUntil=now+900;triggerBoxEjectCelebration();'
if old not in s: raise SystemExit('box eject celebration target missing')
s=s.replace(old,new)

# Fireworks whenever the vortex 3-ball event begins.
old='bonusBallFlashUntil=performance.now()+2600;'
new='bonusBallFlashUntil=performance.now()+3000;spawnBonusFireworks();setTimeout(spawnBonusFireworks,520);setTimeout(spawnBonusFireworks,1040);'
if old not in s: raise SystemExit('vortex bonus flash target missing')
s=s.replace(old,new,1)

# Make the 3-ball caption larger/brighter and keep fireworks drawn with it.
old="ctx.textAlign='center';ctx.shadowBlur=28;ctx.shadowColor='#48b9ff';ctx.fillStyle='#fff';ctx.font='900 38px Impact,Arial Black,Arial';ctx.fillText('BONUS BALLS!',W/2,cameraY+205);\n  ctx.fillStyle='#ffd21f';ctx.font='900 24px Impact,Arial Black,Arial';ctx.fillText('NOW YOU’RE PLAYING WITH 3 BALLS!',W/2,cameraY+246);ctx.restore();"
new="ctx.textAlign='center';ctx.shadowBlur=38;ctx.shadowColor='#48b9ff';ctx.fillStyle='#fff';ctx.font='900 46px Impact,Arial Black,Arial';ctx.fillText('BONUS BALLS!',W/2,cameraY+205);\n  ctx.shadowColor='#ffd21f';ctx.fillStyle='#ffd21f';ctx.font='900 27px Impact,Arial Black,Arial';ctx.fillText('NOW YOU’RE PLAYING WITH 3 BALLS!',W/2,cameraY+250);ctx.fillStyle='#fff';ctx.font='900 18px Impact,Arial Black,Arial';ctx.fillText('🔥 MULTIBALL ACTIVATED 🔥',W/2,cameraY+282);ctx.restore();drawBonusFireworks();"
if old not in s: raise SystemExit('bonus caption target missing')
s=s.replace(old,new,1)

# Add a dedicated +40K caption that erupts from the box with the stars.
needle='function drawBoxStars(){'
caption=r'''let ejectBonusCaptionUntil=0;
const __v66TriggerBoxEjectCelebration=triggerBoxEjectCelebration;
triggerBoxEjectCelebration=function(){ejectBonusCaptionUntil=performance.now()+1500;__v66TriggerBoxEjectCelebration()};
function drawEjectBonusCaption(){const now=performance.now();if(now>=ejectBonusCaptionUntil)return;const q=1-(ejectBonusCaptionUntil-now)/1500,y=690-q*65;ctx.save();ctx.globalAlpha=Math.min(1,(1-q)*2.5);ctx.textAlign='center';ctx.shadowBlur=24;ctx.shadowColor='#ffd21f';ctx.fillStyle='#fff';ctx.font='900 32px Impact,Arial Black,Arial';ctx.fillText('+40,000 POINTS',300,y);ctx.fillStyle='#ffd21f';ctx.font='900 15px Impact,Arial Black,Arial';ctx.fillText('BOX EJECT BONUS',300,y+23);ctx.restore()}
'''
if needle not in s: raise SystemExit('drawBoxStars target missing')
s=s.replace(needle,caption+needle,1)

# Draw eject caption alongside stars.
old='drawRealBall();drawExtraBalls();drawPointPopups();drawBoxStars();drawBonusBallFlash()}'
new='drawRealBall();drawExtraBalls();drawPointPopups();drawBoxStars();drawEjectBonusCaption();drawBonusBallFlash()}'
if old not in s: raise SystemExit('draw effects target missing')
s=s.replace(old,new,1)

# Update help copy if present.
s=s.replace('Each level has <b>2 moving capture holes</b>', 'Each level has <b>1 moving capture hole</b>')
s=s.replace('Every time a ball enters a normal hole, the ball ejects from the box and that hole <b>immediately seals and respawns somewhere else</b>.', 'Every time a ball enters the normal moving hole, the ball ejects from the box and that hole <b>immediately seals and respawns somewhere else</b>. Every box eject also awards <b>+40,000 points</b>.')

if s==orig: raise SystemExit('no changes applied')
p.write_text(s)
print('v66 one moving hole + 40K eject bonus + vortex fireworks applied')
