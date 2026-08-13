from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
s=re.sub(r'<title>.*?</title>','<title>LAME — Howie Lucas Pinball v17</title>',s,count=1)

# While Howie is free, the ball's allowed speed keeps rising with his current continuous OUT streak.
# Launch remains the fastest special state. Losing a ball closes the box and immediately restores normal speed.
old='function capBallSpeed(){const max=inShooter?24:(boxOpen===4?18.5:14.5),sp=Math.hypot(ball.vx,ball.vy);if(sp>max){const k=max/sp;ball.vx*=k;ball.vy*=k}}'
new='''function howieOutStreakSeconds(){return boxOpen===4&&outStartedAt?Math.max(0,(performance.now()-outStartedAt)/1000):0}function capBallSpeed(){const outSecs=howieOutStreakSeconds();const freeMax=Math.min(23,16.5+outSecs*0.18);const max=inShooter?24:(boxOpen===4?freeMax:14.5),sp=Math.hypot(ball.vx,ball.vy);if(sp>max){const k=max/sp;ball.vx*=k;ball.vy*=k}}'''
if old not in s: raise SystemExit('speed cap block not found')
s=s.replace(old,new,1)

# Slightly shorten both paddles while keeping their generous collision thickness for reliable contact.
s=s.replace('const pivot=side==="L"?{x:135,y:1085}:{x:465,y:1085},len=150;','const pivot=side==="L"?{x:135,y:1085}:{x:465,y:1085},len=138;',1)

p.write_text(s)
print('v17 applied')
