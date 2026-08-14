from pathlib import Path
p=Path('index.html')
s=p.read_text()
orig=s
s=s.replace('LAME — Howie Lucas Pinball v67','LAME — Howie Lucas Pinball v68',1)

css='''\n/* v68: controls-first lower layout + centered vortex celebration */\n.vortexCenterBanner{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%) scale(.82);z-index:140;display:none;width:min(88%,520px);padding:20px 14px;text-align:center;border:4px solid #fff;border-radius:22px;background:radial-gradient(circle,#155fdaee 0%,#071b47ee 58%,#020817f2 100%);box-shadow:0 0 26px #fff,0 0 65px #42a5ff;color:#fff;font-family:Impact,Arial Black,sans-serif;pointer-events:none;text-shadow:0 3px 0 #04132b,0 0 18px #fff}\n.vortexCenterBanner.show{display:block;animation:vortexCenterPop 2.5s ease both}\n.vortexCenterBanner .big{display:block;font-size:clamp(34px,8vw,62px);line-height:.95;color:#fff}\n.vortexCenterBanner .sub{display:block;margin-top:8px;font-size:clamp(20px,5vw,36px);line-height:1;color:#8edbff}\n.vortexCenterBanner .three{display:block;margin-top:8px;font-size:clamp(18px,4.5vw,30px);color:#ffd21f}\n@keyframes vortexCenterPop{0%{opacity:0;transform:translate(-50%,-50%) scale(.58)}10%{opacity:1;transform:translate(-50%,-50%) scale(1.08)}20%,72%{opacity:1;transform:translate(-50%,-50%) scale(1)}82%{opacity:1;transform:translate(-50%,-50%) scale(1.06)}100%{opacity:0;transform:translate(-50%,-50%) scale(.86)}}\n.controls{margin-top:8px!important;margin-bottom:8px!important}.powerWrap{margin:0 0 8px!important}.boxStatus{margin:0 0 8px!important}.status{margin:0 0 8px!important}\n'''
if '</style>' not in s: raise SystemExit('style close missing')
s=s.replace('</style>',css+'</style>',1)

# Add a dedicated centered vortex banner to the game table.
needle='<canvas id="game" width="600" height="900"></canvas>'
banner='<canvas id="game" width="600" height="900"></canvas><div class="vortexCenterBanner" id="vortexCenterBanner"><span class="big">BONUS BALLS!</span><span class="sub">NOW YOU’RE PLAYING WITH 3 BALLS!</span><span class="three">● ● ● &nbsp; MULTIBALL ACTIVATED</span></div>'
if needle not in s: raise SystemExit('canvas target missing')
s=s.replace(needle,banner,1)

# Inject after all game functions have been declared, before the final setup call area.
# Use DOM movement so actual document/tab order matches the visual layout.
insert=r'''
/* v68 runtime layout + vortex-center celebration */
(function(){
  const table=document.querySelector('.table'),controls=document.querySelector('.controls'),scorePanel=document.getElementById('launchScorePanel'),boxStatus=document.querySelector('.boxStatus'),status=document.getElementById('status');
  if(table&&controls&&scorePanel&&boxStatus&&status){
    table.after(controls);
    controls.after(scorePanel);
    scorePanel.after(boxStatus);
    boxStatus.after(status);
  }
})();
const vortexCenterBanner=document.getElementById('vortexCenterBanner');
let vortexCenterTimer=0;
function showVortexCenterBanner(){
  if(!vortexCenterBanner)return;
  clearTimeout(vortexCenterTimer);
  vortexCenterBanner.classList.remove('show');
  void vortexCenterBanner.offsetWidth;
  vortexCenterBanner.classList.add('show');
  vortexCenterTimer=setTimeout(()=>vortexCenterBanner.classList.remove('show'),2550);
}
const __v68AwardVortexBonusBalls=awardVortexBonusBalls;
awardVortexBonusBalls=function(){showVortexCenterBanner();return __v68AwardVortexBonusBalls.apply(this,arguments)};
'''
# place immediately before nickname input initialization, which is late in the script and after game functions
needle='nicknameInput.value=playerName;'
if needle not in s: raise SystemExit('late-script insertion target missing')
if 'function awardVortexBonusBalls' not in s: raise SystemExit('awardVortexBonusBalls function missing')
s=s.replace(needle,insert+needle,1)

if s==orig: raise SystemExit('no changes applied')
p.write_text(s)
print('v68 controls-first layout + centered vortex banner applied')
