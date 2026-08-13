from pathlib import Path
p=Path('index.html')
s=p.read_text()
s=s.replace('LAME — Howie Lucas Pinball v26','LAME — Howie Lucas Pinball v27',1)
s=s.replace('let outAccum=0,outStarted=0,wasOpen=false,howieHitAt=0,flipperMotionUntil={L:0,R:0},audioCtx=null,sirenNodes=null;','let outAccum=0,outStarted=0,wasOpen=false,howieHitAt=0,boxHitFlash=0,boxHitAt=0,flipperMotionUntil={L:0,R:0},audioCtx=null,sirenNodes=null;',1)
p.write_text(s)
