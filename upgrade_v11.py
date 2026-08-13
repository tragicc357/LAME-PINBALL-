from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()

def rep(old,new,count=1):
    global s
    if old not in s:
        raise SystemExit('missing replacement target: '+old[:80])
    s=s.replace(old,new,count)

rep('</style>', '''
.leaderboards{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:8px 0}
.boardCard{background:linear-gradient(#111820,#080b0e);border:2px solid #36516a;border-radius:13px;padding:8px;min-width:0}
.boardCard h4{margin:0 0 6px;text-align:center;color:#ffd532;font-size:13px;letter-spacing:.6px}
.rankRow{display:grid;grid-template-columns:24px 1fr auto;gap:5px;align-items:center;padding:5px 2px;border-top:1px solid #27323b;font-size:11px;font-weight:900}
.rankRow:first-of-type{border-top:0}.rankNum{color:#70d7ff}.rankName{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.rankVal{color:#fff}
.nicknameBox{background:#090d11;border:2px solid #36516a;border-radius:12px;padding:10px;margin:12px 0}
.nicknameBox label{display:block;font-size:11px;color:#70d7ff;font-weight:900;letter-spacing:1px;margin-bottom:6px}
.nicknameBox input{width:100%;padding:13px;border-radius:10px;border:2px solid #555;background:#050708;color:#fff;font-size:18px;font-weight:900;text-align:center;outline:none}
.nicknameBox input:focus{border-color:#f2b900;box-shadow:0 0 14px #f2b90044}.playerTag{text-align:center;color:#70d7ff;font-size:12px;font-weight:900;margin:5px 0}
@media(max-width:460px){.leaderboards{grid-template-columns:1fr}.rankRow{font-size:12px}}
</style>''')

stats='''  <div class="gameStats">
    <div><b id="playsStat">0</b><span>GLOBAL PLAYS</span></div>
    <div><b id="highScoreStat">0</b><span>GLOBAL HIGH SCORE</span></div>
    <div><b id="longestOutStat">0:00</b><span>GLOBAL LONGEST OUT</span></div>
  </div>'''
rep(stats,stats+'''\n  <div class="leaderboards">\n    <div class="boardCard"><h4>🏆 TOP 5 SCORES</h4><div id="topScores"></div></div>\n    <div class="boardCard"><h4>⏱️ TOP 5 HOWIE OUT TIMES</h4><div id="topTimes"></div></div>\n  </div>''')

rep('<p>Open the box one flap at a time. Every 50,000 points opens one section.</p>', '<p>Open the box one flap at a time. Every 50,000 points opens one section.</p><div class="nicknameBox"><label>ENTER YOUR NICKNAME</label><input id="nicknameInput" maxlength="18" autocomplete="nickname" placeholder="Your nickname" inputmode="text"></div><div class="playerTag" id="playerTag"></div>')
s=s.replace('3️⃣ Lose a ball through the drain = <b>2 flaps close</b>','3️⃣ Lose a ball through the drain = <b>Howie goes back in the box</b>')
s=s.replace('4️⃣ Keep scoring — later 50,000-point milestones reopen lost flaps','4️⃣ Keep scoring — later 50,000-point milestones open the box again')
s=s.replace('6️⃣ The online leaderboard tracks <b>global plays, high score, and longest OUT TIME</b>','6️⃣ Your <b>nickname</b> can earn a spot in the global Top 5 score or Top 5 OUT TIME')
s=s.replace('These stats are now shared online: every player contributes to the global play count, highest score, and longest Howie-out record.','Global accomplishments stay online: all-time plays, Top 5 scores, and Top 5 Howie-out times are shared by everyone.')
s=s.replace('<title>LAME — Howie Lucas Pinball</title>','<title>LAME — Howie Lucas Pinball v11</title>')

stats_block='''let stats={
  plays:0,
  highScore:0,
  longestOutMs:0
};'''
rep(stats_block,stats_block+'''\nlet topScores=[],topOutTimes=[];\nlet playerName=(localStorage.getItem("lameNicknameV11")||"").trim().slice(0,18);''')

rep('const longestOutStatEl=document.getElementById("longestOutStat");','''const longestOutStatEl=document.getElementById("longestOutStat");
const topScoresEl=document.getElementById("topScores");
const topTimesEl=document.getElementById("topTimes");
const nicknameInput=document.getElementById("nicknameInput");
const playerTag=document.getElementById("playerTag");''')

