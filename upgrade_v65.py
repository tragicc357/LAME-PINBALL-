from pathlib import Path
p=Path('index.html')
s=p.read_text()
orig=s
s=s.replace('LAME — Howie Lucas Pinball v64','LAME — Howie Lucas Pinball v65',1)

# Two moving table holes per level instead of three.
s=s.replace("captureHoleState=pool.slice(0,3).map((q,i)=>({id:i,x:q[0],y:q[1],r:25,hits:0,poolIndex:i}))", "captureHoleState=pool.slice(0,2).map((q,i)=>({id:i,x:q[0],y:q[1],r:25,hits:0,poolIndex:i}))",1)
s=s.replace("captureHoleState.length!==3", "captureHoleState.length!==2",1)
s=s.replace("Each level has <b>3 moving capture holes</b>", "Each level has <b>2 moving capture holes</b>",1)

# Slightly larger balls: main ball, queued multiball, and vortex bonus balls.
s=s.replace("const ball={x:535,y:1165,r:11", "const ball={x:535,y:1165,r:13",1)
s=s.replace("extraBalls.push({id:++extraLaunchSerial,x:535,y:1165,r:11", "extraBalls.push({id:++extraLaunchSerial,x:535,y:1165,r:13",1)
s=s.replace("extraBalls.push({id:++extraLaunchSerial,x:300+dir*18,y:735,r:11", "extraBalls.push({id:++extraLaunchSerial,x:300+dir*18,y:735,r:13",1)

# CSS for personal/global leaderboard tabs.
css='''\n/* v65: global/personal best tabs */\n.bestTabs{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin:9px 0 6px}.bestTab{border:2px solid #36516a;border-radius:10px;background:#0a1117;color:#8edcff;padding:9px 6px;font-weight:1000;font-size:11px}.bestTab.active{background:#ffd21f;color:#111;border-color:#fff1a0;box-shadow:0 0 16px #ffd21f66}.personalBoards{display:none;grid-template-columns:1fr 1fr;gap:7px;margin:7px 0}.personalBoards.show{display:grid}.globalBoardsHidden{display:none!important}.personalSub{grid-column:1/-1;text-align:center;color:#9fb0bd;font-size:9px;font-weight:800;margin:-2px 0 2px}@media(max-width:520px){.personalBoards.show{grid-template-columns:1fr}}\n'''
if '</style>' not in s: raise SystemExit('style close missing')
s=s.replace('</style>',css+'</style>',1)

# Star burst + ball shine helpers before point popup state.
needle='let pointPopups=[];'
insert=r'''let boxStars=[];
function spawnBoxStars(){
  const now=performance.now(),count=3+(Math.random()<.55?1:0);
  for(let i=0;i<count;i++){
    const a=-Math.PI*.82+(i/(Math.max(1,count-1)))*Math.PI*.64+(Math.random()-.5)*.18;
    const sp=4.6+Math.random()*2.9;
    boxStars.push({x:300+(Math.random()-.5)*26,y:735+(Math.random()-.5)*15,vx:Math.cos(a)*sp,vy:Math.sin(a)*sp-1.2,rot:Math.random()*Math.PI,t:now,life:1050+Math.random()*350,size:13+Math.random()*7});
  }
  if(boxStars.length>24)boxStars.splice(0,boxStars.length-24);
}
function drawStarShape(x,y,r,rot){
  ctx.beginPath();for(let i=0;i<10;i++){const rr=i%2===0?r:r*.43,ang=rot-Math.PI/2+i*Math.PI/5,px=x+Math.cos(ang)*rr,py=y+Math.sin(ang)*rr;if(i===0)ctx.moveTo(px,py);else ctx.lineTo(px,py)}ctx.closePath()
}
function drawBoxStars(){
  const now=performance.now();boxStars=boxStars.filter(p=>now-p.t<p.life);ctx.save();
  for(const p of boxStars){const age=now-p.t,q=age/p.life;p.x+=p.vx*.65;p.y+=p.vy*.65;p.vy+=.075;p.rot+=.075;ctx.save();ctx.globalAlpha=Math.max(0,1-q);ctx.shadowBlur=24;ctx.shadowColor='#fff36a';drawStarShape(p.x,p.y,p.size*(1+.22*Math.sin(q*Math.PI)),p.rot);const g=ctx.createRadialGradient(p.x-4,p.y-5,1,p.x,p.y,p.size);g.addColorStop(0,'#ffffff');g.addColorStop(.28,'#fff7a8');g.addColorStop(.62,'#ffd21f');g.addColorStop(1,'#ff8a00');ctx.fillStyle=g;ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=1.5;ctx.stroke();ctx.restore()}
  ctx.restore();ctx.globalAlpha=1;
}
function drawBallShineAt(b){
  if(!b||!b.active&&b!==ball)return;ctx.save();ctx.shadowBlur=18;ctx.shadowColor='rgba(255,255,255,.75)';ctx.beginPath();ctx.arc(b.x,b.y,b.r+1.2,0,Math.PI*2);ctx.strokeStyle='rgba(238,250,255,.9)';ctx.lineWidth=1.7;ctx.stroke();ctx.shadowBlur=8;ctx.fillStyle='rgba(255,255,255,.95)';ctx.beginPath();ctx.arc(b.x-b.r*.34,b.y-b.r*.40,Math.max(2.3,b.r*.22),0,Math.PI*2);ctx.fill();ctx.fillStyle='rgba(180,225,255,.48)';ctx.beginPath();ctx.arc(b.x+b.r*.28,b.y+b.r*.30,Math.max(1.5,b.r*.13),0,Math.PI*2);ctx.fill();ctx.restore()
}
'''
if needle not in s: raise SystemExit('point popup insertion target missing')
s=s.replace(needle,insert+needle,1)

