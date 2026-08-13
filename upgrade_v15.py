from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
s=re.sub(r'<title>.*?</title>','<title>LAME — Howie Lucas Pinball v15</title>',s,count=1)

# Launch faster, but only inside the shooter lane.
s=s.replace('ball.vy=-(14.8+power*6.4)','ball.vy=-(18.5+power*7.5)',1)

# Give the shooter lane its own higher temporary speed cap; once the ball exits,
# gameplay immediately returns to the normal v14 cap.
s=s.replace('function capBallSpeed(){const max=14.5,sp=Math.hypot(ball.vx,ball.vy);if(sp>max){const k=max/sp;ball.vx*=k;ball.vy*=k}}',
'''function capBallSpeed(){const max=inShooter?24:14.5,sp=Math.hypot(ball.vx,ball.vy);if(sp>max){const k=max/sp;ball.vx*=k;ball.vy*=k}}''',1)

# Keep the exit into the main table controlled so only the vertical launch feels faster.
s=s.replace('ball.vx=-(4.9+Math.max(0,(-ball.vy-4))*0.09);ball.vy=Math.max(1.2,Math.abs(ball.vy)*0.14);',
'''ball.vx=-(4.9+Math.max(0,(-ball.vy-4))*0.06);ball.vy=Math.max(1.2,Math.abs(ball.vy)*0.10);capBallSpeed();''',1)

p.write_text(s)
print('v15 applied')
