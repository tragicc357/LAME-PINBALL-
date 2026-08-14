from pathlib import Path
p=Path('index.html')
s=p.read_text()
orig=s
s=s.replace('LAME — Howie Lucas Pinball v66','LAME — Howie Lucas Pinball v67',1)

# Simplify top HUD by hiding BALL and COMBO there; they move to the lower score panel.
css='''\n/* v67: lower gameplay HUD + readability */\n.hud{grid-template-columns:1fr 1fr 1fr 1fr!important}\n.hud>div:nth-child(2),.hud>div:nth-child(4){display:none!important}\n.liveScoreView{grid-template-columns:1fr 150px!important}\n.liveComboBox{display:grid!important;grid-template-columns:1fr 1fr!important;gap:5px!important;align-items:stretch!important}\n.liveComboHalf{display:flex;flex-direction:column;justify-content:center;align-items:center;border-left:1px solid #4b5963;padding-left:4px}\n.liveComboHalf:first-child{border-left:0;padding-left:0}\n#liveBallCount{font-family:Impact,Arial Black,sans-serif;font-size:30px;color:#fff;text-shadow:0 0 12px #70d7ff}\n.boxStatus{margin:7px 0 8px!important}\n.hud span{font-size:12px!important}.levelStrip{font-size:15px!important}.stats span{font-size:12px!important}.nicknameBox label{font-size:14px!important}.howto{font-size:16px!important}.powerLabel{font-size:15px!important}.liveScoreLabel,.liveComboBox span{font-size:14px!important}.ballChoice label{font-size:14px!important}.ballChoice small{font-size:13px!important}.replaySummary{font-size:14px!important}.missionStrip span{font-size:12px!important}.missionStrip b{font-size:16px!important}.missionProgress{font-size:15px!important}.jackpotLamp{font-size:13px!important}.boxTitle{font-size:14px!important}.flap{font-size:16px!important}.boardCard h4{font-size:15px!important}.rankRow{font-size:14px!important}.rankRow .stamp{font-size:12px!important}.rankNote{font-size:15px!important}.tip{font-size:15px!important}.bestTab{font-size:15px!important}.personalSub{font-size:13px!important}.boardLoading{font-size:14px!important}.status{font-size:16px!important}.brand small{font-size:14px!important}\n@media(max-width:520px){.liveScoreView{grid-template-columns:1fr 142px!important}.liveComboBox #liveComboX,#liveBallCount{font-size:27px!important}.howto{font-size:15px!important}}\n'''
if '</style>' not in s: raise SystemExit('style close missing')
s=s.replace('</style>',css+'</style>',1)

# Move box status below the lower score panel and split right-hand score panel between COMBO and BALLS LEFT.
old='<div class="boxStatus"><div class="boxTitle"><span>BOX STATUS</span><span>20,000 PTS = OPEN 1 FLAP</span></div><div class="flaps"><div class="flap" id="flap1">1</div><div class="flap" id="flap2">2</div><div class="flap" id="flap3">3</div><div class="flap" id="flap4">4</div></div></div><div class="table">'
new='<div class="table">'
if old not in s: raise SystemExit('original box status position missing')
s=s.replace(old,new,1)

old='<div id="liveScoreView" class="liveScoreView hide"><div><span class="liveScoreLabel">TOTAL SCORE</span><b id="liveScoreNumber">0</b></div><div class="liveComboBox"><span>COMBO</span><b id="liveComboX">x1</b></div></div></div><div class="controls">'
new='<div id="liveScoreView" class="liveScoreView hide"><div><span class="liveScoreLabel">TOTAL SCORE</span><b id="liveScoreNumber">0</b></div><div class="liveComboBox"><div class="liveComboHalf"><span>COMBO</span><b id="liveComboX">x1</b></div><div class="liveComboHalf"><span>BALLS LEFT</span><b id="liveBallCount">3</b></div></div></div></div><div class="boxStatus"><div class="boxTitle"><span>BOX STATUS</span><span>20,000 PTS = OPEN 1 FLAP</span></div><div class="flaps"><div class="flap" id="flap1">1</div><div class="flap" id="flap2">2</div><div class="flap" id="flap3">3</div><div class="flap" id="flap4">4</div></div></div><div class="controls">'
if old not in s: raise SystemExit('live score panel target missing')
s=s.replace(old,new,1)

# Add BALLS LEFT element and keep it synced with current ball count.
old='liveComboX=document.getElementById("liveComboX");const playsEl='
new='liveComboX=document.getElementById("liveComboX"),liveBallCount=document.getElementById("liveBallCount");const playsEl='
if old not in s: raise SystemExit('live ball element declaration target missing')
s=s.replace(old,new,1)
old='if(liveComboX)liveComboX.textContent="x"+combo;outEl.textContent=fmt(outMs());'
new='if(liveComboX)liveComboX.textContent="x"+combo;if(liveBallCount)liveBallCount.textContent=Math.max(0,4-currentBall);outEl.textContent=fmt(outMs());'
if old not in s: raise SystemExit('HUD update target missing')
s=s.replace(old,new,1)

if s==orig: raise SystemExit('no changes applied')
p.write_text(s)
print('v67 lower HUD + readability update applied')
