from pathlib import Path
p=Path('index.html')
s=p.read_text()

def rep(a,b):
    global s
    if a not in s:
        raise SystemExit('missing target: '+a[:160])
    s=s.replace(a,b,1)

rep('LAME — Howie Lucas Pinball v33','LAME — Howie Lucas Pinball v34')
rep('let score=0,currentBall=1,level=1,playing=false,waiting=true,left=false,right=false,combo=1,lastHit=0,cameraY=400,inShooter=true,boxOpen=0,nextFlapScore=FLAP_GOAL,transitioning=false,won=false,drainCommitted=false,autoPlay=false,computerLaunchAt=0,computerFlipAt=0,computerLastDecision=null,computerLastHitAt=0;', 'let score=0,currentBall=1,level=1,playing=false,waiting=true,left=false,right=false,combo=1,lastHit=0,cameraY=400,inShooter=true,boxOpen=0,nextFlapScore=FLAP_GOAL,transitioning=false,won=false,drainCommitted=false,autoPlay=false,computerLaunchAt=0,computerFlipAt=0,computerLastDecision=null,computerLastHitAt=0,howieOutPoints=0;')
rep('if(boxOpen===4)setStatus("HOWIE IS OUT THE BOX! DOUBLE POINTS!")', 'if(boxOpen===4){howieOutPoints=0;setStatus("HOWIE IS OUT THE BOX! DOUBLE POINTS!")}')
rep('const n=base*combo*(boxOpen===4?2:1);score+=n;updateHud();openFlapsAndLevels()', 'const n=base*combo*(boxOpen===4?2:1);score+=n;if(boxOpen===4)howieOutPoints+=n;updateHud();openFlapsAndLevels()')
rep('score+=100000;updateHud();openFlapsAndLevels();setStatus("HOWIE BUMPER! +100,000 POINTS • BALL KICKED WITH HIS MOMENTUM")', 'score+=100000;howieOutPoints+=100000;updateHud();openFlapsAndLevels();setStatus("HOWIE BUMPER! +100,000 POINTS • BALL KICKED WITH HIS MOMENTUM")')
rep('score=0;currentBall=1;level=1;combo=1;playing=true;', 'score=0;howieOutPoints=0;currentBall=1;level=1;combo=1;playing=true;')
old='if(boxOpen===4){ctx.save();ctx.fillStyle="rgba(0,0,0,.84)";ctx.strokeStyle="#ffd21f";ctx.lineWidth=3;ctx.fillRect(142,646,316,38);ctx.strokeRect(142,646,316,38);ctx.fillStyle="#ffd21f";ctx.font="900 15px Arial";ctx.textAlign="center";ctx.fillText("HOWIE IS OUTSIDE THE BOX • DOUBLE POINTS ‼️",300,671);ctx.restore()}'
new='if(boxOpen===4){ctx.save();ctx.fillStyle="rgba(0,0,0,.90)";ctx.strokeStyle="#ffd21f";ctx.lineWidth=5;ctx.shadowBlur=16;ctx.shadowColor="#55bfff";ctx.fillRect(82,615,436,112);ctx.strokeRect(82,615,436,112);ctx.shadowBlur=0;ctx.textAlign="center";ctx.fillStyle="#fff";ctx.font="900 24px Impact, Arial Black, Arial";ctx.fillText("HOWIE IS OUTSIDE THE BOX",300,649,410);ctx.fillStyle="#6ec8ff";ctx.font="900 22px Impact, Arial Black, Arial";ctx.fillText("DOUBLE POINTS ‼️",300,678,410);ctx.fillStyle="#ffd21f";ctx.font="900 30px Impact, Arial Black, Arial";ctx.fillText("+"+howieOutPoints.toLocaleString()+" POINTS",300,713,410);ctx.restore()}'
rep(old,new)
p.write_text(s)
print('v34 patched: large Howie-out caption with live points counter')
