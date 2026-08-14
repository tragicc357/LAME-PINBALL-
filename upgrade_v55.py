from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
s=s.replace('LAME — Howie Lucas Pinball v54','LAME — Howie Lucas Pinball v55',1)
# Make leaderboard area prominent and impossible to collapse visually.
css='''\n/* v55: persistent global leaderboard visibility */\n.leaderboardHeader{margin:10px 0 5px;text-align:center;font-family:Impact,Arial Black,sans-serif;font-size:20px;letter-spacing:1px;color:#ffd21f;text-shadow:0 0 14px #ffbf00}\n.leaderboards{display:grid!important;visibility:visible!important;opacity:1!important;position:relative!important;z-index:5!important;min-height:96px!important}\n.boardCard{display:block!important;visibility:visible!important;opacity:1!important;min-height:92px!important}\n.boardLoading{padding:10px;text-align:center;color:#8fcfff;font-size:10px;font-weight:900}\n@media(max-width:520px){.leaderboards{grid-template-columns:1fr!important}}\n'''
if 'persistent global leaderboard visibility' not in s:
    s=s.replace('</style>',css+'</style>',1)
# Add a clear title directly above the existing two cards.
needle='<div class="leaderboards"><div class="boardCard"><h4>🌎 TOP 5 SCORES</h4>'
if needle not in s: raise SystemExit('leaderboard HTML anchor not found')
s=s.replace(needle,'<div class="leaderboardHeader">🌎 GLOBAL TOP 5</div>'+needle,1)
# Replace silent stats loader with retrying loader and visible state.
old='async function loadStats(){try{const d=await api("GET");if(d?.stats){stats.plays=Number(d.stats.total_plays)||0;stats.highScore=Number(d.stats.high_score)||0;stats.longestOutMs=Number(d.stats.longest_howie_out_ms)||0}topScores=(d?.topScores||[]).slice(0,5);topOutTimes=(d?.topOutTimes||[]).slice(0,5);updateHud();renderLeaderboards()}catch(e){}}'
new='''let statsRetryTimer=0,statsRefreshTimer=0;function showLeaderboardLoading(msg="REFRESHING GLOBAL TOP 5..."){if(topScoresBoard&&!topScoresBoard.children.length)topScoresBoard.innerHTML=`<div class="boardLoading">${msg}</div>`;if(topTimesBoard&&!topTimesBoard.children.length)topTimesBoard.innerHTML=`<div class="boardLoading">${msg}</div>`}async function loadStats(){showLeaderboardLoading();try{const d=await api("GET");if(d?.stats){stats.plays=Number(d.stats.total_plays)||0;stats.highScore=Number(d.stats.high_score)||0;stats.longestOutMs=Number(d.stats.longest_howie_out_ms)||0}topScores=Array.isArray(d?.topScores)?d.topScores.slice(0,5):[];topOutTimes=Array.isArray(d?.topOutTimes)?d.topOutTimes.slice(0,5):[];updateHud();renderLeaderboards();if(statsRetryTimer){clearTimeout(statsRetryTimer);statsRetryTimer=0}return true}catch(e){if(topScoresBoard)topScoresBoard.innerHTML='<div class="boardLoading">GLOBAL SCORES RECONNECTING...</div>';if(topTimesBoard)topTimesBoard.innerHTML='<div class="boardLoading">GLOBAL TIMES RECONNECTING...</div>';if(!statsRetryTimer)statsRetryTimer=setTimeout(()=>{statsRetryTimer=0;loadStats()},2500);return false}}function startGlobalStatsRefresh(){if(statsRefreshTimer)clearInterval(statsRefreshTimer);statsRefreshTimer=setInterval(()=>loadStats(),20000)}'''
if old not in s: raise SystemExit('loadStats target not found')
s=s.replace(old,new,1)
# Ensure the refresh starts on page load.
old2='nicknameInput.value=playerName;updateAchievementCount();applyLayout();updateHud();refreshMissionUI();loadStats();loop();'
new2='nicknameInput.value=playerName;updateAchievementCount();applyLayout();updateHud();refreshMissionUI();showLeaderboardLoading();loadStats();startGlobalStatsRefresh();loop();'
if old2 not in s: raise SystemExit('startup stats target not found')
s=s.replace(old2,new2,1)
for token in ['LAME — Howie Lucas Pinball v55','GLOBAL TOP 5','startGlobalStatsRefresh','GLOBAL SCORES RECONNECTING','loadStats();startGlobalStatsRefresh();loop()']:
    if token not in s: raise SystemExit('missing '+token)
p.write_text(s)