# Fire stars whenever a hole/ramp eject sequence starts at the box.
if 'boxEjectFlashUntil=now+900;' not in s: raise SystemExit('box eject flash target missing')
s=s.replace('boxEjectFlashUntil=now+900;','boxEjectFlashUntil=now+900;spawnBoxStars();')

# Draw stars with the board effects.
old='drawRealBall();drawExtraBalls();drawPointPopups();drawBonusBallFlash()}'
new='drawRealBall();drawExtraBalls();drawPointPopups();drawBoxStars();drawBonusBallFlash()}'
if old not in s: raise SystemExit('world effects draw target missing')
s=s.replace(old,new,1)

# Add extra chrome glints after existing ball renderers while respecting captured/hidden main ball states.
needle='nicknameInput.value=playerName;'
shine=r'''const __v65DrawRealBall=drawRealBall;drawRealBall=function(){__v65DrawRealBall();const hn=holeCapture?performance.now()-holeCapture.start:-1;if(holeCapture&&hn>=720&&hn<2050)return;if(trickMode==='ramp'&&typeof rampHoleScored!=='undefined'&&rampHoleScored&&(performance.now()-trickStart)<2600)return;drawBallShineAt(ball)};
const __v65DrawExtraBalls=drawExtraBalls;drawExtraBalls=function(){__v65DrawExtraBalls();for(const b of extraBalls){if(b.active)drawBallShineAt(b)}};
'''
if needle not in s: raise SystemExit('nickname init target missing')
s=s.replace(needle,shine+needle,1)

