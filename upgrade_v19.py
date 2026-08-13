from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
s=re.sub(r'<title>.*?</title>','<title>LAME — Howie Lucas Pinball v19</title>',s,count=1)

# Make both paddles a little shorter.
s=s.replace('const pivot=side==="L"?{x:135,y:1085}:{x:465,y:1085},len=138;','const pivot=side==="L"?{x:135,y:1085}:{x:465,y:1085},len=128;',1)

# Add a drain commitment state so once the ball gets below the flippers in the center gap,
# it cannot hover, bounce back, or be rescued by the stuck-ball reset.
s=s.replace('let flipperHitAt={L:0,R:0};let howieHitAt=0;','let flipperHitAt={L:0,R:0};let howieHitAt=0;let drainCommitted=false;',1)

# Reset the drain state for every new ball.
s=s.replace('function resetBall(){ball.x=535;ball.y=1165;ball.vx=ball.vy=0;','function resetBall(){drainCommitted=false;ball.x=535;ball.y=1165;ball.vx=ball.vy=0;',1)
s=s.replace('function fireBall(power){if(!waiting||!playing)return;waiting=false;inShooter=true;','function fireBall(power){if(!waiting||!playing)return;drainCommitted=false;waiting=false;inShooter=true;',1)

# Do not let the stuck-ball rescue pull a ball back out of the drain corridor.
s=s.replace('function stuckBallReset(){const low=ball.y>960;const slow=Math.hypot(ball.vx,ball.vy)<2.2;','function stuckBallReset(){if(drainCommitted)return;const low=ball.y>960;const slow=Math.hypot(ball.vx,ball.vy)<2.2;',1)

# Once the ball crosses below the flipper line inside the wide center gap, force a real drain.
needle='ball.vx*=0.9988;ball.vy*=0.9988;if(inShooter)shooterPhysics();else{'
replacement='''ball.vx*=0.9988;ball.vy*=0.9988;if(!inShooter&&ball.x>135&&ball.x<465&&ball.y>1120)drainCommitted=true;if(drainCommitted){ball.vx*=0.90;ball.vy=Math.max(ball.vy+0.65,5.2);if(ball.y>1215){loseBall();return}return}if(inShooter)shooterPhysics();else{'''
if needle not in s: raise SystemExit('physics insertion point not found')
s=s.replace(needle,replacement,1)

p.write_text(s)
print('v19 applied')