m=re.search(r'function refreshStatsDisplay\(\)\{.*?\n\}',s,re.S)
if not m: raise SystemExit('refreshStatsDisplay not found')
refresh='''function escName(v){return String(v||"Anonymous").replace(/[&<>\"']/g,ch=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[ch]))}
function renderBoards(){
 const scoreRows=topScores.slice(0,5),timeRows=topOutTimes.slice(0,5);
 topScoresEl.innerHTML=scoreRows.length?scoreRows.map((r,i)=>`<div class="rankRow"><span class="rankNum">#${i+1}</span><span class="rankName">${escName(r.player_name)}</span><span class="rankVal">${Number(r.score||0).toLocaleString()}</span></div>`).join(""):'<div class="rankRow"><span>—</span><span class="rankName">No scores yet</span><span></span></div>';
 topTimesEl.innerHTML=timeRows.length?timeRows.map((r,i)=>`<div class="rankRow"><span class="rankNum">#${i+1}</span><span class="rankName">${escName(r.player_name)}</span><span class="rankVal">${formatTime(Number(r.howie_out_ms)||0)}</span></div>`).join(""):'<div class="rankRow"><span>—</span><span class="rankName">No times yet</span><span></span></div>';
}
function refreshStatsDisplay(){
  bestEl.textContent=stats.highScore.toLocaleString();playsStatEl.textContent=stats.plays.toLocaleString();highScoreStatEl.textContent=stats.highScore.toLocaleString();longestOutStatEl.textContent=formatTime(stats.longestOutMs);renderBoards();
}'''
s=s[:m.start()]+refresh+s[m.end():]

rep('''      stats.longestOutMs=Number(data.stats.longest_howie_out_ms)||0;
      refreshStatsDisplay();''','''      stats.longestOutMs=Number(data.stats.longest_howie_out_ms)||0;
      topScores=Array.isArray(data.topScores)?data.topScores.slice(0,5):[];
      topOutTimes=Array.isArray(data.topOutTimes)?data.topOutTimes.slice(0,5):[];
      refreshStatsDisplay();''')
s=s.replace('await apiRequest("POST",{action:"start",playerId});','await apiRequest("POST",{action:"start",playerId,playerName});')
rep('''      action:"finish",
      playerId,
      score:''','''      action:"finish",
      playerId,
      playerName,
      score:''')

rep('''function newGame(){
 score=0;currentBall=1;combo=1;playing=true;boxOpen=0;nextFlapScore=50000;''','''function newGame(){
 const typed=(nicknameInput?.value||playerName||"").trim().replace(/\\s+/g," ").slice(0,18);
 if(!typed){document.getElementById("startScreen").classList.remove("hide");nicknameInput?.focus();setStatus("Enter a nickname before you play");return;}
 playerName=typed;localStorage.setItem("lameNicknameV11",playerName);if(nicknameInput)nicknameInput.value=playerName;if(playerTag)playerTag.textContent="PLAYING AS: "+playerName;
 score=0;currentBall=1;combo=1;playing=true;boxOpen=0;nextFlapScore=50000;''')

s=s.replace(''' boxOpen=Math.max(0,boxOpen-2);
 updateFlaps();
 setStatus("BALL LOST — 2 BOX FLAPS CLOSED");''',''' boxOpen=0;
 updateFlaps();
 setStatus("BALL LOST — HOWIE IS BACK IN THE BOX");''')

m=re.search(r'function drawHowieEmerging\(\)\{.*?\n\}',s,re.S)
if not m: raise SystemExit('drawHowieEmerging not found')
running='''function drawHowieRunning(){
 if(boxOpen<4||!theme.complete||!theme.naturalWidth)return;
 const t=performance.now()/1000,a=t*.9,cx=300,cy=610,rx=205,ry=390;
 let x=clamp(cx+Math.cos(a)*rx,72,468),y=clamp(cy+Math.sin(a)*ry,185,970);
 const dir=-Math.sin(a)>=0?1:-1,bob=Math.sin(t*12)*5;
 const sw=theme.naturalWidth*.46,sh=theme.naturalHeight*.70,sx=theme.naturalWidth*.27,sy=theme.naturalHeight*.13;
 const h=150,w=92;
 ctx.save();ctx.translate(x,y+bob);ctx.scale(dir,1);
 ctx.beginPath();ctx.roundRect(-w/2,-h/2,w,h,22);ctx.clip();
 ctx.shadowBlur=18;ctx.shadowColor="#ffd21f";ctx.drawImage(theme,sx,sy,sw,sh,-w/2,-h/2,w,h);ctx.shadowBlur=0;
 ctx.restore();
 ctx.save();ctx.translate(x,y+bob);ctx.strokeStyle="#ffd21f";ctx.lineWidth=4;ctx.globalAlpha=.8;ctx.strokeRect(-w/2,-h/2,w,h);ctx.restore();
}'''
s=s[:m.start()]+running+s[m.end():]
s=s.replace('drawHowieEmerging();','drawHowieRunning();')

rep('document.getElementById("startBtn").onclick=newGame;','''if(nicknameInput){nicknameInput.value=playerName;nicknameInput.addEventListener("keydown",e=>{if(e.key==="Enter")newGame()});}
if(playerTag&&playerName)playerTag.textContent="PLAYING AS: "+playerName;
document.getElementById("startBtn").onclick=newGame;''')

p.write_text(s)
print('Upgraded index.html to v11')