# Personal best storage + tab UI. Personal records are per nickname on this browser/device.
needle='const __v65DrawRealBall=drawRealBall;'
personal=r'''const PERSONAL_BEST_KEY='lamePersonalBestV65';let personalRunSaved=false;
function personalAll(){try{return JSON.parse(localStorage.getItem(PERSONAL_BEST_KEY)||'{}')||{}}catch(e){return{}}}
function personalKey(){return String(playerName||'PLAYER').trim().toLowerCase()||'player'}
function personalRuns(){const all=personalAll(),arr=all[personalKey()];return Array.isArray(arr)?arr:[]}
function savePersonalRun(){if(personalRunSaved||!playerName)return;personalRunSaved=true;const all=personalAll(),k=personalKey(),arr=Array.isArray(all[k])?all[k]:[];arr.push({player_name:playerName,score:Math.floor(score),howie_out_ms:Math.floor(outMs()),created_at:new Date().toISOString()});all[k]=arr.sort((a,b)=>Math.max(Number(b.score)||0,Number(b.howie_out_ms)||0)-Math.max(Number(a.score)||0,Number(a.howie_out_ms)||0)).slice(0,40);try{localStorage.setItem(PERSONAL_BEST_KEY,JSON.stringify(all))}catch(e){}}
function personalRowsHtml(rows,type){const arr=(rows||[]).slice(0,5);return arr.length?arr.map((r,i)=>`<div class="rankRow"><span class="rk">#${i+1}</span><span class="nm">${esc(r.player_name||playerName||'PLAYER')}</span><span class="val">${type==='time'?fmt(Number(r.howie_out_ms)||0):(Number(r.score)||0).toLocaleString()}</span><span class="stamp">${recordStamp(r.created_at)}</span></div>`).join(''):'<div class="rankRow"><span class="rk">—</span><span class="nm">No personal record yet</span><span class="val">—</span></div>'}
function renderPersonalBoards(){const wrap=document.getElementById('personalBestBoards');if(!wrap)return;const runs=personalRuns(),scores=[...runs].sort((a,b)=>(Number(b.score)||0)-(Number(a.score)||0)).slice(0,5),times=[...runs].sort((a,b)=>(Number(b.howie_out_ms)||0)-(Number(a.howie_out_ms)||0)).slice(0,5);document.getElementById('personalScoreBoard').innerHTML=personalRowsHtml(scores,'score');document.getElementById('personalTimeBoard').innerHTML=personalRowsHtml(times,'time');const sub=document.getElementById('personalBestName');if(sub)sub.textContent='PERSONAL RECORDS FOR '+String(playerName||'PLAYER').toUpperCase()+' • SAVED ON THIS DEVICE'}
function setBestTab(which){const globalOn=which==='global',globalHeader=document.querySelector('.leaderboardHeader'),globalBoards=document.querySelector('.leaderboards');document.getElementById('globalBestTab')?.classList.toggle('active',globalOn);document.getElementById('personalBestTab')?.classList.toggle('active',!globalOn);globalHeader?.classList.toggle('globalBoardsHidden',!globalOn);globalBoards?.classList.toggle('globalBoardsHidden',!globalOn);document.getElementById('personalBestBoards')?.classList.toggle('show',!globalOn);if(!globalOn)renderPersonalBoards()}
function initBestTabs(){const hdr=document.querySelector('.leaderboardHeader'),gb=document.querySelector('.leaderboards');if(!hdr||!gb||document.getElementById('globalBestTab'))return;const tabs=document.createElement('div');tabs.className='bestTabs';tabs.innerHTML='<button class="bestTab active" id="globalBestTab">🌎 GLOBAL BEST</button><button class="bestTab" id="personalBestTab">👤 MY TOP 5</button>';hdr.parentNode.insertBefore(tabs,hdr);const p=document.createElement('div');p.id='personalBestBoards';p.className='personalBoards';p.innerHTML='<div class="personalSub" id="personalBestName"></div><div class="boardCard"><h4>👤 MY TOP 5 SCORES</h4><div id="personalScoreBoard"></div></div><div class="boardCard"><h4>⏱️ MY TOP 5 HOWIE-OUT TIMES</h4><div id="personalTimeBoard"></div></div>';gb.parentNode.insertBefore(p,gb.nextSibling);document.getElementById('globalBestTab').onclick=()=>setBestTab('global');document.getElementById('personalBestTab').onclick=()=>setBestTab('personal');renderPersonalBoards()}
const __v65FinishRecord=finishRecord;finishRecord=async function(){savePersonalRun();const r=await __v65FinishRecord();renderPersonalBoards();return r};
const __v65StartGame=startGame;startGame=function(){personalRunSaved=false;const r=__v65StartGame();setTimeout(()=>{renderPersonalBoards();setBestTab('global')},0);return r};
initBestTabs();
'''
if needle not in s: raise SystemExit('personal insert target missing')
s=s.replace(needle,personal+needle,1)

if s==orig: raise SystemExit('no changes applied')
p.write_text(s)
print('v65 two holes + chrome ball + personal best tabs + stars applied')
# trigger v65 workflow
